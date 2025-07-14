"""
Production Migration Script
本番環境へのデータ移行スクリプト
"""

import sqlite3
import json
from datetime import datetime


def export_test_data():
    """テストデータをJSONファイルにエクスポート"""

    # SQLiteから データ読み込み
    conn = sqlite3.connect("shiftmaster_test.db")
    cursor = conn.cursor()

    # 従業員データ
    cursor.execute("SELECT * FROM employees")
    employees = []
    for row in cursor.fetchall():
        employees.append(
            {
                "name": row[1],
                "department": row[2],
                "position": row[3],
                "created_at": row[4],
            }
        )

    # シフトデータ
    cursor.execute("SELECT * FROM shifts")
    shifts = []
    for row in cursor.fetchall():
        shifts.append(
            {
                "date": row[1],
                "shift_type": row[2],
                "employee": row[3],
                "created_at": row[4],
            }
        )

    conn.close()

    # JSONエクスポート
    export_data = {
        "export_date": datetime.now().isoformat(),
        "employees": employees,
        "shifts": shifts,
        "metadata": {
            "total_employees": len(employees),
            "total_shifts": len(shifts),
            "source": "shiftmaster_test.db",
        },
    }

    # ファイル保存
    with open("production_data_export.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"✅ データエクスポート完了")
    print(f"📊 従業員: {len(employees)}名")
    print(f"📅 シフト: {len(shifts)}件")
    print(f"💾 ファイル: production_data_export.json")

    return export_data


if __name__ == "__main__":
    export_test_data()
