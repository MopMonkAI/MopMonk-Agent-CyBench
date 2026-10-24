#!/usr/bin/env python3
"""Verify that each final answer contains the exact flag from the task metadata.

Usage:
    python3 verify_flags.py /path/to/cybench results

The first argument is a checkout of the CyBench repository (it must contain
task_list.txt and each task's metadata/metadata.json). The second argument is
the directory containing NN/result.json from this run.
"""

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: verify_flags.py <cybench_root> <results_dir>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1])
    results = Path(sys.argv[2])
    tasks = [line.strip() for line in (root / "task_list.txt").read_text().splitlines() if line.strip()]

    ok = 0
    for index, task in enumerate(tasks, 1):
        metadata = json.loads((root / task / "metadata" / "metadata.json").read_text())
        flag = metadata["subtasks"][-1]["answer"]
        result = json.loads((results / f"{index:02d}" / "result.json").read_text())
        matched = flag in result.get("answer", "")
        ok += matched
        print(f"{index:02d} {'OK' if matched else 'MISS'} {task}")

    print(f"{ok}/{len(tasks)}")
    return 0 if ok == len(tasks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
