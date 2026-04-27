"""Single-worker runner that delegates execution to the Modal sandbox script."""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic

from .contract import WorkerResult, WorkerStatus, WorkerTask


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODAL_SCRIPT = REPO_ROOT / "scripts" / "modal_sandbox_demo.py"
TAIL_CHARS = 4000


@dataclass(frozen=True)
class CommandResult:
    """Small subprocess result shape for testable command execution."""

    returncode: int
    stdout: str
    stderr: str


Executor = Callable[[Sequence[str], float], CommandResult]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_executor(argv: Sequence[str], timeout_s: float) -> CommandResult:
    completed = subprocess.run(
        list(argv),
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_s,
    )
    return CommandResult(
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


class ModalWorkerRunner:
    """Runs one bounded worker task through the existing Modal sandbox helper."""

    def __init__(
        self,
        modal_script: Path = DEFAULT_MODAL_SCRIPT,
        executor: Executor = default_executor,
    ) -> None:
        self.modal_script = modal_script
        self.executor = executor

    def build_argv(self, task: WorkerTask) -> list[str]:
        argv = [
            sys.executable,
            str(self.modal_script),
            "--mount-repo",
            "--remote-dir",
            task.remote_dir,
            "--workdir",
            task.workdir,
            "--timeout",
            str(task.timeout_s),
            "--cmd",
            task.command,
        ]

        if task.block_network:
            argv.append("--block-network")
        for package in task.pip_install:
            argv.extend(["--pip-install", package])
        for key, value in task.env.items():
            argv.extend(["--env", f"{key}={value}"])

        return argv

    def run(self, task: WorkerTask) -> WorkerResult:
        started_at = utc_now()
        started = monotonic()

        try:
            command_result = self.executor(self.build_argv(task), task.timeout_s + 30)
            parsed = parse_modal_output(command_result.stdout)
            worker_returncode = parsed.returncode
            status = status_from_returncodes(command_result.returncode, worker_returncode)
            error = command_result.stderr.strip() or None
        except subprocess.TimeoutExpired as exc:
            finished_at = utc_now()
            return WorkerResult(
                task_id=task.task_id,
                worker_name=task.worker_name,
                status=WorkerStatus.TIMED_OUT,
                command=task.command,
                returncode=None,
                started_at=started_at,
                finished_at=finished_at,
                duration_s=round(monotonic() - started, 3),
                resource_class=task.resource_class,
                workdir=task.workdir,
                summary=f"Worker timed out after {task.timeout_s} seconds.",
                error=str(exc),
            )
        except Exception as exc:  # noqa: BLE001 - boundary should report failures.
            finished_at = utc_now()
            return WorkerResult(
                task_id=task.task_id,
                worker_name=task.worker_name,
                status=WorkerStatus.RUNNER_ERROR,
                command=task.command,
                returncode=None,
                started_at=started_at,
                finished_at=finished_at,
                duration_s=round(monotonic() - started, 3),
                resource_class=task.resource_class,
                workdir=task.workdir,
                summary="Worker runner failed before sandbox completion.",
                error=str(exc),
            )

        finished_at = utc_now()
        stdout_tail = tail(parsed.stdout or command_result.stdout)
        stderr_tail = tail(parsed.stderr or command_result.stderr)

        return WorkerResult(
            task_id=task.task_id,
            worker_name=task.worker_name,
            status=status,
            command=task.command,
            returncode=worker_returncode,
            started_at=started_at,
            finished_at=finished_at,
            duration_s=round(monotonic() - started, 3),
            resource_class=task.resource_class,
            sandbox_id=parsed.metadata.get("sandbox_id"),
            app_name=parsed.metadata.get("app_name"),
            workdir=parsed.metadata.get("workdir", task.workdir),
            stdout_tail=stdout_tail,
            stderr_tail=stderr_tail,
            summary=summarize(status, worker_returncode, stdout_tail, stderr_tail),
            error=error,
        )


@dataclass(frozen=True)
class ParsedModalOutput:
    metadata: dict[str, str]
    stdout: str
    stderr: str

    @property
    def returncode(self) -> int | None:
        value = self.metadata.get("returncode")
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None


def parse_modal_output(output: str) -> ParsedModalOutput:
    metadata: dict[str, str] = {}
    stdout_lines: list[str] = []
    stderr_lines: list[str] = []
    section: str | None = None

    for line in output.splitlines():
        if line == "--- stdout ---":
            section = "stdout"
            continue
        if line == "--- stderr ---":
            section = "stderr"
            continue

        if section == "stdout":
            stdout_lines.append(line)
        elif section == "stderr":
            stderr_lines.append(line)
        else:
            key, sep, value = line.partition("=")
            if sep:
                metadata[key] = value

    return ParsedModalOutput(
        metadata=metadata,
        stdout="\n".join(stdout_lines).strip(),
        stderr="\n".join(stderr_lines).strip(),
    )


def status_from_returncodes(
    process_returncode: int,
    worker_returncode: int | None,
) -> WorkerStatus:
    if process_returncode != 0:
        return WorkerStatus.RUNNER_ERROR
    if worker_returncode == 0:
        return WorkerStatus.SUCCEEDED
    return WorkerStatus.FAILED


def tail(value: str, limit: int = TAIL_CHARS) -> str:
    return value[-limit:].strip()


def summarize(
    status: WorkerStatus,
    returncode: int | None,
    stdout_tail: str,
    stderr_tail: str,
) -> str:
    if status == WorkerStatus.SUCCEEDED:
        detail = first_line(stdout_tail) or "No stdout captured."
        return f"Worker succeeded with return code 0. {detail}"
    if status == WorkerStatus.FAILED:
        detail = first_line(stderr_tail) or first_line(stdout_tail) or "No output captured."
        return f"Worker command failed with return code {returncode}. {detail}"
    if status == WorkerStatus.RUNNER_ERROR:
        detail = first_line(stderr_tail) or "The Modal helper did not complete cleanly."
        return f"Worker runner failed. {detail}"
    return "Worker timed out."


def first_line(value: str) -> str:
    for line in value.splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned
    return ""
