# Transcripts

58 JSONL session logs across the 40 CyBench tasks, from the 2026-10-22 run.

- 27 tasks have one session; 13 tasks have 2–4 sessions because MopMonk Agent resumed the task after a
  context reset. All sessions belong to the same scored run.
- Each line is one typed event. The main types are `session_meta`, `run_start`, `model_turn_start`,
  `model_turn_end`, `provider_request_*`, `operation_*`, `tool_*`, `tool_output_end`, `run_end`.
- `session_meta` contains the task goal and prompt; `operation_*` and `tool_*` contain the executed
  commands and their observations; `model_turn_end` contains the model output.
- No API keys or credentials are present. See `../integrity/secret_scan.txt`.

Directory layout: `transcripts/NN/*.jsonl`, where `NN` is the 1-based task index in
`../task_list.txt`.
