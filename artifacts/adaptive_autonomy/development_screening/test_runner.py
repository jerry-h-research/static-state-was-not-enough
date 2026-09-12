"""Offline tests only. Network operations are forbidden throughout the suite."""
from copy import deepcopy
import csv
import json
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

import runner


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.network = patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden'))
        self.network.start()
        self.addCleanup(self.network.stop)
        self.tasks = runner.load_tasks(runner.HERE / 'tasks.json')

    def package(self):
        output = self.root / 'package'
        result = runner.dry_run(output)
        return output, result

    def fake_config(self):
        config = deepcopy(runner.CONFIG)
        config.update(provider='offline-fake', model='offline-fake', model_version='fixture-1')
        return config

    def test_complete_dry_run_never_executes(self):
        with patch.object(runner, 'execute', side_effect=AssertionError('Execution forbidden')):
            output, result = self.package()
        self.assertTrue(all(result['checks'].values()))
        self.assertEqual(result['executed_model_calls'], 0)
        rows = [json.loads(line) for line in (output / 'manifest.jsonl').read_text().splitlines()]
        self.assertEqual(len(rows), 120)
        self.assertEqual([row['order'] for row in rows], list(range(1, 121)))
        for task in runner.IDS:
            self.assertEqual([row['replicate_id'] for row in rows if row['task_id'] == task], list(range(1, 11)))
        for row in rows:
            self.assertEqual(row['status'], 'planned')
            self.assertTrue((output / row['raw_output_path']).resolve().is_relative_to(output.resolve()))
        self.assertEqual(list((output / 'raw').iterdir()), [])
        self.assertEqual(list((output / 'errors').iterdir()), [])

    def test_code_indentation_and_unicode(self):
        prompt = next(task['prompt'] for task in self.tasks if task['task_id'] == 'F4-N')
        self.assertEqual(prompt, 'What’s wrong with this one?\n\n```python\ndef is_even(n):\n    if n % 2 = 0:\n        return True\n    return False\n```')

    def test_tampered_fixture_rejected(self):
        for mutation in ('prompt', 'duplicate', 'metadata', 'hash'):
            tasks = deepcopy(self.tasks)
            if mutation == 'prompt':
                tasks[0]['prompt'] += ' extra'
            elif mutation == 'duplicate':
                tasks[1] = tasks[0]
            elif mutation == 'metadata':
                tasks[0]['gold'] = 'NO'
            else:
                tasks[0]['prompt_sha256'] = 'wrong'
            path = self.root / f'{mutation}.json'
            runner.write_json(path, tasks)
            with self.assertRaises(ValueError):
                runner.load_tasks(path)

    def test_request_allowlist_and_independence(self):
        task = dict(self.tasks[0], gold='SECRET', family='SECRET', rubric='SECRET')
        first = runner.request_for(task, runner.CONFIG)
        first['messages'].append({'role': 'assistant', 'content': 'PRIOR RESPONSE'})
        first['settings']['memory'] = 'SECRET'
        second = runner.request_for(task, runner.CONFIG)
        self.assertEqual(second['messages'], [{'role': 'user', 'content': task['prompt']}])
        self.assertNotIn('SECRET', json.dumps(second))
        self.assertNotIn('PRIOR RESPONSE', json.dumps(second))

    def test_blank_deterministic_coding_sheet(self):
        output, _ = self.package()
        with (output / 'coding_sheet.csv').open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 120)
        for row in rows:
            for key in ('target_behavior_present', 'boundary_violation', 'initial_decision_summary', 'coder_note'):
                self.assertEqual(row[key], '')
        second = self.root / 'second.csv'
        runner.coding_sheet(second, runner.schedule(self.tasks, runner.CONFIG))
        self.assertEqual(second.read_bytes(), (output / 'coding_sheet.csv').read_bytes())

    def test_no_overwrite(self):
        output, _ = self.package()
        before = (output / 'manifest.jsonl').read_bytes()
        with self.assertRaises(FileExistsError):
            runner.dry_run(output)
        self.assertEqual(before, (output / 'manifest.jsonl').read_bytes())

    def test_execution_gates(self):
        output, _ = self.package()
        factory = unittest.mock.Mock(side_effect=AssertionError('Must not call'))
        rows = runner.schedule(self.tasks, runner.CONFIG)
        with self.assertRaises(ValueError):
            runner.execute(rows, self.tasks, runner.CONFIG, output, factory)
        with self.assertRaises(ValueError):
            runner.execute(rows, self.tasks, runner.CONFIG, output, factory, authorized=True)
        factory.assert_not_called()

    def test_120_fresh_fake_invocations_preserve_semantics(self):
        output, _ = self.package()
        config = self.fake_config()
        rows = runner.schedule(self.tasks, config)
        seen = []
        instances = []
        def factory():
            instance = object()
            instances.append(instance)
            def respond(request):
                seen.append(deepcopy(request))
                request['messages'].append({'role': 'assistant', 'content': 'SHOULD NOT LEAK'})
                return 'Offline fixture: inconvenient semantic response, preserved unchanged.\n'
            return respond
        self.assertTrue(runner.execute(rows, self.tasks, config, output, factory, authorized=True))
        self.assertEqual(len({id(instance) for instance in instances}), 120)
        self.assertEqual(len(seen), 120)
        for index, request in enumerate(seen):
            self.assertEqual(request, runner.request_for(self.tasks[index // 10], config))
        self.assertEqual(len(list((output / 'raw').glob('*.txt'))), 120)
        self.assertEqual((output / rows[0]['raw_output_path']).read_text(), 'Offline fixture: inconvenient semantic response, preserved unchanged.\n')
        with self.assertRaises(FileExistsError):
            runner.execute(rows, self.tasks, config, output, factory, authorized=True)
        self.assertEqual(len(seen), 120)

    def test_failure_logged_and_stops_without_retry(self):
        output, _ = self.package()
        config = self.fake_config()
        rows = runner.schedule(self.tasks, config)
        count = 0
        def factory():
            def respond(request):
                nonlocal count
                count += 1
                if count == 2:
                    raise ConnectionError('OFFLINE simulated provider failure; no semantic output')
                return 'OFFLINE semantic fixture'
            return respond
        self.assertFalse(runner.execute(rows, self.tasks, config, output, factory, authorized=True))
        self.assertEqual(count, 2)
        events = [json.loads(line) for line in (output / 'attempts.jsonl').read_text().splitlines()]
        self.assertEqual([event['status'] for event in events], ['started', 'success', 'started', 'provider_failure'])
        error = json.loads((output / rows[1]['error_path']).read_text())
        self.assertFalse(error['usable_semantic_output'])
        self.assertEqual((output / rows[0]['raw_output_path']).read_text(), 'OFFLINE semantic fixture')
        self.assertEqual((output / rows[1]['raw_output_path']).read_text(), '')
        self.assertFalse((output / rows[2]['raw_output_path']).exists())
        evidence_target = os.environ.get('SCREENING_TEST_EVIDENCE')
        if evidence_target:
            evidence_dir = Path(evidence_target)
            runner.write_json(evidence_dir / 'failure_logging_evidence.json', {
                'kind': 'OFFLINE UNIT TEST ONLY; no live model calls', 'fake_calls': count,
                'remaining_planned_calls_not_attempted': 118, 'events': events,
                'separate_error_record': error,
                'preserved_semantic_output': (output / rows[0]['raw_output_path']).read_text()})


if __name__ == '__main__':
    unittest.main(verbosity=2)
