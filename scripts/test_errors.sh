#!/bin/sh
# Этап 2: неверные параметры и отсутствующий стартовый скрипт.
cd "$(dirname "$0")/.." || exit 1

echo "=== run.sh --script examples/missing.txt ==="
./run.sh --script examples/missing.txt
echo "exit status: $?"

echo "=== run.sh --unknown ==="
./run.sh --unknown
echo "exit status: $?"

echo "=== run.sh --vfs (no value) ==="
./run.sh --vfs
echo "exit status: $?"
