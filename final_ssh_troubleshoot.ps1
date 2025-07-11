# Final SSH Troubleshooting Script
# 最終的なSSH接続問題の解決

Write-Host "=== Final SSH Connection Troubleshooting ===" -ForegroundColor Green

Write-Host "`n1. VPS側で実行してください（別のターミナルで）:" -ForegroundColor Cyan
Write-Host "sudo tail -f /var/log/auth.log | grep ssh" -ForegroundColor White
Write-Host ""
Write-Host "2. 上記のコマンドを実行した後、このスクリプトを続行してください"
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host "`n3. SSH接続を試行中..." -ForegroundColor Cyan

# SSH接続を試行
$sshCommand = 'ssh -o IdentitiesOnly=yes -i "C:\Users\jinna\.ssh\company_vps_key" root@160.251.181.238 "echo SUCCESS && whoami && date"'
Write-Host "Command: $sshCommand" -ForegroundColor Gray

try {
    $result = Invoke-Expression $sshCommand
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ SSH接続成功!" -ForegroundColor Green
        Write-Host "結果: $result" -ForegroundColor Green
    } else {
        Write-Host "`n❌ SSH接続失敗" -ForegroundColor Red
        Write-Host "Exit Code: $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host "`n❌ SSH接続エラー: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n4. VPS側のauth.logで確認してください:" -ForegroundColor Magenta
Write-Host "• 接続試行のログが表示されましたか？"
Write-Host "• 認証失敗の具体的な理由が記録されていますか？"
Write-Host "• 公開鍵認証の詳細なエラーメッセージはありましたか？"

Write-Host "`n5. 最後の手段 - VPS側で強制的に公開鍵を再設定:" -ForegroundColor Yellow
Write-Host "# バックアップを作成"
Write-Host "cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.$(date +%Y%m%d_%H%M%S)"
Write-Host ""
Write-Host "# Windows側の公開鍵を直接ファイルに書き込み"

$publicKey = Get-Content "C:\Users\jinna\.ssh\company_vps_key.pub" -Raw
$cleanKey = $publicKey.Trim()

Write-Host "cat > ~/.ssh/authorized_keys << 'EOF'" -ForegroundColor White
Write-Host $cleanKey -ForegroundColor White
Write-Host "EOF" -ForegroundColor White
Write-Host ""
Write-Host "# 権限設定"
Write-Host "chmod 600 ~/.ssh/authorized_keys" -ForegroundColor White
Write-Host "chmod 700 ~/.ssh" -ForegroundColor White
Write-Host ""
Write-Host "# SSHDサービス再起動"
Write-Host "sudo systemctl restart ssh" -ForegroundColor White

Write-Host "`n6. 公開鍵の内容（確認用）:" -ForegroundColor Cyan
Write-Host "Length: $($cleanKey.Length) characters" -ForegroundColor Gray
Write-Host "First 50 chars: $($cleanKey.Substring(0, [Math]::Min(50, $cleanKey.Length)))" -ForegroundColor Gray
Write-Host "Last 50 chars: $($cleanKey.Substring([Math]::Max(0, $cleanKey.Length - 50)))" -ForegroundColor Gray
