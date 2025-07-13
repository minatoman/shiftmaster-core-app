# 🩺 ShiftMaster API Documentation

## 📋 目次

1. [概要](#概要)
2. [認証](#認証)
3. [エンドポイント一覧](#エンドポイント一覧)
4. [データモデル](#データモデル)
5. [エラーハンドリング](#エラーハンドリング)
6. [使用例](#使用例)
7. [レート制限](#レート制限)
8. [SDKとライブラリ](#sdkとライブラリ)

## 🎯 概要

ShiftMaster REST APIは、医療施設のシフト管理システムに対するプログラマティックアクセスを提供します。
このAPIを使用して、シフトスケジュール、スタッフ管理、勤怠記録などの操作を行うことができます。

### 基本情報

- **ベースURL**: `https://your-domain.com/api/v1/`
- **API バージョン**: v1
- **データ形式**: JSON
- **文字エンコーディング**: UTF-8
- **タイムゾーン**: Asia/Tokyo (JST)

### 医療データコンプライアンス

本APIは以下の医療データ保護基準に準拠しています：
- **HIPAA** (Health Insurance Portability and Accountability Act)
- **個人情報保護法** (日本)
- **医療情報システムの安全管理に関するガイドライン**

## 🔐 認証

### Token認証

すべてのAPIリクエストには認証が必要です。以下のヘッダーを含めてください：

```http
Authorization: Token your-api-token-here
Content-Type: application/json
```

### トークン取得

```http
POST /api/v1/auth/token/
Content-Type: application/json

{
  "username": "your-username",
  "password": "your-password"
}
```

**レスポンス**:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "doctor_yamada",
    "email": "yamada@hospital.com",
    "role": "doctor",
    "department": "内科"
  }
}
```

### トークン更新

```http
POST /api/v1/auth/token/refresh/
Authorization: Token your-current-token
```

## 📚 エンドポイント一覧

### 👥 スタッフ管理

#### スタッフ一覧取得

```http
GET /api/v1/staff/
Authorization: Token your-token
```

**クエリパラメータ**:
- `department` (string): 部署でフィルター
- `role` (string): 役職でフィルター
- `status` (string): ステータス (active, inactive)
- `page` (int): ページ番号
- `limit` (int): 1ページあたりの件数 (最大100)

**レスポンス**:
```json
{
  "count": 150,
  "next": "https://api.example.com/api/v1/staff/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "employee_id": "DOC001",
      "first_name": "太郎",
      "last_name": "山田",
      "email": "yamada@hospital.com",
      "department": "内科",
      "role": "doctor",
      "hire_date": "2023-01-15",
      "is_active": true,
      "qualifications": ["医師免許", "内科専門医"],
      "created_at": "2023-01-15T09:00:00+09:00",
      "updated_at": "2024-01-15T14:30:00+09:00"
    }
  ]
}
```

#### スタッフ詳細取得

```http
GET /api/v1/staff/{staff_id}/
Authorization: Token your-token
```

#### スタッフ作成

```http
POST /api/v1/staff/
Authorization: Token your-token
Content-Type: application/json

{
  "employee_id": "NUR023",
  "first_name": "花子",
  "last_name": "佐藤",
  "email": "sato@hospital.com",
  "department": "外科",
  "role": "nurse",
  "hire_date": "2024-01-20",
  "qualifications": ["看護師免許"]
}
```

### 📅 シフト管理

#### シフト一覧取得

```http
GET /api/v1/shifts/
Authorization: Token your-token
```

**クエリパラメータ**:
- `start_date` (date): 開始日 (YYYY-MM-DD)
- `end_date` (date): 終了日 (YYYY-MM-DD)
- `department` (string): 部署
- `staff_id` (int): スタッフID
- `shift_type` (string): シフトタイプ (day, night, on_call)

**レスポンス**:
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "staff": {
        "id": 1,
        "name": "山田太郎",
        "employee_id": "DOC001"
      },
      "date": "2024-01-20",
      "shift_type": "day",
      "start_time": "08:00:00",
      "end_time": "17:00:00",
      "department": "内科",
      "status": "confirmed",
      "notes": "通常勤務",
      "created_at": "2024-01-15T10:00:00+09:00"
    }
  ]
}
```

#### シフト作成

```http
POST /api/v1/shifts/
Authorization: Token your-token
Content-Type: application/json

{
  "staff_id": 1,
  "date": "2024-01-25",
  "shift_type": "day",
  "start_time": "08:00:00",
  "end_time": "17:00:00",
  "department": "内科",
  "notes": "通常勤務"
}
```

#### シフト更新

```http
PUT /api/v1/shifts/{shift_id}/
Authorization: Token your-token
Content-Type: application/json

{
  "status": "confirmed",
  "notes": "変更なし"
}
```

### 🕐 勤怠記録

#### 出勤記録

```http
POST /api/v1/attendance/check-in/
Authorization: Token your-token
Content-Type: application/json

{
  "staff_id": 1,
  "timestamp": "2024-01-20T08:00:00+09:00",
  "location": "main_entrance"
}
```

#### 退勤記録

```http
POST /api/v1/attendance/check-out/
Authorization: Token your-token
Content-Type: application/json

{
  "staff_id": 1,
  "timestamp": "2024-01-20T17:00:00+09:00",
  "location": "main_entrance"
}
```

#### 勤怠履歴取得

```http
GET /api/v1/attendance/
Authorization: Token your-token
```

### 📊 レポート

#### 月次勤怠レポート

```http
GET /api/v1/reports/monthly-attendance/
Authorization: Token your-token
```

**クエリパラメータ**:
- `year` (int): 年
- `month` (int): 月
- `department` (string): 部署

#### シフト充足率レポート

```http
GET /api/v1/reports/shift-coverage/
Authorization: Token your-token
```

## 🏗️ データモデル

### Staff（スタッフ）

```json
{
  "id": "integer",
  "employee_id": "string (unique)",
  "first_name": "string",
  "last_name": "string",
  "email": "string (email format)",
  "department": "string",
  "role": "string (doctor|nurse|admin|other)",
  "hire_date": "date (YYYY-MM-DD)",
  "is_active": "boolean",
  "qualifications": "array of strings",
  "phone_number": "string",
  "emergency_contact": "object",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### Shift（シフト）

```json
{
  "id": "integer",
  "staff_id": "integer",
  "date": "date (YYYY-MM-DD)",
  "shift_type": "string (day|night|on_call)",
  "start_time": "time (HH:MM:SS)",
  "end_time": "time (HH:MM:SS)",
  "department": "string",
  "status": "string (draft|confirmed|cancelled)",
  "notes": "string",
  "created_by": "integer",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### Attendance（勤怠）

```json
{
  "id": "integer",
  "staff_id": "integer",
  "date": "date (YYYY-MM-DD)",
  "check_in_time": "datetime (ISO 8601)",
  "check_out_time": "datetime (ISO 8601)",
  "break_duration": "integer (minutes)",
  "total_hours": "decimal",
  "overtime_hours": "decimal",
  "status": "string (present|absent|late|early_leave)",
  "notes": "string",
  "created_at": "datetime (ISO 8601)"
}
```

## ⚠️ エラーハンドリング

### HTTPステータスコード

- `200 OK`: 正常
- `201 Created`: リソース作成成功
- `400 Bad Request`: リクエストエラー
- `401 Unauthorized`: 認証エラー
- `403 Forbidden`: 権限不足
- `404 Not Found`: リソースが見つからない
- `429 Too Many Requests`: レート制限超過
- `500 Internal Server Error`: サーバーエラー

### エラーレスポンス形式

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力データに問題があります",
    "details": {
      "email": ["有効なメールアドレスを入力してください"],
      "hire_date": ["未来の日付は指定できません"]
    },
    "timestamp": "2024-01-20T10:30:00+09:00",
    "request_id": "req_abc123"
  }
}
```

### 一般的なエラーコード

- `AUTHENTICATION_REQUIRED`: 認証が必要
- `INVALID_TOKEN`: 無効なトークン
- `PERMISSION_DENIED`: 権限不足
- `VALIDATION_ERROR`: バリデーションエラー
- `RESOURCE_NOT_FOUND`: リソースが見つからない
- `RATE_LIMIT_EXCEEDED`: レート制限超過
- `MAINTENANCE_MODE`: メンテナンスモード

## 💡 使用例

### Python (requests)

```python
import requests

# 認証
auth_response = requests.post(
    'https://your-domain.com/api/v1/auth/token/',
    json={
        'username': 'your-username',
        'password': 'your-password'
    }
)
token = auth_response.json()['token']

# ヘッダー設定
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# スタッフ一覧取得
staff_response = requests.get(
    'https://your-domain.com/api/v1/staff/',
    headers=headers
)
staff_list = staff_response.json()

# シフト作成
shift_data = {
    'staff_id': 1,
    'date': '2024-01-25',
    'shift_type': 'day',
    'start_time': '08:00:00',
    'end_time': '17:00:00',
    'department': '内科'
}

shift_response = requests.post(
    'https://your-domain.com/api/v1/shifts/',
    headers=headers,
    json=shift_data
)
```

### JavaScript (fetch)

```javascript
// 認証
const authResponse = await fetch('https://your-domain.com/api/v1/auth/token/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'your-username',
    password: 'your-password'
  })
});

