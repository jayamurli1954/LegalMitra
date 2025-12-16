# Script to create desktop shortcut for LegalMitra

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ScriptPath = $PSScriptRoot

# Use VBS launcher for better compatibility (no file association issues)
$LauncherPath = Join-Path $ScriptPath "START_LEGALMITRA.vbs"

# If VBS doesn't exist, fall back to batch file
if (-not (Test-Path $LauncherPath)) {
    $LauncherPath = Join-Path $ScriptPath "START_LEGALMITRA.bat"
}

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\LegalMitra.lnk")

# If using .bat file, wrap it with cmd.exe to ensure it runs
if ($LauncherPath.EndsWith(".bat")) {
    $Shortcut.TargetPath = "cmd.exe"
    $Shortcut.Arguments = "/c `"$LauncherPath`""
} else {
    $Shortcut.TargetPath = $LauncherPath
}

$Shortcut.WorkingDirectory = $ScriptPath
$Shortcut.Description = "LegalMitra - AI Legal Assistant"
$Shortcut.IconLocation = "C:\Windows\System32\imageres.dll,2"  # Folder icon
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
Write-Host "You can now double-click 'LegalMitra' on your desktop to start the application." -ForegroundColor Green
Write-Host ""
Write-Host "Tip: If the .bat file doesn't work, use START_LEGALMITRA.vbs instead!" -ForegroundColor Yellow

