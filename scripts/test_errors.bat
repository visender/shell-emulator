@echo off
rem Stage 2: invalid parameters and missing startup script.
pushd "%~dp0.."

echo === run.bat --script examples\missing.txt ===
call .\run.bat --script examples\missing.txt
echo exit status: %ERRORLEVEL%

echo === run.bat --unknown ===
call .\run.bat --unknown
echo exit status: %ERRORLEVEL%

echo === run.bat --vfs (no value) ===
call .\run.bat --vfs
echo exit status: %ERRORLEVEL%
popd
