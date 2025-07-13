# 🏥 ShiftMaster - 医療シフト管理システム

[![Deploy Status](https://img.shields.io/badge/deploy-ready-green.svg)](https://github.com/minatoman/shiftmaster-core-app)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](./docker-compose.prod.yml)
[![Security](https://img.shields.io/badge/security-HIPAA--ready-red.svg)](./DEPLOYMENT_GUIDE.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 医療施設向け24時間安定運用対応のシフト管理システム

## ✨ 主要機能

### 🏥 医療施設特化機能
- **シフト管理**: 医師・看護師・技師のローテーション管理
- **緊急呼び出し**: オンコール体制の自動管理
- **勤務時間追跡**: 労働基準法準拠の勤務時間管理
- **資格管理**: 医療資格・更新期限の追跡
- **病院部門連携**: 診療科・病棟間のシフト調整

### 🛡️ セキュリティ・コンプライアンス
- **医療データ暗号化**: AES-256暗号化による機密情報保護
- **監査ログ**: すべてのアクセス・操作履歴の記録
- **HIPAA準拠**: 医療情報プライバシー規則対応
- **役割ベースアクセス**: 職種・職位に応じた権限管理
- **二要素認証**: セキュアなログイン機能

### 🚀 Docker本番環境
- **高可用性**: PostgreSQL + Redis + Nginx + Celery構成
- **自動スケーリング**: 負荷に応じたコンテナ自動調整
- **ゼロダウンタイム**: ローリングアップデート対応
- **SSL/TLS**: Let's Encrypt自動証明書管理
- **バックアップ**: 自動データベースバックアップ・復元

## 🛠️ 技術スタック

| カテゴリ | 技術 | バージョン |
|----------|------|------------|
| **Backend** | Django | 5.2+ |
| **Database** | PostgreSQL | 15+ |
| **Cache** | Redis | 7+ |
| **Web Server** | Nginx | 1.24+ |
| **Task Queue** | Celery | 5.3+ |
| **Container** | Docker | 24+ |
| **Frontend** | Bootstrap | 5.3+ |
| **Language** | Python | 3.8+ |

## 🚀 クイックスタート

### 開発環境セットアップ

```powershell
# 1. リポジトリクローン
git clone https://github.com/minatoman/shiftmaster-core-app.git
cd shiftmaster-core-app

# 2. 開発環境起動
.\scripts\manage.ps1 -Action start -Environment dev

# 3. ブラウザでアクセス
# http://localhost:8000
```

### 本番環境デプロイ

```bash
# 1. VPSでの初回セットアップ
sudo ./scripts/deploy.sh install -d your-domain.com -e admin@example.com

# 2. SSL証明書設定
./scripts/ssl_manager.sh init -d your-domain.com -e admin@example.com

# 3. 自動バックアップ設定
./scripts/backup_manager.sh schedule
```

## 📋 システム要件

### 最小システム要件
- **CPU**: 2コア以上
- **メモリ**: 4GB以上
- **ストレージ**: 20GB以上
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+

### 推奨システム要件
- **CPU**: 4コア以上
- **メモリ**: 8GB以上
- **ストレージ**: 100GB以上（SSD推奨）
- **ネットワーク**: 1Gbps以上

## 🔧 管理・運用

### 日常運用コマンド

```powershell
# サービス状態確認
.\scripts\manage.ps1 -Action status

# ログ確認
.\scripts\manage.ps1 -Action logs

# データベースバックアップ
.\scripts\manage.ps1 -Action backup

# アプリケーション更新
.\scripts\manage.ps1 -Action update
```

### 緊急時対応

```bash
# サービス再起動
./scripts/deploy.sh restart

# 前バージョンにロールバック
./scripts/deploy.sh rollback

# データベース復元
./scripts/backup_manager.sh restore -f backup_file.sql.gz
```

## 📊 監視・アラート

### ダッシュボード
- **システム監視**: CPU、メモリ、ディスク使用率
- **アプリケーション監視**: レスポンス時間、エラー率
- **データベース監視**: 接続数、クエリパフォーマンス
- **セキュリティ監視**: 不正アクセス試行、認証失敗

### アラート設定
- **緊急**: システム停止、データベースダウン
- **警告**: 高負荷状態、ディスク容量不足
- **情報**: 定期バックアップ完了、更新通知

## 🔐 セキュリティ

### 実装済みセキュリティ対策
- ✅ **データ暗号化**: 保存時・転送時の暗号化
- ✅ **アクセス制御**: 役割ベースアクセス制御（RBAC）
- ✅ **監査ログ**: 全操作の追跡・記録
- ✅ **脆弱性対策**: 定期的なセキュリティスキャン
- ✅ **バックアップ**: 暗号化されたバックアップ

### コンプライアンス
- 🏥 **HIPAA**: 医療情報プライバシー規則準拠
- 📊 **医療法**: 医療施設管理基準対応
- 🔒 **個人情報保護法**: 個人情報適切管理
- 📋 **労働基準法**: 勤務時間管理規則準拠

## 📖 ドキュメント

| ドキュメント | 説明 |
|--------------|------|
| [運用ガイド](./DEPLOYMENT_GUIDE.md) | 本番環境運用・保守マニュアル |
| [API仕様書](./docs/api.md) | REST API仕様・エンドポイント |
| [開発者ガイド](./docs/development.md) | 開発環境セットアップ・コーディング規約 |
| [FAQ](./docs/faq.md) | よくある質問・トラブルシューティング |

## 🤝 GitHub Copilot連携

このプロジェクトはGitHub Copilotとの連携に最適化されています：

```markdown
# Copilot Agentでの継続開発
@github #github-pull-request_copilot-coding-agent
```

詳細な連携方法は [COPILOT_AGENT_PROMPT.md](./COPILOT_AGENT_PROMPT.md) を参照してください。

## 📞 サポート

### コミュニティサポート
- **GitHub Issues**: バグ報告・機能要望
- **Discussions**: 技術的な質問・相談
- **Wiki**: 詳細なドキュメント

### 企業サポート
- **技術サポート**: 24時間365日対応
- **導入支援**: カスタマイズ・移行支援
- **研修**: システム管理者・利用者研修

## 📄 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

## 🚀 ロードマップ

### v2.0 (2025年Q3)
- [ ] マルチテナント対応
- [ ] モバイルアプリ
- [ ] AI自動シフト生成
- [ ] 多言語対応

### v2.1 (2025年Q4)
- [ ] BI・レポート機能拡張
- [ ] 外部システム連携API
- [ ] クラウドネイティブ化
- [ ] マイクロサービス分割

---

## 🌟 貢献者

- **[@minatoman](https://github.com/minatoman)** - プロジェクトリード・メイン開発者
- **GitHub Copilot** - AI開発支援

## 🙏 謝辞

このプロジェクトは以下の技術・プロジェクトの恩恵を受けています：

- [Django](https://djangoproject.com/) - 高品質なWebフレームワーク
- [Bootstrap](https://getbootstrap.com/) - レスポンシブUIフレームワーク
- [Docker](https://docker.com/) - コンテナ仮想化技術
- [PostgreSQL](https://postgresql.org/) - 高性能データベース
- [Redis](https://redis.io/) - 高速インメモリデータベース

---

<div align="center">

**🏥 医療施設の皆様の安全で効率的な勤務管理を支援します 🏥**

[**📥 今すぐダウンロード**](https://github.com/minatoman/shiftmaster-core-app/releases) | [**📖 ドキュメント**](./DEPLOYMENT_GUIDE.md) | [**💬 サポート**](https://github.com/minatoman/shiftmaster-core-app/issues)

</div>

---

**最終更新**: 2025年7月14日  
**自動生成**: ShiftMaster開発チーム
