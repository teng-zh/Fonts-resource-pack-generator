@echo off
chcp 65001
rem ���Python�Ƿ��Ѱ�װ
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python�Ѱ�װ����ʼִ�нű�...
) else (
    echo Pythonδ��װ����ʼ�Զ���װPython...
    rem ����Python��װ����
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe', 'python-installer.exe')"
    rem ��Ĭ��װPython
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    rem ɾ����װ����
    del python-installer.exe
    echo Python��װ��ɣ���ʼִ�нű�...
)

rem ִ�нű�
python .\downloaded_script.py

pause    