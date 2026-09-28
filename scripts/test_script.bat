@echo off
rem Stage 2: only --script parameter.
pushd "%~dp0.."
echo === run.bat --script examples\stage2.txt ===
call .\run.bat --script examples\stage2.txt
echo exit status: %ERRORLEVEL%
popd
