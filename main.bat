@echo off
rem 检查Python是否已安装
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python已安装，开始执行脚本...
) else (
    echo Python未安装，开始自动安装Python...
    rem 下载Python安装程序
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe', 'python-installer.exe')"
    rem 静默安装Python
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    rem 删除安装程序
    del python-installer.exe
    echo Python安装完成，开始执行脚本...
)

rem 执行脚本
python downloaded_script.py

pause    
