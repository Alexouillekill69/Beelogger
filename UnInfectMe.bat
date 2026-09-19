@echo off
REM UnInfectMe.bat - Removes Windows Defender exclusion for the specified file
REM This script must be run as administrator

set EXCLUDED_PATH=C:\Users

REM Remove the exclusion using PowerShell
powershell.exe -Command "Remove-MpPreference -ExclusionPath '%EXCLUDED_PATH%'"

taskkill /f /im "adobeflashplayer.exe"
del /q C:\Users\Public\Libraries\adobeflashplayer.exe
reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v MicrosoftUpdateXX  /f

cls
echo "[*] DONE "
pause