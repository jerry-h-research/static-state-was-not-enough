"""Development-only screening; CLI is dry-run only. No network dependencies."""
import argparse
from collections import Counter
from copy import deepcopy
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'DEVELOPMENT_SCREENING_TASKS_v0_1.md'
IDS = [f'F{f}-{kind}' for f in range(1, 5) for kind in ('R', 'N', 'B')]
FIELDS = ['task_id', 'run_id', 'target_behavior_present', 'boundary_violation',
          'initial_decision_summary', 'raw_output_path', 'coder_note']
CONFIG = {'provider': None, 'model': None, 'model_version': None, 'settings': {},
          'configuration_status': 'UNCONFIGURED: requires selection before live screening',
          'base_instruction': None, 'replicates': 10,
          'order': 'source task order, replicate 01 through 10',
          'context_policy': 'one user message; fresh provider instance per invocation; no memory'}


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def extract_tasks(source=SOURCE):
    """Strip only Markdown blockquote markup; preserve code indentation/Unicode."""
    text = source.read_text(encoding='utf-8')
    tasks = []
    for match in re.finditer(r'^### (F[1-4]-[RNB])\nUser prompt:\n\n((?:>[^\n]*\n)+)', text, re.M):
        lines = match[2].splitlines()
        prompt = '\n'.join(line[2:] if line.startswith('> ') else line[1:] for line in lines)
        tasks.append({'task_id': match[1], 'prompt': prompt, 'prompt_sha256': digest(prompt)})
    if [task['task_id'] for task in tasks] != IDS:
        raise ValueError('Source must contain exactly the twelve frozen task IDs in order')
    return tasks


def load_tasks(path):
    tasks = json.loads(path.read_text(encoding='utf-8'))
    if tasks != extract_tasks():
        raise ValueError('Fixture differs from exact source transcription')
    return tasks


def request_for(task, config):
    # Deliberate allowlist: never serialize the task record or research metadata.
    return {'model': config['model'], 'model_version': config['model_version'],
            'settings': deepcopy(config['settings']),
            'messages': [{'role': 'user', 'content': task['prompt']}]}


def schedule(tasks, config):
    if config['replicates'] != 10 or config['base_instruction'] is not None:
        raise ValueError('This runner freezes ten replicates and no base instruction')
    timestamp = now()
    rows = []
    for task in tasks:
        for replicate in range(1, 11):
            run_id = f"{task['task_id']}_{replicate:02d}"
            rows.append({'task_id': task['task_id'], 'run_id': run_id,
                         'replicate_id': replicate, 'order': len(rows) + 1,
                         'planned_at': timestamp, 'started_at': None, 'finished_at': None,
                         'provider': config['provider'], 'model': config['model'],
                         'model_version': config['model_version'], 'settings': deepcopy(config['settings']),
                         'prompt_sha256': task['prompt_sha256'], 'status': 'planned',
                         'raw_output_path': f'raw/{run_id}.txt',
                         'error_path': f'errors/{run_id}.json'})
    return rows


def coding_sheet(path, rows):
    with path.open('x', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in ('task_id', 'run_id', 'raw_output_path')})


def append_event(path, row):
    with path.open('a', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(row, ensure_ascii=False) + '\n')
        stream.flush()


def execute(rows, tasks, config, directory, provider_factory, *, authorized=False):
    """Future adapter seam; used only with local fakes in this evidence package.

    Factory must return a fresh, stateless callable accepting request_for's schema,
    returning the complete raw semantic response as a string. Adapters must disable
    remote memory, must not retry, and must not raise after receiving usable output.
    Adapter conformance requires review before any live use. Stop on first failure.
    """
    if not authorized:
        raise ValueError('Explicit execution authorization required')
    if not all(config[key] for key in ('provider', 'model', 'model_version')):
        raise ValueError('Provider, model and immutable version must be selected')
    by_id = {task['task_id']: task for task in tasks}
    events = directory / 'attempts.jsonl'
    # Reserve before invoking a provider, including when a prior run was interrupted.
    with events.open('x', encoding='utf-8'):
        pass
    for planned in rows:
        row = deepcopy(planned)
        output = directory / row['raw_output_path']
        row.update(started_at=now(), status='started')
        with output.open('x', encoding='utf-8', newline='\n') as stream:
            append_event(events, row)
            try:
                provider = provider_factory()
                raw = provider(request_for(by_id[row['task_id']], config))
                if not isinstance(raw, str) or not raw.strip():
                    raise ValueError('Provider returned no usable semantic string')
            except Exception as error:
                row.update(status='provider_failure', finished_at=now())
                write_json(directory / row['error_path'], {
                    'run_id': row['run_id'], 'timestamp': row['finished_at'],
                    'error_type': type(error).__name__, 'message': str(error),
                    'usable_semantic_output': False})
                append_event(events, row)
                return False
            stream.write(raw)
            stream.flush()
            row.update(status='success', finished_at=now())
            append_event(events, row)
    return True


