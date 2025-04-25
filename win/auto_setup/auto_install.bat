@echo off
setlocal

set "BASE=https://files-hosterino.vercel.app"
set "TARGET=%APPDATA%\games\data"
set "TEMPFILE=%TEMP%\auto_pythono_path.bat"

mkdir "%TARGET%" >nul 2>&1

powershell -Command "(New-Object Net.WebClient).DownloadFile('%BASE%/pythono_game.bat', '%TARGET%\game.bat')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('%BASE%/pythono_launcher.py', '%TARGET%\launcher.py')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('%BASE%/auto_pythono_path.bat', '%TEMPFILE%')"

call "%TEMPFILE%"
endlocal
cls
echo Pythono installed! you can now use the command "game" in cmd.
pause