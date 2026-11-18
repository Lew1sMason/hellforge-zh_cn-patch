@echo off
setlocal DisableDelayedExpansion
if "%HF_TARGET%"=="" (
    echo Drag the HellForge installation folder onto the batch file.
    exit /b 1
)
if not exist "%HF_TARGET%\app\app-build.json" (
    echo Select the HellForge folder that contains app.
    exit /b 1
)
if not exist "support\hashes.txt" (
    echo Extract the entire package first.
    exit /b 1
)

set "HF_HASH_RESULT=.hash-%RANDOM%-%RANDOM%.tmp"
if exist "%HF_HASH_RESULT%" exit /b 1
if /i "%~1"=="backup" goto backup
if /i "%~1"=="restore" goto restore
exit /b 1

:backup
for /f "usebackq tokens=1-3" %%A in ("support\hashes.txt") do (
    call :check_original "%%A" "%%B" || goto fail
    call :check_payload "%%A" "%%C" || goto fail
)
if not exist "backup\app\launcher" md "backup\app\launcher"
if not exist "backup\app\launcher" goto fail
for /f "usebackq tokens=1-3" %%A in ("support\hashes.txt") do (
    call :save "%%A" "%%B" || goto fail
)
echo Backup OK. Copy the app folder inside payload into your HellForge folder.
goto success

:restore
for /f "usebackq tokens=1-3" %%A in ("support\hashes.txt") do (
    call :check_backup "%%A" "%%B" || goto fail
    call :check_installed "%%A" "%%B" "%%C" || goto fail
)
for /f "usebackq tokens=1-3" %%A in ("support\hashes.txt") do (
    call :restore_file "%%A" "%%B" "%%C" || goto fail
)
echo Restore OK. All three original files are in place.
goto success

:check_original
set "HF_FILE=%HF_TARGET%\%~1"
call :hash "%~2"
exit /b %errorlevel%

:check_payload
set "HF_FILE=payload\%~1"
call :hash "%~2"
exit /b %errorlevel%

:check_backup
set "HF_FILE=backup\%~1"
call :hash "%~2"
exit /b %errorlevel%

:check_installed
set "HF_FILE=%HF_TARGET%\%~1"
call :hash "%~2" quiet && exit /b 0
call :hash "%~3"
exit /b %errorlevel%

:save
if exist "backup\%~1" (
    call :check_backup "%~1" "%~2"
    exit /b
)
set "HF_TEMP=backup\%~1.hfzh-%RANDOM%-%RANDOM%.tmp"
if exist "%HF_TEMP%" exit /b 1
copy /b "%HF_TARGET%\%~1" "%HF_TEMP%" >nul || goto bad_temp
set "HF_FILE=%HF_TEMP%"
call :hash "%~2" || goto bad_temp
move /-y "%HF_TEMP%" "backup\%~1" <nul >nul || goto bad_temp
exit /b 0

:restore_file
set "HF_FILE=%HF_TARGET%\%~1"
call :hash "%~2" quiet && exit /b 0
call :hash "%~3" || exit /b 1
set "HF_TEMP=%HF_FILE%.hfzh-%RANDOM%-%RANDOM%.tmp"
if exist "%HF_TEMP%" exit /b 1
copy /b "backup\%~1" "%HF_TEMP%" >nul || goto bad_temp
set "HF_FILE=%HF_TEMP%"
call :hash "%~2" || goto bad_temp
move /y "%HF_TEMP%" "%HF_TARGET%\%~1" >nul || goto bad_temp
call :check_original "%~1" "%~2"
exit /b %errorlevel%

:hash
"%SystemRoot%\System32\certutil.exe" -hashfile "%HF_FILE%" SHA256 >"%HF_HASH_RESULT%" 2>nul
if not errorlevel 1 (
    "%SystemRoot%\System32\findstr.exe" /i /x /c:"%~1" "%HF_HASH_RESULT%" >nul
    if not errorlevel 1 exit /b 0
)
if /i not "%~2"=="quiet" echo File missing or SHA-256 mismatch: "%HF_FILE%"
exit /b 1

:bad_temp
if exist "%HF_TEMP%" del /q "%HF_TEMP%"
exit /b 1

:fail
if exist "%HF_HASH_RESULT%" del /q "%HF_HASH_RESULT%"
echo Operation stopped. Keep the backup and check file permissions and version.
exit /b 1

:success
del /q "%HF_HASH_RESULT%"
exit /b 0
