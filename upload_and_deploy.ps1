# ShiftMaster プロジェクトファイル VPS アップロードスクリプト
# PowerShell版

$VPS_IP = "160.251.181.238"
$VPS_USER = "root"
$SSH_KEY = "C:\Users\jinna\.ssh\mednext_vps_key"
$LOCAL_PROJECT = "h:\Projects\ShiftMaster"
$REMOTE_PROJECT = "/var/www/shiftmaster"

Write-Host "🚀 ShiftMaster プロジェクトをVPSにアップロード中..." -ForegroundColor Green
Write-Host "📦 ローカル: $LOCAL_PROJECT" -ForegroundColor Cyan
Write-Host "🌐 リモート: ${VPS_USER}@${VPS_IP}:${REMOTE_PROJECT}" -ForegroundColor Cyan

# 1. リモートディレクトリ作成
Write-Host "`n📁 リモートディレクトリを作成中..." -ForegroundColor Yellow
ssh -i $SSH_KEY $VPS_USER@$VPS_IP "sudo mkdir -p $REMOTE_PROJECT && sudo chown $VPS_USER`:$VPS_USER $REMOTE_PROJECT"

# 2. プロジェクトファイル同期（rsync使用）
Write-Host "`n📤 プロジェクトファイルを同期中..." -ForegroundColor Yellow

# 除外するファイル・ディレクトリリスト
$excludeList = @(
    "--exclude=*.pyc",
    "--exclude=__pycache__/",
    "--exclude=.git/",
    "--exclude=venv/",
    "--exclude=env/",
    "--exclude=*.log",
    "--exclude=db.sqlite3",
    "--exclude=.env",
    "--exclude=node_modules/",
    "--exclude=*.tmp"
)

# rsyncでファイル同期
$rsyncCmd = "rsync -avz --delete " + ($excludeList -join " ") + " -e `"ssh -i $SSH_KEY`" $LOCAL_PROJECT/ $VPS_USER@${VPS_IP}:$REMOTE_PROJECT/"
Write-Host "実行コマンド: $rsyncCmd" -ForegroundColor Gray

Invoke-Expression $rsyncCmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ ファイル同期完了" -ForegroundColor Green
} else {
    Write-Host "`n❌ ファイル同期失敗" -ForegroundColor Red
    exit 1
}

# 3. デプロイスクリプト実行
Write-Host "`n🔧 VPS上でデプロイスクリプトを実行中..." -ForegroundColor Yellow
ssh -i $SSH_KEY $VPS_USER@$VPS_IP "cd $REMOTE_PROJECT && chmod +x vps_django_deployment_script.sh && sudo bash vps_django_deployment_script.sh"

# 4. サービス状態確認
Write-Host "`n📋 サービス状態を確認中..." -ForegroundColor Yellow
ssh -i $SSH_KEY $VPS_USER@$VPS_IP "sudo supervisorctl status && sudo systemctl status nginx"

Write-Host "`n🎉 デプロイ完了!" -ForegroundColor Green
Write-Host "🌐 アクセス可能URL: http://$VPS_IP" -ForegroundColor Cyan
Write-Host "📋 ログ確認: ssh -i $SSH_KEY $VPS_USER@$VPS_IP 'sudo tail -f /var/log/shiftmaster.out.log'" -ForegroundColor Gray
