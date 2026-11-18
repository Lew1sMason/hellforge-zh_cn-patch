@echo off
setlocal DisableDelayedExpansion
if "%~1"=="" goto usage
set "TARGET=%~f1"
set "MODE=install"
if /i "%~2"=="/uninstall" set "MODE=uninstall"
set "BACKUP=%~dp0backup"
set "PAYLOAD=%~dp0payload"
if not exist "%PAYLOAD%\app\" set "PAYLOAD=%~dp0."

if not exist "%TARGET%\app\app-build.json" goto usage
call :files check || goto failed
if /i "%MODE%"=="uninstall" goto uninstall
if not exist "%BACKUP%\app\launcher\" md "%BACKUP%\app\launcher"
if not exist "%BACKUP%\app\launcher\" goto failed
call :files save || goto failed
call :files install || goto failed
echo Install OK.
goto done

:uninstall
call :files restore || goto failed
echo Uninstall OK.
goto done

:files
call :%~1 app\launcher\HellForge.Launcher.dll 3ebfc7e270564deeb688465cc6f9613cfcb4fed67be201ec4f0d3288c06d4fe1 5908d435fee9a427a8ad43936ddf050e5661bcf9b2d4baec9545076d2516c16e || exit /b 1
call :%~1 app\launcher\HellForge.SteamDownload.dll 98bb04f1edd25e52896fb8b58839f07f1047c01f6810b7ab796128ca5304101a 26ada22edfb3f35bf6975f013de56688aa079c2c1cef6ffdb1091fc41cdee04a || exit /b 1
call :%~1 app\profile-templates.json c8722cc7ec3378eb343c3f70b4651b84614e5d68312e92565660f4c747b50d53 08da0437b0557ef2c92e64af0f799f7633257e91eed93d984f761f27744805d4 || exit /b 1
exit /b 0

:check
set "FILE=%TARGET%\%~1"
call :verify %~2 %~3 || exit /b 1
set "CURRENT=%HASH%"
if /i "%MODE%"=="install" (
    set "FILE=%PAYLOAD%\%~1"
    call :verify %~3 || exit /b 1
    if /i "%CURRENT%"=="%~2" if not exist "%BACKUP%\%~1" exit /b 0
)
set "FILE=%BACKUP%\%~1"
call :verify %~2
exit /b

:save
set "DST=%BACKUP%\%~1"
if exist "%DST%" (
    set "FILE=%DST%"
    call :verify %~2
    exit /b
)
set "SRC=%TARGET%\%~1"
call :put %~2 /-y
exit /b

:install
set "SRC=%PAYLOAD%\%~1"
set "WANTED=%~3"
goto apply

:restore
set "SRC=%BACKUP%\%~1"
set "WANTED=%~2"

:apply
set "DST=%TARGET%\%~1"
set "FILE=%DST%"
call :verify %~2 %~3 || exit /b 1
if /i "%HASH%"=="%WANTED%" exit /b 0
call :put %WANTED% /y
exit /b

:put
set "TMPFILE=%DST%.hfzh-%RANDOM%-%RANDOM%.tmp"
if exist "%TMPFILE%" exit /b 1
copy /b "%SRC%" "%TMPFILE%" >nul || goto write_failed
set "FILE=%TMPFILE%"
call :verify %~1 || goto write_failed
move %~2 "%TMPFILE%" "%DST%" <nul >nul || goto write_failed
set "FILE=%DST%"
call :verify %~1
exit /b

:verify
set "HASH="
for /f "skip=1 delims=" %%H in ('%SystemRoot%\System32\certutil.exe -hashfile "%FILE%" SHA256 2^>nul') do if not defined HASH set "HASH=%%H"
if /i "%HASH%"=="%~1" exit /b 0
if not "%~2"=="" if /i "%HASH%"=="%~2" exit /b 0
echo File missing, unreadable, or SHA-256 mismatch: "%FILE%"
exit /b 1

:write_failed
if exist "%TMPFILE%" del /q "%TMPFILE%" >nul
echo Could not write "%DST%"
exit /b 1

:usage
echo Close HellForge and drag its installation folder onto this BAT.
goto failed

:failed
echo Stopped. Keep the backup and check the message above.
pause
exit /b 1

:done
pause
exit /b 0