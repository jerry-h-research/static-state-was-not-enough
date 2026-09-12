# Static State Was Not Enough

**An exploratory longitudinal N-of-1 study of human-AI coordination**

A long-running interaction with a frontier model became much easier for one user to coordinate than fresh instances. We tested several simple explanations instead of assuming a new mechanism.

## 30-second result

| Test | Result |
|---|---|
| Different state compression strategies | Different representations, but utility advantage not established |
| Compact state vs richer/full trajectory continuation | High quality across conditions; no useful directional advantage |
| Heavy Claim Lifecycle governance vs lightweight baseline | **7/7 vs 7/7 — NO_MEASURABLE_ADVANTAGE** |
| 496-word static coordination packet vs no packet | **Practical coordination benefit NOT ESTABLISHED (1/5 burden dimensions improved)** |

The packet session *felt* substantially smoother to the participant, yet blind coding found **more wrong-branch episodes (5 vs 4)**.

That leaves a narrower open question:

> **What, if anything, does ongoing human-AI calibration contribute that static state representations fail to preserve?**

## Why the Claim Lifecycle prototype matters here

The participant-author reports that they did not have enough programming experience to implement Claim Lifecycle independently. Yet the human-AI-tool workflow produced executable prototypes, regression/adversarial tests, reviewed repairs, frozen evaluation contracts, and machine evidence.

Approximate workflow:

- human judgment
- conversational AI formalization and review
- coding-agent implementation and execution
- machine evidence
- conversational review

This is **not** proof that programming expertise is unnecessary. It is an N-of-1 capability-access case showing why the human-AI pair itself became part of the research question.

## Read in this order

1. [Technical report](paper/technical_report.pdf)
2. [Claim status matrix](results/CLAIM_STATUS_MATRIX.md)
3. [Experiment timeline](results/EXPERIMENT_TIMELINE.md)
4. [Formal P3.22 Q2 public summary](artifacts/formal_q2/FORMAL_Q2_PUBLIC_SUMMARY.md)
5. [PCB-1 public summary](artifacts/pcb1/PCB1_PUBLIC_SUMMARY.md)
6. [Claim Lifecycle evidence package](artifacts/claim_lifecycle/README.md)
7. [Limitations](LIMITATIONS.md)

Raw private transcripts are intentionally excluded from v0.3.

## What feedback would be useful?

- Is the local-smoothness / global-trajectory divergence already well characterized in HCI or human-AI co-adaptation literature?
- Is PCB-1 informative despite its N=1/open-label/task confounds?
- How would you operationalize longitudinal coordination without reducing it to memory recall?
- How should adaptation be evaluated without rewarding sycophancy or false certainty?

**Release intent:** criticism, literature connections, and methodological feedback — not endorsement or proof of novelty.