const { token } = await authResponse.json();

// スタッフ一覧取得
const staffResponse = await fetch('https://your-domain.com/api/v1/staff/', {
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  }
});

const staffData = await staffResponse.json();

// 出勤記録
const checkInResponse = await fetch('https://your-domain.com/api/v1/attendance/check-in/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    staff_id: 1,
    timestamp: new Date().toISOString(),
    location: 'main_entrance'
  })
});
```

### cURL

```bash
# 認証
curl -X POST https://your-domain.com/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your-username","password":"your-password"}'

# スタッフ一覧取得
curl -X GET https://your-domain.com/api/v1/staff/ \
  -H "Authorization: Token your-token" \
  -H "Content-Type: application/json"

# シフト作成
curl -X POST https://your-domain.com/api/v1/shifts/ \
  -H "Authorization: Token your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "staff_id": 1,
    "date": "2024-01-25",
    "shift_type": "day",
    "start_time": "08:00:00",
    "end_time": "17:00:00",
    "department": "内科"
  }'
```

## 🚦 レート制限

APIの安定性とパフォーマンスを確保するため、レート制限を設けています：

### 制限内容

- **認証済みユーザー**: 1時間あたり1000リクエスト
- **未認証ユーザー**: 1時間あたり100リクエスト
- **バルク操作**: 1分あたり10リクエスト

### レスポンスヘッダー

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642694400
```

