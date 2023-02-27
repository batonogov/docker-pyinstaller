#!/bin/bash

if [ -z $1 ];
then
    echo "Enter dockerfile name"
else
    docker build -f $1 --platform=linux/arm64 -t test_arm64 . && \
    docker build -f $1 --platform=linux/amd64 -t test_amd64 . && \
    docker run -v "$(pwd)/test:/src/" test_arm64 "pyinstaller main.py --onefile" && \
    docker run -v "$(pwd)/test:/src/" test_amd64 "pyinstaller main.py --onefile"
fi
