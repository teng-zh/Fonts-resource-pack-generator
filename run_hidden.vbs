Set objShell = CreateObject("WScript.Shell")
currentPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
batPath = currentPath & "\main.bat"

objShell.Run "cmd.exe /c """ & batPath & """", 1, false    
