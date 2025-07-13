# 🩺 ShiftMaster - テスト自動化フレームワーク

## 📋 テスト概要

ShiftMasterの品質保証のための包括的テスト戦略を提供します。医療システムとして要求される高い信頼性を確保するため、多層的なテスト手法を採用しています。

## 🧪 テスト構成

### テストピラミッド

```
        🔺 E2Eテスト (5%)
       ────────────────
      🔺 統合テスト (20%)
     ────────────────────
    🔺 単体テスト (75%)
   ────────────────────────
```

### テスト種別

| テスト種別 | 目的 | ツール | 実行頻度 |
|-----------|------|--------|----------|
| **単体テスト** | 個別機能検証 | pytest + Django TestCase | 毎コミット |
| **統合テスト** | API・DB連携検証 | pytest + DRF TestCase | 毎PR |
| **E2Eテスト** | ユーザーシナリオ検証 | Playwright + pytest | 毎リリース |
| **セキュリティテスト** | 脆弱性検証 | bandit + safety | 毎日 |
| **パフォーマンステスト** | 負荷・速度検証 | locust + pytest-benchmark | 毎週 |
| **医療規制テスト** | HIPAA準拠検証 | カスタムテスト | 毎リリース |

## 🚀 テスト実行

### クイック実行

```powershell
# 全テスト実行
.\scripts\run-all-tests.ps1

# 単体テストのみ
.\scripts\run-unit-tests.ps1

# 統合テストのみ
.\scripts\run-integration-tests.ps1

# E2Eテストのみ
.\scripts\run-e2e-tests.ps1
```

### 詳細実行

```powershell
# カバレッジ付き単体テスト
pytest tests/unit/ --cov=shifts --cov=shiftmaster --cov-report=html

# 特定アプリのテスト
pytest tests/unit/test_shifts.py -v

# 統合テスト（データベース使用）
pytest tests/integration/ --reuse-db

# E2Eテスト（ブラウザ使用）
pytest tests/e2e/ --headed --browser=chromium
```

## 📁 テスト構造

```
tests/
├── conftest.py                 # pytest設定・フィクスチャ
├── unit/                       # 単体テスト
│   ├── test_models.py         # モデルテスト
│   ├── test_views.py          # ビューテスト
│   ├── test_forms.py          # フォームテスト
│   ├── test_utils.py          # ユーティリティテスト
│   └── shifts/                # アプリ別テスト
│       ├── test_shift_models.py
│       ├── test_shift_views.py
│       └── test_shift_api.py
├── integration/                # 統合テスト
│   ├── test_api_endpoints.py  # API統合テスト
│   ├── test_database.py       # DB統合テスト
│   ├── test_authentication.py # 認証統合テスト
│   └── test_workflows.py      # ワークフロー統合テスト
├── e2e/                        # E2Eテスト
│   ├── test_user_registration.py
│   ├── test_shift_management.py
│   ├── test_admin_workflows.py
│   └── test_mobile_responsive.py
├── security/                   # セキュリティテスト
│   ├── test_hipaa_compliance.py
│   ├── test_data_encryption.py
│   ├── test_access_control.py
│   └── test_audit_logging.py
├── performance/                # パフォーマンステスト
│   ├── test_load_testing.py
│   ├── test_stress_testing.py
│   ├── test_database_performance.py
│   └── locustfile.py
└── fixtures/                   # テストデータ
    ├── sample_users.json
    ├── sample_shifts.json
    ├── medical_test_data.json
    └── compliance_test_cases.json
```

## 🔧 テスト設定

### pytest設定 (pytest.ini)

```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = shiftmaster.settings.testing
addopts = 
    --strict-markers
    --strict-config
    --verbose
    --tb=short
    --cov=shifts
    --cov=shiftmaster
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=xml
    --cov-fail-under=85
    --reuse-db
    --nomigrations
markers =
    unit: 単体テスト
    integration: 統合テスト
    e2e: E2Eテスト
    security: セキュリティテスト
    performance: パフォーマンステスト
    slow: 実行時間の長いテスト
    hipaa: HIPAA準拠テスト
    critical: 重要機能テスト
    api: APIテスト
    database: データベーステスト
python_files = test_*.py
python_classes = Test*
python_functions = test_*
testpaths = tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

### テスト専用設定 (settings/testing.py)

```python
from .base import *

