@echo off
setlocal


set PYTHON_SCRIPT=susage.py


set SCRIPT_ALIAS=myscript


set SCRIPT_DIR=%~dp0


set SCRIPT_PATH=%SCRIPT_DIR%%PYTHON_SCRIPT%


if not exist "%SCRIPT_PATH%" (
    echo Error: The file %SCRIPT_PATH% does not exist.
    exit /b 1
)


set WRAPPER_PATH=%SCRIPT_DIR%%SCRIPT_ALIAS%.bat
echo @echo off > "%WRAPPER_PATH%"
echo python "%SCRIPT_PATH%" %%* >> "%WRAPPER_PATH%"


setx PATH "%PATH%;%SCRIPT_DIR%" >nul


pip3 show psutil >nul 2>&1
if %errorlevel% neq 0 (
    echo psutil is not installed. Installing...
    pip3 install psutil
) else (
    echo psutil is already installed.
)

echo Setup complete. You can now run the script by typing '%SCRIPT_ALIAS%' from any command prompt.

endlocal
