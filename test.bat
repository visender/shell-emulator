@echo off
rem Run unit tests.
set "PYTHONPATH=%~dp0src"
py -m unittest discover -s "%~dp0tests" -v
