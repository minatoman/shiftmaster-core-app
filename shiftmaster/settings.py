"""
Django settings for shiftmaster project - Minimal Configuration
"""

import os
from pathlib import Path
import logging

# 📁 ベースディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 セキュリティキー
SECRET_KEY = 'django-insecure-j!f*hmy)6(th389zzib8(@xho*99%5e+ju%&h)&0@#ssc50&fd'

# 🔧 デバッグモード
DEBUG = True

# 🌐 ホスト許可設定
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# 📦 アプリケーション定義（ミニマル構成）
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shifts',
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

# 🎨 テンプレート設定（シンプル版）
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# 🗃️ データベース（SQLite）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

# 📂 静的ファイル
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 🔐 認証
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

# ⚙️ モデル自動フィールド型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ ログ設定無効化
LOGGING_CONFIG = None
logging.disable(logging.CRITICAL)
