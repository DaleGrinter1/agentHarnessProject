"""Run one bounded worker task through the Modal sandbox harness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from agent_harness import DEFAULT_STATUS_PATH, ModalWorkerRunner, WorkerTask  # noqa: E402
from agent_harness.status_store import (  # noqa: E402
    append_worker_record,
    result_record,
    running_record,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--cmd", required=True)
    parser.add_argument("--worker-name", default="modal-worker")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--resource-class", default="cpu")
    parser.add_argument("--block-network", action="store_true")
    parser.add_argument("--pip-install", action="append", default=[])
    parser.add_argument("--env", action="append", default=[], metavar="KEY=VALUE")
    parser.add_argument("--status-file", type=Path, default=DEFAULT_STATUS_PATH)
    parser.add_argument(
        "--no-status-file",
        action="store_true",
        help="Do not append worker records to the status JSONL file.",
    )
    return parser.parse_args()


def parse_env(items: list[str]) -> dict[str, str]:
    env: dict[str, str] = {}
    for item in items:
        key, sep, value = item.partition("=")
        if not sep or not key:
            raise SystemExit(f"Invalid --env value: {item!r}. Expected KEY=VALUE.")
        env[key] = value
    return env


def main() -> None:
    args = parse_args()
    task = WorkerTask(
        task_id=args.task_id,
        objective=args.objective,
        command=args.cmd,
        worker_name=args.worker_name,
        timeout_s=args.timeout,
        resource_class=args.resource_class,
        block_network=args.block_network,
        pip_install=tuple(args.pip_install),
        env=parse_env(args.env),
    )

    if not args.no_status_file:
        append_worker_record(args.status_file, running_record(task))

    result = ModalWorkerRunner().run(task)
    if not args.no_status_file:
        append_worker_record(args.status_file, result_record(result, task.objective))

    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    if result.status.value != "succeeded":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
