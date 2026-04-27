"""Typed task and result contracts for sandboxed workers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class WorkerStatus(StrEnum):
    """Worker states surfaced by the harness."""

    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    RUNNER_ERROR = "runner_error"


@dataclass(frozen=True)
class WorkerTask:
    """Bounded work request owned by the orchestrator."""

    task_id: str
    objective: str
    command: str
    worker_name: str = "modal-worker"
    remote_dir: str = "/workspace"
    workdir: str = "/workspace"
    timeout_s: int = 300
    resource_class: str = "cpu"
    block_network: bool = False
    pip_install: tuple[str, ...] = ()
    env: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["pip_install"] = list(self.pip_install)
        return data


@dataclass(frozen=True)
class WorkerResult:
    """Machine-readable summary returned by a worker run."""

    task_id: str
    worker_name: str
    status: WorkerStatus
    command: str
    returncode: int | None
    started_at: str
    finished_at: str
    duration_s: float
    resource_class: str
    sandbox_id: str | None = None
    app_name: str | None = None
    workdir: str | None = None
    stdout_tail: str = ""
    stderr_tail: str = ""
    summary: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data
