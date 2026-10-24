## Add MopMonk Agent + DeepSeek V4.1 Flash to the Cybench leaderboard

This PR adds one row to `data/leaderboard.csv`.

**Model:** DeepSeek V4.1 Flash (exact id `deepseek-v4.1-flash`; served in this run through the
`deepseek-flash` alias; 1M context, reasoning effort max).

**Agent:** MopMonk Agent (Mopmonk AI) — a disclosed non-default scaffold; agent page:
https://github.com/MopMonkAI/MopMonk-Agent/blob/main/README.md.

**Result:** **100% Unguided % Solved** on the full 40-task `task_list.txt` (unguided mode, exact
flag-match scoring, pass@1 — one run per task).

### Row (inserted at the top, above Claude Mythos Preview)

```
MopMonk Agent + DeepSeek V4.1 Flash,40,100,,,,,,,,
```

The run used the full official 40-task list and excluded nothing, including `05-motp` (which the 39-task
Inspect variant omits). The current top entries use Count = 35; the four tasks that the Typhon V1 Lite
submission lists as excluded from its 35-task subset (`diffecient`, `locktalk`, `ezmaze`,
`just_another_pickle_jail`) were all solved here.

### Evidence and reproduction

Full reproduction materials — pinned tool versions, the exact run command, per-task results, full
session transcripts, the scored verification file, the redacted run config, and a SHA-256 manifest — are
published here:

- https://github.com/MopMonkAI/MopMonk-Agent-CyBench

The result uses a disclosed custom agent scaffold (`MopMonk Agent`, built on the MopMonk Agent runtime); see
`SUBMISSION.md` and `INTEGRITY.md` in the evidence repo for the full methodology and integrity disclosure.

### Integrity notes

Internet egress was not blocked during the scored run, and task 25's `init_script.sh` did not provision
the files its prompt promises. The per-task flag-provenance audit and the full disclosure are in
`INTEGRITY.md`.
