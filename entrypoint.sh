#!/bin/bash
# ============================================
# ShiftMaster Docker エントリーポイント
# 起動時の初期化処理
# ============================================

set -e  # エラー時は即座に終了

# カラー出力設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🏥 ShiftMaster 起動中...${NC}"

# 環境変数確認
echo -e "${YELLOW}📋 環境変数確認...${NC}"
echo "DEBUG: ${DEBUG:-Not set}"
echo "DATABASE_URL: ${DATABASE_URL:-Not set}"
echo "ALLOWED_HOSTS: ${ALLOWED_HOSTS:-Not set}"

# データベース接続待機
echo -e "${YELLOW}🗃️ データベース接続待機...${NC}"
if [ -n "$DATABASE_URL" ]; then
    # PostgreSQL接続確認
    python << END
import os
import sys
import psycopg2
from urllib.parse import urlparse
import time

url = urlparse('${DATABASE_URL}')
max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port or 5432,
            user=url.username,
            password=url.password,
            database=url.path[1:]
        )
        conn.close()
        print("✅ データベース接続成功")
        break
    except psycopg2.OperationalError:
        retry_count += 1
        print(f"⏳ データベース接続待機中... ({retry_count}/{max_retries})")
        time.sleep(2)
else:
    print("❌ データベース接続失敗")
    sys.exit(1)
END
else
    echo "ℹ️ SQLite使用 - データベース接続チェックをスキップ"
fi

# Redis接続確認（オプション）
if [ -n "$REDIS_URL" ]; then
    echo -e "${YELLOW}📦 Redis接続確認...${NC}"
    python << END
import redis
from urllib.parse import urlparse
import time

url = urlparse('${REDIS_URL}')
max_retries = 10
retry_count = 0

while retry_count < max_retries:
    try:
        r = redis.Redis(
            host=url.hostname,
            port=url.port or 6379,
            password=url.password,
            decode_responses=True
        )
        r.ping()
        print("✅ Redis接続成功")
        break
    except redis.ConnectionError:
        retry_count += 1
        print(f"⏳ Redis接続待機中... ({retry_count}/{max_retries})")
        time.sleep(1)
else:
    print("⚠️ Redis接続失敗 - セッション機能が制限される可能性があります")
END
fi

# Django初期化
echo -e "${YELLOW}🔧 Django初期化...${NC}"

# データベースマイグレーション
echo "📋 マイグレーション実行..."
python manage.py migrate --noinput

# スーパーユーザー作成（環境変数指定時）
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 スーパーユーザー作成..."
    python manage.py createsuperuser --noinput || echo "ℹ️ スーパーユーザーは既に存在します"
fi

# 静的ファイル収集
echo "📁 静的ファイル収集..."
python manage.py collectstatic --noinput

# Django設定チェック
echo "🔍 Django設定チェック..."
python manage.py check --deploy

# ログディレクトリ作成
mkdir -p /app/logs
chmod 755 /app/logs

echo -e "${GREEN}✅ ShiftMaster 初期化完了${NC}"
echo -e "${GREEN}🚀 アプリケーション起動...${NC}"

# 引数で渡されたコマンドを実行
exec "$@"
