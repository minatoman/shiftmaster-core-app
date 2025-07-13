# 🔧 ShiftMaster - 開発・運用自動化スクリプト集

## 📋 概要

このディレクトリには、ShiftMaster医療シフト管理システムの開発・運用を効率化するための各種自動化スクリプトが含まれています。

## 🚀 クイックスタート

### 開発環境セットアップ

```powershell
# 全自動セットアップ
.\scripts\setup-development.ps1

# または手動で段階的に
.\scripts\install-dependencies.ps1
.\scripts\setup-database.ps1
.\scripts\configure-environment.ps1
```

### 本番環境デプロイ

```powershell
# Docker本番環境構築
.\scripts\deploy-production.ps1

# または個別に実行
.\scripts\build-containers.ps1
.\scripts\deploy-ssl.ps1
.\scripts\start-services.ps1
```

## 📁 スクリプト構成

### 🔨 開発支援スクリプト

| スクリプト | 説明 | 使用タイミング |
|-----------|------|---------------|
| `setup-development.ps1` | 開発環境の完全セットアップ | 初回セットアップ時 |
| `install-dependencies.ps1` | 依存関係のインストール | 依存関係更新時 |
| `run-tests.ps1` | テスト実行 | 開発中・CI/CD |
| `lint-code.ps1` | コード品質チェック | 開発中・PR前 |
| `format-code.ps1` | コードフォーマット | 開発中 |
| `generate-migrations.ps1` | DBマイグレーション生成 | モデル変更時 |
| `backup-development.ps1` | 開発環境バックアップ | 定期的 |

### 🚀 デプロイ・運用スクリプト

| スクリプト | 説明 | 使用タイミング |
|-----------|------|---------------|
| `deploy-production.ps1` | 本番環境デプロイ | リリース時 |
| `build-containers.ps1` | Dockerコンテナビルド | デプロイ前 |
| `deploy-ssl.ps1` | SSL証明書設定 | 初回・更新時 |
| `backup-production.ps1` | 本番環境バックアップ | 定期実行 |
| `health-check.ps1` | システム稼働状況確認 | 監視・トラブル時 |
| `performance-monitor.ps1` | パフォーマンス監視 | 定期監視 |
| `security-scan.ps1` | セキュリティスキャン | 定期・リリース前 |

### 🛠️ ユーティリティスクリプト

| スクリプト | 説明 | 使用タイミング |
|-----------|------|---------------|
| `database-utils.ps1` | データベース操作支援 | DB操作時 |
| `log-analyzer.ps1` | ログ解析ツール | トラブル時 |
| `config-validator.ps1` | 設定ファイル検証 | 設定変更時 |
| `cleanup-system.ps1` | システムクリーンアップ | 定期メンテナンス |
| `generate-docs.ps1` | ドキュメント自動生成 | ドキュメント更新時 |

## 📝 詳細ガイド

### 開発環境セットアップ詳細

```powershell
# 1. 基本セットアップ
.\scripts\setup-development.ps1 -Full

# 2. 特定コンポーネントのみ
.\scripts\setup-development.ps1 -Component Database
.\scripts\setup-development.ps1 -Component Python
.\scripts\setup-development.ps1 -Component Docker

# 3. 設定確認
.\scripts\config-validator.ps1 -Environment Development
```

### 本番デプロイ手順

```powershell
# 1. 事前チェック
.\scripts\pre-deploy-check.ps1

# 2. バックアップ作成
.\scripts\backup-production.ps1 -CreateSnapshot

# 3. デプロイ実行
.\scripts\deploy-production.ps1 -Version "v1.2.0"

# 4. デプロイ後チェック
.\scripts\post-deploy-check.ps1
.\scripts\health-check.ps1 -Detailed
```

### データベース操作

```powershell
# マイグレーション
.\scripts\database-utils.ps1 -Action Migrate

# バックアップ
.\scripts\database-utils.ps1 -Action Backup -Output "backup_20240120.sql"

# リストア
.\scripts\database-utils.ps1 -Action Restore -Input "backup_20240120.sql"

# データ初期化
.\scripts\database-utils.ps1 -Action Initialize -SampleData
```

### 監視・メンテナンス

```powershell
# システム稼働状況
.\scripts\health-check.ps1

# パフォーマンス監視
.\scripts\performance-monitor.ps1 -Duration 3600 -Report

# ログ解析
.\scripts\log-analyzer.ps1 -LogLevel Error -TimeRange "24h"

# セキュリティスキャン
.\scripts\security-scan.ps1 -FullScan
```

## ⚙️ 設定ファイル

### 環境設定

各スクリプトは以下の設定ファイルを参照します：

