# Test SSH Connection with Fixed Key
# 修正済み鍵でSSH接続をテスト

Write-Host "=== Testing SSH Connection with Fixed Key ===" -ForegroundColor Green

$PRIVATE_KEY = "C:\Users\jinna\.ssh\mednext_vps_key_new"
$VPS_IP = "160.251.181.238"
$VPS_USER = "root"

Write-Host "`nTesting SSH connection..." -ForegroundColor Cyan
Write-Host "Command: ssh -o IdentitiesOnly=yes -i `"$PRIVATE_KEY`" $VPS_USER@$VPS_IP 'echo Connection successful; whoami; pwd'" -ForegroundColor Gray

# Test connection
$sshCmd = "ssh -o IdentitiesOnly=yes -i `"$PRIVATE_KEY`" $VPS_USER@$VPS_IP 'echo Connection successful; whoami; pwd'"
Invoke-Expression $sshCmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n接続成功!" -ForegroundColor Green
    Write-Host "VSCodeのRemote-SSH拡張機能でも接続できるはずです。" -ForegroundColor Green
} else {
    Write-Host "`n接続失敗。さらなる診断が必要です。" -ForegroundColor Red
    Write-Host "Verbose接続を試行中..." -ForegroundColor Yellow
    
    $verboseCmd = "ssh -vvv -o IdentitiesOnly=yes -i `"$PRIVATE_KEY`" $VPS_USER@$VPS_IP 'echo Verbose connection test'"
    Invoke-Expression $verboseCmd
}
