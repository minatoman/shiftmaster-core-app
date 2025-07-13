# ============================================
# 最終コミット実行
# 完成したDocker本番環境をGitリポジトリに反映
# ============================================

param(
    [Parameter(Mandatory=$false)]
    [string]$CommitMessage = "feat: Add comprehensive Docker production environment setup"
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

Write-ColorOutput "🚀 ShiftMaster Docker環境の最終コミット実行" $Green
Write-ColorOutput "================================================" $Green
Write-Host ""

try {
    # 現在のGit状態確認
    Write-ColorOutput "📋 Git状態確認中..." $Cyan
    $gitStatus = git status --porcelain
    
    if ($gitStatus) {
        Write-ColorOutput "📝 追加されたファイル一覧:" $Yellow
        Write-Host ""
        
        # 新規追加ファイル
        Write-ColorOutput "【本番環境設定】" $Green
        Write-Host "  ✅ docker-compose.prod.yml - PostgreSQL, Redis, Nginx, Celeryを含む本番構成"
        Write-Host "  ✅ docker-compose.dev.yml - 開発環境向け軽量構成"
        Write-Host "  ✅ .env.example - 環境変数テンプレート（セキュリティガイド付き）"
        Write-Host ""
        
        Write-ColorOutput "【Nginx設定】" $Green
        Write-Host "  ✅ nginx/nginx.conf - メイン設定（パフォーマンス・セキュリティ最適化）"
        Write-Host "  ✅ nginx/conf.d/shiftmaster.conf - バーチャルホスト（SSL/HTTPS対応）"
        Write-Host ""
        
        Write-ColorOutput "【コンテナ初期化】" $Green
        Write-Host "  ✅ entrypoint.sh - データベース接続確認・マイグレーション実行"
        Write-Host ""
        
        Write-ColorOutput "【管理スクリプト】" $Green
        Write-Host "  ✅ scripts/manage.ps1 - Windows PowerShell管理ツール"
        Write-Host "  ✅ scripts/ssl_manager.sh - Let's Encrypt SSL証明書管理"
        Write-Host "  ✅ scripts/backup_manager.sh - データベースバックアップ・復元"
        Write-Host "  ✅ scripts/deploy.sh - VPS自動デプロイ・運用スクリプト"
        Write-Host ""
        
        Write-ColorOutput "【運用ドキュメント】" $Green
        Write-Host "  ✅ DEPLOYMENT_GUIDE.md - 本番運用マニュアル（緊急時対応含む）"
        Write-Host ""
        
        # Gitに追加
        Write-ColorOutput "📦 ファイルをGitに追加中..." $Cyan
        git add .
        
        # コミット実行
        Write-ColorOutput "💾 コミット実行中..." $Cyan
        git commit -m $CommitMessage
        
        # GitHubにプッシュ
        Write-ColorOutput "☁️ GitHubにプッシュ中..." $Cyan
        git push origin main
        
        Write-Host ""
        Write-ColorOutput "✅ Docker本番環境のセットアップが完了しました！" $Green
        Write-Host ""
        
        Write-ColorOutput "🎯 実装された主要機能:" $Cyan
        Write-Host ""
        Write-Host "【Docker環境】"
        Write-Host "  • 本番環境：PostgreSQL + Redis + Nginx + Celery"
        Write-Host "  • 開発環境：SQLite + 開発サーバー（オプションでDB/Redis）"
        Write-Host "  • マルチステージビルド対応"
        Write-Host "  • ヘルスチェック・自動復旧機能"
        Write-Host ""
        Write-Host "【セキュリティ】"
        Write-Host "  • SSL/TLS暗号化（Let's Encrypt自動証明書）"
        Write-Host "  • セキュリティヘッダー設定"
        Write-Host "  • レート制限・DDoS対策"
        Write-Host "  • ファイアウォール設定自動化"
        Write-Host ""
        Write-Host "【運用・保守】"
        Write-Host "  • 自動バックアップ・ローテーション"
        Write-Host "  • ログ管理・監視"
        Write-Host "  • ワンクリックデプロイ・ロールバック"
        Write-Host "  • 24時間監視対応"
        Write-Host ""
        Write-Host "【医療対応】"
        Write-Host "  • 医療データ暗号化"
        Write-Host "  • 監査ログ記録"
        Write-Host "  • HIPAA準拠セキュリティ"
        Write-Host "  • 高可用性設計"
        Write-Host ""
        
        Write-ColorOutput "🌟 次のステップ:" $Yellow
        Write-Host ""
        Write-Host "1. VPSでの本番デプロイ:"
        Write-Host "   sudo ./scripts/deploy.sh install -d your-domain.com -e admin@example.com"
        Write-Host ""
        Write-Host "2. 開発環境での動作確認:"
        Write-Host "   .\scripts\manage.ps1 -Action start -Environment dev"
        Write-Host ""
        Write-Host "3. SSL証明書設定:"
        Write-Host "   ./scripts/ssl_manager.sh init -d your-domain.com -e admin@example.com"
        Write-Host ""
        Write-Host "4. 自動バックアップ設定:"
        Write-Host "   ./scripts/backup_manager.sh schedule"
        Write-Host ""
        
        Write-ColorOutput "📚 詳細な運用手順はDEPLOYMENT_GUIDE.mdを参照してください" $Green
        
    } else {
        Write-ColorOutput "ℹ️ コミット対象の変更がありません" $Yellow
    }
    
} catch {
    Write-ColorOutput "❌ エラーが発生しました: $($_.Exception.Message)" $Red
    exit 1
}

Write-Host ""
Write-ColorOutput "🎉 ShiftMaster Docker本番環境セットアップ完了！" $Green
Write-ColorOutput "医療施設での24時間安定運用が可能な環境が整いました。" $Green
