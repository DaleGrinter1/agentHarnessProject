"""Show the latest agent worker status records."""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from agent_harness import DEFAULT_STATUS_PATH, latest_worker_records  # noqa: E402
from agent_harness.status_view import render_status  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status-file", type=Path, default=DEFAULT_STATUS_PATH)
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--no-color", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    color = not args.no_color

    while True:
        records = latest_worker_records(args.status_file)
        if args.watch:
            os.system("cls" if os.name == "nt" else "clear")
        print(render_status(records, color=color))
        if not args.watch:
            return
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
