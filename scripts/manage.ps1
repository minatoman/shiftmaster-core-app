# ============================================
# ShiftMaster 管理スクリプト
# Docker環境での運用・保守コマンド集
# ============================================

param(
    [Parameter(Mandatory = $false)]
    [ValidateSet("start", "stop", "restart", "logs", "backup", "restore", "update", "shell", "test", "status", "help")]
    [string]$Action = "help",
    
    [Parameter(Mandatory = $false)]
    [ValidateSet("dev", "prod")]
    [string]$Environment = "dev",
    
    [Parameter(Mandatory = $false)]
    [string]$Service = "",
    
    [Parameter(Mandatory = $false)]
    [string]$BackupFile = ""
)

$ErrorActionPreference = "Stop"

# カラー設定
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
$Cyan = "Cyan"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Show-Help {
    Write-ColorOutput "🏥 ShiftMaster 管理スクリプト" $Green
    Write-ColorOutput "================================" $Green
    Write-Host ""
    Write-ColorOutput "使用方法:" $Cyan
    Write-Host "  .\scripts\manage.ps1 -Action <action> [-Environment <env>] [-Service <service>]"
    Write-Host ""
    Write-ColorOutput "アクション:" $Cyan
    Write-Host "  start     - サービス開始"
    Write-Host "  stop      - サービス停止"
    Write-Host "  restart   - サービス再起動"
    Write-Host "  logs      - ログ表示"
    Write-Host "  backup    - データベースバックアップ"
    Write-Host "  restore   - データベース復元"
    Write-Host "  update    - アプリケーション更新"
    Write-Host "  shell     - Djangoシェル起動"
    Write-Host "  test      - テスト実行"
    Write-Host "  status    - サービス状態確認"
    Write-Host ""
    Write-ColorOutput "環境指定:" $Cyan
    Write-Host "  dev       - 開発環境 (デフォルト)"
    Write-Host "  prod      - 本番環境"
    Write-Host ""
    Write-ColorOutput "使用例:" $Yellow
    Write-Host "  .\scripts\manage.ps1 -Action start -Environment dev"
    Write-Host "  .\scripts\manage.ps1 -Action logs -Service web"
    Write-Host "  .\scripts\manage.ps1 -Action backup"
}

function Get-ComposeFile {
    if ($Environment -eq "prod") {
        return "docker-compose.prod.yml"
    }
    else {
        return "docker-compose.dev.yml"
    }
}

function Start-Services {
    $composeFile = Get-ComposeFile
    Write-ColorOutput "🚀 ShiftMaster起動中 ($Environment環境)..." $Green
    
    if ($Environment -eq "dev") {
        docker-compose -f $composeFile up -d
    }
    else {
        # 本番環境では環境変数ファイルをチェック
        if (-not (Test-Path ".env")) {
            Write-ColorOutput "❌ .envファイルが見つかりません。.env.exampleを参考に作成してください。" $Red
            exit 1
        }
        docker-compose -f $composeFile up -d
    }
    
    Write-ColorOutput "✅ サービス起動完了" $Green
    Get-ServiceStatus
}

function Stop-Services {
    $composeFile = Get-ComposeFile
    Write-ColorOutput "🛑 ShiftMaster停止中..." $Yellow
    docker-compose -f $composeFile down
    Write-ColorOutput "✅ サービス停止完了" $Green
}

function Restart-Services {
    Write-ColorOutput "🔄 ShiftMaster再起動中..." $Yellow
    Stop-Services
    Start-Sleep -Seconds 3
    Start-Services
}

function Show-Logs {
    $composeFile = Get-ComposeFile
    if ($Service) {
        Write-ColorOutput "📋 ログ表示: $Service" $Cyan
        docker-compose -f $composeFile logs -f $Service
    }
    else {
        Write-ColorOutput "📋 全サービスログ表示" $Cyan
        docker-compose -f $composeFile logs -f
    }
}

