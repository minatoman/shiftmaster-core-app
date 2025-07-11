#!/usr/bin/env pwsh
# 最終SSH診断とauthorized_keys再作成スクリプト

Write-Host "🔧 最終SSH診断とauthorized_keys再作成" -ForegroundColor Cyan
Write-Host "=" * 50

# 公開鍵内容表示
$SSH_PUB_KEY = "C:\Users\jinna\.ssh\mednext_vps_key_new.pub"

Write-Host "`n📋 ステップ1: 公開鍵内容確認" -ForegroundColor Yellow
Write-Host "-" * 30

if (Test-Path $SSH_PUB_KEY) {
    $pubKeyContent = Get-Content $SSH_PUB_KEY -Raw
    $pubKeyTrimmed = $pubKeyContent.Trim()
    
    Write-Host "✅ 公開鍵ファイル読み込み成功" -ForegroundColor Green
    Write-Host "📏 公開鍵長さ: $($pubKeyTrimmed.Length) 文字"
    Write-Host ""
    Write-Host "🔑 公開鍵内容（完全版）:" -ForegroundColor Cyan
    Write-Host $pubKeyTrimmed -ForegroundColor White
    Write-Host ""
    
    # VPS側でのauthorized_keys再作成コマンド生成
    Write-Host "`n📋 ステップ2: VPS側でのauthorized_keys再作成コマンド" -ForegroundColor Yellow
    Write-Host "-" * 50
    
    Write-Host "🔧 VPS側で以下のコマンドを順番に実行してください:" -ForegroundColor Green
    Write-Host ""
    Write-Host "# 1. 既存のauthorized_keysをバックアップ"
    Write-Host "cp /root/.ssh/authorized_keys /root/.ssh/authorized_keys.backup.$(date +%Y%m%d_%H%M%S)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "# 2. authorized_keysを完全に再作成"
    Write-Host "rm /root/.ssh/authorized_keys" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "# 3. 新しい公開鍵を設定（以下の内容をコピペしてください）"
    Write-Host "cat > /root/.ssh/authorized_keys << 'EOF'" -ForegroundColor Cyan
    Write-Host $pubKeyTrimmed -ForegroundColor White
    Write-Host "EOF" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "# 4. 権限設定"
    Write-Host "chmod 600 /root/.ssh/authorized_keys" -ForegroundColor Cyan
    Write-Host "chown root:root /root/.ssh/authorized_keys" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "# 5. 設定確認"
    Write-Host "ls -la /root/.ssh/authorized_keys" -ForegroundColor Cyan
    Write-Host "wc -l /root/.ssh/authorized_keys" -ForegroundColor Cyan
    Write-Host "head -c 50 /root/.ssh/authorized_keys" -ForegroundColor Cyan
    
} else {
    Write-Host "❌ 公開鍵ファイルが見つかりません: $SSH_PUB_KEY" -ForegroundColor Red
    exit 1
}

Write-Host "`n📋 ステップ3: SSH接続再テスト用コマンド" -ForegroundColor Yellow
Write-Host "-" * 40

Write-Host "🔧 VPS側でauthorized_keys再作成後、以下で接続をテストしてください:" -ForegroundColor Green
Write-Host ""
Write-Host "ssh -v vps-server whoami" -ForegroundColor Cyan
Write-Host ""

Write-Host "`n📋 ステップ4: VPS側でのリアルタイムログ監視" -ForegroundColor Yellow
Write-Host "-" * 45

Write-Host "🔧 VPS側で以下のコマンドでSSH認証ログをリアルタイム監視:" -ForegroundColor Green
Write-Host ""
Write-Host "tail -f /var/log/auth.log | grep --line-buffered 'sshd\|SSH'" -ForegroundColor Cyan
Write-Host ""
Write-Host "または、別のターミナルで:" -ForegroundColor Green
Write-Host "journalctl -u ssh -f" -ForegroundColor Cyan

Write-Host "`n🎯 実行順序:" -ForegroundColor Green
Write-Host "1. VPS側でauthorized_keysを再作成（上記コマンド使用）"
Write-Host "2. VPS側でリアルタイムログ監視を開始"
Write-Host "3. Windows側からSSH接続テストを実行"
Write-Host "4. ログに表示されるエラーメッセージを確認"
Write-Host ""
Write-Host "✨ authorized_keys再作成後に接続が成功すれば、VSCode Remote-SSH接続も可能になります！" -ForegroundColor Green
