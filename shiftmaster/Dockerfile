FROM python:3.11-slim

# 作業ディレクトリ設定
WORKDIR /app

# システム依存関係
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーション
COPY . .

# 静的ファイル収集
RUN python manage.py collectstatic --noinput || true

# ポート公開
EXPOSE 8000

# 健康チェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python manage.py check || exit 1

# 起動コマンド
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "shiftmaster.wsgi:application"]
