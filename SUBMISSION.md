# MopMonk Agent + DeepSeek V4.1 Flash — CyBench submission

- Authors: Mopmonk AI
- Contact: contact@mopmonk.org
- Agent: MopMonk Agent (https://github.com/MopMonkAI/MopMonk-Agent/blob/main/README.md)
- Model: DeepSeek V4.1 Flash (exact id `deepseek-v4.1-flash`; served through the `deepseek-flash` alias in this run), 1M context, reasoning effort max
- Benchmark: CyBench, official `task_list.txt` (40 tasks), commit `ca483c6443f17a20ba7d6bac3d274859a1721e51`
- Date: 2026-10-22 (UTC)

## Result

**40/40 tasks solved — 100% Unguided % Solved, pass@1.**

- Mode: unguided (`hard_prompt`); one run per task
- Scoring: the final answer must contain the exact flag from the task's `metadata/metadata.json`
- All 40 final results are `status: reported` with `returncode: 0`
- 2,783 model calls, 3,380 tool calls, ~213M input tokens (~204M cached), ~7.0M output tokens
- Estimated cost: ~$0.16/task at DeepSeek V4.1 Flash off-peak prices

## Method

1. Each task environment was prepared with `harness/start_mopmonkagent_envs.py`: the task's `init_script.sh`
   populates `/workspace`, the challenge services are started on an isolated Docker network, and the
   agent container runs with `/workspace` mounted.
2. `harness/run_mopmonkagent_benchmark.py` runs MopMonk Agent (MopMonk Agent runtime) once per task with the task's
   `hard_prompt` plus the benchmark constraints. The task contract forbids inspecting benchmark
   metadata, answer keys, or published challenge solutions.
3. The runner records `result.json` per task; `solved` is true when the exact metadata flag appears in
   the final answer. `verification.json` re-checks the exact flag match and the terminal run status.

## Reproduction

- Agent runtime binary SHA-256: `b354896c55ef9ee14f81576bfe74a1c44f01cadf722aad868e1911ff2ae349c8`
- Config: `config/mopmonkagent.toml` (API key removed)
- Run command: `config/run-command.txt`
- Task list: `task_list.txt`
- Task commit: `ca483c6443f17a20ba7d6bac3d274859a1721e51`

The challenge containers require the CyBench task images; see the CyBench repository for setup.

This run used the MopMonk Agent runner, not Inspect, so there is no Inspect `.eval` file. The per-task
`results/NN/result.json` files plus `verification.json` are the equivalent record.

## Files

| Path | Contents |
| --- | --- |
| `results.json` | aggregate machine-readable result |
| `leaderboard_row.csv` | the exact CSV row submitted to the leaderboard |
| `results/NN/result.json` | per-task status, solved, exact answer, returncode, usage |
| `transcripts/NN/*.jsonl` | full session logs (model outputs, tool calls, observations) |
| `verification.json` | exact flag match against each task's metadata |
| `SYSTEM_CARD.md` | model/agent card and leaderboard row |
| `config/` | run config, provider, exact command |
| `harness/` | environment preparation and run scripts |
| `report/SUMMARY.md` | per-task table |
| `integrity/` | flag provenance audit and secret scan |
| `SUBMISSION.md` | this file |
| `INTEGRITY.md` | internet access, task 25, provisioning defects |
| `MANIFEST.sha256` | SHA-256 of every published file |

## Caveats

The scored run did **not** block internet egress, and task 25's `init_script.sh` did not provision the
files its prompt promises. Details, including the per-task flag-provenance audit, are in
`INTEGRITY.md`. A clean rerun with egress blocked and task 25 fixed can be provided on request.
