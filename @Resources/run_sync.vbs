
' Ejecuta keep_sync.py sin abrir ninguna ventana.
' Usa la carpeta donde esta este mismo archivo, asi no hay rutas personales.
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
 
carpeta = fso.GetParentFolderName(WScript.ScriptFullName)
script = carpeta & "\keep_sync.py"
 
' Si Python viene de la Microsoft Store, pythonw esta en WindowsApps
alias = sh.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Microsoft\WindowsApps\pythonw.exe"
If fso.FileExists(alias) Then
    pythonw = alias
Else
    pythonw = "pythonw"
End If
 
sh.Run """" & pythonw & """ """ & script & """", 0, False
 