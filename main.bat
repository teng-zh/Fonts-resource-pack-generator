@echo off
chcp 65001
echo Please do not close this console window. The script is running...
rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed. Starting to execute the script...
) else (
    echo Python is not installed. Starting to download the latest Python installer...
    rem Get the download link of the latest Python version (using PowerShell script)
    powershell -Command "$response = Invoke-WebRequest -Uri 'https://www.python.org/downloads/'; $links = $response.Links | Where-Object { $_.href -like '*windows-amd64.exe' }; $latestLink = $links | Sort-Object { [version]($_.href -replace '\D+(\d+(\.\d+)*).*', '$1') } -Descending | Select-Object -First 1; $downloadUrl = 'https://www.python.org' + $latestLink.href; (New-Object System.Net.WebClient).DownloadFile($downloadUrl, 'python-installer.exe')"
    if %errorlevel% neq 0 (
        echo Failed to download the Python installer. Please check your network connection!
        pause
        exit /b 1
    )
    echo Python installer downloaded successfully. Starting to install Python...
    rem Run the installer directly
    start python-installer.exe
    pause
    rem Check again if Python is installed successfully
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Python installation failed. Please install it manually!
        pause
        exit /b 1
    )
    rem Delete the installer
    del python-installer.exe
    echo Python installed successfully. Starting to execute the script...
)

rem Execute the Python script
python .\Main.py    
