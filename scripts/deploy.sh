#!/bin/bash

# ============================================
# ShiftMaster デプロイメントスクリプト
# VPS環境への自動デプロイと設定
# ============================================

set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 設定
DEPLOY_DIR="/opt/shiftmaster"
SERVICE_USER="shiftmaster"
NGINX_CONF_DIR="/etc/nginx/sites-available"
SYSTEMD_DIR="/etc/systemd/system"
LOG_DIR="/var/log/shiftmaster"

function print_help() {
    echo -e "${GREEN}🚀 ShiftMaster デプロイメントスクリプト${NC}"
    echo "======================================="
    echo ""
    echo -e "${BLUE}使用方法:${NC}"
    echo "  ./scripts/deploy.sh <action> [options]"
    echo ""
    echo -e "${BLUE}アクション:${NC}"
    echo "  install     - 初回インストール"
    echo "  update      - アプリケーション更新"
    echo "  rollback    - 前バージョンにロールバック"
    echo "  status      - サービス状態確認"
    echo "  logs        - ログ表示"
    echo "  restart     - サービス再起動"
    echo "  backup      - デプロイ前バックアップ"
    echo "  help        - ヘルプ表示"
    echo ""
    echo -e "${BLUE}オプション:${NC}"
    echo "  -d DOMAIN   - ドメイン名"
    echo "  -e EMAIL    - 管理者メールアドレス"
    echo "  -b BRANCH   - デプロイ対象ブランチ（デフォルト: main）"
    echo "  --no-ssl    - SSL証明書設定をスキップ"
    echo ""
    echo -e "${YELLOW}使用例:${NC}"
    echo "  ./scripts/deploy.sh install -d example.com -e admin@example.com"
    echo "  ./scripts/deploy.sh update"
    echo "  ./scripts/deploy.sh rollback"
}

function log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        "ERROR")
            echo -e "${RED}❌ [$timestamp] $message${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}⚠️ [$timestamp] $message${NC}"
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️ [$timestamp] $message${NC}"
            ;;
        "SUCCESS")
            echo -e "${GREEN}✅ [$timestamp] $message${NC}"
            ;;
        "STEP")
            echo -e "${CYAN}🔄 [$timestamp] $message${NC}"
            ;;
    esac
    
    # ログファイルにも記録
    if [ -d "$LOG_DIR" ]; then
        echo "[$timestamp] [$level] $message" >> "$LOG_DIR/deploy.log"
    fi
}

function check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_message "ERROR" "このスクリプトはroot権限で実行してください"
        exit 1
    fi
}

function check_requirements() {
    log_message "STEP" "システム要件チェック中..."
    
    # Docker確認
    if ! command -v docker &> /dev/null; then
        log_message "ERROR" "Dockerがインストールされていません"
        exit 1
    fi
    
    # Docker Compose確認
    if ! command -v docker-compose &> /dev/null; then
        log_message "ERROR" "Docker Composeがインストールされていません"
        exit 1
    fi
    
    # Git確認
    if ! command -v git &> /dev/null; then
        log_message "ERROR" "Gitがインストールされていません"
        exit 1
    fi
    
    log_message "SUCCESS" "システム要件チェック完了"
}

function create_system_user() {
    log_message "STEP" "システムユーザー作成中..."
    
    if ! id "$SERVICE_USER" &>/dev/null; then
        useradd -r -s /bin/bash -d "$DEPLOY_DIR" -m "$SERVICE_USER"
        usermod -aG docker "$SERVICE_USER"
        log_message "SUCCESS" "ユーザー '$SERVICE_USER' を作成しました"
    else
        log_message "INFO" "ユーザー '$SERVICE_USER' は既に存在します"
    fi
    
    # ディレクトリ作成
    mkdir -p "$DEPLOY_DIR"
    mkdir -p "$LOG_DIR"
    chown -R "$SERVICE_USER:$SERVICE_USER" "$DEPLOY_DIR"
    chown -R "$SERVICE_USER:$SERVICE_USER" "$LOG_DIR"
}

function install_system_dependencies() {
    log_message "STEP" "システム依存関係インストール中..."
    
    # パッケージ更新
    apt-get update
    
    # 必要パッケージインストール
    apt-get install -y \
        curl \
        wget \
        unzip \
        nginx \
        certbot \
        python3-certbot-nginx \
        postgresql-client \
        redis-tools \
        htop \
        fail2ban \
        ufw
    
    log_message "SUCCESS" "システム依存関係インストール完了"
}

