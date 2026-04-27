# Modal Sandbox Quickstart

This repo includes a reusable helper for creating a Modal sandbox from a local
script:

`scripts/modal_sandbox_demo.py`

There is also a convenience wrapper for the common "mount this repo into
`/workspace` and run a command there" workflow:

`scripts/run_modal_sandbox.sh`

The first agent-harness layer wraps that same Modal execution path in a typed
worker task/result contract:

`scripts/run_agent_worker.py`

Worker status can be displayed from the JSONL status log:

`scripts/agent_status.py`

## First-Time Setup

1. Activate the existing virtual environment:

   ```sh
   source .venv-modal/bin/activate
   ```

2. Authenticate with Modal if needed:

   ```sh
   modal setup
   ```

   Alternatively, create a repo-root `.env` file from `.env.example` and set
   `MODAL_TOKEN_ID` plus `MODAL_TOKEN_SECRET` there.

## Basic Usage

Run a simple command in a Modal sandbox:

```sh
python scripts/modal_sandbox_demo.py --cmd "python -V"
```

The helper automatically loads `.env` from the repo root by default before it
talks to Modal.

Run a command with the repo mounted at `/workspace` using the wrapper:

```sh
scripts/run_modal_sandbox.sh "ls -la"
```

Run one bounded worker task and print machine-readable JSON metadata:

```sh
python scripts/run_agent_worker.py \
  --task-id smoke \
  --objective "prove the worker path" \
  --cmd "python -V"
```

Show the latest worker statuses:

```sh
python scripts/agent_status.py
```

Watch the status file while another terminal runs workers:

```sh
python scripts/agent_status.py --watch
```

Upload the current repo into the sandbox and execute a command inside it:

```sh
python scripts/modal_sandbox_demo.py \
  --mount-repo \
  --remote-dir /workspace \
  --workdir /workspace \
  --cmd "ls -la && python -c 'print(\"sandbox ready\")'"
```

Install additional packages into the sandbox image:

```sh
python scripts/modal_sandbox_demo.py \
  --pip-install requests \
  --pip-install rich \
  --cmd "python -c 'import requests, rich; print(\"deps ok\")'"
```

Block outbound network access for a safer sandbox:

```sh
scripts/run_modal_sandbox.sh \
  "python -c 'print(\"offline sandbox\")'" \
  -- --block-network
```

## Notes

- The helper creates or reuses a Modal app based on the repo name by default.
  Override it with `--app-name` or `MODAL_APP_NAME`.
- If `--mount-repo` or `--mount-local-dir` is used, the default sandbox working
  directory becomes the matching `--remote-dir`.
- `--env KEY=VALUE` can be passed multiple times to set sandbox environment
  variables.
- `--cpu` and `--memory` can be used when you want a more explicit sandbox
  resource shape.
- `--timeout` controls the sandbox lifetime in seconds. Modal documents a
  maximum of 24 hours for a single sandbox.
- `scripts/run_agent_worker.py` currently supports the first single-worker
  control-plane path. Use it when the caller wants structured status,
  timestamps, sandbox id, return code, output tails, and a concise summary.
- Worker runs append status records to `docs/generated/agent-workers.jsonl` by
  default. Pass `--no-status-file` to skip persistence or `--status-file` to
  write somewhere else.
