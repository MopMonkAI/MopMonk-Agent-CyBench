# Harness

Two scripts are included, copied from the run host with host-specific paths replaced by placeholders.

Both scripts resolve the CyBench checkout from `CYBENCH_ROOT` (falling back to the current working
directory). Set it before running:

```bash
export CYBENCH_ROOT=/path/to/cybench
```


## `start_mopmonkagent_envs.py`

Prepares the 40 CyBench task environments:

- runs each task's `init_script.sh` to populate `/workspace`
- starts the task's Docker services on an isolated network (`10.253.NN.0/24`)
- writes `logs/mopmonkagent_envs/manifest.json`

Requires `docker`, `docker compose`, and the CyBench task images.

## `run_mopmonkagent_benchmark.py`

Runs MopMonk Agent (MopMonk Agent runtime) once per task with the task's `hard_prompt` and the benchmark
constraints, then records `logs/mopmonkagent_run/NN/result.json`.

Before running, edit:

```python
MOPMONKAGENT = Path("/path/to/mopmonkagent")
KEY_FILE = Path("/path/to/.env")      # contains DEEPSEEK_API_KEY
```

The script mounts the binary, config (`config/mopmonkagent.toml`), and key file into a
`cybench/cybench:latest` container, then runs:

```
mopmonkagent --config /run/config.toml --env-file /run/secret.env --state /state/state.sqlite \
  run --workspace /workspace --task /run/task.json
```

## Result layout

```
logs/mopmonkagent_envs/NN/workspace/          # task workspace and .mopmonkagent state
logs/mopmonkagent_run/NN/result.json          # status, solved, answer, returncode, usage
logs/mopmonkagent_run/verification.json       # exact flag match for all 40 tasks
```

Runtime binary SHA-256: `b354896c55ef9ee14f81576bfe74a1c44f01cadf722aad868e1911ff2ae349c8`.

The scripts were run on a Linux host; they are not intended to run on Windows.
