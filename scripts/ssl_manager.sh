#!/bin/bash

# ============================================
# SSL証明書管理スクリプト
# Let's Encrypt証明書の取得・更新・管理
# ============================================

set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 設定
DOMAIN=""
EMAIL=""
COMPOSE_FILE="docker-compose.prod.yml"
NGINX_CONTAINER="shiftmaster_nginx"
CERTBOT_CONTAINER="shiftmaster_certbot"

function print_help() {
    echo -e "${GREEN}🔐 SSL証明書管理スクリプト${NC}"
    echo "================================"
    echo ""
    echo -e "${BLUE}使用方法:${NC}"
    echo "  ./scripts/ssl_manager.sh <action> [options]"
    echo ""
    echo -e "${BLUE}アクション:${NC}"
    echo "  init        - 初回証明書取得"
    echo "  renew       - 証明書更新"
    echo "  status      - 証明書状態確認"
    echo "  setup       - 証明書管理環境セットアップ"
    echo "  help        - ヘルプ表示"
    echo ""
    echo -e "${BLUE}オプション:${NC}"
    echo "  -d DOMAIN   - ドメイン名"
    echo "  -e EMAIL    - メールアドレス"
    echo ""
    echo -e "${YELLOW}使用例:${NC}"
    echo "  ./scripts/ssl_manager.sh init -d example.com -e admin@example.com"
    echo "  ./scripts/ssl_manager.sh renew"
    echo "  ./scripts/ssl_manager.sh status"
}

function check_requirements() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Dockerがインストールされていません${NC}"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Composeがインストールされていません${NC}"
        exit 1
    fi
}

function setup_certbot_environment() {
    echo -e "${YELLOW}🔧 証明書管理環境セットアップ中...${NC}"
    
    # 必要なディレクトリ作成
    mkdir -p ./ssl/certbot/conf
    mkdir -p ./ssl/certbot/www
    mkdir -p ./ssl/dhparam
    
    # DH パラメータ生成（存在しない場合）
    if [ ! -f "./ssl/dhparam/dhparam.pem" ]; then
        echo -e "${YELLOW}🔐 DHパラメータ生成中（時間がかかります）...${NC}"
        openssl dhparam -out ./ssl/dhparam/dhparam.pem 2048
    fi
    
    # Certbot設定ファイル作成
    cat > ./ssl/certbot/conf/cli.ini << EOF
# Certbot設定ファイル
email = ${EMAIL}
agree-tos = true
no-eff-email = true
rsa-key-size = 4096
authenticator = webroot
webroot-path = /var/www/certbot
EOF
    
    echo -e "${GREEN}✅ 証明書管理環境セットアップ完了${NC}"
}

function create_temp_certificate() {
    echo -e "${YELLOW}🔧 一時証明書作成中...${NC}"
    
    mkdir -p ./ssl/certbot/conf/live/${DOMAIN}
    
    # 一時的な自己署名証明書作成
    openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
        -keyout ./ssl/certbot/conf/live/${DOMAIN}/privkey.pem \
        -out ./ssl/certbot/conf/live/${DOMAIN}/fullchain.pem \
        -subj "/CN=${DOMAIN}"
    
    echo -e "${GREEN}✅ 一時証明書作成完了${NC}"
}

function init_certificate() {
    if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
        echo -e "${RED}❌ ドメイン名とメールアドレスを指定してください${NC}"
        echo "使用方法: $0 init -d example.com -e admin@example.com"
        exit 1
    fi
    
    echo -e "${GREEN}🔐 SSL証明書初期設定開始${NC}"
    echo "ドメイン: $DOMAIN"
    echo "メール: $EMAIL"
    echo ""
    
    # 環境セットアップ
    setup_certbot_environment
    
    # 一時証明書作成
    create_temp_certificate
    
    # Nginxコンテナ起動
    echo -e "${YELLOW}🌐 Nginxコンテナ起動中...${NC}"
    docker-compose -f $COMPOSE_FILE up -d nginx
    
    # Let's Encrypt証明書取得
    echo -e "${YELLOW}🔐 Let's Encrypt証明書取得中...${NC}"
    docker-compose -f $COMPOSE_FILE run --rm certbot \
        certonly --webroot \
        --webroot-path=/var/www/certbot \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        --force-renewal \
        -d $DOMAIN
    
    # Nginx再起動
    echo -e "${YELLOW}🔄 Nginx再起動中...${NC}"
    docker-compose -f $COMPOSE_FILE exec nginx nginx -s reload
    
    echo -e "${GREEN}✅ SSL証明書初期設定完了${NC}"
    echo -e "${BLUE}ℹ️ 証明書は90日ごとに更新が必要です${NC}"
    echo -e "${BLUE}ℹ️ 自動更新のためにcronジョブを設定することを推奨します${NC}"
}

