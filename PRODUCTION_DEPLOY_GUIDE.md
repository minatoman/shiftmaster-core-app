# 🚀 ShiftMaster 本番デプロイガイド

## ✅ **デプロイ前チェックリスト**

### 1. **システム動作確認**
- [x] ローカルテストサーバー起動
- [x] データベース読み書き確認
- [x] API エンドポイント動作確認
- [x] ヘルスチェック成功
- [x] UI/UX 動作確認

### 2. **テストデータ**
- [x] 従業員データ: 1名登録済み
- [x] シフトデータ: 入力可能状態
- [x] データエクスポート完了

### 3. **本番環境準備**
- [ ] 本番サーバー準備
- [ ] ドメイン設定
- [ ] SSL証明書取得
- [ ] データベースサーバー構築
- [ ] 環境変数設定

---

## 🖥️ **本番サーバー要件**

### **最小構成**
```
CPU: 2 vCPU
メモリ: 4GB RAM
ストレージ: 50GB SSD
OS: Ubuntu 22.04 LTS
```

### **推奨構成**
```
CPU: 4 vCPU
メモリ: 8GB RAM
ストレージ: 100GB SSD
OS: Ubuntu 22.04 LTS
```

### **必要ソフトウェア**
- Docker Engine 24.0+
- Docker Compose 2.0+
- Nginx 1.20+
- PostgreSQL 15+
- Redis 7+

---

## 📋 **デプロイ手順**

### **Step 1: サーバー準備**

```bash
# サーバーにログイン
ssh root@your-server.com

# システム更新
apt update && apt upgrade -y

# Docker インストール
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Docker Compose インストール
apt install docker-compose-plugin -y

# ユーザー追加
useradd -m -s /bin/bash deploy
usermod -aG docker deploy
```

### **Step 2: アプリケーション配置**

```bash
# デプロイユーザーに切り替え
su - deploy

# プロジェクト配置
mkdir -p /var/www/shiftmaster
cd /var/www/shiftmaster

# Gitからクローン（またはファイル転送）
git clone https://github.com/your-username/shiftmaster.git .
```

### **Step 3: 環境設定**

```bash
# 環境変数ファイル作成
cp .env.production.example .env.production

# 環境変数編集
nano .env.production
```

**重要な設定項目:**
```bash
# Django設定
DJANGO_ENV=production
SECRET_KEY=YOUR_SECURE_SECRET_KEY_HERE
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# データベース
POSTGRES_DB=shiftmaster_production
POSTGRES_USER=shiftmaster_admin
POSTGRES_PASSWORD=SECURE_DATABASE_PASSWORD

# Redis
REDIS_PASSWORD=SECURE_REDIS_PASSWORD

# SSL
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
```

### **Step 4: SSL証明書設定**

```bash
# Let's Encrypt証明書取得
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com -d www.your-domain.com
```

### **Step 5: データベース初期化**

```bash
# データベースコンテナ起動
docker-compose -f docker-compose.prod.yml up -d db redis

# マイグレーション実行
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# スーパーユーザー作成
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# 静的ファイル収集
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### **Step 6: 本番データ投入**

```bash
# エクスポートデータ転送
scp production_data_export.json deploy@your-server:/var/www/shiftmaster/

# データ投入
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata production_data_export.json
```

### **Step 7: アプリケーション起動**

```bash
# 全サービス起動
docker-compose -f docker-compose.prod.yml up -d

# サービス状態確認
docker-compose -f docker-compose.prod.yml ps

# ログ確認
docker-compose -f docker-compose.prod.yml logs -f web
```

### **Step 8: 動作確認**

```bash
# ヘルスチェック
curl -f https://your-domain.com/health/

# 管理画面アクセス
curl -f https://your-domain.com/admin/

# API確認
curl -f https://your-domain.com/api/employees/
```

---

## 🔧 **運用コマンド**

### **サービス管理**
```bash
# サービス起動
docker-compose -f docker-compose.prod.yml up -d

# サービス停止
docker-compose -f docker-compose.prod.yml down

# サービス再起動
docker-compose -f docker-compose.prod.yml restart

# ログ確認
docker-compose -f docker-compose.prod.yml logs -f [service_name]
```

### **データベース管理**
```bash
# バックアップ
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres shiftmaster > backup_$(date +%Y%m%d).sql

# リストア
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres shiftmaster < backup_file.sql

# データベース接続
docker-compose -f docker-compose.prod.yml exec db psql -U postgres shiftmaster
```

### **アプリケーション管理**
```bash
# マイグレーション
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# 静的ファイル更新
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Django シェル
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
```

---

## 🔍 **監視・メンテナンス**

### **ログ監視**
```bash
# リアルタイムログ
docker-compose -f docker-compose.prod.yml logs -f --tail=100

# エラーログ抽出
docker-compose -f docker-compose.prod.yml logs web | grep ERROR

# アクセスログ確認
docker-compose -f docker-compose.prod.yml logs nginx | tail -100
```

### **パフォーマンス監視**
```bash
# コンテナリソース使用量
docker stats

# ディスク使用量
df -h

# メモリ使用量
free -h

# プロセス確認
docker-compose -f docker-compose.prod.yml top
```

### **セキュリティ更新**
```bash
# システム更新
apt update && apt upgrade -y

# Docker イメージ更新
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🆘 **トラブルシューティング**

### **よくある問題**

1. **サービスが起動しない**
   ```bash
   # ログ確認
   docker-compose -f docker-compose.prod.yml logs
   
   # 設定確認
   docker-compose -f docker-compose.prod.yml config
   ```

2. **データベース接続エラー**
   ```bash
   # データベース状態確認
   docker-compose -f docker-compose.prod.yml exec db pg_isready
   
   # 接続テスト
   docker-compose -f docker-compose.prod.yml exec db psql -U postgres -c "SELECT 1;"
   ```

3. **パフォーマンス問題**
   ```bash
   # スロークエリログ確認
   docker-compose -f docker-compose.prod.yml logs db | grep "slow query"
   
   # メモリ使用量確認
   docker stats --no-stream
   ```

### **緊急時対応**
```bash
# 緊急停止
docker-compose -f docker-compose.prod.yml down

# 以前のバージョンに戻す
git checkout previous-stable-tag
docker-compose -f docker-compose.prod.yml up -d

# データベース復旧
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres shiftmaster < latest_backup.sql
```

---

## 📞 **サポート連絡先**

- **技術サポート**: tech-support@your-domain.com
- **緊急時連絡**: emergency@your-domain.com
- **ドキュメント**: https://docs.your-domain.com/

---

**🎉 デプロイ成功後は、ShiftMasterが本番環境で稼働します！**

**📊 運用開始後の推奨モニタリング:**
- ✅ 日次バックアップ確認
- ✅ ログローテーション設定
- ✅ SSL証明書更新アラート
- ✅ リソース使用量監視
- ✅ セキュリティアップデート適用
