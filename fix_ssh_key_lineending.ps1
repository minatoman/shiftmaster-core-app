# Fix SSH Key Line Endings and Re-register
# 公開鍵の行末文字を修正してVPSに再登録

Write-Host "=== SSH Key Line Ending Fix and Re-registration ===" -ForegroundColor Green

$PUBLIC_KEY = "C:\Users\jinna\.ssh\mednext_vps_key_new.pub"
$PUBLIC_KEY_FIXED = "C:\Users\jinna\.ssh\mednext_vps_key_new_fixed.pub"
$VPS_IP = "160.251.181.238"

Write-Host "`n1. Original Public Key Analysis" -ForegroundColor Cyan
if (Test-Path $PUBLIC_KEY) {
    $originalContent = Get-Content $PUBLIC_KEY -Raw
    Write-Host "Original key length: $($originalContent.Length) characters"
    
    if ($originalContent.Contains("`r`n")) {
        Write-Host "Line endings: CRLF (Windows) - 這個可能是問題的原因!" -ForegroundColor Red
    } elseif ($originalContent.Contains("`n")) {
        Write-Host "Line endings: LF (Unix)" -ForegroundColor Green
    } else {
        Write-Host "No line endings detected" -ForegroundColor Yellow
    }
    
    Write-Host "`n2. Creating Fixed Version" -ForegroundColor Cyan
    # Remove all CR and LF characters, then add single LF at the end
    $fixedContent = $originalContent.Replace("`r`n", "").Replace("`r", "").Replace("`n", "").Trim()
    
    # Write the fixed content with Unix line ending
    [System.IO.File]::WriteAllText($PUBLIC_KEY_FIXED, $fixedContent + "`n", [System.Text.Encoding]::UTF8)
    
    Write-Host "Fixed key created at: $PUBLIC_KEY_FIXED" -ForegroundColor Green
    
    $fixedKeyContent = Get-Content $PUBLIC_KEY_FIXED -Raw
    Write-Host "Fixed key length: $($fixedKeyContent.Length) characters"
    
    Write-Host "`n3. Verify Fixed Key Fingerprint" -ForegroundColor Cyan
    ssh-keygen -l -f $PUBLIC_KEY_FIXED
    
    Write-Host "`n4. Fixed Key Content (for manual copying)" -ForegroundColor Cyan
    Write-Host "コピーして下記の内容をVPSのauthorized_keysに手動で貼り付けてください:" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    $fixedKeyContent
    Write-Host "========================================" -ForegroundColor Yellow
    
} else {
    Write-Host "Public key file not found: $PUBLIC_KEY" -ForegroundColor Red
}

Write-Host "`n=== VPS側での手動操作手順 ===" -ForegroundColor Magenta
Write-Host "1. ConoHaコンソールでVPSにログイン"
Write-Host "2. 下記のコマンドでauthorized_keysをバックアップ:"
Write-Host "   cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup"
Write-Host ""
Write-Host "3. authorized_keysを完全にクリア:"
Write-Host "   echo '' > ~/.ssh/authorized_keys"
Write-Host ""
Write-Host "4. 上記で表示された固定済み公開鍵を追加:"
Write-Host "   nano ~/.ssh/authorized_keys"
Write-Host "   # 上記の固定済み公開鍵を1行でペースト"
Write-Host ""
Write-Host "5. 権限を再設定:"
Write-Host "   chmod 600 ~/.ssh/authorized_keys"
Write-Host "   chmod 700 ~/.ssh"
Write-Host ""
Write-Host "6. SSH接続をテスト:"
Write-Host "   # 会社PCから:"
Write-Host "   ssh -o IdentitiesOnly=yes -i `"C:\Users\jinna\.ssh\mednext_vps_key_new`" root@$VPS_IP"
