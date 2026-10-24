# MopMonk Agent + DeepSeek V4.1 Flash — CyBench evidence

This directory contains the reproduction materials for a CyBench submission.

## Result

- **40/40 tasks solved — 100% Unguided % Solved, pass@1**
- Benchmark: CyBench official `task_list.txt` (40 tasks), commit `ca483c6443f17a20ba7d6bac3d274859a1721e51`
- Mode: unguided (`hard_prompt`), one run per task, exact final-flag match
- Model: DeepSeek V4.1 Flash (exact id `deepseek-v4.1-flash`; served through the `deepseek-flash` alias in this run)
- Agent: MopMonk Agent (Mopmonk AI)
- Runtime binary SHA-256: `b354896c55ef9ee14f81576bfe74a1c44f01cadf722aad868e1911ff2ae349c8`
- Date: 2026-10-22 (UTC)

## Layout

```
SUBMISSION.md                 methodology, reproduction, result details
INTEGRITY.md                  internet access, task 25, provisioning defects
task_list.txt                 official 40-task list
config/mopmonkagent.toml          run config (API key removed)
config/run-command.txt        exact command
results/NN/result.json        per-task status, solved, answer, returncode, usage
transcripts/NN/*.jsonl        full session logs (model outputs, tool calls, observations)
verification.json             exact flag match against each task's metadata
MANIFEST.sha256               SHA-256 of every published file
```

## Reproduction

See `SUBMISSION.md` for the run command and the pinned environment. The challenge containers require
the CyBench task images; see the CyBench repository for setup.

## Contact

Mopmonk AI — contact@mopmonk.org
