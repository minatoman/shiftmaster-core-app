# 🩺 ShiftMaster - 医療シフト管理システム デプロイメントガイド

## 📋 目次

1. [デプロイメント概要](#デプロイメント概要)
2. [環境要件](#環境要件)
3. [事前準備](#事前準備)
4. [本番環境デプロイ](#本番環境デプロイ)
5. [CI/CD パイプライン](#cicd-パイプライン)
6. [監視とメンテナンス](#監視とメンテナンス)
7. [トラブルシューティング](#トラブルシューティング)
8. [セキュリティ設定](#セキュリティ設定)

---

## 🚀 デプロイメント手順 {#deployment}

### 初回デプロイ

```bash
# 1. VPSにroot権限でログイン
ssh root@your-server-ip

# 2. ShiftMasterリポジトリをクローン
git clone https://github.com/your-username/ShiftMaster.git /opt/shiftmaster-deploy
cd /opt/shiftmaster-deploy

# 3. デプロイスクリプト実行
chmod +x scripts/deploy.sh
./scripts/deploy.sh install -d your-domain.com -e admin@your-domain.com
```

### アプリケーション更新

```bash
# 定期更新（メインブランチから）
./scripts/deploy.sh update

# 特定ブランチから更新
./scripts/deploy.sh update -b feature-branch

# 緊急ロールバック
./scripts/deploy.sh rollback
```

---

## 🔄 日常運用 {#daily-operations}

### サービス状態確認

```powershell
# PowerShellから管理
.\scripts\manage.ps1 -Action status

# 個別サービス確認
.\scripts\manage.ps1 -Action logs -Service web
.\scripts\manage.ps1 -Action logs -Service db
.\scripts\manage.ps1 -Action logs -Service nginx
```

### サービス操作

```powershell
# サービス開始
.\scripts\manage.ps1 -Action start -Environment prod

# サービス停止
.\scripts\manage.ps1 -Action stop

# サービス再起動
.\scripts\manage.ps1 -Action restart
```

### Djangoシェルアクセス

```powershell
# Django管理シェル起動
.\scripts\manage.ps1 -Action shell
```

---

## 💾 バックアップ・復元 {#backup-restore}

### 自動バックアップ設定

```bash
# バックアップスケジュール設定
./scripts/backup_manager.sh schedule

# 設定内容をcrontabに追加
crontab -e
```

### 手動バックアップ

```bash
# 即座にバックアップ実行
./scripts/backup_manager.sh backup

# 特定タイプのバックアップ
./scripts/backup_manager.sh backup -t daily
./scripts/backup_manager.sh backup -t weekly
./scripts/backup_manager.sh backup -t monthly
```

### データベース復元

```bash
# バックアップ一覧確認
./scripts/backup_manager.sh list

# 特定バックアップから復元
./scripts/backup_manager.sh restore -f ./backups/shiftmaster_backup_20240101_120000.sql.gz

# バックアップ整合性確認
./scripts/backup_manager.sh verify
```

### バックアップクリーンアップ

```bash
# 30日以上古いバックアップ削除
./scripts/backup_manager.sh cleanup

# 7日以上古いバックアップ削除
./scripts/backup_manager.sh cleanup -d 7
```

---

## 🔐 SSL証明書管理 {#ssl-management}

### 初回SSL設定

```bash
# SSL証明書環境セットアップ
./scripts/ssl_manager.sh setup -e admin@your-domain.com

# 初回証明書取得
./scripts/ssl_manager.sh init -d your-domain.com -e admin@your-domain.com
```

### 証明書更新

```bash
# 手動更新
./scripts/ssl_manager.sh renew

# 証明書状態確認
./scripts/ssl_manager.sh status
```

### 自動更新設定

```bash
# crontabに以下を追加
0 3 * * * cd /opt/shiftmaster && ./scripts/ssl_manager.sh renew >> ./logs/ssl_renewal.log 2>&1
```

---

## 📊 監視・ログ管理 {#monitoring}

### ログファイル場所

```
logs/
├── backup.log          # バックアップログ
├── ssl_renewal.log     # SSL更新ログ
├── deploy.log          # デプロイログ
└── application.log     # アプリケーションログ
```

### ログ監視コマンド

```bash
# リアルタイムログ監視
tail -f logs/application.log

# エラーログ抽出
grep -i error logs/application.log

# 最新100行表示
tail -100 logs/application.log
```

### システムリソース監視

```bash
# Docker コンテナ状態
docker-compose -f docker-compose.prod.yml ps

# システムリソース使用状況
docker stats

# ディスク使用量
df -h

# メモリ使用量
free -h
```

---

## 🚨 トラブルシューティング {#troubleshooting}

### よくある問題と解決方法

#### 1. サービスが起動しない

```bash
# ログ確認
./scripts/deploy.sh logs

# コンテナ状態確認
docker-compose -f docker-compose.prod.yml ps

# 設定ファイル確認
cat .env

# 手動再起動
./scripts/deploy.sh restart
```

#### 2. データベース接続エラー

```bash
# データベースコンテナ状態確認
docker-compose -f docker-compose.prod.yml exec db pg_isready -U shiftmaster_user

# データベースログ確認
docker-compose -f docker-compose.prod.yml logs db

# データベース手動再起動
docker-compose -f docker-compose.prod.yml restart db
```

#### 3. SSL証明書エラー

```bash
# 証明書状態確認
./scripts/ssl_manager.sh status

# Nginx設定確認
nginx -t

# 証明書手動更新
./scripts/ssl_manager.sh renew
```

#### 4. 高負荷状態

```bash
# システムリソース確認
htop

# Docker統計情報
docker stats

# ログファイルサイズ確認
du -sh logs/*

# 不要なDockerイメージ削除
docker system prune -a
```

### 緊急時対応手順

1. **サービス完全停止**
   ```bash
   ./scripts/deploy.sh stop
   ```

2. **最新バックアップから復元**
   ```bash
   ./scripts/backup_manager.sh list
   ./scripts/backup_manager.sh restore -f <backup-file>
   ```

3. **前バージョンにロールバック**
   ```bash
   ./scripts/deploy.sh rollback
   ```

---

## 🛡️ セキュリティ対策 {#security}

### 定期セキュリティチェック

#### 1. システム更新

```bash
# パッケージ更新確認
apt list --upgradable

# セキュリティ更新適用
apt update && apt upgrade -y
```

#### 2. ログ監視

```bash
# 認証失敗ログ確認
grep -i "authentication failure" /var/log/auth.log

# 不審なアクセス確認
grep -i "invalid user" /var/log/auth.log

# Nginx アクセスログ確認
tail -f /var/log/nginx/access.log
```

#### 3. ファイアウォール状態確認

```bash
# UFW状態確認
ufw status verbose

# 開放ポート確認
netstat -tulpn | grep LISTEN
```

### セキュリティ設定推奨事項

1. **強力なパスワードポリシー**
   - 最低12文字以上
   - 大文字・小文字・数字・記号を含む
   - 定期的な変更（90日ごと）

2. **二要素認証（2FA）の有効化**
   - Django管理画面での2FA設定
   - VPSアクセス用のSSH鍵認証

3. **定期的なセキュリティ監査**
   - 週次: ログ確認
   - 月次: システム更新
   - 四半期: 侵入テスト

---

## 🔧 メンテナンス {#maintenance}

### 定期メンテナンス項目

#### 毎日

```bash
# サービス状態確認
./scripts/deploy.sh status

# ディスク容量確認
df -h
```

#### 毎週

```bash
# バックアップ確認
./scripts/backup_manager.sh list

# ログファイル確認
ls -lah logs/

# セキュリティログ確認
grep -i error /var/log/auth.log
```

#### 毎月

```bash
# システム更新
apt update && apt upgrade -y

# Docker イメージクリーンアップ
docker system prune -a

# ログローテーション確認
logrotate -d /etc/logrotate.d/shiftmaster
```

#### 四半期

```bash
# 全バックアップ整合性確認
./scripts/backup_manager.sh verify

# SSL証明書有効期限確認
./scripts/ssl_manager.sh status

# パフォーマンステスト実行
# (負荷テストツールを使用)
```

### アップデート計画

1. **開発環境でのテスト**
   ```bash
   # 開発環境でテスト
   docker-compose -f docker-compose.dev.yml up
   ```

2. **本番環境へのデプロイ**
   ```bash
   # バックアップ作成
   ./scripts/backup_manager.sh backup
   
   # アップデート実行
   ./scripts/deploy.sh update
   ```

3. **ロールバック準備**
   ```bash
   # 問題発生時のロールバック
   ./scripts/deploy.sh rollback
   ```

---

## 🆘 サポート・エスカレーション

### サポートレベル

1. **Level 1**: 基本的な運用問題
   - サービス再起動
   - ログ確認
   - 基本的なトラブルシューティング

2. **Level 2**: 技術的な問題
   - データベース問題
   - 設定変更
   - パフォーマンス問題

3. **Level 3**: 緊急事態
   - システム停止
   - セキュリティインシデント
   - データ損失

### エスカレーション手順

1. **即座に実行**
   ```bash
   # 現在状態のスナップショット取得
   ./scripts/deploy.sh status > incident_report_$(date +%Y%m%d_%H%M%S).txt
   ./scripts/backup_manager.sh list >> incident_report_$(date +%Y%m%d_%H%M%S).txt
   ```

2. **ログ収集**
   ```bash
   # 関連ログを収集
   tar -czf logs_$(date +%Y%m%d_%H%M%S).tar.gz logs/
   ```

3. **技術サポートへ連絡**
   - インシデント詳細
   - エラーメッセージ
   - 実行したコマンド
   - ログファイル

---

## 📞 緊急連絡先

- **システム管理者**: admin@your-domain.com
- **技術サポート**: support@your-domain.com
- **緊急時**: +81-XX-XXXX-XXXX

---

## 📚 関連ドキュメント

- [GitHub リポジトリ](https://github.com/your-username/ShiftMaster)
- [API ドキュメント](https://your-domain.com/api/docs/)
- [ユーザーマニュアル](https://your-domain.com/docs/)

---

**最終更新**: 2024年1月1日
**バージョン**: 1.0
**作成者**: ShiftMaster開発チーム
