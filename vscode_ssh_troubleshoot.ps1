# VSCode Remote-SSH トラブルシューティングスクリプト
# 実行方法: PowerShell -ExecutionPolicy Bypass -File vscode_ssh_troubleshoot.ps1

Write-Host "=== VSCode Remote-SSH Troubleshooting ===" -ForegroundColor Green

# 1. SSH接続テスト
Write-Host "`n1. SSH Connection Test" -ForegroundColor Yellow
Write-Host "Testing..." -ForegroundColor Gray

try {
    $result = ssh -i "C:\Users\jinna\.ssh\mednext_vps_key_new" -o BatchMode=yes -o ConnectTimeout=10 root@160.251.181.238 "echo 'SSH_SUCCESS'" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ SSH Connection: SUCCESS" -ForegroundColor Green
    } else {
        Write-Host "✗ SSH Connection: FAILED" -ForegroundColor Red
        Write-Host "  Error details:" -ForegroundColor Gray
        Write-Host "  $result" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ SSH Connection: ERROR" -ForegroundColor Red
    Write-Host "  Exception: $($_.Exception.Message)" -ForegroundColor Red
}

# 2. SSH設定ファイル確認
Write-Host "`n2. SSH Config File Check" -ForegroundColor Yellow
$sshConfigPath = "C:\Users\jinna\.ssh\config"
if (Test-Path $sshConfigPath) {
    Write-Host "✓ SSH Config File: EXISTS" -ForegroundColor Green
    Write-Host "Config content:" -ForegroundColor Gray
    Get-Content $sshConfigPath | Select-String "Host|HostName|User|IdentityFile" | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
} else {
    Write-Host "✗ SSH Config File: NOT FOUND" -ForegroundColor Red
}

# 3. SSH鍵ファイル確認
Write-Host "`n3. SSH Key Files Check" -ForegroundColor Yellow
$keyPath = "C:\Users\jinna\.ssh\mednext_vps_key_new"
$pubKeyPath = "C:\Users\jinna\.ssh\mednext_vps_key_new.pub"

if (Test-Path $keyPath) {
    Write-Host "✓ Private Key File: EXISTS" -ForegroundColor Green
} else {
    Write-Host "✗ Private Key File: NOT FOUND" -ForegroundColor Red
}

if (Test-Path $pubKeyPath) {
    Write-Host "✓ Public Key File: EXISTS" -ForegroundColor Green
    Write-Host "  Public key content:" -ForegroundColor Gray
    $pubKey = Get-Content $pubKeyPath
    Write-Host "  $($pubKey.Substring(0, 50))..." -ForegroundColor Gray
} else {
    Write-Host "✗ Public Key File: NOT FOUND" -ForegroundColor Red
}

# 4. VSCode Remote-SSH拡張機能確認
Write-Host "`n4. VSCode Remote-SSH Extension Check" -ForegroundColor Yellow
try {
    $vscodeExtensions = code --list-extensions 2>$null
    if ($vscodeExtensions -contains "ms-vscode-remote.remote-ssh") {
        Write-Host "✓ Remote-SSH Extension: INSTALLED" -ForegroundColor Green
    } else {
        Write-Host "✗ Remote-SSH Extension: NOT INSTALLED" -ForegroundColor Red
        Write-Host "  Install command: code --install-extension ms-vscode-remote.remote-ssh" -ForegroundColor Gray
    }
} catch {
    Write-Host "? VSCode not found or not in PATH" -ForegroundColor Yellow
}

# 5. Recommended Actions
Write-Host "`n=== RECOMMENDED ACTIONS ===" -ForegroundColor Green
Write-Host "1. Verify public key is correctly registered in ConoHa console" -ForegroundColor Cyan
Write-Host "2. Ensure VSCode Remote-SSH extension is enabled" -ForegroundColor Cyan
Write-Host "3. Use VSCode Command Palette (Ctrl+Shift+P) -> 'Remote-SSH: Connect to Host'" -ForegroundColor Cyan
Write-Host "4. Select 'mednext-vps' or '160.251.181.238' from host list" -ForegroundColor Cyan

Write-Host "`n=== VSCode Remote-SSH Connection Steps ===" -ForegroundColor Green
Write-Host "1. Launch VSCode" -ForegroundColor White
Write-Host "2. Press Ctrl+Shift+P to open Command Palette" -ForegroundColor White
Write-Host "3. Type 'Remote-SSH: Connect to Host' and select it" -ForegroundColor White
Write-Host "4. Select 'mednext-vps' from the list" -ForegroundColor White
Write-Host "5. Wait for new VSCode window to open" -ForegroundColor White
Write-Host "6. Open terminal and run 'pwd' to verify connection" -ForegroundColor White

Write-Host "`nTroubleshooting completed" -ForegroundColor Green
