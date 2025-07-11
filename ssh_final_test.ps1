# SSH Connection Final Test Script
# Usage: PowerShell -ExecutionPolicy Bypass -File ssh_final_test.ps1

Write-Host "=== SSH Connection Final Test ===" -ForegroundColor Green

# 1. SSH Basic Connection Test
Write-Host "`n1. SSH Basic Connection Test" -ForegroundColor Yellow
try {
    $sshCmd = 'ssh -i "C:\Users\jinna\.ssh\mednext_vps_key_new" -o BatchMode=yes -o ConnectTimeout=10 root@160.251.181.238 "echo SUCCESS; whoami; pwd; date"'
    $result = Invoke-Expression $sshCmd 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ SSH Connection: SUCCESS!" -ForegroundColor Green
        Write-Host "Server Response:" -ForegroundColor Gray
        $result | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
        $connectionSuccess = $true
    } else {
        Write-Host "✗ SSH Connection: FAILED" -ForegroundColor Red
        Write-Host "Error Details:" -ForegroundColor Red
        $result | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
        $connectionSuccess = $false
    }
} catch {
    Write-Host "✗ SSH Connection: EXCEPTION ERROR" -ForegroundColor Red
    Write-Host "Error Details: $($_.Exception.Message)" -ForegroundColor Red
    $connectionSuccess = $false
}

# 2. VSCode Remote-SSH Preparation
if ($connectionSuccess) {
    Write-Host "`n=== 🎉 SSH CONNECTION SUCCESS! ===" -ForegroundColor Green
    Write-Host "VSCode Remote-SSH connection is ready!" -ForegroundColor Cyan
    
    Write-Host "`n🚀 VSCode Remote-SSH Connection Steps:" -ForegroundColor Yellow
    Write-Host "1. Launch VSCode" -ForegroundColor White
    Write-Host "2. Press Ctrl+Shift+P to open Command Palette" -ForegroundColor White
    Write-Host "3. Type 'Remote-SSH: Connect to Host'" -ForegroundColor White
    Write-Host "4. Select 'mednext-vps'" -ForegroundColor White
    Write-Host "5. Wait for new VSCode window to open" -ForegroundColor White
    Write-Host "6. Check bottom-left corner shows '[SSH: mednext-vps]'" -ForegroundColor White
    
    Write-Host "`n📁 Django Deployment Next Steps:" -ForegroundColor Cyan
    Write-Host "1. After VSCode Remote-SSH connection, open terminal" -ForegroundColor White
    Write-Host "2. Run VPS environment setup script" -ForegroundColor White
    Write-Host "3. Upload ShiftMaster project" -ForegroundColor White
    Write-Host "4. Configure Django + Nginx + Gunicorn + PostgreSQL" -ForegroundColor White
    
    # VSCode Auto Launch Option
    Write-Host "`n💡 Launch VSCode now? (y/N): " -NoNewline -ForegroundColor Yellow
    $launch = Read-Host
    if ($launch -eq "y" -or $launch -eq "Y") {
        Write-Host "Launching VSCode..." -ForegroundColor Green
        try {
            Start-Process "code" -ArgumentList "."
            Start-Sleep 2
            Write-Host "VSCode launched. Please start Remote-SSH connection." -ForegroundColor Green
        } catch {
            Write-Host "VSCode launch failed. Please launch manually." -ForegroundColor Yellow
        }
    }
    
} else {
    Write-Host "`n=== SSH Connection Issues Detected ===" -ForegroundColor Red
    Write-Host "`n🔧 Please check the following:" -ForegroundColor Yellow
    Write-Host "1. Did you execute the commands correctly in ConoHa console?" -ForegroundColor White
    Write-Host "2. Is authorized_keys file free of line breaks?" -ForegroundColor White
    Write-Host "3. Is file permission set to 600?" -ForegroundColor White
    Write-Host "4. Is SSH service restarted?" -ForegroundColor White
    
    Write-Host "`n📋 Commands to run in ConoHa VPS Console:" -ForegroundColor Cyan
    Write-Host "chmod 700 ~/.ssh" -ForegroundColor Gray
    Write-Host "chmod 600 ~/.ssh/authorized_keys" -ForegroundColor Gray
    Write-Host "chown root:root ~/.ssh/authorized_keys" -ForegroundColor Gray
    Write-Host "systemctl restart ssh" -ForegroundColor Gray
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Green
