"""Create and run a reusable Modal sandbox from this repository.

Examples:
  source .venv-modal/bin/activate
  python scripts/modal_sandbox_demo.py
  python scripts/modal_sandbox_demo.py --cmd "python -V"
  python scripts/modal_sandbox_demo.py \
    --mount-local-dir . \
    --remote-dir /workspace \
    --workdir /workspace \
    --cmd "ls -la && python -c 'print(\"sandbox ready\")'"

Environment variable fallbacks:
  MODAL_APP_NAME
  MODAL_SANDBOX_CMD
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENV_FILE = REPO_ROOT / ".env"


def default_app_name() -> str:
    configured = os.environ.get("MODAL_APP_NAME")
    if configured:
        return configured

    repo_name = re.sub(r"[^A-Za-z0-9._-]+", "-", REPO_ROOT.name).strip("-")
    return f"{repo_name or 'workspace'}-sandbox"


DEFAULT_APP_NAME = default_app_name()
DEFAULT_SANDBOX_CMD = os.environ.get(
    "MODAL_SANDBOX_CMD",
    "python -c \"print('hello from modal sandbox')\"",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-name", default=DEFAULT_APP_NAME)
    parser.add_argument("--cmd", default=DEFAULT_SANDBOX_CMD)
    parser.add_argument("--python-version", default="3.12")
    parser.add_argument(
        "--env-file",
        type=Path,
        default=DEFAULT_ENV_FILE,
        help="Path to a local .env file to load before creating the sandbox.",
    )
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--idle-timeout", type=int)
    parser.add_argument(
        "--pip-install",
        action="append",
        default=[],
        metavar="PACKAGE",
        help="Repeat to add packages to the sandbox image.",
    )
    parser.add_argument(
        "--mount-repo",
        action="store_true",
        help="Upload the repository root into the sandbox.",
    )
    parser.add_argument(
        "--mount-local-dir",
        type=Path,
        help="Upload a local directory into the image before the sandbox starts.",
    )
    parser.add_argument(
        "--remote-dir",
        default="/workspace",
        help="Remote directory for --mount-repo or --mount-local-dir and default workdir.",
    )
    parser.add_argument(
        "--workdir",
        help="Working directory inside the sandbox. Defaults to --remote-dir when mounting.",
    )
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Repeat to set environment variables inside the sandbox.",
    )
    parser.add_argument(
        "--block-network",
        action="store_true",
        help="Disable outbound network access inside the sandbox.",
    )
    parser.add_argument(
        "--cpu",
        type=float,
        help="Requested CPU cores for the sandbox.",
    )
    parser.add_argument(
        "--memory",
        type=int,
        help="Requested memory in MiB for the sandbox.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Stream Modal image build and sandbox logs.",
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


def selected_mount_dir(args: argparse.Namespace) -> Path | None:
    if args.mount_repo:
        return REPO_ROOT
    return args.mount_local_dir


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :]

        key, sep, value = line.partition("=")
        if not sep or not key:
            raise SystemExit(f"Invalid line in env file {path}: {raw_line!r}")

        cleaned = value.strip().strip("\"'")
        os.environ.setdefault(key.strip(), cleaned)


def build_image(args: argparse.Namespace):
    import modal

    image = modal.Image.debian_slim(python_version=args.python_version)

    mount_dir = selected_mount_dir(args)
    if mount_dir:
        local_path = mount_dir.expanduser().resolve()
        if not local_path.is_dir():
            raise SystemExit(f"--mount-local-dir must point to a directory: {local_path}")
        image = image.add_local_dir(local_path=local_path, remote_path=args.remote_dir)

    if args.pip_install:
        image = image.pip_install(args.pip_install)

    return image


def read_stream(stream: object) -> str:
    data = stream.read()
    if isinstance(data, bytes):
        return data.decode()
    return str(data)


def sandbox_returncode(sandbox: object, wait_result: object) -> int | None:
    if isinstance(wait_result, int):
        return wait_result

    returncode = getattr(sandbox, "returncode", None)
    if isinstance(returncode, int):
        return returncode

    poll = getattr(sandbox, "poll", None)
    if callable(poll):
        polled = poll()
        if isinstance(polled, int):
            return polled

    return None


def main() -> None:
    import modal

    args = parse_args()
    load_env_file(args.env_file.expanduser().resolve())
    env = parse_env(args.env)
    image = build_image(args)
    app = modal.App.lookup(args.app_name, create_if_missing=True)
    mount_dir = selected_mount_dir(args)
    workdir = args.workdir or (args.remote_dir if mount_dir else None)

    sandbox = modal.Sandbox.create(
        "bash",
        "-lc",
        args.cmd,
        app=app,
        image=image,
        env=env or None,
        timeout=args.timeout,
        idle_timeout=args.idle_timeout,
        workdir=workdir,
        block_network=args.block_network,
        cpu=args.cpu,
        memory=args.memory,
        verbose=args.verbose,
    )

    try:
        wait_result = sandbox.wait()
        returncode = sandbox_returncode(sandbox, wait_result)
        stdout = read_stream(sandbox.stdout)
        stderr = read_stream(sandbox.stderr)
    finally:
        sandbox.detach()

    print(f"sandbox_id={sandbox.object_id}")
    print(f"app_name={args.app_name}")
    print(f"returncode={returncode}")
    if workdir:
        print(f"workdir={workdir}")
    if mount_dir:
        print(f"mounted_local_dir={mount_dir.expanduser().resolve()}")
        print(f"mounted_remote_dir={args.remote_dir}")
    if stdout:
        print("--- stdout ---")
        print(stdout)
    if stderr:
        print("--- stderr ---")
        print(stderr)


if __name__ == "__main__":
    main()