### 制限超過時の対応

レート制限に達した場合、以下のレスポンスが返されます：

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "レート制限に達しました。しばらく待ってから再試行してください。",
    "retry_after": 3600
  }
}
```

## 📦 SDKとライブラリ

### 公式SDK

#### Python SDK

```bash
pip install shiftmaster-python-sdk
```

```python
from shiftmaster import ShiftMasterClient

client = ShiftMasterClient(
    base_url='https://your-domain.com/api/v1/',
    token='your-api-token'
)

# スタッフ一覧取得
staff = client.staff.list(department='内科')

# シフト作成
shift = client.shifts.create(
    staff_id=1,
    date='2024-01-25',
    shift_type='day'
)
```

#### JavaScript SDK

```bash
npm install @shiftmaster/javascript-sdk
```

```javascript
import { ShiftMasterClient } from '@shiftmaster/javascript-sdk';

const client = new ShiftMasterClient({
  baseUrl: 'https://your-domain.com/api/v1/',
  token: 'your-api-token'
});

// スタッフ一覧取得
const staff = await client.staff.list({ department: '内科' });

// 出勤記録
await client.attendance.checkIn({
  staffId: 1,
  timestamp: new Date(),
  location: 'main_entrance'
});
```

## 🔒 セキュリティ

### HTTPS必須

すべてのAPI通信はHTTPS経由で行ってください。HTTP接続は拒否されます。

### トークンセキュリティ

- トークンは安全な場所に保存してください
- 定期的にトークンを更新してください
- トークンをURLパラメータに含めないでください

### データプライバシー

- 患者情報は最小限のアクセス権限で取り扱ってください
- ログには機密情報を記録しないでください
- 監査ログは7年間保持されます

## 📞 サポート

### 技術サポート

- **メール**: api-support@shiftmaster.com
- **ドキュメント**: https://docs.shiftmaster.com
- **ステータスページ**: https://status.shiftmaster.com

### コミュニティ

- **GitHub**: https://github.com/shiftmaster/api
- **フォーラム**: https://community.shiftmaster.com
- **Slack**: https://shiftmaster.slack.com

---

**最終更新**: 2024年1月20日
**APIバージョン**: v1.0.0
