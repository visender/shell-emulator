@echo off
rem Stage 2: only --vfs parameter.
pushd "%~dp0.."
echo === run.bat --vfs vfs_samples\minimal ===
echo exit| .\run.bat --vfs vfs_samples\minimal
echo exit status: %ERRORLEVEL%
popd
