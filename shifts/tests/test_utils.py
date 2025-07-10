# shifts/tests/test_utils.py
from django.contrib.auth.models import User
from shifts.models import Employee

def create_test_employee(name="田中", email="tanaka@example.com", position="看護師", 
                         department="透析室", employment_type="常勤", work_details={"業務": "透析看護"}):
    """
    Test用のEmployeeインスタンスを作成する関数。

    引数:
    - name (str): 名前
    - email (str): メールアドレス
    - position (str): 役職
    - department (str): 部署
    - employment_type (str): 雇用形態（必須フィールド）
    - work_details (dict): 業務内容（必須フィールド）

    戻り値:
    - Employeeインスタンス
    """
    # Userの作成
    user = User.objects.create_user(username=email.split('@')[0], password="testpass")

    # Employeeの作成
    employee = Employee.objects.create(
        name=name,
        email=email,
        position=position,
        department=department,
        employment_type=employment_type,  # 必須フィールド
        work_details=work_details,  # 必須フィールド
        user=user  # 必須フィールド
    )

    return employee

