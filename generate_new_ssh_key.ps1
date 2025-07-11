# Generate New SSH Key Pair and Test Connection
# 新しいSSHキーペアを生成して接続をテスト

Write-Host "=== Generating New SSH Key Pair ===" -ForegroundColor Green

$KeyPath = "C:\Users\jinna\.ssh\company_vps_key"
$PublicKeyPath = "$KeyPath.pub"
$VPS_IP = "160.251.181.238"

# Remove existing files if they exist
if (Test-Path $KeyPath) {
    Remove-Item $KeyPath -Force
    Write-Host "Removed existing private key" -ForegroundColor Yellow
}
if (Test-Path $PublicKeyPath) {
    Remove-Item $PublicKeyPath -Force
    Write-Host "Removed existing public key" -ForegroundColor Yellow
}

Write-Host "`n1. Generating new SSH key pair..." -ForegroundColor Cyan
ssh-keygen -t rsa -b 4096 -f $KeyPath -N "" -C "company-pc-vps-key"

if ((Test-Path $KeyPath) -and (Test-Path $PublicKeyPath)) {
    Write-Host "`n2. New key pair generated successfully!" -ForegroundColor Green
    
    Write-Host "`n3. Key information:" -ForegroundColor Cyan
    ssh-keygen -l -f $PublicKeyPath
    
    Write-Host "`n4. Public key content (for VPS registration):" -ForegroundColor Cyan
    $publicKeyContent = Get-Content $PublicKeyPath -Raw
    Write-Host "Length: $($publicKeyContent.Length) characters" -ForegroundColor Gray
    Write-Host "================================" -ForegroundColor Yellow
    Write-Host $publicKeyContent -ForegroundColor White
    Write-Host "================================" -ForegroundColor Yellow
    
    Write-Host "`n5. VPS側で実行してください:" -ForegroundColor Magenta
    Write-Host "echo `"$($publicKeyContent.Trim())`" > ~/.ssh/authorized_keys" -ForegroundColor White
    Write-Host "chmod 600 ~/.ssh/authorized_keys" -ForegroundColor White
    Write-Host "chmod 700 ~/.ssh" -ForegroundColor White
    
    Write-Host "`n6. 上記のVPS作業完了後、下記コマンドでテストしてください:" -ForegroundColor Magenta
    Write-Host "ssh -o IdentitiesOnly=yes -i `"$KeyPath`" root@$VPS_IP 'echo Success; whoami; hostname'" -ForegroundColor White
    
    # Copy public key to clipboard
    Set-Clipboard -Value $publicKeyContent.Trim()
    Write-Host "`n✅ 公開鍵をクリップボードにコピーしました" -ForegroundColor Green
    
} else {
    Write-Host "`n❌ Key generation failed" -ForegroundColor Red
}
