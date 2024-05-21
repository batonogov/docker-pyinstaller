#!/bin/bash

if [ -z $1 ]; then
    echo "Enter dockerfile name"
    exit 1
fi

build_and_run() {
    local build_cmd=$1
    local run_cmd=$2
    local dockerfile=$3

    $build_cmd -f $dockerfile -t pyinstaller_test . && \
    $run_cmd -v "$(pwd)/test:/src/" pyinstaller_test "pyinstaller main.py --onefile"
}

# Try with Docker
if ! build_and_run "docker build" "docker run" $1; then
    # If Docker fails, try with Podman
    build_and_run "podman build" "podman run" $1
fi
