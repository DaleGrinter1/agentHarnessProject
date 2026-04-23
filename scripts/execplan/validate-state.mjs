#!/usr/bin/env python3

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd()
ACTIVE_ROOT = ROOT / "docs" / "exec-plans" / "active"
PRODUCT_DIR = Path("docs") / ("product-" + "specs")
PRODUCT_INDEX = PRODUCT_DIR / "index.md"
LEGACY_AGENT_PATTERN = "." + "agent/"
LEGACY_PRODUCT_PATTERN = "sp" + "ecs/"
REQUIRED_SECTIONS = [
    "## Purpose / Big Picture",
    "## Surprises & Discoveries",
    "## Decision Log",
    "## Outcomes & Retrospective",
    "## Context and Orientation",
    "## Plan of Work",
    "## Concrete Steps",
    "## Machine State",
    "## Progress",
    "## Testing Approach",
    "## Constraints & Considerations",
]
CANONICAL_FILES = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("ARCHITECTURE.md"),
    Path("docs") / "design-docs" / "index.md",
    Path("docs") / "design-docs" / "core-beliefs.md",
    Path("docs") / "exec-plans" / "PLAN_TEMPLATE.md",
    Path("docs") / "exec-plans" / "index.md",
    Path("docs") / "exec-plans" / "active" / "README.md",
    Path("docs") / "exec-plans" / "tech-debt-tracker.md",
    Path("docs") / "generated" / "db-schema.md",
    PRODUCT_INDEX,
    Path("docs") / "references" / "index.md",
    Path("docs") / "DESIGN.md",
    Path("docs") / "FRONTEND.md",
    Path("docs") / "PLANS.md",
    Path("docs") / "PRODUCT_SENSE.md",
    Path("docs") / "QUALITY_SCORE.md",
    Path("docs") / "RELIABILITY.md",
    Path("docs") / "SECURITY.md",
]

problems = []


