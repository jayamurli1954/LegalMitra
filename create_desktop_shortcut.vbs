Set WshShell = CreateObject("WScript.Shell")
Set oShellLink = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") & "\LegalMitra.lnk")

' Get current directory
strCurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Set shortcut properties
oShellLink.TargetPath = strCurrentDirectory & "\start_legalmitra.bat"
oShellLink.WorkingDirectory = strCurrentDirectory
oShellLink.Description = "Launch LegalMitra Application (Backend + Frontend)"
oShellLink.IconLocation = "shell32.dll,16"  ' Using a built-in Windows icon (folder with document)
oShellLink.Save

MsgBox "Desktop shortcut 'LegalMitra' created successfully!" & vbCrLf & vbCrLf & "Double-click the shortcut to launch LegalMitra.", vbInformation, "Shortcut Created"
