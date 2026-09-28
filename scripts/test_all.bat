@echo off
rem Stage 2: all parameters together.
pushd "%~dp0.."
echo === run.bat --vfs vfs_samples\minimal --script examples\stage2.txt ===
call .\run.bat --vfs vfs_samples\minimal --script examples\stage2.txt
echo exit status: %ERRORLEVEL%
popd
