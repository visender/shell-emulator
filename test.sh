#!/bin/sh
# Запуск модульных тестов.
DIR="$(dirname "$0")"
PYTHONPATH="$DIR/src" exec python3 -m unittest discover -s "$DIR/tests" -v
