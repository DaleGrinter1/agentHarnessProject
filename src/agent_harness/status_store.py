"""JSONL persistence for worker status records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contract import WorkerResult, WorkerStatus, WorkerTask
from .modal_worker import utc_now


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STATUS_PATH = REPO_ROOT / "docs" / "generated" / "agent-workers.jsonl"


def running_record(task: WorkerTask) -> dict[str, Any]:
    return {
        "task_id": task.task_id,
        "worker_name": task.worker_name,
        "objective": task.objective,
        "status": WorkerStatus.RUNNING.value,
        "command": task.command,
        "returncode": None,
        "started_at": utc_now(),
        "finished_at": None,
        "duration_s": 0,
        "resource_class": task.resource_class,
        "sandbox_id": None,
        "app_name": None,
        "workdir": task.workdir,
        "stdout_tail": "",
        "stderr_tail": "",
        "summary": "Worker is running.",
        "error": None,
    }


def result_record(result: WorkerResult, objective: str) -> dict[str, Any]:
    record = result.to_dict()
    record["objective"] = objective
    return record


def append_worker_record(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True))
        handle.write("\n")


def load_worker_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path} line {line_number} is not valid JSON: {exc}") from exc
        if isinstance(record, dict):
            records.append(record)
    return records


def latest_worker_records(path: Path) -> list[dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for record in load_worker_records(path):
        task_id = record.get("task_id")
        if isinstance(task_id, str) and task_id:
            latest[task_id] = record
    return sorted(
        latest.values(),
        key=lambda item: str(item.get("started_at") or item.get("finished_at") or ""),
        reverse=True,
    )