def main() -> int:
    for rel_path in CANONICAL_FILES:
      if not (ROOT / rel_path).exists():
          problems.append(f"Missing canonical file: {rel_path}")

    if not ACTIVE_ROOT.exists():
        problems.append("Missing active exec-plans directory: docs/exec-plans/active")
    else:
        for initiative_dir in sorted([p for p in ACTIVE_ROOT.iterdir() if p.is_dir()]):
            validate_initiative(initiative_dir)

    for rel_path in markdown_files():
        validate_markdown_links(rel_path)

    validate_deprecated_paths()

    if problems:
        print("Execplan validation failed:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1

    print("Execplan state validation passed.")
    return 0


def validate_initiative(initiative_dir: Path) -> None:
    initiative = initiative_dir.name
    markdown_files_in_root = sorted(p.name for p in initiative_dir.glob("*.md"))
    plan_files = [name for name in markdown_files_in_root if re.match(r"^PLAN_.+\.md$", name)]
    non_plan_markdown = [name for name in markdown_files_in_root if name not in plan_files]

    if len(plan_files) != 1:
        problems.append(
            f"{initiative}: expected exactly one PLAN_*.md file, found {len(plan_files)}"
        )
        return

    if non_plan_markdown:
        problems.append(
            f"{initiative}: unexpected markdown files in active initiative: {', '.join(non_plan_markdown)}"
        )

    if has_tasks_directory(initiative_dir):
        problems.append(f"{initiative}: deprecated tasks directory found in active initiative")

    plan_file = plan_files[0]
    plan_path = initiative_dir / plan_file
    state_dir = initiative_dir / "state"
    feature_list_path = state_dir / "feature-list.json"
    session_state_path = state_dir / "session-state.json"
    progress_path = state_dir / "progress.jsonl"

    if not state_dir.exists():
        problems.append(f"{initiative}: missing state directory")
        return

    for required in [feature_list_path, session_state_path, progress_path]:
        if not required.exists():
            problems.append(f"{initiative}: missing required state file {required.name}")

    plan_text = safe_read(plan_path)
    for section in REQUIRED_SECTIONS:
        if section not in plan_text:
            problems.append(f"{initiative}: plan missing required section '{section}'")

    feature_list = parse_json(feature_list_path, f"{initiative}: feature-list.json")
    session_state = parse_json(session_state_path, f"{initiative}: session-state.json")
    progress_entries = parse_jsonl(progress_path, f"{initiative}: progress.jsonl")

    if feature_list is None or session_state is None or progress_entries is None:
        return

    if feature_list.get("initiative") != initiative:
        problems.append(f"{initiative}: feature-list.json initiative must equal directory name")

    if feature_list.get("plan") != plan_file:
        problems.append(f"{initiative}: feature-list.json plan must equal {plan_file}")

    features = feature_list.get("features")
    if not isinstance(features, list) or not features:
        problems.append(f"{initiative}: feature-list.json must contain a non-empty features array")
        return

    feature_ids = set()
    for feature in features:
        if not isinstance(feature, dict):
            problems.append(f"{initiative}: feature entries must be objects")
            continue
        feature_id = feature.get("id")
        if not is_non_empty_string(feature_id):
            problems.append(f"{initiative}: each feature needs a non-empty id")
            continue
        if feature_id in feature_ids:
            problems.append(f"{initiative}: duplicate feature id '{feature_id}'")
        feature_ids.add(feature_id)
        if not is_non_empty_string(feature.get("title")):
            problems.append(f"{initiative}: feature '{feature_id}' is missing a title")
        if not is_non_empty_string(feature.get("description")):
            problems.append(f"{initiative}: feature '{feature_id}' is missing a description")
        if not isinstance(feature.get("passes"), bool):
            problems.append(f"{initiative}: feature '{feature_id}' must have boolean passes")

    if session_state.get("initiative") != initiative:
        problems.append(f"{initiative}: session-state.json initiative must equal directory name")

    if session_state.get("plan") != plan_file:
        problems.append(f"{initiative}: session-state.json plan must equal {plan_file}")

    active_feature_id = session_state.get("active_feature_id")
    if active_feature_id not in (None, "") and active_feature_id not in feature_ids:
        problems.append(
            f"{initiative}: session-state.json active_feature_id must reference a valid feature id"
        )

    if not isinstance(session_state.get("blockers"), list):
        problems.append(f"{initiative}: session-state.json blockers must be an array")
    if not is_non_empty_string(session_state.get("next_action")):
        problems.append(f"{initiative}: session-state.json next_action must be a non-empty string")
    if not isinstance(session_state.get("handoff_rules"), list) or not session_state.get(
        "handoff_rules"
    ):
        problems.append(f"{initiative}: session-state.json handoff_rules must be a non-empty array")
    if not is_iso_timestamp(session_state.get("updated_at")):
        problems.append(f"{initiative}: session-state.json updated_at must be an ISO timestamp")

    if not progress_entries:
        problems.append(f"{initiative}: progress.jsonl must contain at least one entry")

    last_timestamp = None
    for index, entry in enumerate(progress_entries, start=1):
        label = f"{initiative}: progress entry {index}"
        if not is_iso_timestamp(entry.get("timestamp")):
            problems.append(f"{label} must include an ISO timestamp")
        if not is_non_empty_string(entry.get("actor")):
            problems.append(f"{label} must include actor")
        if not is_non_empty_string(entry.get("type")):
            problems.append(f"{label} must include type")
        if not is_non_empty_string(entry.get("summary")):
            problems.append(f"{label} must include summary")
        feature_refs = entry.get("feature_refs")
        if not isinstance(feature_refs, list) or not feature_refs:
            problems.append(f"{label} must include non-empty feature_refs")
        else:
            for feature_ref in feature_refs:
                if feature_ref not in feature_ids:
                    problems.append(f"{label} references unknown feature '{feature_ref}'")
        evidence = entry.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            problems.append(f"{label} must include non-empty evidence")
        timestamp = entry.get("timestamp")
        if last_timestamp and isinstance(timestamp, str) and timestamp < last_timestamp:
            problems.append(f"{label} timestamps must be non-decreasing")
        last_timestamp = timestamp


def validate_markdown_links(rel_path: Path) -> None:
    abs_path = ROOT / rel_path
    text = safe_read(abs_path)
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        normalized = target.strip("<>").split("#", 1)[0]
        if normalized.startswith("/"):
            resolved = ROOT / normalized.lstrip("/")
        else:
            resolved = (abs_path.parent / normalized).resolve()
        if not resolved.exists():
            problems.append(f"{rel_path}: broken local markdown link target '{target}'")


def validate_deprecated_paths() -> None:
    tracked_files = git_tracked_files()
    for rel_path in tracked_files:
        text = safe_read(ROOT / rel_path)
        if LEGACY_AGENT_PATTERN in text:
            problems.append(f"{rel_path}: contains deprecated hidden agent directory path")
        if rel_path.parts[:2] == PRODUCT_DIR.parts[:2]:
            continue
        if LEGACY_PRODUCT_PATTERN in text:
            problems.append(f"{rel_path}: contains deprecated product shortcut path")


def git_tracked_files():
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        return [Path(line) for line in result.stdout.splitlines() if line.strip()]
    except subprocess.CalledProcessError as error:
        problems.append(f"Unable to list tracked files: {error}")
        return []


def markdown_files():
    files = [Path("AGENTS.md"), Path("README.md"), Path("ARCHITECTURE.md")]
    docs_dir = ROOT / "docs"
    if docs_dir.exists():
        files.extend(sorted(path.relative_to(ROOT) for path in docs_dir.rglob("*.md")))
    return files


def has_tasks_directory(directory: Path) -> bool:
    for child in directory.rglob("*"):
        if child.is_dir() and child.name == "tasks":
            return True
    return False


def safe_read(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8")
    except OSError as error:
        problems.append(f"Unable to read {file_path.relative_to(ROOT)}: {error}")
        return ""


def parse_json(file_path: Path, label: str):
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        problems.append(f"{label} is not valid JSON: {error}")
        return None


def parse_jsonl(file_path: Path, label: str):
    try:
        lines = [line for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except OSError as error:
        problems.append(f"{label} could not be read: {error}")
        return None

    entries = []
    for index, line in enumerate(lines, start=1):
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as error:
            problems.append(f"{label} line {index} is not valid JSON: {error}")
    return entries


def is_iso_timestamp(value) -> bool:
    return is_non_empty_string(value) and value.endswith("Z")


def is_non_empty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


if __name__ == "__main__":
    sys.exit(main())
