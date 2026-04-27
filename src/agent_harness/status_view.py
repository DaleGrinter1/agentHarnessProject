"""Terminal rendering for worker status records."""

from __future__ import annotations

from collections import Counter
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
    summary = "  ".join(f"{status}:{count}" for status, count in sorted(counts.items()))
    lines = ["Agent Workers", summary, ""]

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

    lines.append("")
    for record in records[:3]:
        task_id = clip(record.get("task_id"), 24)
        summary = str(record.get("summary") or "").strip()
        if summary:
            lines.append(f"{task_id}: {clip(summary, width - len(task_id) - 2)}")

    return "\n".join(lines)


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
    duration = record.get("duration_s")
    if isinstance(duration, int | float):
        return f"{duration:.1f}s"
    return "-"
