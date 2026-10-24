"""Prepare every Cybench task without exposing answer metadata to the agent."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import os
import subprocess
import time


ROOT = Path(os.environ.get("CYBENCH_ROOT", Path.cwd())).resolve()
OUTPUT = ROOT / "logs" / "mopmonkagent_envs"
IMAGE = "cybench/cybench:latest"
PROBE = """import socket, sys, time
for _ in range(30):
    try:
        with socket.create_connection((sys.argv[1], int(sys.argv[2])), 3):
            break
    except OSError:
        time.sleep(2)
else:
    sys.exit(1)
"""


def logged(command, path, *, timeout):
    with path.open("w") as output:
        result = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{' '.join(command[:3])} failed: {path.read_text()[-1200:]}")


def prepare(index, relative):
    task = ROOT / relative
    directory = OUTPUT / f"{index:02d}"
    workspace = directory / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    logged(
        [
            "docker", "run", "--rm", "--network", "none",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "-v", f"{task}:/task:ro", "-v", f"{workspace}:/workspace",
            "-w", "/task", "--entrypoint", "/bin/bash", IMAGE,
            "init_script.sh", "/workspace", "false",
        ],
        directory / "init.log",
        timeout=120,
    )

    result = {"task": relative, "workspace": str(workspace), "status": "ready"}
    if not (task / "start_docker.sh").is_file():
        if not any(path.is_file() for path in workspace.rglob("*")):
            raise RuntimeError("file task has no initialized files")
        return result

    compose_files = [
        path for path in task.rglob("*compose*.yml")
        if "solution" not in path.parts
    ] + [
        path for path in task.rglob("*compose*.yaml")
        if "solution" not in path.parts
    ]
    if len(compose_files) != 1:
        raise RuntimeError(f"expected one Compose file, found {len(compose_files)}")

    source = subprocess.run(
        ["docker", "compose", "-f", str(compose_files[0]), "config", "--format", "json"],
        check=True, capture_output=True, text=True, timeout=60,
    )
    config = json.loads(source.stdout)
    source_project = config["name"]
    project = f"cybenchcrux{index:02d}"
    network = f"cybench-crux-{index:02d}"
    subnet = f"10.253.{index}.0/24"
    config["name"] = project
    config["networks"] = {"bench": {"name": network, "external": True}}
    for name, service in config["services"].items():
        if service.get("network_mode"):
            raise RuntimeError("host or shared network mode cannot be isolated")
        service.pop("container_name", None)
        ports = service.pop("ports", None)
        if index == 3 and name == "cache":
            # shortcut: Chunky's JWKS callback needs host TCP 8080; use an internal relay if occupied.
            service["ports"] = ports
        service["networks"] = {"bench": None}
        if "healthcheck" in service:
            service["healthcheck"] = {"disable": True}
        if service.pop("build", None):
            service["image"] = f"{source_project}-{name}:latest"
    compose = directory / "compose.json"
    compose.write_text(json.dumps(config, indent=2) + "\n")
    subprocess.run(["docker", "compose", "-f", str(compose), "config", "-q"], check=True, timeout=60)

    inspect = subprocess.run(["docker", "network", "inspect", network], capture_output=True, text=True)
    if inspect.returncode:
        subprocess.run(["docker", "network", "create", "--subnet", subnet, network], check=True, timeout=60)
    elif json.loads(inspect.stdout)[0]["IPAM"]["Config"][0]["Subnet"] != subnet:
        raise RuntimeError(f"network {network} has an unexpected subnet")

    command = ["docker", "compose", "-p", project, "-f", str(compose)]
    logged(command + ["up", "-d", "--no-build", "--pull", "never"], directory / "start.log", timeout=1800)
    time.sleep(5)
    state = subprocess.run(command + ["ps", "--all", "--format", "json"], check=True, capture_output=True, text=True, timeout=60)
    services = [json.loads(line) for line in state.stdout.splitlines() if line.strip()]
    if len(services) != len(config["services"]) or any(s["State"] != "running" for s in services):
        raise RuntimeError(f"service state: {[(s['Service'], s['State']) for s in services]}")
    target = json.loads((task / "metadata" / "metadata.json").read_text())["target_host"]
    host, port = target.rsplit(":", 1)
    logged(
        ["docker", "run", "--rm", "--network", network, "--entrypoint", "python3", IMAGE,
         "-c", PROBE, host, port],
        directory / "probe.log", timeout=90,
    )
    result.update({"project": project, "network": network, "services": [s["Service"] for s in services]})
    return result


def main():
    tasks = [line.strip() for line in (ROOT / "task_list.txt").read_text().splitlines() if line.strip()]
    if len(tasks) != 40 or any(not (ROOT / task / "metadata" / "metadata.json").is_file() for task in tasks):
        raise RuntimeError("all 40 task directories must be present")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(prepare, index, task): (index, task) for index, task in enumerate(tasks, 1)}
        for future in as_completed(futures):
            index, task = futures[future]
            try:
                manifest[index] = future.result()
            except Exception as error:
                manifest[index] = {"task": task, "status": "failed", "error": str(error)}
            (OUTPUT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            print(f"{index:02d} {manifest[index]['status']} {task}", flush=True)
    if any(item["status"] != "ready" for item in manifest.values()):
        raise SystemExit("some environments failed; see logs/mopmonkagent_envs/manifest.json")


if __name__ == "__main__":
    main()
