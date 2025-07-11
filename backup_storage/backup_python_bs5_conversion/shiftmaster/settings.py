"""
Django settings for shiftmaster project.
"""

import os
from pathlib import Path

# 📁 ベースディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 セキュリティキー（本番では .env で管理推奨）
SECRET_KEY = 'django-insecure-j!f*hmy)6(th389zzib8(@xho*99%5e+ju%&h)&0@#ssc50&fd'

# 🔧 デバッグモード（本番は False）
DEBUG = True

# 🌐 ホスト許可設定
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-domain.com']

# 📦 アプリケーション定義
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🌟 カスタムアプリ
    'shifts',

    # 🌐 外部ライブラリ
    'bootstrap4',
]

# 🧱 ミドルウェア
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shiftmaster.urls'

# 🎨 テンプレート設定
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shiftmaster.wsgi.application'

# 🗃️ データベース（PostgreSQL）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shiftmaster_db',
        'USER': 'postgres',
        'PASSWORD': 'pass',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
            'connect_timeout': 10,  # 接続失敗時にタイムアウト秒数
        },
        'CONN_MAX_AGE': 600,  # 持続接続（秒）
    }
}

# 🔐 パスワードバリデーション
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 ロケール
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True
USE_L10N = False  # 自動ローカライズ無効化（表示整形を手動で制御）

# 📂 静的ファイル
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'shifts', 'static'),
]

# 📂 メディアファイル
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 🔐 認証
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/profile/'

# ⚙️ モデル自動フィールド型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 📧 メール設定（Gmail など使用時）
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jin.nana2005128@gmail.com'  # ✅ Gmailアドレス
EMAIL_HOST_PASSWORD = 'qsmr pyez meuf qrrf'     # ✅ Gmailのアプリパスワード
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ✅ テスト・CI用：エラー表示制御（任意）
SILENCED_SYSTEM_CHECKS = []

# ✅ ローカルPostgreSQL接続チェック用
# 実行前に `pg_ctl` または `pgAdmin` などで PostgreSQL 起動確認を！

