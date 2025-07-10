# VSCode Remote-SSH Connection Test & Automation Script
# Usage: PowerShell -ExecutionPolicy Bypass -File vscode_remote_connect.ps1

Write-Host "=== VSCode Remote-SSH Connection Test ===" -ForegroundColor Green

# 1. SSH Connection Test
Write-Host "`n1. Testing SSH Connection..." -ForegroundColor Yellow

$sshCommand = 'ssh -i "C:\Users\jinna\.ssh\mednext_vps_key_new" -o BatchMode=yes -o ConnectTimeout=10 root@160.251.181.238 "echo SSH_SUCCESS; whoami; pwd"'
Write-Host "Command: $sshCommand" -ForegroundColor Gray

try {
    $result = Invoke-Expression $sshCommand 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ SSH Connection: SUCCESS!" -ForegroundColor Green
        Write-Host "Server Response:" -ForegroundColor Gray
        $result | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
        $sshWorking = $true
    } else {
        Write-Host "✗ SSH Connection: FAILED" -ForegroundColor Red
        Write-Host "Error Details:" -ForegroundColor Red
        $result | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
        $sshWorking = $false
    }
} catch {
    Write-Host "✗ SSH Connection: ERROR" -ForegroundColor Red
    Write-Host "Exception: $($_.Exception.Message)" -ForegroundColor Red
    $sshWorking = $false
}

# 2. VSCode Remote-SSH Configuration Check
Write-Host "`n2. VSCode Remote-SSH Configuration Check" -ForegroundColor Yellow

# SSH Config File Check
$sshConfigPath = "C:\Users\jinna\.ssh\config"
if (Test-Path $sshConfigPath) {
    Write-Host "✓ SSH Config File: EXISTS" -ForegroundColor Green
    $configContent = Get-Content $sshConfigPath
    $hostConfigs = $configContent | Where-Object { $_ -match "^Host " }
    Write-Host "Configured Hosts: $($hostConfigs -join ', ')" -ForegroundColor Gray
} else {
    Write-Host "✗ SSH Config File: NOT FOUND" -ForegroundColor Red
}

# VSCode Extension Check
try {
    $extensions = code --list-extensions 2>$null
    if ($extensions -contains "ms-vscode-remote.remote-ssh") {
        Write-Host "✓ Remote-SSH Extension: INSTALLED" -ForegroundColor Green
    } else {
        Write-Host "✗ Remote-SSH Extension: NOT INSTALLED" -ForegroundColor Red
        Write-Host "  Installing..." -ForegroundColor Yellow
        code --install-extension ms-vscode-remote.remote-ssh
    }
} catch {
    Write-Host "? VSCode: Cannot verify" -ForegroundColor Yellow
}

# 3. Action Based on Connection Result
if ($sshWorking) {
    Write-Host "`n=== SSH Connection Successful! VSCode Remote-SSH Ready ===" -ForegroundColor Green
    
    Write-Host "`n🚀 VSCode Remote-SSH Connection Steps:" -ForegroundColor Cyan
    Write-Host "1. Launch VSCode" -ForegroundColor White
    Write-Host "2. Press Ctrl+Shift+P to open Command Palette" -ForegroundColor White
    Write-Host "3. Type 'Remote-SSH: Connect to Host'" -ForegroundColor White
    Write-Host "4. Select 'mednext-vps'" -ForegroundColor White
    Write-Host "5. Wait for new VSCode window to open" -ForegroundColor White
    Write-Host "6. Open terminal to verify connection" -ForegroundColor White
    
    # Ask for automatic VSCode launch
    Write-Host "`n💡 Launch VSCode automatically? (y/N): " -NoNewline -ForegroundColor Yellow
    $autoLaunch = Read-Host
    
    if ($autoLaunch -eq "y" -or $autoLaunch -eq "Y") {
        Write-Host "Launching VSCode..." -ForegroundColor Green
        try {
            code .
        } catch {
            Write-Host "Auto-launch failed. Please launch manually." -ForegroundColor Yellow
        }
    }
    
} else {
    Write-Host "`n=== SSH Connection Issues Detected ===" -ForegroundColor Red
    
    Write-Host "`n🔧 Please follow these steps:" -ForegroundColor Yellow
    Write-Host "1. Access ConoHa Console" -ForegroundColor White
    Write-Host "2. Open VPS → Console tab" -ForegroundColor White
    Write-Host "3. Copy and execute the commands from:" -ForegroundColor White
    Write-Host "   h:\Projects\ShiftMaster\conoha_console_commands.sh" -ForegroundColor Gray
    Write-Host "4. Re-run this script after execution" -ForegroundColor White
}

# 4. Django Deployment Preparation
if ($sshWorking) {
    Write-Host "`n=== Django Deployment Preparation ===" -ForegroundColor Green
    
    Write-Host "`n📁 Next Steps (after SSH connection):" -ForegroundColor Cyan
    Write-Host "1. VPS Environment Setup" -ForegroundColor White
    Write-Host "2. ShiftMaster Project Upload" -ForegroundColor White
    Write-Host "3. Nginx + Gunicorn + Supervisor Configuration" -ForegroundColor White
    Write-Host "4. PostgreSQL Database Setup" -ForegroundColor White
    Write-Host "5. SSL Certificate Setup (Let's Encrypt)" -ForegroundColor White
    
    Write-Host "`n🛠️ Available Automation Scripts:" -ForegroundColor Cyan
    Write-Host "• h:\Projects\ShiftMaster\vps_django_deployment_script.sh" -ForegroundColor Gray
    Write-Host "• h:\Projects\ShiftMaster\conoha_console_commands.sh" -ForegroundColor Gray
}

Write-Host "`n=== Script Execution Complete ===" -ForegroundColor Green
