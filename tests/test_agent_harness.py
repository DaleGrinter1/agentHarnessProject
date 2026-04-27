from __future__ import annotations

import subprocess
import sys
import unittest
from contextlib import suppress
from pathlib import Path
from uuid import uuid4

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from agent_harness.contract import WorkerStatus, WorkerTask
from agent_harness.modal_worker import (
    CommandResult,
    ModalWorkerRunner,
    parse_modal_output,
)
from agent_harness.status_store import (
    append_worker_record,
    latest_worker_records,
    result_record,
    running_record,
)
from agent_harness.status_view import render_status
from scripts.modal_sandbox_demo import sandbox_returncode


class ModalWorkerTests(unittest.TestCase):
    def test_sandbox_returncode_uses_wait_result_when_available(self) -> None:
        class Sandbox:
            returncode = None

        self.assertEqual(sandbox_returncode(Sandbox(), 0), 0)

    def test_sandbox_returncode_falls_back_to_property(self) -> None:
        class Sandbox:
            returncode = 0

        self.assertEqual(sandbox_returncode(Sandbox(), None), 0)

    def test_sandbox_returncode_falls_back_to_poll(self) -> None:
        class Sandbox:
            returncode = None

            def poll(self) -> int:
                return 0

        self.assertEqual(sandbox_returncode(Sandbox(), None), 0)

    def test_parse_modal_output_splits_metadata_and_streams(self) -> None:
        parsed = parse_modal_output(
            "\n".join(
                [
                    "sandbox_id=sb-123",
                    "app_name=test-app",
                    "returncode=0",
                    "workdir=/workspace",
                    "--- stdout ---",
                    "hello",
                    "--- stderr ---",
                    "warning",
                ]
            )
        )

        self.assertEqual(parsed.metadata["sandbox_id"], "sb-123")
        self.assertEqual(parsed.returncode, 0)
        self.assertEqual(parsed.stdout, "hello")
        self.assertEqual(parsed.stderr, "warning")

    def test_runner_reports_success_from_modal_helper_output(self) -> None:
        def executor(argv: list[str], timeout_s: float) -> CommandResult:
            self.assertIn("--mount-repo", argv)
            self.assertIn("--cmd", argv)
            self.assertGreater(timeout_s, 30)
            return CommandResult(
                returncode=0,
                stdout=(
                    "sandbox_id=sb-123\n"
                    "app_name=test-app\n"
                    "returncode=0\n"
                    "workdir=/workspace\n"
                    "--- stdout ---\n"
                    "ok\n"
                ),
                stderr="",
            )

        result = ModalWorkerRunner(executor=executor).run(
            WorkerTask(
                task_id="smoke",
                objective="prove worker path",
                command="python -V",
            )
        )

        self.assertEqual(result.status, WorkerStatus.SUCCEEDED)
        self.assertEqual(result.sandbox_id, "sb-123")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Worker succeeded", result.summary)

    def test_runner_reports_worker_command_failure(self) -> None:
        def executor(argv: list[str], timeout_s: float) -> CommandResult:
            return CommandResult(
                returncode=0,
                stdout=(
                    "sandbox_id=sb-123\n"
                    "returncode=2\n"
                    "--- stderr ---\n"
                    "bad command\n"
                ),
                stderr="",
            )

        result = ModalWorkerRunner(executor=executor).run(
            WorkerTask(
                task_id="fail",
                objective="show failure",
                command="exit 2",
            )
        )

        self.assertEqual(result.status, WorkerStatus.FAILED)
        self.assertEqual(result.returncode, 2)
        self.assertIn("bad command", result.summary)

    def test_runner_reports_timeout(self) -> None:
        def executor(argv: list[str], timeout_s: float) -> CommandResult:
            raise subprocess.TimeoutExpired(argv, timeout_s)

        result = ModalWorkerRunner(executor=executor).run(
            WorkerTask(
                task_id="timeout",
                objective="show timeout",
                command="sleep 999",
                timeout_s=1,
            )
        )

        self.assertEqual(result.status, WorkerStatus.TIMED_OUT)
        self.assertIsNone(result.returncode)

    def test_status_store_keeps_latest_record_per_task(self) -> None:
        temp_dir = REPO_ROOT / "tests" / ".tmp" / uuid4().hex
        status_file = temp_dir / "workers.jsonl"
        try:
            task = WorkerTask(
                task_id="smoke",
                objective="prove worker path",
                command="python -V",
            )
            running = running_record(task)
            append_worker_record(status_file, running)

            result = ModalWorkerRunner(
                executor=lambda argv, timeout_s: CommandResult(
                    returncode=0,
                    stdout="returncode=0\n--- stdout ---\nok\n",
                    stderr="",
                )
            ).run(task)
            append_worker_record(status_file, result_record(result, task.objective))

            latest = latest_worker_records(status_file)

            self.assertEqual(len(latest), 1)
            self.assertEqual(latest[0]["task_id"], "smoke")
            self.assertEqual(latest[0]["status"], "succeeded")
            self.assertEqual(latest[0]["objective"], "prove worker path")
        finally:
            with suppress(FileNotFoundError):
                status_file.unlink()
            with suppress(FileNotFoundError):
                temp_dir.rmdir()
            with suppress(FileNotFoundError):
                temp_dir.parent.rmdir()

    def test_status_view_renders_worker_table(self) -> None:
        output = render_status(
            [
                {
                    "task_id": "smoke",
                    "worker_name": "modal-worker",
                    "objective": "prove worker path",
                    "status": "running",
                    "resource_class": "cpu",
                    "duration_s": 1.2,
                    "returncode": None,
                    "sandbox_id": "sb-123",
                    "summary": "Worker is running.",
                }
            ],
            color=False,
        )

        self.assertIn("Agent Workers", output)
        self.assertIn("running", output)
        self.assertIn("smoke", output)
        self.assertIn("prove worker", output)


if __name__ == "__main__":
    unittest.main()
