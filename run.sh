#!/bin/sh
# Запуск эмулятора. Все аргументы передаются эмулятору.
PYTHONPATH="$(dirname "$0")/src" exec python3 -m shell_emulator "$@"
