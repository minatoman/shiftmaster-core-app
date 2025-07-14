"""
Testing Configuration for ShiftMaster
テスト専用設定
"""

from .base import *
import os

# ========================================
# テスト環境設定
# ========================================

# テストモード
TESTING = True

# デバッグ設定
DEBUG = True
TEMPLATE_DEBUG = True

# データベース設定（テスト用）
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",  # インメモリDB（高速）
        "TEST": {
            "NAME": ":memory:",
        },
    }
}

# 外部データベースが必要なテスト用
if os.environ.get("USE_POSTGRES_TEST"):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("TEST_DB_NAME", "test_shiftmaster"),
        "USER": os.environ.get("TEST_DB_USER", "test_user"),
        "PASSWORD": os.environ.get("TEST_DB_PASSWORD", "test_password"),
        "HOST": os.environ.get("TEST_DB_HOST", "localhost"),
        "PORT": os.environ.get("TEST_DB_PORT", "5432"),
        "TEST": {
            "NAME": "test_shiftmaster_test",
        },
    }

# Redis設定（テスト用）
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "test-cache",
    }
}

# セッション設定
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# メール設定（テスト用）
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Celery設定（テスト用）
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# ログ設定（テスト用）
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
        "shifts": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# 静的ファイル設定
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# メディアファイル設定
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# セキュリティ設定（テスト用）
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "test-secret-key-not-for-production"

# パスワード検証無効化（テスト高速化）
AUTH_PASSWORD_VALIDATORS = []

# 国際化設定
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ===============================
# テスト専用設定
# ===============================

# テストデータベース設定
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# ファクトリ設定
FACTORY_FOR_DJANGO_SETTINGS = True

# モック設定
MOCK_EXTERNAL_APIS = True

# 外部サービス無効化
ENABLE_EXTERNAL_NOTIFICATIONS = False
ENABLE_FILE_UPLOADS = False
ENABLE_AUDIT_LOGGING = False

# パフォーマンステスト設定
PERFORMANCE_TEST_THRESHOLD = {
    "database_queries": 10,  # N+1クエリ検出
    "response_time_ms": 1000,  # レスポンス時間
    "memory_usage_mb": 100,  # メモリ使用量
}

# テストカバレッジ設定
COVERAGE_MINIMUM_PERCENTAGE = 80