function setup_firewall() {
    log_message "STEP" "ファイアウォール設定中..."
    
    # UFW設定
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    
    # 必要ポート開放
    ufw allow ssh
    ufw allow http
    ufw allow https
    
    # SSH設定強化
    sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
    systemctl restart ssh
    
    # ファイアウォール有効化
    ufw --force enable
    
    log_message "SUCCESS" "ファイアウォール設定完了"
}

function clone_repository() {
    local branch="${1:-main}"
    
    log_message "STEP" "リポジトリクローン中 (ブランチ: $branch)..."
    
    if [ -d "$DEPLOY_DIR/.git" ]; then
        cd "$DEPLOY_DIR"
        sudo -u "$SERVICE_USER" git fetch origin
        sudo -u "$SERVICE_USER" git checkout "$branch"
        sudo -u "$SERVICE_USER" git pull origin "$branch"
        log_message "SUCCESS" "リポジトリ更新完了"
    else
        sudo -u "$SERVICE_USER" git clone https://github.com/your-username/ShiftMaster.git "$DEPLOY_DIR"
        cd "$DEPLOY_DIR"
        sudo -u "$SERVICE_USER" git checkout "$branch"
        log_message "SUCCESS" "リポジトリクローン完了"
    fi
}

function setup_environment() {
    log_message "STEP" "環境設定ファイル作成中..."
    
    # .envファイル作成
    if [ ! -f "$DEPLOY_DIR/.env" ]; then
        cat > "$DEPLOY_DIR/.env" << EOF
# Django設定
DJANGO_SECRET_KEY=$(openssl rand -base64 32)
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=$DOMAIN,localhost,127.0.0.1

# データベース設定
POSTGRES_DB=shiftmaster
POSTGRES_USER=shiftmaster_user
POSTGRES_PASSWORD=$(openssl rand -base64 24)
DATABASE_URL=postgresql://shiftmaster_user:$(openssl rand -base64 24)@db:5432/shiftmaster

# Redis設定
REDIS_URL=redis://redis:6379/0

# メール設定
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=$EMAIL
EMAIL_HOST_PASSWORD=your_app_password

# セキュリティ設定
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# 医療データ設定
MEDICAL_DATA_ENCRYPTION_KEY=$(openssl rand -base64 32)
AUDIT_LOG_ENABLED=True
SESSION_TIMEOUT=3600

EOF
        chown "$SERVICE_USER:$SERVICE_USER" "$DEPLOY_DIR/.env"
        chmod 600 "$DEPLOY_DIR/.env"
        log_message "SUCCESS" "環境設定ファイル作成完了"
    else
        log_message "INFO" ".envファイルは既に存在します"
    fi
}

function build_and_start_services() {
    log_message "STEP" "Dockerサービス構築・起動中..."
    
    cd "$DEPLOY_DIR"
    
    # イメージビルド
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml build
    
    # サービス起動
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml up -d
    
    # 起動待機
    log_message "INFO" "サービス起動待機中..."
    sleep 30
    
    # データベースマイグレーション
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate
    
    # 静的ファイル収集
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
    
    # スーパーユーザー作成（対話式）
    echo -e "${YELLOW}Django管理者ユーザーを作成してください:${NC}"
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
    
    log_message "SUCCESS" "Dockerサービス起動完了"
}

function setup_ssl_certificate() {
    if [ "$SKIP_SSL" = "true" ]; then
        log_message "INFO" "SSL証明書設定をスキップしました"
        return 0
    fi
    
    log_message "STEP" "SSL証明書設定中..."
    
    # Let's Encrypt証明書取得
    if certbot --nginx -d "$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive; then
        log_message "SUCCESS" "SSL証明書設定完了"
    else
        log_message "WARNING" "SSL証明書の自動設定に失敗しました"
        log_message "INFO" "手動で設定してください: certbot --nginx -d $DOMAIN"
    fi
}

function setup_systemd_service() {
    log_message "STEP" "systemdサービス設定中..."
    
    cat > "$SYSTEMD_DIR/shiftmaster.service" << EOF
[Unit]
Description=ShiftMaster Medical Shift Management System
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$DEPLOY_DIR
User=$SERVICE_USER
Group=$SERVICE_USER
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable shiftmaster.service
    log_message "SUCCESS" "systemdサービス設定完了"
}

function setup_log_rotation() {
    log_message "STEP" "ログローテーション設定中..."
    
    cat > "/etc/logrotate.d/shiftmaster" << EOF
$LOG_DIR/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_USER
    postrotate
        systemctl reload shiftmaster 2> /dev/null || true
    endscript
}
EOF
    
    log_message "SUCCESS" "ログローテーション設定完了"
}

