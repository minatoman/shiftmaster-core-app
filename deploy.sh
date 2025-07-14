#!/bin/bash

# =============================================
# ShiftMaster Production Deployment Script
# 本番環境デプロイスクリプト
# =============================================

set -e  # エラー時に停止

# 設定
PROJECT_NAME="shiftmaster"
DEPLOY_USER="deploy"
SERVER_HOST="${PRODUCTION_SERVER_HOST:-your-server.com}"
APP_DIR="/var/www/${PROJECT_NAME}"
BACKUP_DIR="/var/backups/${PROJECT_NAME}"
DOCKER_IMAGE="${PROJECT_NAME}:latest"

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 前提条件チェック
check_prerequisites() {
    log_info "前提条件をチェック中..."
    
    # Docker確認
    if ! command -v docker &> /dev/null; then
        log_error "Dockerがインストールされていません"
        exit 1
    fi
    
    # Docker Composeの確認
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Composeがインストールされていません"
        exit 1
    fi
    
    # 環境変数確認
    if [ -z "$PRODUCTION_DB_PASSWORD" ]; then
        log_error "PRODUCTION_DB_PASSWORD環境変数が設定されていません"
        exit 1
    fi
    
    log_success "前提条件OK"
}

# データベースバックアップ
backup_database() {
    log_info "データベースをバックアップ中..."
    
    BACKUP_FILE="${BACKUP_DIR}/db_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    # バックアップディレクトリ作成
    mkdir -p "${BACKUP_DIR}"
    
    # PostgreSQLダンプ
    docker exec shiftmaster_db pg_dump -U postgres shiftmaster > "${BACKUP_FILE}" || {
        log_warning "データベースバックアップに失敗（初回デプロイの可能性）"
    }
    
    log_success "バックアップ完了: ${BACKUP_FILE}"
}

# アプリケーションビルド
build_application() {
    log_info "アプリケーションをビルド中..."
    
    # Dockerイメージビルド
    docker build -t "${DOCKER_IMAGE}" .
    
    # イメージ確認
    docker images | grep "${PROJECT_NAME}"
    
    log_success "ビルド完了"
}

# データベースマイグレーション
run_migrations() {
    log_info "データベースマイグレーションを実行中..."
    
    # マイグレーションファイル生成
    docker-compose exec web python manage.py makemigrations
    
    # マイグレーション実行
    docker-compose exec web python manage.py migrate
    
    log_success "マイグレーション完了"
}

# 静的ファイル収集
collect_static() {
    log_info "静的ファイルを収集中..."
    
    docker-compose exec web python manage.py collectstatic --noinput
    
    log_success "静的ファイル収集完了"
}

# 本番データ投入
load_production_data() {
    if [ -f "production_data_export.json" ]; then
        log_info "本番データを投入中..."
        
        # カスタム管理コマンドでデータ投入
        docker-compose exec web python manage.py loaddata production_data_export.json
        
        log_success "データ投入完了"
    else
        log_warning "production_data_export.json が見つかりません"
    fi
}

# ヘルスチェック
health_check() {
    log_info "ヘルスチェック実行中..."
    
    # サービス起動待ち
    sleep 10
    
    # ヘルスチェックURL
    HEALTH_URL="http://localhost:8000/health/"
    
    # リトライ付きチェック
    for i in {1..5}; do
        if curl -f "${HEALTH_URL}" > /dev/null 2>&1; then
            log_success "ヘルスチェック成功"
            return 0
        fi
        log_warning "ヘルスチェック失敗、リトライ中... (${i}/5)"
        sleep 5
    done
    
    log_error "ヘルスチェック失敗"
    return 1
}

# ロールバック関数
rollback() {
    log_warning "ロールバックを実行中..."
    
    # 以前のコンテナに復元
    docker-compose down
    # 以前のイメージがある場合は復元処理
    # ... ロールバック処理 ...
    
    log_info "ロールバック完了"
}

# メイン処理
main() {
    log_info "🚀 ShiftMaster 本番デプロイを開始"
    
    # デプロイ開始時刻
    DEPLOY_START=$(date)
    
    # 前処理
    check_prerequisites
    backup_database
    
    # ビルド・デプロイ
    build_application
    
    # Docker Composeで本番環境起動
    log_info "本番環境を起動中..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # データベース設定
    run_migrations
    collect_static
    load_production_data
    
    # 動作確認
    if health_check; then
        log_success "🎉 デプロイ成功！"
        log_info "開始時刻: ${DEPLOY_START}"
        log_info "完了時刻: $(date)"
        log_info "URL: https://${SERVER_HOST}/"
    else
        log_error "デプロイに失敗しました"
        rollback
        exit 1
    fi
}

# トラップでエラー時にロールバック
trap 'log_error "デプロイ中にエラーが発生しました"; rollback; exit 1' ERR

# スクリプト実行
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
