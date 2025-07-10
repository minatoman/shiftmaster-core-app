# shifts/views/__init__.py 

# 🔄 モジュール単位の汎用インポート（全体読み込み）
from .shift_views import *
from .calendar_views import *
from .dashboard_views import *
from .dialysis_views import *
from .staff_views import *
from .upload_views import *
from .template_views import *
from .auth_views import *
from .request_views import *

# ✅ 明示的なビュー関数の再インポート（reverse() / テスト対応）

# 📋 シフト操作ビュー
from .shift_views import (
    shift_list,
    add_shift,  # ✅ shift_register 互換用にも使用
    edit_shift,
    delete_shift,
    confirm_delete_shift,
    approve_shift,
    auto_assign,
    export_shift_pdf,
    monthly_shift_summary,
)

# 🙋‍♀️ 勤務希望・休暇申請
from .request_views import (
    shift_request_list,
    add_holiday_request,
    shift_request_api,
    import_shift_requests_csv,
    export_shift_requests_csv,
    import_shift_requests_excel,
    export_shift_requests_excel,
)

# 📂 アップロード関連（CSV/Fixture + 休暇CSVインポート/エクスポート）
from .upload_views import (
    upload_shifts_csv,
    download_error_log_csv,
    upload_employee_csv,
    upload_fixture,
    import_holiday_requests_csv,  # ✅ ← 正しい場所に移動済
    export_holiday_requests_csv,
)

# 🗂️ スタッフ管理
from .staff_views import (
    employee_list,
    employee_create,
    edit_employee,
    employee_detail,
    delete_duplicates,
)

# 💉 透析関連
from .dialysis_views import (
    dialysis_daily_view,
    dialysis_register_view,
    import_dialysis_csv,
    dialysis_pdf_export,
    dialysis_calendar_api_events,
)

# 📅 カレンダー関連
from .calendar_views import (
    calendar_view,
    calendar_event_api,
)

# 📊 ダッシュボード関連
from .dashboard_views import (
    dashboard_view,
    admin_dashboard,
    dashboard_chart_json,
)

# 📄 テンプレート
from .template_views import (
    view_generated_shift_template,
    template_links_view,
)

# 🔐 認証
from .auth_views import (
    logout_view,
    signup_view,
    profile,
)

# ✅ フォームのインポート
from ..forms import *  # type: ignore # shifts/forms.py からフォームをインポート
