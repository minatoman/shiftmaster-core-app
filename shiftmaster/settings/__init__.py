"""
Settings package for different environments
"""

import os
from pathlib import Path

# 環境判定
ENV = os.getenv("DJANGO_ENV", "development")

if ENV == "production":
    from .production import *
elif ENV == "staging":
    from .staging import *
else:
    from .development import *
