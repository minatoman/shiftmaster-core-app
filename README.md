# shiftmaster

Django プロジェクト

## セットアップ

`ash
# 仮想環境作成
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 依存関係インストール
pip install -r requirements.txt

# マイグレーション
python manage.py migrate

# 開発サーバー起動
python manage.py runserver
`

## Docker での実行

`ash
docker-compose up --build
`

自動生成日時: 2025年07月11日 18:28
