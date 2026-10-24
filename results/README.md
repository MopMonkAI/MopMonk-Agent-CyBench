# Results

40 `result.json` files, one per task (`results/NN/result.json`).

Each file contains:

- `task` — the CyBench task path
- `status` — MopMonk Agent terminal status (`reported` for all 40)
- `solved` — true when the exact metadata flag appears in the final answer
- `answer` — the agent's final answer
- `returncode` — process exit code (`0` for all 40)
- `usage` — input/output/cached tokens, model calls, tool calls

`../verification.json` re-checks the exact flag match against each task's
`metadata/metadata.json` and records the terminal run status.

This run used the MopMonk Agent runner, not Inspect, so there is no Inspect `.eval` file. These per-task
`result.json` files are the equivalent record.
