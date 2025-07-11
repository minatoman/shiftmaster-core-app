# Create new SSH key pair and setup
# 新しいSSHキーペアを作成してセットアップ

Write-Host "=== Creating New SSH Key Pair ===" -ForegroundColor Green

$keyName = "mednext_vps_key_final"
$keyPath = "C:\Users\jinna\.ssh\$keyName"
$pubKeyPath = "$keyPath.pub"

Write-Host "`n1. Creating new SSH key pair..." -ForegroundColor Cyan
ssh-keygen -t rsa -b 4096 -f $keyPath -N '""' -C "company-pc-final-key"

if (Test-Path $pubKeyPath) {
    Write-Host "Key pair created successfully!" -ForegroundColor Green
    
    Write-Host "`n2. Public key content (single line):" -ForegroundColor Cyan
    $pubKeyContent = Get-Content $pubKeyPath -Raw
    $cleanPubKey = $pubKeyContent.Trim().Replace("`r`n", "").Replace("`r", "").Replace("`n", "")
    Write-Host $cleanPubKey
    
    Write-Host "`n3. Key fingerprint:" -ForegroundColor Cyan
    ssh-keygen -l -f $pubKeyPath
    
    Write-Host "`n4. VPS side command to register this key:" -ForegroundColor Yellow
    Write-Host "Execute this command on VPS via ConoHa console:" -ForegroundColor Yellow
    Write-Host "echo `"$cleanPubKey`" > ~/.ssh/authorized_keys" -ForegroundColor White
    Write-Host "chmod 600 ~/.ssh/authorized_keys" -ForegroundColor White
    Write-Host "chmod 700 ~/.ssh" -ForegroundColor White
    
    Write-Host "`n5. Test command for Windows after VPS setup:" -ForegroundColor Cyan
    Write-Host "ssh -o IdentitiesOnly=yes -i `"$keyPath`" root@160.251.181.238 'echo Success'" -ForegroundColor White
    
    Write-Host "`n6. Copy this command for clipboard:" -ForegroundColor Magenta
    $vpsCommand = "echo `"$cleanPubKey`" > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && chmod 700 ~/.ssh"
    Write-Host $vpsCommand -ForegroundColor White
    Set-Clipboard -Value $vpsCommand
    Write-Host "`nVPS command copied to clipboard!" -ForegroundColor Green
    
} else {
    Write-Host "Failed to create key pair!" -ForegroundColor Red
}
