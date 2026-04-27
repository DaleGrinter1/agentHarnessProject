"""Terminal rendering for worker status records."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from shutil import get_terminal_size
from typing import Any


STATUS_COLORS = {
    "running": "36",
    "succeeded": "32",
    "failed": "31",
    "timed_out": "33",
    "runner_error": "35",
}


def render_status(records: list[dict[str, Any]], color: bool = True) -> str:
    width = max(80, get_terminal_size(fallback=(100, 24)).columns)
    if not records:
        return "Agent Workers\n\nNo worker status records found."

    counts = Counter(str(record.get("status", "unknown")) for record in records)
    active = [record for record in records if is_active(record)]
    inactive = [record for record in records if not is_active(record)]
    summary = "  ".join(f"{status}:{count}" for status, count in sorted(counts.items()))
    lines = [
        "Agent Workers",
        f"active:{len(active)}  inactive:{len(inactive)}  {summary}",
        "",
    ]

    lines.extend(render_table("Active Tasks", active, width, color))
    lines.append("")
    lines.extend(render_table("Recent Completed", inactive[:10], width, color))

    return "\n".join(lines)


def render_table(
    title: str,
    records: list[dict[str, Any]],
    width: int,
    color: bool,
) -> list[str]:
    if not records:
        return [title, "  None"]

    columns = [
        ("status", 13),
        ("task", 18),
        ("worker", 16),
        ("resource", 10),
        ("duration", 9),
        ("return", 8),
        ("sandbox", 16),
    ]
    objective_width = max(16, width - sum(size for _, size in columns) - len(columns) * 3)

    lines = [title]
    header = (
        f"{'status':13}  {'task':18}  {'worker':16}  {'resource':10}  "
        f"{'duration':9}  {'return':8}  {'sandbox':16}  {'objective':{objective_width}}"
    )
    lines.append(header)
    lines.append("-" * min(width, len(header)))

    for record in records:
        status = str(record.get("status") or "unknown")
        rendered_status = colorize(status, status, color)
        lines.append(
            f"{rendered_status:22}  "
            f"{clip(record.get('task_id'), 18):18}  "
            f"{clip(record.get('worker_name'), 16):16}  "
            f"{clip(record.get('resource_class'), 10):10}  "
            f"{format_duration(record):9}  "
            f"{clip(record.get('returncode'), 8):8}  "
            f"{clip(record.get('sandbox_id'), 16):16}  "
            f"{clip(record.get('objective'), objective_width):{objective_width}}"
        )

    return lines


def is_active(record: dict[str, Any]) -> bool:
    return str(record.get("status") or "") == "running"


def colorize(value: str, status: str, enabled: bool) -> str:
    if not enabled:
        return value
    color = STATUS_COLORS.get(status)
    if not color:
        return value
    return f"\033[{color}m{value}\033[0m"


def clip(value: object, width: int) -> str:
    if value is None:
        text = "-"
    else:
        text = str(value)
    if len(text) <= width:
        return text
    if width <= 3:
        return text[:width]
    return text[: width - 3] + "..."


def format_duration(record: dict[str, Any]) -> str:
    if is_active(record):
        elapsed = elapsed_seconds(record.get("started_at"))
        if elapsed is not None:
            return f"{elapsed:.1f}s"

    duration = record.get("duration_s")
    if isinstance(duration, int | float):
        return f"{duration:.1f}s"
    return "-"


def elapsed_seconds(started_at: object) -> float | None:
    if not isinstance(started_at, str) or not started_at:
        return None
    try:
        started = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
    except ValueError:
        return None
    return max(0.0, (datetime.now(UTC) - started).total_seconds())
