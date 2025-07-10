FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルをコピー
COPY . .

# 静的ファイルを収集
RUN python manage.py collectstatic --noinput

# ポート8000を公開
EXPOSE 8000

# アプリケーションを起動
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]