# テスト専用データベース
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'OPTIONS': {
            'timeout': 20,
        }
    }
}

# テスト高速化
DEBUG = False
TEMPLATE_DEBUG = False
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# キャッシュ無効化
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# メール送信無効化
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# ファイルストレージ無効化
DEFAULT_FILE_STORAGE = 'django.core.files.storage.InMemoryStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# ログ簡素化
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
}

# セキュリティ設定（テスト用）
SECRET_KEY = 'test-secret-key-not-for-production'
MEDICAL_DATA_ENCRYPTION_KEY = 'test-encryption-key-32-bytes!!'

# 外部サービス無効化
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
```

## 📝 テスト例

### 単体テスト例

```python
# tests/unit/shifts/test_shift_models.py
import pytest
from datetime import date, time
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from shifts.models import Shift, Staff, Department

User = get_user_model()

@pytest.mark.django_db
class TestShiftModel:
    """シフトモデルの単体テスト"""
    
    def test_shift_creation(self, staff_user, department):
        """正常なシフト作成テスト"""
        shift = Shift.objects.create(
            staff=staff_user,
            date=date(2024, 1, 20),
            start_time=time(9, 0),
            end_time=time(17, 0),
            department=department,
            shift_type='day'
        )
        assert shift.staff == staff_user
        assert shift.duration == 8.0
        assert str(shift) == f"{staff_user.get_full_name()} - 2024-01-20 (日勤)"
    
    def test_shift_overlap_validation(self, staff_user, department):
        """シフト重複バリデーションテスト"""
        # 最初のシフト作成
        Shift.objects.create(
            staff=staff_user,
            date=date(2024, 1, 20),
            start_time=time(9, 0),
            end_time=time(17, 0),
            department=department
        )
        
        # 重複するシフト作成（エラーになるべき）
        with pytest.raises(ValidationError):
            shift = Shift(
                staff=staff_user,
                date=date(2024, 1, 20),
                start_time=time(13, 0),
                end_time=time(21, 0),
                department=department
            )
            shift.full_clean()
    
    def test_shift_medical_compliance(self, staff_user, department):
        """医療法準拠テスト（連続勤務制限）"""
        # 7日連続勤務を作成
        for day in range(7):
            Shift.objects.create(
                staff=staff_user,
                date=date(2024, 1, 1) + timedelta(days=day),
                start_time=time(9, 0),
                end_time=time(17, 0),
                department=department
            )
        
        # 8日目のシフト作成（制限に引っかかるべき）
        with pytest.raises(ValidationError, match="連続勤務日数制限"):
            shift = Shift(
                staff=staff_user,
                date=date(2024, 1, 8),
                start_time=time(9, 0),
                end_time=time(17, 0),
                department=department
            )
            shift.full_clean()
```

### 統合テスト例

```python
# tests/integration/test_api_endpoints.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from shifts.models import Shift

User = get_user_model()