function renew_certificate() {
    echo -e "${YELLOW}🔄 SSL証明書更新中...${NC}"
    
    # 証明書更新
    docker-compose -f $COMPOSE_FILE run --rm certbot renew
    
    # Nginx設定リロード
    docker-compose -f $COMPOSE_FILE exec nginx nginx -s reload
    
    echo -e "${GREEN}✅ SSL証明書更新完了${NC}"
}

function check_certificate_status() {
    echo -e "${BLUE}📋 SSL証明書状態確認${NC}"
    echo "================================"
    
    if [ -d "./ssl/certbot/conf/live" ]; then
        for cert_dir in ./ssl/certbot/conf/live/*/; do
            if [ -d "$cert_dir" ]; then
                domain=$(basename "$cert_dir")
                echo -e "${YELLOW}ドメイン: $domain${NC}"
                
                if [ -f "$cert_dir/fullchain.pem" ]; then
                    # 証明書有効期限チェック
                    expiry_date=$(openssl x509 -enddate -noout -in "$cert_dir/fullchain.pem" | cut -d= -f2)
                    echo "  有効期限: $expiry_date"
                    
                    # 残り日数計算
                    expiry_timestamp=$(date -d "$expiry_date" +%s)
                    current_timestamp=$(date +%s)
                    days_left=$(( (expiry_timestamp - current_timestamp) / 86400 ))
                    
                    if [ $days_left -lt 30 ]; then
                        echo -e "  ${RED}⚠️ 残り${days_left}日（更新推奨）${NC}"
                    elif [ $days_left -lt 7 ]; then
                        echo -e "  ${RED}❌ 残り${days_left}日（緊急更新必要）${NC}"
                    else
                        echo -e "  ${GREEN}✅ 残り${days_left}日${NC}"
                    fi
                    
                    # 証明書詳細
                    echo "  発行者: $(openssl x509 -issuer -noout -in "$cert_dir/fullchain.pem" | cut -d= -f2-)"
                    echo "  サブジェクト: $(openssl x509 -subject -noout -in "$cert_dir/fullchain.pem" | cut -d= -f2-)"
                else
                    echo -e "  ${RED}❌ 証明書ファイルが見つかりません${NC}"
                fi
                echo ""
            fi
        done
    else
        echo -e "${YELLOW}⚠️ 証明書ディレクトリが見つかりません${NC}"
        echo "初回証明書取得を実行してください: $0 init -d <domain> -e <email>"
    fi
}

function create_cron_job() {
    echo -e "${YELLOW}⏰ 自動更新cron設定${NC}"
    echo "以下のcronジョブを追加してください："
    echo ""
    echo -e "${BLUE}# SSL証明書自動更新（毎日午前3時）${NC}"
    echo "0 3 * * * cd $(pwd) && ./scripts/ssl_manager.sh renew >> ./logs/ssl_renewal.log 2>&1"
    echo ""
    echo "設定方法:"
    echo "  crontab -e"
    echo "  上記の行を追加して保存"
}

# 引数解析
while [[ $# -gt 0 ]]; do
    case $1 in
        init|renew|status|setup|help)
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
        *)
            echo -e "${RED}❌ 不明なオプション: $1${NC}"
            print_help
            exit 1
            ;;
    esac
    shift
done

# 事前チェック
check_requirements

# アクション実行
case $ACTION in
    init)
        init_certificate
        ;;
    renew)
        renew_certificate
        ;;
    status)
        check_certificate_status
        ;;
    setup)
        if [ -z "$EMAIL" ]; then
            read -p "メールアドレスを入力してください: " EMAIL
        fi
        setup_certbot_environment
        create_cron_job
        ;;
    help)
        print_help
        ;;
    *)
        print_help
        ;;
esac
