@echo off
rem Stage 2: start without parameters, then exit.
pushd "%~dp0.."
echo === run.bat (no parameters) ===
echo exit| .\run.bat
echo exit status: %ERRORLEVEL%
popd
