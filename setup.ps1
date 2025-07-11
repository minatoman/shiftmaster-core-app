# ============================================
# ShiftMaster開発環境セットアップスクリプト
# PowerShell版 - Windows対応
# ============================================

param(
    [switch]$SkipVenv,
    [switch]$SkipInstall,
    [switch]$SkipMigrate,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
ShiftMaster開発環境セットアップスクリプト

使用方法:
  .\setup.ps1                   # 完全セットアップ
  .\setup.ps1 -SkipVenv         # 仮想環境作成をスキップ
  .\setup.ps1 -SkipInstall      # パッケージインストールをスキップ
  .\setup.ps1 -SkipMigrate      # データベースマイグレーションをスキップ
  .\setup.ps1 -Help             # このヘルプを表示

要件:
  - Python 3.8以上
  - Git
  - PowerShell 5.0以上
"@
    exit 0
}

Write-Host "🚀 ShiftMaster開発環境セットアップ開始..." -ForegroundColor Green

# Python バージョンチェック
Write-Host "📋 Python バージョン確認..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Pythonが見つかりません。Python 3.8以上をインストールしてください。" -ForegroundColor Red
    exit 1
}

# 仮想環境作成
if (-not $SkipVenv) {
    Write-Host "🐍 仮想環境作成..." -ForegroundColor Yellow
    if (Test-Path "venv") {
        Write-Host "⚠️ 既存の仮想環境が見つかりました。削除して再作成しますか？ (y/N)" -ForegroundColor Yellow
        $response = Read-Host
        if ($response -eq "y" -or $response -eq "Y") {
            Remove-Item -Recurse -Force venv
            python -m venv venv
        }
    }
    else {
        python -m venv venv
    }
    
    Write-Host "🔧 仮想環境をアクティベート..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✅ 仮想環境がアクティブになりました" -ForegroundColor Green
}

# 依存関係インストール
if (-not $SkipInstall) {
    Write-Host "📦 パッケージインストール..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "✅ パッケージインストール完了" -ForegroundColor Green
}

# データベースセットアップ
if (-not $SkipMigrate) {
    Write-Host "🗃️ データベースセットアップ..." -ForegroundColor Yellow
    python manage.py makemigrations
    python manage.py migrate
    
    Write-Host "👤 スーパーユーザーを作成しますか？ (y/N)" -ForegroundColor Yellow
    $createSuperuser = Read-Host
    if ($createSuperuser -eq "y" -or $createSuperuser -eq "Y") {
        python manage.py createsuperuser
    }
    Write-Host "✅ データベースセットアップ完了" -ForegroundColor Green
}

# 静的ファイル収集
Write-Host "📁 静的ファイル収集..." -ForegroundColor Yellow
python manage.py collectstatic --noinput
Write-Host "✅ 静的ファイル収集完了" -ForegroundColor Green

Write-Host @"

🎉 セットアップ完了！

次のコマンドでサーバーを起動:
  python manage.py runserver

アクセス:
  - アプリケーション: http://localhost:8000
  - 管理画面: http://localhost:8000/admin/

開発に役立つコマンド:
  - テスト実行: python manage.py test
  - シェル起動: python manage.py shell
  - マイグレーション作成: python manage.py makemigrations
  - 新しいアプリ作成: python manage.py startapp appname

"@ -ForegroundColor Green
