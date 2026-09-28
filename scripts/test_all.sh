#!/bin/sh
# Этап 2: все параметры вместе.
cd "$(dirname "$0")/.." || exit 1
echo "=== run.sh --vfs vfs_samples/minimal --script examples/stage2.txt ==="
./run.sh --vfs vfs_samples/minimal \
    --script examples/stage2.txt
echo "exit status: $?"
