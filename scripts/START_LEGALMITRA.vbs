' LegalMitra - Visual Basic Script Launcher
' This ensures the batch file runs in cmd.exe without prompting

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get script directory
ScriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Try different batch file options
BatchFile1 = ScriptDir & "\START_LEGALMITRA_SIMPLE.bat"
BatchFile2 = ScriptDir & "\START_LEGALMITRA.bat"

' Prefer simple version if it exists
If fso.FileExists(BatchFile1) Then
    BatchFile = BatchFile1
ElseIf fso.FileExists(BatchFile2) Then
    BatchFile = BatchFile2
Else
    MsgBox "Error: No startup script found in:" & vbCrLf & ScriptDir & vbCrLf & vbCrLf & "Looking for:" & vbCrLf & "START_LEGALMITRA_SIMPLE.bat" & vbCrLf & "START_LEGALMITRA.bat", vbCritical, "LegalMitra"
    WScript.Quit
End If

' Change to script directory
WshShell.CurrentDirectory = ScriptDir

' Run batch file in a visible command window
' Using /k keeps the window open even if there's an error
' Set window to normal size and visible
WshShell.Run "cmd.exe /k """ & BatchFile & """", 1, False