function create_backup_version() {
    if [ -d "$DEPLOY_DIR" ]; then
        local backup_dir="$DEPLOY_DIR.backup.$(date +%Y%m%d_%H%M%S)"
        log_message "STEP" "現在のバージョンをバックアップ中..."
        cp -r "$DEPLOY_DIR" "$backup_dir"
        log_message "SUCCESS" "バックアップ作成: $backup_dir"
    fi
}

function update_application() {
    local branch="${1:-main}"
    
    log_message "STEP" "アプリケーション更新開始"
    
    # バックアップ作成
    create_backup_version
    
    # コード更新
    clone_repository "$branch"
    
    # サービス停止
    cd "$DEPLOY_DIR"
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml down
    
    # イメージ再ビルド
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml build --no-cache
    
    # サービス再起動
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml up -d
    
    # マイグレーション実行
    sleep 20
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
    
    log_message "SUCCESS" "アプリケーション更新完了"
}

function rollback_application() {
    log_message "STEP" "ロールバック実行中..."
    
    # 最新のバックアップディレクトリ検索
    local backup_dir=$(ls -td "$DEPLOY_DIR".backup.* 2>/dev/null | head -n1)
    
    if [ -z "$backup_dir" ]; then
        log_message "ERROR" "バックアップディレクトリが見つかりません"
        exit 1
    fi
    
    log_message "INFO" "ロールバック先: $backup_dir"
    
    # 現在のサービス停止
    cd "$DEPLOY_DIR"
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml down
    
    # ディレクトリ入れ替え
    mv "$DEPLOY_DIR" "$DEPLOY_DIR.failed.$(date +%Y%m%d_%H%M%S)"
    mv "$backup_dir" "$DEPLOY_DIR"
    
    # サービス再起動
    cd "$DEPLOY_DIR"
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml up -d
    
    log_message "SUCCESS" "ロールバック完了"
}

function show_service_status() {
    log_message "INFO" "サービス状態確認"
    
    echo -e "${BLUE}=== Docker Compose Services ===${NC}"
    cd "$DEPLOY_DIR"
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml ps
    
    echo -e "\n${BLUE}=== System Service ===${NC}"
    systemctl status shiftmaster.service --no-pager
    
    echo -e "\n${BLUE}=== Nginx Status ===${NC}"
    systemctl status nginx --no-pager
    
    echo -e "\n${BLUE}=== Access URLs ===${NC}"
    echo "  アプリケーション: https://$DOMAIN"
    echo "  管理画面: https://$DOMAIN/admin/"
}

function show_logs() {
    local service="$1"
    
    if [ -n "$service" ]; then
        log_message "INFO" "ログ表示: $service"
        cd "$DEPLOY_DIR"
        sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml logs -f "$service"
    else
        log_message "INFO" "全サービスログ表示"
        cd "$DEPLOY_DIR"
        sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml logs -f
    fi
}

function restart_services() {
    log_message "STEP" "サービス再起動中..."
    
    cd "$DEPLOY_DIR"
    sudo -u "$SERVICE_USER" docker-compose -f docker-compose.prod.yml restart
    
    log_message "SUCCESS" "サービス再起動完了"
}

# 引数解析
ACTION=""
DOMAIN=""
EMAIL=""
BRANCH="main"
SKIP_SSL="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        install|update|rollback|status|logs|restart|backup|help)
            ACTION="$1"
            ;;
        -d|--domain)
            DOMAIN="$2"
            shift
            ;;
        -e|--email)
            EMAIL="$2"
            shift
            ;;
        -b|--branch)
            BRANCH="$2"
            shift
            ;;
        --no-ssl)
            SKIP_SSL="true"
            ;;
        *)
            log_message "ERROR" "不明なオプション: $1"
            print_help
            exit 1
            ;;
    esac
    shift
done

# 権限チェック
check_root

# アクション実行
case $ACTION in
    install)
        if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
            log_message "ERROR" "ドメイン名とメールアドレスを指定してください"
            print_help
            exit 1
        fi
        
        log_message "SUCCESS" "ShiftMaster初回インストール開始"
        check_requirements
        create_system_user
        install_system_dependencies
        setup_firewall
        clone_repository "$BRANCH"
        setup_environment
        build_and_start_services
        setup_ssl_certificate
        setup_systemd_service
        setup_log_rotation
        log_message "SUCCESS" "ShiftMaster初回インストール完了"
        show_service_status
        ;;
    update)
        update_application "$BRANCH"
        ;;
    rollback)
        rollback_application
        ;;
    status)
        show_service_status
        ;;
    logs)
        show_logs "$2"
        ;;
    restart)
        restart_services
        ;;
    backup)
        create_backup_version
        ;;
    help)
        print_help
        ;;
    *)
        print_help
        ;;
esac