@pytest.mark.django_db
class TestShiftAPI:
    """シフトAPI統合テスト"""
    
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testdoc',
            email='test@hospital.com',
            password='testpass123',
            role='doctor'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_shift_via_api(self, department):
        """API経由でのシフト作成テスト"""
        data = {
            'staff': self.user.id,
            'date': '2024-01-20',
            'start_time': '09:00:00',
            'end_time': '17:00:00',
            'department': department.id,
            'shift_type': 'day'
        }
        
        response = self.client.post('/api/v1/shifts/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Shift.objects.count() == 1
        shift = Shift.objects.first()
        assert shift.staff == self.user
        assert shift.duration == 8.0
    
    def test_unauthorized_access(self):
        """未認証アクセステスト"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/shifts/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_hipaa_audit_logging(self, department):
        """HIPAA監査ログテスト"""
        data = {
            'staff': self.user.id,
            'date': '2024-01-20',
            'start_time': '09:00:00',
            'end_time': '17:00:00',
            'department': department.id
        }
        
        response = self.client.post('/api/v1/shifts/', data)
        
        # 監査ログが作成されているか確認
        from audit.models import AuditLog
        audit_logs = AuditLog.objects.filter(
            user=self.user,
            action='CREATE',
            model_name='Shift'
        )
        assert audit_logs.exists()
        assert 'shift_creation' in audit_logs.first().details
```

### E2Eテスト例

```python
# tests/e2e/test_shift_management.py
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
class TestShiftManagementWorkflow:
    """シフト管理E2Eテスト"""
    
    def test_doctor_creates_shift(self, page: Page, live_server):
        """医師がシフトを作成するワークフロー"""
        # ログインページへ移動
        page.goto(f"{live_server.url}/login/")
        
        # ログイン
        page.fill('[name="username"]', 'doctor@hospital.com')
        page.fill('[name="password"]', 'testpass123')
        page.click('button[type="submit"]')
        
        # シフト管理ページへ移動
        page.click('text=シフト管理')
        expect(page).to_have_url(f"{live_server.url}/shifts/")
        
        # 新規シフト作成
        page.click('text=新規シフト作成')
        page.select_option('[name="department"]', '内科')
        page.fill('[name="date"]', '2024-01-20')
        page.select_option('[name="shift_type"]', 'day')
        page.fill('[name="start_time"]', '09:00')
        page.fill('[name="end_time"]', '17:00')
        
        # 作成実行
        page.click('button[type="submit"]')
        
        # 成功メッセージ確認
        expect(page.locator('.alert-success')).to_contain_text('シフトが作成されました')
        
        # シフト一覧に表示されることを確認
        expect(page.locator('.shift-list')).to_contain_text('2024-01-20')
        expect(page.locator('.shift-list')).to_contain_text('日勤')
    
    def test_mobile_responsive_design(self, page: Page, live_server):
        """モバイル対応テスト"""
        # モバイルサイズに設定
        page.set_viewport_size({"width": 375, "height": 667})
        
        page.goto(f"{live_server.url}/")
        
        # ハンバーガーメニューが表示されるか
        expect(page.locator('.navbar-toggler')).to_be_visible()
        
        # メニューをクリック
        page.click('.navbar-toggler')
        expect(page.locator('.navbar-collapse')).to_be_visible()
        
        # シフト一覧がモバイルで適切に表示されるか
        page.click('text=シフト管理')
        expect(page.locator('.table-responsive')).to_be_visible()
```

### セキュリティテスト例

```python
# tests/security/test_hipaa_compliance.py
import pytest
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from audit.models import AuditLog
from shifts.models import Shift

User = get_user_model()

@pytest.mark.hipaa
class TestHIPAACompliance:
    """HIPAA準拠テスト"""
    
    @pytest.mark.django_db
    def test_patient_data_encryption(self):
        """患者データ暗号化テスト"""
        from medical.models import PatientData
        from medical.encryption import encrypt_medical_data
        
        # 機密医療データ
        sensitive_data = {
            'patient_id': 'P12345',
            'diagnosis': '高血圧症',
            'medication': 'アムロジピン 5mg'
        }
        
        # 暗号化してDB保存
        patient_data = PatientData.objects.create(
            encrypted_data=encrypt_medical_data(sensitive_data)
        )
        
        # DBに平文で保存されていないことを確認
        assert '高血圧症' not in str(patient_data.encrypted_data)
        assert 'アムロジピン' not in str(patient_data.encrypted_data)
        
        # 復号化が正常に動作することを確認
        decrypted = patient_data.get_decrypted_data()
        assert decrypted['diagnosis'] == '高血圧症'
    
    @pytest.mark.django_db
    def test_audit_trail_creation(self, staff_user, department):
        """監査証跡作成テスト"""
        # シフト作成
        shift = Shift.objects.create(
            staff=staff_user,
            date=date(2024, 1, 20),
            start_time=time(9, 0),
            end_time=time(17, 0),
            department=department
        )
        
        # 監査ログが自動作成されることを確認
        audit_logs = AuditLog.objects.filter(
            user=staff_user,
            action='CREATE',
            model_name='Shift',
            object_id=shift.id
        )
        assert audit_logs.exists()
        
        # 必要な情報が記録されていることを確認
        log = audit_logs.first()
        assert log.ip_address is not None
        assert log.user_agent is not None
        assert log.timestamp is not None
        assert 'shift_data' in log.details
    
    def test_data_retention_policy(self):
        """データ保持ポリシーテスト"""
        from medical.management.commands import cleanup_old_data
        
        # 8年前のデータ作成（保持期限7年を超過）
        old_date = date.today() - timedelta(days=8*365)
        
        # 古いデータがクリーンアップされることを確認
        # (実際の実装に応じてテスト内容を調整)
        pass
```

### パフォーマンステスト例

```python
# tests/performance/locustfile.py
from locust import HttpUser, task, between
import random

class ShiftMasterUser(HttpUser):
    """負荷テスト用ユーザー行動シミュレーション"""
    
    wait_time = between(1, 3)
    
    def on_start(self):
        """テスト開始時のログイン"""
        response = self.client.post("/api/v1/auth/token/", json={
            "username": "loadtest@hospital.com",
            "password": "loadtest123"
        })
        if response.status_code == 200:
            self.token = response.json()["token"]
            self.client.headers.update({"Authorization": f"Token {self.token}"})
    
    @task(3)
    def view_shifts(self):
        """シフト一覧表示（最も頻繁な操作）"""
        self.client.get("/api/v1/shifts/")
    
    @task(2)
    def view_staff(self):
        """スタッフ一覧表示"""
        self.client.get("/api/v1/staff/")
    
    @task(1)
    def create_shift(self):
        """シフト作成（重い処理）"""
        shift_data = {
            "staff_id": random.randint(1, 10),
            "date": "2024-01-20",
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "department": "内科",
            "shift_type": "day"
        }
        self.client.post("/api/v1/shifts/", json=shift_data)
    
    @task(1)
    def search_shifts(self):
        """シフト検索"""
        params = {
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "department": "内科"
        }
        self.client.get("/api/v1/shifts/", params=params)
```

## 🔄 CI/CD統合

### GitHub Actions ワークフロー

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements/testing.txt
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ --cov --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  integration-tests:
    needs: unit-tests
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
      redis:
        image: redis:7
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements/testing.txt
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v

  e2e-tests:
    needs: integration-tests
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements/testing.txt
        playwright install
    
    - name: Run E2E tests
      run: |
        pytest tests/e2e/ --headed=false
    
    - name: Upload test artifacts
      uses: actions/upload-artifact@v3
      if: failure()
      with:
        name: e2e-artifacts
        path: test-results/

  security-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install security tools
      run: |
        pip install bandit safety semgrep
    
    - name: Run security scan
      run: |
        bandit -r . -ll -f json -o bandit-report.json
        safety check --json --output safety-report.json
        semgrep --config=auto --json -o semgrep-report.json
    
    - name: Run HIPAA compliance tests
      run: |
        pytest tests/security/ -m hipaa -v
```

## 📊 テストメトリクス

### カバレッジ要件

- **最小カバレッジ**: 85%
- **重要機能**: 95%以上
- **セキュリティ機能**: 100%
- **医療規制関連**: 100%

### 品質ゲート

```yaml
# テスト品質ゲート設定
quality_gates:
  unit_test_coverage: 85%
  integration_test_coverage: 75%
  security_test_coverage: 100%
  performance_response_time: 200ms
  error_rate: 0.1%
  security_vulnerabilities: 0
```

## 🛠️ 継続的改善

### テストメンテナンス

```powershell
# テストデータクリーンアップ
.\scripts\cleanup-test-data.ps1

# テストカバレッジレポート生成
.\scripts\generate-coverage-report.ps1

# フレイキーテスト検出
.\scripts\detect-flaky-tests.ps1

# パフォーマンステストレポート
.\scripts\performance-test-report.ps1
```

### テスト分析

```powershell
# テスト実行時間分析
pytest tests/ --durations=10

# メモリ使用量プロファイリング
pytest tests/ --profile-svg

# テスト依存関係分析
.\scripts\analyze-test-dependencies.ps1
```

---

**最終更新**: 2024年1月20日  
**テストフレームワークバージョン**: 1.0.0
