# ShiftMaster 統合実行スクリプト
# プロンプト生成器と自動管理機能を統合

param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "menu",
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# 文字エンコーディング設定
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Show-MainMenu {
    Clear-Host
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host " 🚀 ShiftMaster 統合管理システム v2.0" -ForegroundColor Yellow
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📝 プロンプト生成器:" -ForegroundColor Green
    Write-Host "   1. 新しいプロンプトを生成" -ForegroundColor White
    Write-Host "   2. 対話モードで起動" -ForegroundColor White
    Write-Host "   3. プロンプト履歴を表示" -ForegroundColor White
    Write-Host "   4. 統計情報を表示" -ForegroundColor White
    Write-Host ""
    Write-Host "🤖 自動管理機能:" -ForegroundColor Green
    Write-Host "   5. システム状態をチェック" -ForegroundColor White
    Write-Host "   6. 問題を自動修正" -ForegroundColor White
    Write-Host "   7. 自動監視を開始" -ForegroundColor White
    Write-Host ""
    Write-Host "⚙️  その他:" -ForegroundColor Green
    Write-Host "   8. 設定をエクスポート" -ForegroundColor White
    Write-Host "   9. ヘルプを表示" -ForegroundColor White
    Write-Host "   0. 終了" -ForegroundColor White
    Write-Host ""
    Write-Host "-" * 70 -ForegroundColor Gray
}

function Invoke-PromptGenerator {
    param([string]$Command, [string[]]$Args)
    
    $pythonFile = Join-Path $PSScriptRoot "Get_ChildItem.py"
    
    if ($Command -and $Args) {
        python $pythonFile $Command @Args
    } elseif ($Command) {
        python $pythonFile $Command
    } else {
        python $pythonFile
    }
}

function Invoke-AutoManager {
    param([string]$Command, [string[]]$Args)
    
    $pythonFile = Join-Path $PSScriptRoot "auto_manager.py"
    
    if ($Command -and $Args) {
        python $pythonFile $Command @Args
    } elseif ($Command) {
        python $pythonFile $Command
    } else {
        python $pythonFile
    }
}

function Get-UserInput {
    param([string]$Prompt)
    return Read-Host $Prompt
}

# メイン処理
switch ($Action.ToLower()) {
    "menu" {
        do {
            Show-MainMenu
            $choice = Get-UserInput "選択してください (0-9)"
            
            switch ($choice) {
                "1" {
                    Write-Host "📝 新しいプロンプトを生成します" -ForegroundColor Yellow
                    $userInput = Get-UserInput "GitHub Copilot Agentへの質問・指示を入力してください"
                    if ($userInput) {
                        Invoke-PromptGenerator $userInput
                    }
                    Read-Host "Enterキーで続行..."
                }
                "2" {
                    Write-Host "💬 対話モードで起動します" -ForegroundColor Yellow
                    Invoke-PromptGenerator
                }
                "3" {
                    Write-Host "📋 プロンプト履歴を表示します" -ForegroundColor Yellow
                    $count = Get-UserInput "表示件数 (デフォルト10)"
                    if (-not $count) { $count = "10" }
                    Invoke-PromptGenerator "--history" $count
                    Read-Host "Enterキーで続行..."
                }
                "4" {
                    Write-Host "📊 統計情報を表示します" -ForegroundColor Yellow
                    Invoke-PromptGenerator "--stats"
                    Read-Host "Enterキーで続行..."
                }
                "5" {
                    Write-Host "🔍 システム状態をチェックします" -ForegroundColor Yellow
                    Invoke-AutoManager "check"
                    Read-Host "Enterキーで続行..."
                }
                "6" {
                    Write-Host "🔧 問題を自動修正します" -ForegroundColor Yellow
                    Invoke-AutoManager "fix"
                    Read-Host "Enterキーで続行..."
                }
                "7" {
                    Write-Host "🤖 自動監視を開始します" -ForegroundColor Yellow
                    $interval = Get-UserInput "監視間隔（秒、デフォルト300）"
                    if (-not $interval) { $interval = "300" }
                    Invoke-AutoManager "monitor" $interval
                }
                "8" {
                    Write-Host "📤 設定をエクスポートします" -ForegroundColor Yellow
                    Invoke-PromptGenerator "--export"
                    Read-Host "Enterキーで続行..."
                }
                "9" {
                    Write-Host "📖 ヘルプを表示します" -ForegroundColor Yellow
                    Invoke-PromptGenerator "--help"
                    Write-Host ""
                    Invoke-AutoManager
                    Read-Host "Enterキーで続行..."
                }
                "0" {
                    Write-Host "👋 ShiftMaster統合管理システムを終了します" -ForegroundColor Green
                    exit 0
                }
                default {
                    Write-Host "⚠️  無効な選択です。0-9の数字を入力してください。" -ForegroundColor Red
                    Start-Sleep 2
                }
            }
        } while ($true)
    }
    "prompt" {
        if ($Arguments) {
            Invoke-PromptGenerator ($Arguments -join " ")
        } else {
            Invoke-PromptGenerator
        }
    }
    "auto" {
        if ($Arguments) {
            Invoke-AutoManager $Arguments[0] $Arguments[1..($Arguments.Length-1)]
        } else {
            Invoke-AutoManager
        }
    }
    "check" {
        Invoke-AutoManager "check"
    }
    "fix" {
        Invoke-AutoManager "fix"
    }
    "monitor" {
        $interval = if ($Arguments) { $Arguments[0] } else { "300" }
        Invoke-AutoManager "monitor" $interval
    }
    default {
        Write-Host "🚀 ShiftMaster 統合管理システム" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "使用方法:" -ForegroundColor Green
        Write-Host "  .\ShiftMaster.ps1                    # メニューモード"
        Write-Host "  .\ShiftMaster.ps1 prompt `"質問`"      # プロンプト生成"
        Write-Host "  .\ShiftMaster.ps1 check              # システムチェック"
        Write-Host "  .\ShiftMaster.ps1 fix                # 自動修正"
        Write-Host "  .\ShiftMaster.ps1 monitor [間隔]      # 自動監視"
        Write-Host ""
    }
}
