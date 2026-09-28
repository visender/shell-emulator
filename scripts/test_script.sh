#!/bin/sh
# Этап 2: только параметр --script.
cd "$(dirname "$0")/.." || exit 1
echo "=== run.sh --script examples/stage2.txt ==="
./run.sh --script examples/stage2.txt
echo "exit status: $?"
