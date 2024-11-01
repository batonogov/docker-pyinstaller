#!/bin/bash

if [ -z "$1" ]; then
    echo "Enter Dockerfile name"
    exit 1
fi

if ! command -v docker &>/dev/null && ! command -v podman &>/dev/null; then
    echo "Neither Docker nor Podman is installed"
    exit 1
fi

build_and_run() {
    local build_cmd=$1
    local run_cmd=$2
    local dockerfile=$3
    local pyinstaller_args=${4:-"--onefile"}

    $build_cmd -f "$dockerfile" -t pyinstaller_test . && \
    $run_cmd -v "$(pwd)/test:/src/" pyinstaller_test "pyinstaller main.py $pyinstaller_args"
}

if ! build_and_run "docker build" "docker run" "$1"; then
    echo "Docker build failed, trying Podman..."
    build_and_run "podman build" "podman run" "$1"
fi
