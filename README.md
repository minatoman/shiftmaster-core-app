# 🏥 ShiftMaster - 医療機関向け勤務シフト管理システム

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Djangoベースの医療機関向け勤務シフト管理システム - 複雑な医療現場のシフト調整を効率化

## 📋 概要

ShiftMasterは医療機関の複雑な勤務シフト管理を効率化するWebアプリケーションです。看護師・医師の勤務スケジュール、透析業務、休暇申請を一元管理できます。

### ✨ 主な機能
- 👥 **スタッフ管理** - 従業員情報・職種・資格管理
- 📅 **シフト作成・編集** - 直感的なカレンダーインターface
- 🙋‍♀️ **勤務希望申請** - スタッフからの希望申請システム
- 🤖 **自動シフト割り当て** - AI風自動最適化
- 📊 **月次統計・レポート** - 勤務実績・コスト分析
- 💉 **透析日誌管理** - 透析患者・スタッフ管理
- 📤 **データ連携** - CSV/Excel インポート・エクスポート
- 🔔 **通知システム** - リアルタイム通知

## 🛠 技術スタック

- **Backend**: Django 5.2+ (Python)
- **Database**: SQLite (開発) / PostgreSQL (本番推奨)
- **Frontend**: Bootstrap 5, JavaScript, jQuery
- **Language**: Python 3.8+
- **Development**: Django Debug Toolbar, pytest
- **Deployment**: Docker対応

## 🚀 クイックスタート

### 前提条件
- Python 3.8以上
- Git
- pip (Python package manager)

### インストール手順

1. **リポジトリのクローン**
```bash
git clone https://github.com/your-username/shiftmaster-django.git
cd shiftmaster-django
```

2. **仮想環境の作成**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

4. **データベースのセットアップ**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **スーパーユーザーの作成**
```bash
python manage.py createsuperuser
```

6. **開発サーバーの起動**
```bash
python manage.py runserver
```

http://localhost:8000 でアクセス可能

## 📦 Docker での実行

```bash
# イメージのビルド
docker build -t shiftmaster .

# コンテナの実行
docker run -p 8000:8000 shiftmaster
```

## 🔧 設定

### 環境変数

本番環境では以下の環境変数を設定してください：

```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres://user:pass@localhost/dbname
```

### データベース設定

- **開発環境**: SQLite (自動設定)
- **本番環境**: PostgreSQL推奨

## 📁 プロジェクト構造

```
shiftmaster/
├── shiftmaster/           # プロジェクト設定
├── shifts/               # メインアプリケーション
│   ├── models.py        # データモデル
│   ├── views/           # ビューファイル
│   ├── templates/       # HTMLテンプレート
│   └── static/          # CSS/JS/画像
├── templates/           # 共通テンプレート
├── static/              # 静的ファイル
├── requirements.txt     # Python依存関係
├── manage.py           # Django管理コマンド
└── README.md           # このファイル
```

## 🧪 テスト

```bash
python manage.py test
```

## 📊 使用方法

### 基本的なワークフロー

1. **スタッフ登録**: 管理画面またはCSVインポートでスタッフを登録
2. **勤務希望入力**: スタッフが勤務希望を入力
3. **シフト作成**: 管理者がシフトを作成・調整
4. **自動割り当て**: AIアシストによる効率的なシフト割り当て
5. **承認・公開**: シフトの最終確認と公開

### CSV インポート・エクスポート

- スタッフデータの一括登録
- 勤務希望データの一括処理
- シフト結果のエクスポート

## 🔐 セキュリティ

- Django標準のセキュリティ機能を使用
- ユーザー認証・認可
- CSRF保護
- SQLインジェクション対策

## 🤝 貢献

プルリクエストや課題報告を歓迎します。

1. フォークしてブランチを作成
2. 変更をコミット
3. テストを実行
4. プルリクエストを作成

## 📄 ライセンス

MIT License

## 🆘 サポート

問題や質問がある場合は、GitHubのIssuesでご報告ください。

## 📝 更新履歴

- **v1.0.0** - 初回リリース
  - 基本的なシフト管理機能
  - スタッフ管理
  - 勤務希望申請

---

**開発者**: ShiftMaster Development Team  
**連絡先**: [GitHub Issues](https://github.com/your-username/shiftmaster-django/issues)