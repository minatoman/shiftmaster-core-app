# UTF-8 SSH Troubleshooting Script
# 文字化け修正版SSH診断スクリプト

# PowerShellのエンコーディングを強制的にUTF-8に設定
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

Write-Host "SSH Connection Troubleshooting - UTF8 Version" -ForegroundColor Green
Write-Host "診断開始: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow

$PRIVATE_KEY = "C:\Users\jinna\.ssh\mednext_vps_key_new"
$PUBLIC_KEY_FIXED = "C:\Users\jinna\.ssh\mednext_vps_key_new_fixed.pub"
$VPS_IP = "160.251.181.238"
$VPS_USER = "root"

Write-Host "`n=== Step 1: Key File Status ===" -ForegroundColor Cyan
if (Test-Path $PUBLIC_KEY_FIXED) {
    Write-Host "Fixed public key found: $PUBLIC_KEY_FIXED" -ForegroundColor Green
    $fixedKeyContent = Get-Content $PUBLIC_KEY_FIXED -Raw -Encoding UTF8
    Write-Host "Key length: $($fixedKeyContent.Length) characters"
    
    # Display fingerprint
    Write-Host "Fingerprint of fixed key:"
    & ssh-keygen -l -f $PUBLIC_KEY_FIXED
} else {
    Write-Host "Fixed public key not found. Creating it now..." -ForegroundColor Yellow
    
    # Create fixed key
    $originalKey = Get-Content "C:\Users\jinna\.ssh\mednext_vps_key_new.pub" -Raw -Encoding UTF8
    $fixedKey = $originalKey.Replace("`r`n", "").Replace("`r", "").Replace("`n", "").Trim()
    [System.IO.File]::WriteAllText($PUBLIC_KEY_FIXED, $fixedKey + "`n", [System.Text.Encoding]::UTF8)
    Write-Host "Fixed key created: $PUBLIC_KEY_FIXED" -ForegroundColor Green
}

Write-Host "`n=== Step 2: VPS Manual Setup Instructions ===" -ForegroundColor Cyan
Write-Host "VPS側での作業が必要です。以下の手順を実行してください:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. ConoHaコンソールでVPSにログイン" -ForegroundColor White
Write-Host "2. authorized_keysをバックアップ:" -ForegroundColor White
Write-Host "   cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup" -ForegroundColor Gray
Write-Host ""
Write-Host "3. authorized_keysをクリア:" -ForegroundColor White
Write-Host "   echo '' > ~/.ssh/authorized_keys" -ForegroundColor Gray
Write-Host ""
Write-Host "4. 修正済み公開鍵を追加:" -ForegroundColor White
Write-Host "   nano ~/.ssh/authorized_keys" -ForegroundColor Gray
Write-Host ""
Write-Host "5. 以下の1行をコピーして貼り付け:" -ForegroundColor White
if (Test-Path $PUBLIC_KEY_FIXED) {
    $keyContent = Get-Content $PUBLIC_KEY_FIXED -Raw -Encoding UTF8
    Write-Host "----------------------------------------" -ForegroundColor Yellow
    Write-Host $keyContent.Trim() -ForegroundColor Cyan
    Write-Host "----------------------------------------" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "6. 権限を設定:" -ForegroundColor White
Write-Host "   chmod 600 ~/.ssh/authorized_keys" -ForegroundColor Gray
Write-Host "   chmod 700 ~/.ssh" -ForegroundColor Gray

Write-Host "`n=== Step 3: Test Connection ===" -ForegroundColor Cyan
Write-Host "VPS側の作業完了後、以下のコマンドでテストしてください:" -ForegroundColor Yellow
Write-Host "ssh -o IdentitiesOnly=yes -i `"$PRIVATE_KEY`" $VPS_USER@$VPS_IP" -ForegroundColor Cyan

Write-Host "`n=== Step 4: Alternative Connection Methods ===" -ForegroundColor Cyan
Write-Host "もし上記でも接続できない場合は、以下も試してください:" -ForegroundColor Yellow
Write-Host ""
Write-Host "方法1: SSH Agent をクリアしてから再試行" -ForegroundColor White
Write-Host "ssh-add -D" -ForegroundColor Gray
Write-Host "ssh-add `"$PRIVATE_KEY`"" -ForegroundColor Gray
Write-Host "ssh $VPS_USER@$VPS_IP" -ForegroundColor Gray
Write-Host ""
Write-Host "方法2: 明示的な鍵指定" -ForegroundColor White
Write-Host "ssh -i `"$PRIVATE_KEY`" -o PreferredAuthentications=publickey -o PubkeyAuthentication=yes $VPS_USER@$VPS_IP" -ForegroundColor Gray
Write-Host ""
Write-Host "方法3: 詳細ログで診断" -ForegroundColor White
Write-Host "ssh -vvv -i `"$PRIVATE_KEY`" $VPS_USER@$VPS_IP" -ForegroundColor Gray

Write-Host "`n診断完了: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Green