function Backup-Database {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupDir = "backups"
    $backupFile = "$backupDir/shiftmaster_backup_$timestamp.sql"
    
    # バックアップディレクトリ作成
    if (-not (Test-Path $backupDir)) {
        New-Item -ItemType Directory -Path $backupDir
    }
    
    Write-ColorOutput "💾 データベースバックアップ開始..." $Yellow
    
    if ($Environment -eq "prod") {
        # PostgreSQLバックアップ
        docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U shiftmaster_user shiftmaster > $backupFile
    }
    else {
        # SQLiteバックアップ
        Copy-Item "db.sqlite3" "$backupDir/shiftmaster_backup_$timestamp.sqlite3" -ErrorAction SilentlyContinue
        $backupFile = "$backupDir/shiftmaster_backup_$timestamp.sqlite3"
    }
    
    Write-ColorOutput "✅ バックアップ完了: $backupFile" $Green
}

function Restore-Database {
    if (-not $BackupFile) {
        Write-ColorOutput "❌ バックアップファイルを指定してください: -BackupFile <path>" $Red
        exit 1
    }
    
    if (-not (Test-Path $BackupFile)) {
        Write-ColorOutput "❌ バックアップファイルが見つかりません: $BackupFile" $Red
        exit 1
    }
    
    Write-ColorOutput "🔄 データベース復元中..." $Yellow
    Write-ColorOutput "⚠️ 既存のデータは削除されます。続行しますか？ (y/N)" $Yellow
    $confirm = Read-Host
    
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-ColorOutput "❌ 復元をキャンセルしました" $Red
        exit 0
    }
    
    if ($Environment -eq "prod") {
        # PostgreSQL復元
        Get-Content $BackupFile | docker-compose -f docker-compose.prod.yml exec -T db psql -U shiftmaster_user -d shiftmaster
    }
    else {
        # SQLite復元
        Copy-Item $BackupFile "db.sqlite3" -Force
    }
    
    Write-ColorOutput "✅ データベース復元完了" $Green
}

function Update-Application {
    Write-ColorOutput "🔄 アプリケーション更新中..." $Yellow
    
    # Gitから最新版取得
    git pull origin main
    
    # イメージ再ビルド
    $composeFile = Get-ComposeFile
    docker-compose -f $composeFile build --no-cache
    
    # サービス再起動
    Restart-Services
    
    Write-ColorOutput "✅ アプリケーション更新完了" $Green
}

function Start-Shell {
    $composeFile = Get-ComposeFile
    Write-ColorOutput "🐚 Djangoシェル起動..." $Cyan
    docker-compose -f $composeFile exec web python manage.py shell
}

function Invoke-Tests {
    $composeFile = Get-ComposeFile
    Write-ColorOutput "🧪 テスト実行中..." $Yellow
    docker-compose -f $composeFile exec web python manage.py test
}

function Get-ServiceStatus {
    $composeFile = Get-ComposeFile
    Write-ColorOutput "📊 サービス状態:" $Cyan
    docker-compose -f $composeFile ps
    
    Write-Host ""
    Write-ColorOutput "🌐 アクセス情報:" $Cyan
    if ($Environment -eq "dev") {
        Write-Host "  アプリケーション: http://localhost:8000"
        Write-Host "  管理画面: http://localhost:8000/admin/"
    }
    else {
        Write-Host "  アプリケーション: https://localhost"
        Write-Host "  管理画面: https://localhost/admin/"
    }
}

# メイン処理
switch ($Action) {
    "start" { Start-Services }
    "stop" { Stop-Services }
    "restart" { Restart-Services }
    "logs" { Show-Logs }
    "backup" { Backup-Database }
    "restore" { Restore-Database }
    "update" { Update-Application }
    "shell" { Start-Shell }
    "test" { Invoke-Tests }
    "status" { Get-ServiceStatus }
    "help" { Show-Help }
    default { Show-Help }
}
