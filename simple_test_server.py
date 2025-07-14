#!/usr/bin/env python3
"""
Simple HTTP server for ShiftMaster
Pythonの組み込みサーバーを使用した基本テスト
"""

import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs
import sqlite3
from datetime import datetime

# ポート設定
PORT = 8000


class ShiftMasterHandler(http.server.SimpleHTTPRequestHandler):
    """ShiftMaster用のHTTPハンドラー"""

    def __init__(self, *args, **kwargs):
        # 静的ファイルのルートディレクトリを設定
        super().__init__(*args, directory="static", **kwargs)

    def do_GET(self):
        """GET リクエストの処理"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/":
            self.serve_dashboard()
        elif parsed_path.path == "/health/":
            self.serve_health_check()
        elif parsed_path.path == "/api/employees/":
            self.serve_api_employees()
        elif parsed_path.path == "/api/shifts/":
            self.serve_api_shifts()
        elif parsed_path.path.startswith("/static/"):
            # 静的ファイル配信
            super().do_GET()
        else:
            self.serve_404()

    def do_POST(self):
        """POST リクエストの処理"""
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/api/employees/":
            self.create_employee()
        elif parsed_path.path == "/api/shifts/":
            self.create_shift()
        else:
            self.serve_404()

    def serve_dashboard(self):
        """ダッシュボード画面"""
        html = """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ShiftMaster - 医療シフト管理システム</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
                .button:hover { background: #2980b9; }
                .success { background: #2ecc71; }
                .warning { background: #f39c12; }
                .danger { background: #e74c3c; }
                .form-group { margin-bottom: 15px; }
                .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
                .form-group input, .form-group select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
                .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                #response { margin-top: 20px; padding: 10px; border-radius: 4px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏥 ShiftMaster</h1>
                    <p>医療機関向け高機能シフト管理システム</p>
                </div>
                
                <div class="grid">
                    <div class="card">
                        <h2>📊 システム状況</h2>
                        <p><strong>サーバー:</strong> <span style="color: #2ecc71;">稼働中</span></p>
                        <p><strong>データベース:</strong> <span style="color: #2ecc71;">接続中</span></p>
                        <p><strong>時刻:</strong> <span id="currentTime"></span></p>
                        <button class="button" onclick="checkHealth()">ヘルスチェック</button>
                        <button class="button danger" onclick="testAlert()">デバッグテスト</button>
                    </div>
                    
                    <div class="card">
                        <h2>👥 従業員管理</h2>
                        <div class="form-group">
                            <label>従業員名:</label>
                            <input type="text" id="empName" placeholder="山田太郎">
                        </div>
                        <div class="form-group">
                            <label>部署:</label>
                            <select id="empDept">
                                <option value="内科">内科</option>
                                <option value="外科">外科</option>
                                <option value="小児科">小児科</option>
                                <option value="看護部">看護部</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>役職:</label>
                            <select id="empPosition">
                                <option value="医師">医師</option>
                                <option value="看護師">看護師</option>
                                <option value="薬剤師">薬剤師</option>
                                <option value="事務">事務</option>
                            </select>
                        </div>
                        <button class="button success" onclick="addEmployee()">従業員追加</button>
                        <button class="button" onclick="loadEmployees()">従業員一覧</button>
                    </div>
                    
                    <div class="card">
                        <h2>📅 シフト管理</h2>
                        <div class="form-group">
                            <label>シフト日:</label>
                            <input type="date" id="shiftDate">
                        </div>
                        <div class="form-group">
                            <label>シフト種別:</label>
                            <select id="shiftType">
                                <option value="日勤">日勤 (8:00-17:00)</option>
                                <option value="夜勤">夜勤 (20:00-8:00)</option>
                                <option value="準夜勤">準夜勤 (16:00-1:00)</option>
                                <option value="深夜勤">深夜勤 (0:00-9:00)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>担当者:</label>
                            <input type="text" id="shiftEmployee" placeholder="従業員名">
                        </div>
                        <button class="button warning" onclick="addShift()">シフト追加</button>
                        <button class="button" onclick="loadShifts()">シフト一覧</button>
                    </div>
                </div>
                
                <div class="card">
                    <h2>📋 応答</h2>
                    <div id="response">操作結果がここに表示されます</div>
                </div>
            </div>
            
            <script>
                // 最小限のJavaScriptテスト
                console.log('JavaScriptテスト開始');
                
                function testAlert() {
                    alert('テスト成功！');
                }
                
                // ページ読み込み完了時
                window.onload = function() {
                    console.log('ページ読み込み完了');
                    document.getElementById('response').innerHTML = '<h3 style="color: green;">JavaScript正常動作中</h3>';
                };
            </script>
            </script>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def serve_health_check(self):
        """ヘルスチェックAPI"""
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "database": "connected",
            "services": {
                "web_server": "running",
                "database": "available",
                "cache": "available",
            },
        }

        self.send_json_response(health_data)

    def serve_api_employees(self):
        """従業員API（GET）"""
        # SQLiteデータベースから従業員データを取得
        employees = self.get_employees_from_db()
        self.send_json_response(employees)

    def serve_api_shifts(self):
        """シフトAPI（GET）"""
        # SQLiteデータベースからシフトデータを取得
        shifts = self.get_shifts_from_db()
        self.send_json_response(shifts)

    def create_employee(self):
        """従業員作成API（POST）"""
        try:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            # データベースに従業員を追加
            employee_id = self.add_employee_to_db(data)

            response_data = {
                "status": "success",
                "message": "従業員が追加されました",
                "employee_id": employee_id,
                "data": data,
            }

            self.send_json_response(response_data, 201)

        except Exception as e:
            self.send_json_response({"error": str(e)}, 400)

    def create_shift(self):
        """シフト作成API（POST）"""
        try:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            # データベースにシフトを追加
            shift_id = self.add_shift_to_db(data)

            response_data = {
                "status": "success",
                "message": "シフトが追加されました",
                "shift_id": shift_id,
                "data": data,
            }

            self.send_json_response(response_data, 201)

        except Exception as e:
            self.send_json_response({"error": str(e)}, 400)

    def serve_404(self):
        """404エラー"""
        self.send_response(404)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """
        <html><body>
        <h1>404 - ページが見つかりません</h1>
        <p><a href="/">ホームに戻る</a></p>
        </body></html>
        """
        self.wfile.write(html.encode("utf-8"))

    def send_json_response(self, data, status_code=200):
        """JSON レスポンスの送信"""
        self.send_response(status_code)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        response_json = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response_json.encode("utf-8"))

    def init_database(self):
        """データベース初期化"""
        conn = sqlite3.connect("shiftmaster_test.db")
        cursor = conn.cursor()

        # 従業員テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # シフトテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                shift_type TEXT NOT NULL,
                employee TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def get_employees_from_db(self):
        """従業員データ取得"""
        self.init_database()
        conn = sqlite3.connect("shiftmaster_test.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()

        employees = []
        for row in rows:
            employees.append(
                {
                    "id": row[0],
                    "name": row[1],
                    "department": row[2],
                    "position": row[3],
                    "created_at": row[4],
                }
            )
        return employees

    def add_employee_to_db(self, data):
        """従業員データ追加"""
        self.init_database()
        conn = sqlite3.connect("shiftmaster_test.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (name, department, position) VALUES (?, ?, ?)",
            (data["name"], data["department"], data["position"]),
        )
        employee_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return employee_id

    def get_shifts_from_db(self):
        """シフトデータ取得"""
        self.init_database()
        conn = sqlite3.connect("shiftmaster_test.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM shifts ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()

        shifts = []
        for row in rows:
            shifts.append(
                {
                    "id": row[0],
                    "date": row[1],
                    "shift_type": row[2],
                    "employee": row[3],
                    "created_at": row[4],
                }
            )
        return shifts

    def add_shift_to_db(self, data):
        """シフトデータ追加"""
        self.init_database()
        conn = sqlite3.connect("shiftmaster_test.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO shifts (date, shift_type, employee) VALUES (?, ?, ?)",
            (data["date"], data["shift_type"], data["employee"]),
        )
        shift_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return shift_id


if __name__ == "__main__":
    print(f"🏥 ShiftMaster テストサーバーを起動中...")
    print(f"📍 ポート: {PORT}")
    print(f"🌐 URL: http://localhost:{PORT}/")
    print(f"💊 ヘルスチェック: http://localhost:{PORT}/health/")
    print("📊 Ctrl+C で停止")

    with socketserver.TCPServer(("", PORT), ShiftMasterHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 サーバーを停止しています...")
            httpd.shutdown()
            print("✅ 停止完了")
