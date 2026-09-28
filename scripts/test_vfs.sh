#!/bin/sh
# Этап 2: только параметр --vfs.
cd "$(dirname "$0")/.." || exit 1
echo "=== run.sh --vfs vfs_samples/minimal ==="
echo exit | ./run.sh --vfs vfs_samples/minimal
echo "exit status: $?"
