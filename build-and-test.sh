#!/bin/bash

if [ -z $1 ];
then
    echo "Enter dockerfile name"
else
    docker build -f $1 -t pyinstaller_test . && \
    docker run -v "$(pwd)/test:/src/" pyinstaller_test "pyinstaller main.py --onefile"
fi
