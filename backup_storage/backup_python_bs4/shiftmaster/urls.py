# shiftmaster/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # 🛠 管理者用：Django管理画面
    path('admin/', admin.site.urls),

    # 🚀 ShiftMasterメイン：shiftsアプリのルーティング全般（login/logout含む）
    path('', include(('shifts.urls', 'shifts'), namespace='shifts')),

    # ✅ ルートURL（"/"）を特定ページへリダイレクトしたい場合（オプション）
    # path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
]
