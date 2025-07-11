# SSH Connection Problem Resolution Guide
# SSH接続問題解決ガイド

Write-Host "=== SSH Connection Problem Resolution Guide ===" -ForegroundColor Green
Write-Host "Date: $(Get-Date)" -ForegroundColor Yellow

$PRIVATE_KEY = "C:\Users\jinna\.ssh\mednext_vps_key_new"
$PUBLIC_KEY_FIXED = "C:\Users\jinna\.ssh\mednext_vps_key_new_fixed.pub"
$VPS_IP = "160.251.181.238"

Write-Host "`n=== Step 1: Windows Side - Key Information ===" -ForegroundColor Cyan

if (Test-Path $PUBLIC_KEY_FIXED) {
    Write-Host "Fixed public key exists!" -ForegroundColor Green
    $fixedKey = Get-Content $PUBLIC_KEY_FIXED -Raw
    Write-Host "`nFixed Key Fingerprint:" -ForegroundColor Yellow
    ssh-keygen -l -f $PUBLIC_KEY_FIXED
    
    Write-Host "`nKey to copy to VPS:" -ForegroundColor Yellow
    Write-Host "===========================================" -ForegroundColor Cyan
    Write-Host $fixedKey.Trim() -ForegroundColor White
    Write-Host "===========================================" -ForegroundColor Cyan
    
    # Save to clipboard if possible
    try {
        $fixedKey.Trim() | Set-Clipboard
        Write-Host "`nKey copied to clipboard!" -ForegroundColor Green
    } catch {
        Write-Host "`nCould not copy to clipboard automatically." -ForegroundColor Yellow
    }
} else {
    Write-Host "Fixed public key not found. Creating it..." -ForegroundColor Red
    
    if (Test-Path "C:\Users\jinna\.ssh\mednext_vps_key_new.pub") {
        $originalKey = Get-Content "C:\Users\jinna\.ssh\mednext_vps_key_new.pub" -Raw
        $fixedKey = $originalKey.Replace("`r`n", "").Replace("`r", "").Replace("`n", "").Trim()
        [System.IO.File]::WriteAllText($PUBLIC_KEY_FIXED, $fixedKey + "`n", [System.Text.Encoding]::UTF8)
        Write-Host "Fixed key created!" -ForegroundColor Green
        
        Write-Host "`nKey to copy to VPS:" -ForegroundColor Yellow
        Write-Host "===========================================" -ForegroundColor Cyan
        Write-Host $fixedKey -ForegroundColor White
        Write-Host "===========================================" -ForegroundColor Cyan
    }
}

Write-Host "`n=== Step 2: VPS Side - Manual Operations Required ===" -ForegroundColor Cyan
Write-Host "You need to log into your VPS via ConoHa console and run these commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Check current status:" -ForegroundColor Green
Write-Host "   bash /path/to/vps_check_keys_manual.sh" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Backup existing keys:" -ForegroundColor Green
Write-Host "   cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Clear authorized_keys completely:" -ForegroundColor Green
Write-Host "   echo '' > ~/.ssh/authorized_keys" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Add the correct key:" -ForegroundColor Green
Write-Host "   nano ~/.ssh/authorized_keys" -ForegroundColor Gray
Write-Host "   # Paste the key shown above (the one in the blue box)" -ForegroundColor Gray
Write-Host "   # Make sure it's all on ONE line with no line breaks" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Set correct permissions:" -ForegroundColor Green
Write-Host "   chmod 600 ~/.ssh/authorized_keys" -ForegroundColor Gray
Write-Host "   chmod 700 ~/.ssh" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Verify the key was added correctly:" -ForegroundColor Green
Write-Host "   cat ~/.ssh/authorized_keys" -ForegroundColor Gray
Write-Host "   # Should show exactly one line with your public key" -ForegroundColor Gray

Write-Host "`n=== Step 3: Test Connection ===" -ForegroundColor Cyan
Write-Host "After completing VPS-side operations, test connection:" -ForegroundColor Yellow
Write-Host "ssh -o IdentitiesOnly=yes -i `"$PRIVATE_KEY`" root@$VPS_IP" -ForegroundColor Gray

Write-Host "`n=== Troubleshooting Tips ===" -ForegroundColor Magenta
Write-Host "If connection still fails:" -ForegroundColor Yellow
Write-Host "• Make sure the public key is exactly ONE line in authorized_keys" -ForegroundColor White
Write-Host "• No extra spaces, line breaks, or special characters" -ForegroundColor White
Write-Host "• Check VPS auth logs: tail -f /var/log/auth.log" -ForegroundColor White
Write-Host "• Verify permissions: ls -la ~/.ssh/" -ForegroundColor White

Write-Host "`n=== Current Issue Analysis ===" -ForegroundColor Red
Write-Host "The connection is failing because:" -ForegroundColor Yellow
Write-Host "1. The public key on VPS may still have Windows line endings (CRLF)" -ForegroundColor White
Write-Host "2. Or there might be extra characters/spaces in authorized_keys" -ForegroundColor White
Write-Host "3. Or the key isn't properly formatted as a single line" -ForegroundColor White
Write-Host ""
Write-Host "Solution: Manual update of authorized_keys on VPS with the fixed key above." -ForegroundColor Green
