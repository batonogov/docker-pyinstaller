#!/bin/bash

if [ -z $1 ];
then
    echo "Enter dockerfile name"
else
    docker build -f $1 -t test_image . && \
    docker run -v "$(pwd)/test:/src/" test_image "pyinstaller main.py"
fi
