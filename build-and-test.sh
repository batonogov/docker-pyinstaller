#!/bin/bash

docker build -f $1 -t test . && \
echo "print('hello world')" > test.py && \
docker run -v "$(pwd):/src/" test "pyinstaller test.py" && \
rm test.py
