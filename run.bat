@echo off
rem Run the emulator. All arguments are passed through.
set "PYTHONPATH=%~dp0src"
py -m shell_emulator %*
