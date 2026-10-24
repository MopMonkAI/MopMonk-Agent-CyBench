# MopMonk Agent + DeepSeek V4.1 Flash — System Card (CyBench)

## Agent

**MopMonk Agent** is an agent scaffold built by Mopmonk AI. It treats exploitation as a continuing
investigation: observations are kept separate from interpretations, candidate actions are chosen to
resolve the next uncertainty, and the final answer must be backed by an executed path against the
target.

- Agent page: https://github.com/MopMonkAI/MopMonk-Agent/blob/main/README.md
- Runtime binary SHA-256: `b354896c55ef9ee14f81576bfe74a1c44f01cadf722aad868e1911ff2ae349c8`
- Contact: contact@mopmonk.org

## Model

**DeepSeek V4.1 Flash** (exact id `deepseek-v4.1-flash`; served through the `deepseek-flash` alias in
this run), 1M context, reasoning effort `max`.

## CyBench evaluation

| Model | Tasks | Unguided % Solved (pass@1) | Mode | Scoring |
| --- | ---: | ---: | --- | --- |
| MopMonk Agent + DeepSeek V4.1 Flash | 40 | 100% (40/40) | unguided (`hard_prompt`), one run per task | exact final flag match |

- Benchmark: CyBench official `task_list.txt` (40 tasks), commit `ca483c6443f17a20ba7d6bac3d274859a1721e51`
- Date: 2026-10-22 (UTC)
- Full task list: `task_list.txt`; per-task results: `results/`; transcripts: `transcripts/`
- Integrity notes: `INTEGRITY.md` (internet egress was not blocked; task 25 provisioning defect)

## Leaderboard row

```
MopMonk Agent + DeepSeek V4.1 Flash,40,100,,,,,,,,
```

## Reproduction

See `SUBMISSION.md` and `harness/README.md`. The runtime binary and config are described there; the
challenge containers require the CyBench task images.
