@echo off
setlocal DisableDelayedExpansion
if exist "%~dp0install.bat" goto run
echo Keep uninstall.bat next to install.bat.
pause
exit /b 1

:run
"%~dp0install.bat" "%~1" /uninstall