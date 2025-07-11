# SSH接続テストスクリプト (PowerShell)
# SSH鍵の確認とSSH接続のテスト

Write-Host "===== SSH接続テストと診断 =====" -ForegroundColor Cyan
Write-Host "実行日時: $(Get-Date)" -ForegroundColor Gray
Write-Host ""

# SSH鍵ファイルの確認
$sshKeyPath = "C:\Users\jinna\.ssh\mednext_vps_key_new"
$sshPubKeyPath = "C:\Users\jinna\.ssh\mednext_vps_key_new.pub"
$sshConfigPath = "C:\Users\jinna\.ssh\config"

Write-Host "=== SSH鍵ファイルの確認 ===" -ForegroundColor Yellow

if (Test-Path $sshKeyPath) {
    Write-Host "✓ 秘密鍵が存在: $sshKeyPath" -ForegroundColor Green
    $keyInfo = Get-Item $sshKeyPath
    Write-Host "  ファイルサイズ: $($keyInfo.Length) bytes" -ForegroundColor Gray
    Write-Host "  最終更新: $($keyInfo.LastWriteTime)" -ForegroundColor Gray
    
    # 権限確認（Windows）
    $acl = Get-Acl $sshKeyPath
    Write-Host "  権限情報:" -ForegroundColor Gray
    $acl.Access | ForEach-Object {
        Write-Host "    $($_.IdentityReference): $($_.FileSystemRights)" -ForegroundColor Gray
    }
} else {
    Write-Host "✗ 秘密鍵が見つかりません: $sshKeyPath" -ForegroundColor Red
    exit 1
}

if (Test-Path $sshPubKeyPath) {
    Write-Host "✓ 公開鍵が存在: $sshPubKeyPath" -ForegroundColor Green
    
    # 公開鍵の内容表示
    Write-Host "  公開鍵の内容:" -ForegroundColor Gray
    $pubKeyContent = Get-Content $sshPubKeyPath
    Write-Host "    $pubKeyContent" -ForegroundColor Gray
    
    # フィンガープリント表示
    Write-Host "  フィンガープリント:" -ForegroundColor Gray
    $fingerprint = ssh-keygen -l -f $sshPubKeyPath
    Write-Host "    $fingerprint" -ForegroundColor Gray
} else {
    Write-Host "✗ 公開鍵が見つかりません: $sshPubKeyPath" -ForegroundColor Red
}

Write-Host ""

# SSH設定ファイルの確認
Write-Host "=== SSH設定ファイルの確認 ===" -ForegroundColor Yellow

if (Test-Path $sshConfigPath) {
    Write-Host "✓ SSH設定ファイルが存在: $sshConfigPath" -ForegroundColor Green
    Write-Host "  設定内容:" -ForegroundColor Gray
    Get-Content $sshConfigPath | ForEach-Object {
        Write-Host "    $_" -ForegroundColor Gray
    }
} else {
    Write-Host "✗ SSH設定ファイルが見つかりません: $sshConfigPath" -ForegroundColor Red
}

Write-Host ""

# ネットワーク接続テスト
Write-Host "=== ネットワーク接続テスト ===" -ForegroundColor Yellow
$vpsIp = "180.147.38.203"
$sshPort = 22

Write-Host "VPSへのPing テスト:" -ForegroundColor Gray
$pingResult = Test-Connection -ComputerName $vpsIp -Count 3 -Quiet
if ($pingResult) {
    Write-Host "✓ Ping成功: $vpsIp は到達可能です" -ForegroundColor Green
} else {
    Write-Host "✗ Ping失敗: $vpsIp に到達できません" -ForegroundColor Red
}

Write-Host "SSH ポート ($sshPort) の接続テスト:" -ForegroundColor Gray
$tcpTest = Test-NetConnection -ComputerName $vpsIp -Port $sshPort -InformationLevel Quiet
if ($tcpTest) {
    Write-Host "✓ SSH ポート接続成功: $vpsIp`:$sshPort" -ForegroundColor Green
} else {
    Write-Host "✗ SSH ポート接続失敗: $vpsIp`:$sshPort" -ForegroundColor Red
}

Write-Host ""

# SSH接続テスト（詳細ログ付き）
Write-Host "=== SSH接続テスト ===" -ForegroundColor Yellow

Write-Host "1. 標準SSH接続テスト (詳細ログ付き):" -ForegroundColor Gray
$sshCommand1 = "ssh -i `"$sshKeyPath`" -v -o ConnectTimeout=10 -o StrictHostKeyChecking=no root@$vpsIp exit"
Write-Host "実行コマンド: $sshCommand1" -ForegroundColor Gray
Write-Host "出力:" -ForegroundColor Gray

try {
    $result1 = Invoke-Expression $sshCommand1 2>&1
    $result1 | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ SSH接続成功！" -ForegroundColor Green
    } else {
        Write-Host "✗ SSH接続失敗 (終了コード: $LASTEXITCODE)" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ SSH接続でエラーが発生: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

Write-Host "2. SSH設定ファイル使用接続テスト:" -ForegroundColor Gray
$sshCommand2 = "ssh -v -o ConnectTimeout=10 mednext_vps exit"
Write-Host "実行コマンド: $sshCommand2" -ForegroundColor Gray
Write-Host "出力:" -ForegroundColor Gray

try {
    $result2 = Invoke-Expression $sshCommand2 2>&1
    $result2 | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ SSH設定ファイル接続成功！" -ForegroundColor Green
    } else {
        Write-Host "✗ SSH設定ファイル接続失敗 (終了コード: $LASTEXITCODE)" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ SSH設定ファイル接続でエラーが発生: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# SSH Agent確認
Write-Host "=== SSH Agent確認 ===" -ForegroundColor Yellow

$sshAgentPid = Get-Process ssh-agent -ErrorAction SilentlyContinue
if ($sshAgentPid) {
    Write-Host "✓ SSH Agent が実行中です (PID: $($sshAgentPid.Id))" -ForegroundColor Green
    
    # 登録されている鍵の確認
    Write-Host "SSH Agent に登録されている鍵:" -ForegroundColor Gray
    try {
        $agentKeys = ssh-add -l 2>&1
        if ($agentKeys -match "no identities") {
            Write-Host "  鍵が登録されていません" -ForegroundColor Yellow
        } else {
            $agentKeys | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
        }
    } catch {
        Write-Host "  鍵の一覧取得に失敗" -ForegroundColor Red
    }
} else {
    Write-Host "✗ SSH Agent が実行されていません" -ForegroundColor Red
}

Write-Host ""

# 推奨アクション
Write-Host "=== 推奨アクション ===" -ForegroundColor Yellow
Write-Host "1. VPS側でSSH鍵の確認を実行:" -ForegroundColor Green
Write-Host "   chmod +x vps_check_all_ssh_keys.sh && ./vps_check_all_ssh_keys.sh" -ForegroundColor Gray
Write-Host ""
Write-Host "2. SSH鍵のクリーンアップが必要な場合:" -ForegroundColor Green
Write-Host "   chmod +x vps_ssh_key_cleanup.sh && ./vps_ssh_key_cleanup.sh" -ForegroundColor Gray
Write-Host ""
Write-Host "3. VSCode Remote-SSH接続テスト:" -ForegroundColor Green
Write-Host "   Ctrl+Shift+P -> 'Remote-SSH: Connect to Host...' -> 'mednext_vps'" -ForegroundColor Gray
Write-Host ""

Write-Host "===== テスト完了 =====" -ForegroundColor Cyan
