#!/bin/sh
# Этап 2: запуск без параметров и выход.
cd "$(dirname "$0")/.." || exit 1
echo "=== run.sh (no parameters) ==="
echo exit | ./run.sh
echo "exit status: $?"
