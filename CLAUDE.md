# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Docker images for compiling Python applications into standalone executables using PyInstaller. Supports Linux (full/slim), Windows (via Wine), and macOS (via docker-osx).

## Build & Test Commands

Requires [go-task](https://taskfile.dev/). All commands defined in `Taskfile.yml`.

```bash
# Run all tests (builds images + compiles test app + verifies binaries)
task test

# Individual platform build
task build:linux
task build:linux-slim
task build:windows

# Individual platform test (includes build)
task test:linux
task test:linux-slim
task test:windows

# Set up git hooks (pre-push runs task test)
task setup
```

## Architecture

Four Dockerfiles, each producing a separate image variant:

- **Dockerfile-py3-linux** — full Python image (`python:3.13.11`), uses `uv` for fast package installs on amd64/arm64
- **Dockerfile-py3-linux-slim** — minimal image (`python:3.13.11-slim`), adds binutils/gcc/zlib
- **Dockerfile-py3-windows** — Ubuntu 24.04 + Wine + Python MSI + VC++ Redistributable, runs PyInstaller through Wine
- **Dockerfile-py3-osx** — based on `sickcodes/docker-osx:sonoma`, uses pipx

Each Dockerfile has a matching `entrypoint-{platform}.sh` that handles:
- Auto-detection of `.spec` files
- Installing `requirements.txt` (via `uv` if available, else `pip`)
- PyPI mirror support via `PYPI_URL`/`PYPI_INDEX_URL` env vars
- Running PyInstaller and fixing output file ownership

## Key Version ARGs

Python and PyInstaller versions are controlled via Dockerfile ARGs (`PYTHON_VERSION`, `PYINSTALLER_VERSION`). Current defaults: Python 3.13.11, PyInstaller 6.17.0.

## Testing

`test/main.py` is the integration test app — it imports numpy, pandas, flask, psutil, requests, sqlalchemy and runs functional checks. Dependencies listed in `test/requirements.txt`. The test flow: build Docker image → run container to compile `main.py` → execute the resulting binary.

## CI/CD

- **test.yml** — runs on PRs and non-main pushes; builds and tests all three platforms
- **docker-image-linux.yml** — publishes to Docker Hub on tags (`v*.*.*`) and main; multi-arch (up to 8 architectures including riscv64)
- **docker-image-windows.yml** — publishes Windows image to Docker Hub
- **docker-image-linux-ghcr.yml** — publishes to ghcr.io with cosign signing
- **AUTO_PR.yml** — auto-creates PR from feature branches

## Code Quality

Pre-commit hooks configured in `.pre-commit-config.yaml`: black, autoflake, pyupgrade (3.13+), isort, YAML formatting. Run `pre-commit run --all-files` to check.
