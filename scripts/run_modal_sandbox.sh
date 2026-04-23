#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)

if [ -d "$repo_root/.venv-modal" ]; then
  # shellcheck disable=SC1091
  . "$repo_root/.venv-modal/bin/activate"
fi

cmd=${1:-}
if [ -z "$cmd" ]; then
  cat <<'EOF' >&2
Usage:
  scripts/run_modal_sandbox.sh "python -V"
  scripts/run_modal_sandbox.sh "ls -la /workspace"

This wrapper mounts the repository at /workspace and runs the command there.
Add extra Modal options after a literal -- separator:
  scripts/run_modal_sandbox.sh "pytest" -- --pip-install pytest --block-network
EOF
  exit 1
fi

shift

if [ "${1:-}" = "--" ]; then
  shift
fi

exec python "$repo_root/scripts/modal_sandbox_demo.py" \
  --mount-repo \
  --remote-dir /workspace \
  --workdir /workspace \
  --cmd "$cmd" \
  "$@"
