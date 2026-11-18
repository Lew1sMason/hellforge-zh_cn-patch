@echo off
setlocal DisableDelayedExpansion
set "HF_TARGET="
if not "%~1"=="" set "HF_TARGET=%~f1"
pushd "%~dp0" || exit /b 1
call ".\support\files.bat" backup
set "HF_RESULT=%errorlevel%"
popd
pause
exit /b %HF_RESULT%
