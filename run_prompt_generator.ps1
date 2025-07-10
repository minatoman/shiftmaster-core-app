# ShiftMaster 勤怠システム プロンプト生成器 PowerShell スクリプト
# 使用方法: .\run_prompt_generator.ps1 [質問・指示]

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$UserInput
)

# 文字エンコーディング設定
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " 🚀 ShiftMaster 勤怠システム プロンプト生成器" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Pythonファイルの存在確認
$pythonFile = Join-Path $PSScriptRoot "Get_ChildItem.py"
if (-not (Test-Path $pythonFile)) {
    Write-Host "❌ エラー: Get_ChildItem.py が見つかりません。" -ForegroundColor Red
    Write-Host "   パス: $pythonFile" -ForegroundColor Red
    exit 1
}

# Python実行可能ファイルの確認
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python検出: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ エラー: Pythonが見つかりません。Pythonをインストールしてください。" -ForegroundColor Red
    exit 1
}

# 実行
try {
    if ($UserInput) {
        Write-Host "📝 自動モードで実行中..." -ForegroundColor Yellow
        Write-Host "入力: $($UserInput -join ' ')" -ForegroundColor Gray
        Write-Host ""
        python $pythonFile @UserInput
    } else {
        Write-Host "💬 対話モードで起動中..." -ForegroundColor Yellow
        Write-Host ""
        python $pythonFile
    }
} catch {
    Write-Host "❌ 実行エラー: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " ✅ プロンプト生成が完了しました" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