- `config\development.json` - 開発環境設定
- `config\production.json` - 本番環境設定
- `config\testing.json` - テスト環境設定
- `config\monitoring.json` - 監視設定

### 設定例

```json
{
  "environment": "development",
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "shiftmaster_dev"
  },
  "backup": {
    "enabled": true,
    "retention_days": 30,
    "encryption": true
  },
  "monitoring": {
    "health_check_interval": 300,
    "alert_email": "admin@hospital.com"
  }
}
```

## 🔒 セキュリティ

### 機密情報管理

```powershell
# 暗号化キー生成
.\scripts\security-utils.ps1 -GenerateKeys

# 設定ファイル暗号化
.\scripts\security-utils.ps1 -EncryptConfig -File "production.json"

# 権限設定
.\scripts\security-utils.ps1 -SetPermissions -Strict
```

### アクセス制御

- スクリプト実行には管理者権限が必要
- 本番環境操作には追加認証が必要
- 全操作は監査ログに記録

## 📊 監視・アラート

### 自動監視設定

```powershell
# Windows Task Schedulerにタスク登録
.\scripts\setup-monitoring.ps1 -InstallTasks

# 監視対象項目
# - システム稼働状況 (5分間隔)
# - データベース接続 (1分間隔)
# - ディスク使用量 (30分間隔)
# - メモリ使用量 (10分間隔)
# - SSL証明書有効期限 (日次)
```

### アラート設定

```powershell
# メールアラート設定
.\scripts\setup-alerts.ps1 -Email "admin@hospital.com"

# Slack通知設定
.\scripts\setup-alerts.ps1 -Slack "webhook-url"

# SMS通知設定（緊急時）
.\scripts\setup-alerts.ps1 -SMS "+81-90-xxxx-xxxx"
```

## 🔧 トラブルシューティング

### よくある問題と解決方法

#### 1. 依存関係エラー

```powershell
# 依存関係強制再インストール
.\scripts\install-dependencies.ps1 -Force -Clean

# Python環境リセット
.\scripts\reset-python-env.ps1
```

#### 2. データベース接続エラー

```powershell
# 接続テスト
.\scripts\database-utils.ps1 -Action TestConnection

# サービス再起動
.\scripts\restart-services.ps1 -Service Database
```

#### 3. Docker関連エラー

```powershell
# Dockerリセット
.\scripts\docker-utils.ps1 -Reset

# イメージ再ビルド
.\scripts\build-containers.ps1 -NoBuildCache
```

#### 4. SSL証明書エラー

```powershell
# 証明書更新
.\scripts\deploy-ssl.ps1 -Renew

# 証明書確認
.\scripts\ssl-utils.ps1 -Verify
```

### ログ分析

```powershell
# エラーログ抽出
.\scripts\log-analyzer.ps1 -Level Error -Count 100

# 特定期間のログ
.\scripts\log-analyzer.ps1 -StartTime "2024-01-20 09:00" -EndTime "2024-01-20 17:00"

# パフォーマンスログ
.\scripts\log-analyzer.ps1 -Type Performance -Analysis
```

## 📚 リファレンス

### 環境変数

| 変数名 | 説明 | デフォルト値 |
|--------|------|-------------|
| `SHIFTMASTER_ENV` | 実行環境 | `development` |
| `SHIFTMASTER_CONFIG` | 設定ファイルパス | `config\development.json` |
| `SHIFTMASTER_LOG_LEVEL` | ログレベル | `INFO` |
| `SHIFTMASTER_BACKUP_DIR` | バックアップディレクトリ | `backup_storage` |

### コマンドライン引数

共通引数：
- `-Environment` : 実行環境指定 (development/testing/production)
- `-ConfigFile` : 設定ファイル指定
- `-LogLevel` : ログレベル指定
- `-DryRun` : 実際の処理を行わずテスト実行
- `-Verbose` : 詳細ログ出力
- `-Force` : 確認なしで実行

### 戻り値コード

- `0` : 正常終了
- `1` : 一般的なエラー
- `2` : 設定ファイルエラー
- `3` : 依存関係エラー
- `4` : 権限エラー
- `5` : ネットワークエラー

## 🆘 サポート

### ヘルプコマンド

```powershell
# 全スクリプト一覧
.\scripts\help.ps1

# 特定スクリプトのヘルプ
.\scripts\deploy-production.ps1 -Help

# トラブルシューティングガイド
.\scripts\troubleshoot.ps1
```

### 連絡先

- **技術サポート**: tech-support@shiftmaster.com
- **緊急時**: emergency@shiftmaster.com
- **ドキュメント**: https://docs.shiftmaster.com/scripts

---

**最終更新**: 2024年1月20日
**バージョン**: 1.0.0
