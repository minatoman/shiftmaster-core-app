#!/usr/bin/env pwsh
# SSH最終デバッグスクリプト - VPS認証ログ確認と接続テスト

Write-Host "🔍 SSH最終デバッグ - VPS認証ログ確認と接続テスト" -ForegroundColor Cyan
Write-Host "=" * 60

$VPS_IP = "160.251.181.238"
$SSH_USER = "root"
$SSH_KEY = "C:\Users\jinna\.ssh\mednext_vps_key_new"
$SSH_CONFIG_FILE = "C:\Users\jinna\.ssh\config"

# 手順1: SSH設定確認
Write-Host "`n📋 手順1: Windows側SSH設定確認" -ForegroundColor Yellow
Write-Host "-" * 40

Write-Host "🔑 SSH秘密鍵ファイル確認:"
if (Test-Path $SSH_KEY) {
    $keyInfo = Get-ItemProperty $SSH_KEY
    Write-Host "  ✅ ファイル存在: $SSH_KEY" -ForegroundColor Green
    Write-Host "  📏 ファイルサイズ: $($keyInfo.Length) bytes"
    Write-Host "  📅 更新日時: $($keyInfo.LastWriteTime)"
} else {
    Write-Host "  ❌ 秘密鍵ファイルが見つかりません: $SSH_KEY" -ForegroundColor Red
}

Write-Host "`n🔑 SSH公開鍵確認:"
$SSH_PUB_KEY = "${SSH_KEY}.pub"
if (Test-Path $SSH_PUB_KEY) {
    Write-Host "  ✅ 公開鍵ファイル存在: $SSH_PUB_KEY" -ForegroundColor Green
    $pubKeyContent = Get-Content $SSH_PUB_KEY -Raw
    Write-Host "  📏 公開鍵長さ: $($pubKeyContent.Length) 文字"
    Write-Host "  🔍 公開鍵開始: $($pubKeyContent.Substring(0, [Math]::Min(50, $pubKeyContent.Length)))..."
    
    # 公開鍵フィンガープリント取得
    Write-Host "`n🔍 公開鍵フィンガープリント:"
    try {
        $fingerprintResult = ssh-keygen -lf $SSH_PUB_KEY
        Write-Host "  $fingerprintResult" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ フィンガープリント取得エラー: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "  ❌ 公開鍵ファイルが見つかりません: $SSH_PUB_KEY" -ForegroundColor Red
}

# 手順2: SSH config確認
Write-Host "`n📋 手順2: SSH config確認" -ForegroundColor Yellow
Write-Host "-" * 40

if (Test-Path $SSH_CONFIG_FILE) {
    Write-Host "✅ SSH configファイル存在: $SSH_CONFIG_FILE" -ForegroundColor Green
    Write-Host "📋 vps-server設定:"
    $configContent = Get-Content $SSH_CONFIG_FILE
    $vpsSection = $false
    foreach ($line in $configContent) {
        if ($line -match "^Host vps-server") {
            $vpsSection = $true
            Write-Host "  $line" -ForegroundColor Cyan
        } elseif ($vpsSection -and ($line -match "^Host " -and $line -notmatch "vps-server")) {
            break
        } elseif ($vpsSection) {
            Write-Host "  $line" -ForegroundColor White
        }
    }
} else {
    Write-Host "❌ SSH configファイルが見つかりません: $SSH_CONFIG_FILE" -ForegroundColor Red
}

# 手順3: VPS接続テスト（詳細ログ付き）
Write-Host "`n📋 手順3: SSH接続テスト（詳細ログ）" -ForegroundColor Yellow
Write-Host "-" * 40

Write-Host "🔗 SSH接続テスト実行中..."
Write-Host "コマンド: ssh -vvv -o ConnectTimeout=10 -o BatchMode=yes vps-server whoami"

try {
    $sshResult = ssh -vvv -o ConnectTimeout=10 -o BatchMode=yes vps-server whoami 2>&1
    
    Write-Host "`n📋 SSH接続結果:" -ForegroundColor Cyan
    foreach ($line in $sshResult) {
        $line = $line.ToString()
        if ($line -match "debug1:|debug2:|debug3:") {
            if ($line -match "Offering|Trying|Authentication|identity|key") {
                Write-Host "  🔍 $line" -ForegroundColor Green
            }
        } elseif ($line -match "Permission denied") {
            Write-Host "  ❌ $line" -ForegroundColor Red
        } elseif ($line -match "root|whoami") {
            Write-Host "  ✅ $line" -ForegroundColor Green
        } else {
            Write-Host "  📋 $line" -ForegroundColor Yellow
        }
    }
    
    # 最終結果判定
    if ($sshResult -contains "root") {
        Write-Host "`n🎉 SSH接続成功！" -ForegroundColor Green
        return $true
    } else {
        Write-Host "`n❌ SSH接続失敗" -ForegroundColor Red
        return $false
    }
    
} catch {
    Write-Host "`n❌ SSH接続エラー: $($_.Exception.Message)" -ForegroundColor Red
    return $false
}

# 手順4: VPS側ログ確認コマンド生成
Write-Host "`n📋 手順4: VPS側でのログ確認コマンド" -ForegroundColor Yellow
Write-Host "-" * 40

Write-Host "🔍 VPS側で以下のコマンドを実行してSSH認証ログを確認してください:"
Write-Host ""
Write-Host "# 最新のSSH認証ログを確認"
Write-Host "tail -f /var/log/auth.log | grep sshd" -ForegroundColor Cyan
Write-Host ""
Write-Host "# または、最近のSSH関連ログを表示"
Write-Host "tail -20 /var/log/auth.log | grep SSH" -ForegroundColor Cyan
Write-Host ""
Write-Host "# authorized_keysファイルの内容と権限を再確認"
Write-Host "ls -la /root/.ssh/"
Write-Host "cat /root/.ssh/authorized_keys"
Write-Host "wc -l /root/.ssh/authorized_keys" -ForegroundColor Cyan

# 手順5: 追加のトラブルシューティング
Write-Host "`n📋 手順5: 追加のトラブルシューティング手順" -ForegroundColor Yellow
Write-Host "-" * 40

Write-Host "🛠️ 接続が失敗する場合の追加確認項目:"
Write-Host "1. VPS側でSSHサービスが動作しているか確認:"
Write-Host "   systemctl status ssh" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. ファイアウォール設定確認:"
Write-Host "   ufw status" -ForegroundColor Cyan
Write-Host "   iptables -L INPUT -n | grep :22" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. authorized_keysファイルの再作成:"
Write-Host "   rm /root/.ssh/authorized_keys" -ForegroundColor Cyan
Write-Host "   echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDCwrK...' > /root/.ssh/authorized_keys" -ForegroundColor Cyan
Write-Host "   chmod 600 /root/.ssh/authorized_keys" -ForegroundColor Cyan
Write-Host "   chown root:root /root/.ssh/authorized_keys" -ForegroundColor Cyan

Write-Host "`n🎯 次のステップ:" -ForegroundColor Green
Write-Host "1. 上記のSSH接続テストを実行"
Write-Host "2. 失敗した場合は、VPS側でauth.logを確認"
Write-Host "3. 必要に応じてauthorized_keysを再作成"
Write-Host "4. 成功したら、VSCode Remote-SSH接続をテスト"
