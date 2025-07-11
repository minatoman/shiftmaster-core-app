#!/bin/bash
# Django プロジェクト VPS デプロイメント自動化スクリプト
# ShiftMaster プロジェクト用
# 更新日: 2025-06-26 - 最新アップデート対応

echo "🚀 Django プロジェクト VPS デプロイメント開始"
echo "🔄 システム最新アップデート & プロジェクトデプロイ"
echo "=========================================="

# 1. システム更新とパッケージインストール
echo "📦 システムパッケージの更新・インストール..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx supervisor postgresql postgresql-contrib git curl

# 2. プロジェクトディレクトリ作成
echo "📁 プロジェクトディレクトリの作成..."
mkdir -p /var/www/shiftmaster
chown -R root:root /var/www/shiftmaster
cd /var/www/shiftmaster

# 3. 仮想環境作成
echo "🐍 Python仮想環境の作成..."
python3 -m venv venv
source venv/bin/activate

# 4. 基本パッケージインストール
echo "📦 Django関連パッケージのインストール..."
pip install django gunicorn psycopg2-binary

# 5. PostgreSQL設定
echo "🗄️ PostgreSQL設定..."
sudo -u postgres createdb shiftmaster_db
sudo -u postgres psql -c "CREATE USER shiftmaster WITH PASSWORD 'shiftmaster123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE shiftmaster_db TO shiftmaster;"

# 6. Gunicorn設定ファイル作成
echo "⚙️ Gunicorn設定ファイル作成..."
cat > /var/www/shiftmaster/gunicorn_config.py << 'EOF'
bind = 'unix:/run/gunicorn/shiftmaster.sock'
workers = 3
timeout = 120
user = 'root'
group = 'root'
pythonpath = '/var/www/shiftmaster'
django_settings = 'shiftmaster.settings'
EOF

# 7. ソケットディレクトリ作成
echo "📁 Gunicornソケットディレクトリ作成..."
mkdir -p /run/gunicorn
chown -R root:root /run/gunicorn

# 8. Supervisor設定
echo "👮 Supervisor設定ファイル作成..."
cat > /etc/supervisor/conf.d/shiftmaster.conf << 'EOF'
[program:shiftmaster]
directory=/var/www/shiftmaster
command=/var/www/shiftmaster/venv/bin/gunicorn -c gunicorn_config.py shiftmaster.wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/shiftmaster.err.log
stdout_logfile=/var/log/gunicorn/shiftmaster.out.log
user=root
EOF

# 9. Gunicornログディレクトリ作成
mkdir -p /var/log/gunicorn

# 10. Nginx設定
echo "🌐 Nginx設定ファイル作成..."
cat > /etc/nginx/sites-available/shiftmaster << 'EOF'
server {
    listen 80;
    server_name 160.251.181.238;

    location / {
        proxy_pass http://unix:/run/gunicorn/shiftmaster.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /var/www/shiftmaster/static/;
    }

    location /media/ {
        alias /var/www/shiftmaster/media/;
    }

    # セキュリティヘッダー
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
}
EOF

# 11. Nginxサイト有効化
echo "🔗 Nginxサイト有効化..."
ln -sf /etc/nginx/sites-available/shiftmaster /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 12. ファイアウォール設定
echo "🛡️ ファイアウォール設定..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# 13. 設定テスト
echo "🧪 設定テスト..."
nginx -t

# 14. サービス再起動
echo "🔄 サービス再起動..."
supervisorctl reread
supervisorctl update
systemctl restart nginx
systemctl enable nginx
systemctl enable supervisor

echo "✅ デプロイメント基盤セットアップ完了！"
echo ""
echo "次のステップ:"
echo "1. Djangoプロジェクトファイルをアップロード"
echo "2. settings.pyの本番環境設定"
echo "3. データベースマイグレーション実行"
echo "4. 静的ファイル収集"
echo ""
echo "プロジェクトディレクトリ: /var/www/shiftmaster"
echo "アクセスURL: http://160.251.181.238"
