@echo off
set SCRIPT_DIR=%~dp0

set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

echo %PATH% | find "%SCRIPT_DIR%" >nul
if %ERRORLEVEL%==0 (
    echo Il percorso %SCRIPT_DIR% è già nel PATH.
) else (
    echo Adding %SCRIPT_DIR% to the PATH...
    setx PATH "%PATH%;%SCRIPT_DIR%" /M
    if %ERRORLEVEL% neq 0 (
        echo Error while adding directory to PATH.
        pause
        exit /b 1
    ) else (
        echo Directory added to PATH successfully.
    )
)

echo Setup completed. You can now run 'susage' from any location.
pause
