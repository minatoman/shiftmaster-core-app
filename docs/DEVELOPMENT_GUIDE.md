# 🔧 ShiftMaster 開発環境セットアップガイド

## 📋 前提条件

### 必須要件
- **Python**: 3.8以上
- **Node.js**: 16以上（フロントエンド開発時）
- **Docker**: 24以上
- **Git**: 2.30以上

### 推奨要件
- **OS**: Windows 11 / Ubuntu 22.04+ / macOS 12+
- **IDE**: VS Code + Python Extension Pack
- **メモリ**: 8GB以上
- **ストレージ**: 10GB以上の空き容量

## 🚀 クイックスタート

### 1. リポジトリクローン
```bash
git clone https://github.com/minatoman/shiftmaster-core-app.git
cd shiftmaster-core-app
```

### 2. 開発環境起動（推奨）
```powershell
# Windows PowerShell
.\scripts\manage.ps1 -Action start -Environment dev
```

```bash
# Linux/macOS
./scripts/manage.sh start dev
```

### 3. 手動セットアップ（詳細制御が必要な場合）

#### Python仮想環境
```bash
# 仮想環境作成
python -m venv venv

# 仮想環境有効化
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 依存関係インストール
pip install -r requirements.txt
```

#### データベース初期化
```bash
# マイグレーション実行
python manage.py makemigrations
python manage.py migrate

# スーパーユーザー作成
python manage.py createsuperuser

# サンプルデータ投入（オプション）
python manage.py loaddata fixtures/sample_data.json
```

#### 開発サーバー起動
```bash
python manage.py runserver
```

## 🔧 開発ツール設定

### VS Code設定
推奨拡張機能をインストール：
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "ms-vscode.vscode-docker",
    "github.copilot",
    "github.copilot-chat"
  ]
}
```

### プロジェクト設定ファイル
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.testing.pytestEnabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".coverage": true,
    "htmlcov/": true
  }
}
```

## 🧪 テスト実行

### 全テスト実行
```bash
# Django標準テスト
python manage.py test

# pytest使用
pytest

# カバレッジ付きテスト
pytest --cov=. --cov-report=html
```

### 特定アプリのテスト
```bash
python manage.py test shifts.tests
```

### テストデータベース
```bash
# テスト用データベース作成
python manage.py test --keepdb
```

## 🎨 フロントエンド開発

### CSS/JavaScript開発
```bash
# Node.js依存関係インストール
npm install

# 開発用ビルド（ウォッチモード）
npm run dev

# 本番用ビルド
npm run build
```

### 静的ファイル管理
```bash
# 静的ファイル収集
python manage.py collectstatic

# 開発時の静的ファイル配信
python manage.py runserver --insecure
```

## 🐳 Docker開発環境

### 開発環境起動
```bash
# すべてのサービス起動
docker-compose -f docker-compose.dev.yml up

# バックグラウンド起動
docker-compose -f docker-compose.dev.yml up -d

# 特定サービスのみ起動
docker-compose -f docker-compose.dev.yml up web db
```

### コンテナ内での作業
```bash
# Webコンテナにシェルアクセス
docker-compose -f docker-compose.dev.yml exec web bash

# Django管理コマンド実行
docker-compose -f docker-compose.dev.yml exec web python manage.py makemigrations
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
```

## 📊 データベース管理

### マイグレーション
```bash
# マイグレーションファイル作成
python manage.py makemigrations

# 特定アプリのマイグレーション
python manage.py makemigrations shifts

# マイグレーション実行
python manage.py migrate

# マイグレーション状態確認
python manage.py showmigrations
```

### データベース操作
```bash
# Django shell起動
python manage.py shell

# データベースシェル起動
python manage.py dbshell

# データダンプ
python manage.py dumpdata > data.json

# データロード
python manage.py loaddata data.json
```

## 🔍 デバッグ・プロファイリング

### Django Debug Toolbar
```python
# settings/development.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = ['127.0.0.1', 'localhost']
```

### ログ設定
```python
# ログレベル設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### パフォーマンス測定
```bash
# django-silk インストール
pip install django-silk

# プロファイリング有効化
python manage.py runserver --settings=shiftmaster.settings.profiling
```

## 🔐 セキュリティ開発

### セキュリティチェック
```bash
# Django セキュリティチェック
python manage.py check --deploy

# Bandit セキュリティスキャン
bandit -r .

# Safety 脆弱性チェック
safety check
```

### 環境変数管理
```bash
# .env.example を .env にコピー
cp .env.example .env

# 必要な値を設定
# DJANGO_SECRET_KEY=your-secret-key
# DATABASE_URL=sqlite:///db.sqlite3
# DEBUG=True
```

## 📱 モバイル・レスポンシブ開発

### ブレークポイントテスト
```css
/* Bootstrap 5 ブレークポイント */
/* xs: <576px */
/* sm: ≥576px */
/* md: ≥768px */
/* lg: ≥992px */
/* xl: ≥1200px */
/* xxl: ≥1400px */
```

### モバイルエミュレータ
```bash
# Chrome DevTools モバイルエミュレーション
# F12 → デバイスツールバー切り替え
```

## 🤝 コード品質

### コードフォーマット
```bash
# Black フォーマッター
black .

# isort インポート整理
isort .

# flake8 リンター
flake8 .
```

### プリコミットフック
```bash
# pre-commit インストール
pip install pre-commit

# フック設定
pre-commit install

# 手動実行
pre-commit run --all-files
```

## 🚨 トラブルシューティング

### よくある問題

#### 1. マイグレーションエラー
```bash
# マイグレーション履歴確認
python manage.py showmigrations

# 偽のマイグレーション実行
python manage.py migrate --fake

# マイグレーションリセット
python manage.py migrate <app_name> zero
```

#### 2. 静的ファイル404
```bash
# DEBUG=True で確認
# STATIC_URL と STATICFILES_DIRS 設定確認
python manage.py findstatic <filename>
```

#### 3. Docker権限エラー
```bash
# Windows: Docker Desktop 管理者権限で起動
# Linux: ユーザーをdockerグループに追加
sudo usermod -aG docker $USER
```

#### 4. ポート競合
```bash
# 使用中ポート確認
netstat -tulpn | grep :8000

# プロセス終了
kill -9 <PID>
```

## 🎯 開発ワークフロー

### 1. 機能開発
```bash
# 機能ブランチ作成
git checkout -b feature/new-feature

# 開発・テスト
python manage.py test

# コミット
git add .
git commit -m "feat: Add new feature"

# プッシュ
git push origin feature/new-feature
```

### 2. プルリクエスト
- GitHub でプルリクエスト作成
- CI/CD パイプライン確認
- コードレビュー対応
- マージ

### 3. デプロイ
```bash
# 本番環境デプロイ
./scripts/deploy.sh update
```

## 📚 参考資料

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**開発に関する質問やサポートが必要な場合は、GitHub Issuesまたは開発チームまでお気軽にお問い合わせください。**
