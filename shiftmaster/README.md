# shiftmaster

Django プロジェクト

## 概要
このプロジェクトは自動化スクリプトによって作成されました。

## セットアップ

### 仮想環境の作成と有効化
`ash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
`

### 依存関係のインストール
`ash
pip install -r requirements.txt
`

### データベース移行
`ash
python manage.py migrate
`

### 開発サーバーの起動
`ash
python manage.py runserver
`

## Docker での実行
`ash
docker-compose up --build
`

## 開発者向け情報
- 作成日: 2025年07月11日
- Python バージョン: 3.8+
- Django バージョン: 最新

## ライセンス
MIT License
