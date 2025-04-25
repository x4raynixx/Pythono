@echo off
echo Normally do not run this File to launch a game! Instead execute command "game" in cmd!
echo This file adds the game to the path so it can be run.
timeout /t 99999
python "%~dp0launcher.py" %*