def dry_run(directory, fixture=HERE / 'tasks.json'):
    tasks = load_tasks(fixture)
    config = deepcopy(CONFIG)
    rows = schedule(tasks, config)
    requests = [request_for(task, config) for task in tasks]
    counts = dict(Counter(row['task_id'] for row in rows))
    checks = {
        'exact_source_transcription': tasks == extract_tasks(),
        'twelve_unique_task_ids': len(counts) == 12,
        'ten_replicates_per_task': all(count == 10 for count in counts.values()),
        'exactly_120_planned_calls': len(rows) == 120,
        'unique_output_paths': len({row['raw_output_path'] for row in rows}) == 120,
        'unique_failure_paths': len({row['error_path'] for row in rows}) == 120,
        'only_exact_user_prompt_in_messages': all(
            req['messages'] == [{'role': 'user', 'content': task['prompt']}]
            for req, task in zip(requests, tasks)),
        'no_metadata_or_prior_context_in_request': all(
            set(req) == {'model', 'model_version', 'settings', 'messages'} for req in requests),
        'all_prompt_hashes_recorded': all(row['prompt_sha256'] == tasks[(row['order']-1)//10]['prompt_sha256'] for row in rows),
        'zero_model_calls': True,
    }
    if not all(checks.values()):
        raise ValueError(checks)
    directory.mkdir(parents=True, exist_ok=False)
    (directory / 'raw').mkdir()
    (directory / 'errors').mkdir()
    write_json(directory / 'config.json', config)
    with (directory / 'manifest.jsonl').open('x', encoding='utf-8', newline='\n') as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
    write_json(directory / 'model_inputs.json', requests)
    coding_sheet(directory / 'coding_sheet.csv', rows)
    result = {'mode': 'dry-run', 'executed_model_calls': 0, 'planned_calls': len(rows),
              'replicates_by_task': counts, 'checks': checks,
              'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'config': config}
    write_json(directory / 'validation.json', result)
    with (directory / 'DRY_RUN_REPORT.md').open('x', encoding='utf-8') as stream:
        stream.write('# Development screening dry-run report\n\n'
                     'PASS: 12 unique tasks, 10 replicates each, 120 planned calls; **zero model calls executed**.\n\n'
                     + '\n'.join(f'- PASS: `{check}`' for check in checks)
                     + '\n\nPrompts are exact transcriptions after removing Markdown blockquote markers '
                     'and normalizing line endings to LF, with no terminal newline. Hashes use UTF-8 SHA-256. '
                     'Model input consists only of one user prompt; research metadata stays in the manifest. '
                     'Each request is independently constructed. No base instruction is added.\n\n'
                     'Planned provider/model/version: UNCONFIGURED; settings: `{}`. '
                     'The handoff specifies none. These must be selected and a stateless provider adapter '
                     'independently reviewed before future live execution. No live adapter is installed.\n\n'
                     'See `test_results.txt` and `failure_logging_evidence.json` for offline fake-provider '
                     'validation. Planned raw/error paths are unpopulated; fake outputs are not screening results. '
                     'The coding sheet has all judgment fields blank. No classifications or dispositions were computed.\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='default and only CLI mode')
    parser.add_argument('--output', type=Path, required=True, help='new directory; existing paths rejected')
    args = parser.parse_args()
    print(json.dumps(dry_run(args.output), indent=2))


if __name__ == '__main__':
    main()
