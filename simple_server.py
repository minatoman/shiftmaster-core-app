#!/usr/bin/env python3
"""
ShiftMaster - シンプルWebサーバー (Python標準ライブラリ使用)
エラーログ監視機能付き
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import json
import os
from datetime import datetime
from pathlib import Path


class ErrorLogHandler(http.server.SimpleHTTPRequestHandler):
    """エラーログ機能付きHTTPハンドラー"""

    # 定数定義
    HTML_CONTENT_TYPE = "text/html; charset=utf-8"
    JSON_CONTENT_TYPE = "application/json"
    SVG_CONTENT_TYPE = "image/svg+xml"

    def __init__(self, *args, **kwargs):
        self.error_log_file = Path("error_logs/web_errors.log")
        self.error_log_file.parent.mkdir(exist_ok=True)
        super().__init__(*args, **kwargs)

    def log_error(self, format_str, *args):
        """エラーをファイルとコンソールに記録"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = f"[{timestamp}] ERROR: {format_str % args}"

        # コンソールに表示
        print(f"\033[91m{error_msg}\033[0m")  # 赤色で表示

        # ファイルに記録
        with open(self.error_log_file, "a", encoding="utf-8") as f:
            f.write(f"{error_msg}\n")

    def log_message(self, format_str, *args):
        """リクエストログ"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {format_str % args}"
        print(f"\033[92m{log_msg}\033[0m")  # 緑色で表示

    def do_GET(self):
        """GETリクエスト処理"""
        try:
            # VSCodeブラウザのパラメータを除去
            clean_path = self.path.split("?")[0]

            if clean_path == "/" or self.path.startswith("/?id="):
                self.send_response(200)
                self.send_header("Content-type", self.HTML_CONTENT_TYPE)
                self.end_headers()

                # メインページHTMLを返す
                html_content = self.get_main_page_html()
                self.wfile.write(html_content.encode("utf-8"))

            elif clean_path == "/favicon.ico":
                # favicon.icoを提供（簡単なSVGアイコン）
                self.send_response(200)
                self.send_header("Content-type", self.SVG_CONTENT_TYPE)
                self.end_headers()

                favicon_svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
    <rect width="32" height="32" fill="#667eea"/>
    <text x="16" y="20" text-anchor="middle" fill="white" font-family="Arial" font-size="16">🏥</text>
</svg>"""
                self.wfile.write(favicon_svg.encode("utf-8"))

            elif clean_path == "/api/test":
                # APIテストエンドポイント
                self.send_response(200)
                self.send_header("Content-type", self.JSON_CONTENT_TYPE)
                self.end_headers()

                response = {
                    "status": "success",
                    "message": "API接続テスト成功",
                    "timestamp": datetime.now().isoformat(),
                }
                self.wfile.write(
                    json.dumps(response, ensure_ascii=False).encode("utf-8")
                )

            elif clean_path == "/api/error-test":
                # 意図的エラーテスト
                self.log_error("テストエラー: 意図的に発生させたエラーです")
                self.send_response(500)
                self.send_header("Content-type", self.JSON_CONTENT_TYPE)
                self.end_headers()

                error_response = {
                    "status": "error",
                    "message": "テストエラーが発生しました",
                    "timestamp": datetime.now().isoformat(),
                }
                self.wfile.write(
                    json.dumps(error_response, ensure_ascii=False).encode("utf-8")
                )

            elif clean_path == "/shift-create":
                # シフト作成ページ
                self.send_response(200)
                self.send_header("Content-type", self.HTML_CONTENT_TYPE)
                self.end_headers()

                html_content = self.get_shift_create_page()
                self.wfile.write(html_content.encode("utf-8"))

            elif clean_path == "/api/shifts":
                # シフト作成・取得API
                shifts = self.get_shift_list()
                self.send_response(200)
                self.send_header("Content-type", self.JSON_CONTENT_TYPE)
                self.end_headers()
                self.wfile.write(json.dumps(shifts, ensure_ascii=False).encode("utf-8"))

            else:
                # 404エラー
                self.log_error(f"存在しないページへのアクセス: {clean_path}")
                self.send_response(404)
                self.send_header("Content-type", self.HTML_CONTENT_TYPE)
                self.end_headers()

                html_content = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>404 - ページが見つかりません</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; margin: 50px; }}
        .error {{ color: #ff6b6b; }}
    </style>
</head>
<body>
    <h1 class="error">404 - ページが見つかりません</h1>
    <p>リクエストされたページ: <code>{clean_path}</code></p>
    <a href="/">🏠 トップページに戻る</a>
</body>
</html>"""
                self.wfile.write(html_content.encode("utf-8"))

        except Exception as e:
            self.log_error(f"予期しないエラー: {str(e)} | パス: {self.path}")
            self.send_response(500)
            self.send_header("Content-type", self.HTML_CONTENT_TYPE)
            self.end_headers()

            error_html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>500 - サーバーエラー</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; margin: 50px; }}
        .error {{ color: #ff6b6b; }}
        .details {{ background: #f8f9fa; padding: 20px; margin: 20px; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1 class="error">500 - サーバーエラー</h1>
    <div class="details">
        <p><strong>エラー詳細:</strong> {str(e)}</p>
        <p><strong>リクエストパス:</strong> {self.path}</p>
        <p><strong>時刻:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    <a href="/">🏠 トップページに戻る</a>
</body>
</html>"""
            self.wfile.write(error_html.encode("utf-8"))

    def do_POST(self):
        """POSTリクエスト処理"""
        try:
            # VSCodeブラウザのパラメータを除去
            clean_path = self.path.split("?")[0]

            if clean_path == "/api/shifts":
                # シフト作成API
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                shift_data = json.loads(post_data.decode("utf-8"))

                # シフトデータを保存
                result = self.save_shift_data(shift_data)

                self.send_response(200 if result["status"] == "success" else 400)
                self.send_header("Content-type", self.JSON_CONTENT_TYPE)
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            else:
                # 404エラー
                self.log_error(f"存在しないPOSTエンドポイント: {clean_path}")
                self.send_response(404)
                self.send_header("Content-type", self.JSON_CONTENT_TYPE)
                self.end_headers()
                error_response = {
                    "status": "error",
                    "message": "エンドポイントが見つかりません",
                }
                self.wfile.write(
                    json.dumps(error_response, ensure_ascii=False).encode("utf-8")
                )

        except Exception as e:
            self.log_error(f"POST処理エラー: {str(e)} | パス: {self.path}")
            self.send_response(500)
            self.send_header("Content-type", self.JSON_CONTENT_TYPE)
            self.end_headers()
            error_response = {"status": "error", "message": f"サーバーエラー: {str(e)}"}
            self.wfile.write(
                json.dumps(error_response, ensure_ascii=False).encode("utf-8")
            )

    def get_main_page_html(self):
        """メインページHTML生成"""
        return """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShiftMaster - 勤務管理システム</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 3em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-top: 10px;
        }
        .button-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .btn {
            background: rgba(255,255,255,0.2);
            border: none;
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-decoration: none;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            font-size: 1.1em;
            display: block;
        }
        .btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        .btn.primary {
            background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        }
        .btn.success {
            background: linear-gradient(45deg, #4ECDC4, #44A08D);
        }
        .btn.warning {
            background: linear-gradient(45deg, #FFD93D, #FF8C42);
        }
        .btn.danger {
            background: linear-gradient(45deg, #FF6B6B, #C44569);
        }
        .status-panel {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        .status-item {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
        }
        .error-log {
            background: rgba(0,0,0,0.5);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        #errorMessages {
            color: #ff6b6b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 ShiftMaster</h1>
            <p class="subtitle">医療従事者向け勤務管理システム</p>
            <p>ポート: 8500 | サーバー稼働中 ✅</p>
        </div>

        <div class="status-panel">
            <h3>📊 システム状態</h3>
            <div class="status-item">
                <span>サーバー状態:</span>
                <span style="color: #4ECDC4;">稼働中</span>
            </div>
            <div class="status-item">
                <span>エラー監視:</span>
                <span style="color: #4ECDC4;">有効</span>
            </div>
            <div class="status-item">
                <span>最終更新:</span>
                <span id="lastUpdate"></span>
            </div>
        </div>

        <div class="button-grid">
            <button class="btn primary" onclick="testLink('勤務表一覧')">
                📅 勤務表一覧
            </button>
            <button class="btn success" onclick="testLink('勤務登録')">
                ➕ 勤務登録
            </button>
            <button class="btn warning" onclick="testLink('スケジュール管理')">
                📋 スケジュール管理
            </button>
            <button class="btn danger" onclick="testLink('設定')">
                ⚙️ 設定
            </button>
            <button class="btn" onclick="testAPI()">
                🔧 API接続テスト
            </button>
            <button class="btn danger" onclick="testError()">
                ⚠️ エラーテスト
            </button>
        </div>

        <div class="error-log">
            <h3>🚨 エラーログ (リアルタイム表示)</h3>
            <div id="errorMessages">エラーなし - システム正常動作中</div>
        </div>
    </div>

    <script>
        // 現在時刻を表示
        function updateTime() {
            document.getElementById('lastUpdate').textContent = new Date().toLocaleString('ja-JP');
        }
        updateTime();
        setInterval(updateTime, 1000);

        // ボタンテスト関数
        function testLink(buttonName) {
            console.log(`${buttonName} ボタンがクリックされました`);
            addErrorMessage(`INFO: ${buttonName} ボタンがクリックされました - ${new Date().toLocaleTimeString()}`);
            
            // 実際のページ遷移をシミュレート（エラーを発生させる）
            fetch('/nonexistent-page')
                .catch(error => {
                    addErrorMessage(`ERROR: ${buttonName} - ページが見つかりません`);
                });
        }

        // API接続テスト
        function testAPI() {
            addErrorMessage('INFO: API接続テストを開始...');
            fetch('/api/test')
                .then(response => response.json())
                .then(data => {
                    addErrorMessage(`SUCCESS: ${data.message}`);
                })
                .catch(error => {
                    addErrorMessage(`ERROR: API接続に失敗 - ${error.message}`);
                });
        }

        // エラーテスト
        function testError() {
            addErrorMessage('INFO: 意図的エラーテストを実行...');
            fetch('/api/error-test')
                .then(response => response.json())
                .then(data => {
                    addErrorMessage(`ERROR: ${data.message}`);
                })
                .catch(error => {
                    addErrorMessage(`ERROR: ${error.message}`);
                });
        }

        // エラーメッセージ追加
        function addErrorMessage(message) {
            const errorDiv = document.getElementById('errorMessages');
            const timestamp = new Date().toLocaleTimeString();
            const newMessage = `[${timestamp}] ${message}`;
            
            if (errorDiv.textContent === 'エラーなし - システム正常動作中') {
                errorDiv.textContent = newMessage;
            } else {
                errorDiv.textContent = newMessage + '\\n' + errorDiv.textContent;
            }
            
            // 最大20行に制限
            const lines = errorDiv.textContent.split('\\n');
            if (lines.length > 20) {
                errorDiv.textContent = lines.slice(0, 20).join('\\n');
            }
        }

        // 5秒ごとにサーバーの状態をチェック
        setInterval(() => {
            fetch('/api/test')
                .then(response => {
                    if (!response.ok) {
                        addErrorMessage('WARNING: サーバー応答に問題があります');
                    }
                })
                .catch(error => {
                    addErrorMessage('ERROR: サーバーとの接続が切断されました');
                });
        }, 5000);
    </script>
</body>
</html>
        """

    def get_shift_create_page(self):
        """シフト作成ページHTML生成"""
        return """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>シフト作成 - ShiftMaster</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
        }
        input, select, textarea {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: rgba(255,255,255,0.9);
            color: #333;
            font-size: 16px;
        }
        .btn {
            background: linear-gradient(45deg, #4ECDC4, #44A08D);
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 10px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .btn.secondary {
            background: linear-gradient(45deg, #FF6B6B, #C44569);
        }
        .shift-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 10px;
            margin: 20px 0;
        }
        .day-header {
            background: rgba(255,255,255,0.2);
            padding: 10px;
            text-align: center;
            border-radius: 5px;
            font-weight: bold;
        }
        .shift-slot {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .shift-slot:hover {
            background: rgba(255,255,255,0.2);
        }
        .shift-slot.selected {
            background: linear-gradient(45deg, #4ECDC4, #44A08D);
        }
        .time-slots {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 10px 0;
        }
        .time-slot {
            padding: 8px 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .time-slot:hover, .time-slot.selected {
            background: linear-gradient(45deg, #FFD93D, #FF8C42);
            color: #333;
        }
        .result-panel {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            display: none;
        }
        .error {
            color: #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .success {
            color: #4ECDC4;
            background: rgba(78, 205, 196, 0.1);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📅 シフト作成</h1>
            <p>新しいシフトを作成・編集します</p>
            <button class="btn secondary" onclick="location.href='/'">🏠 トップページに戻る</button>
        </div>

        <form id="shiftForm">
            <div class="form-group">
                <label for="staffName">👤 スタッフ名</label>
                <input type="text" id="staffName" name="staffName" required placeholder="例: 田中太郎">
            </div>

            <div class="form-group">
                <label for="department">🏥 部署</label>
                <select id="department" name="department" required>
                    <option value="">部署を選択</option>
                    <option value="内科">内科</option>
                    <option value="外科">外科</option>
                    <option value="小児科">小児科</option>
                    <option value="産婦人科">産婦人科</option>
                    <option value="整形外科">整形外科</option>
                    <option value="皮膚科">皮膚科</option>
                    <option value="眼科">眼科</option>
                    <option value="耳鼻咽喉科">耳鼻咽喉科</option>
                    <option value="放射線科">放射線科</option>
                    <option value="看護部">看護部</option>
                    <option value="薬剤部">薬剤部</option>
                    <option value="検査科">検査科</option>
                    <option value="事務">事務</option>
                </select>
            </div>

            <div class="form-group">
                <label for="shiftDate">📅 勤務日</label>
                <input type="date" id="shiftDate" name="shiftDate" required>
            </div>

            <div class="form-group">
                <label>⏰ 勤務時間帯</label>
                <div class="time-slots">
                    <div class="time-slot" data-shift="morning">🌅 日勤 (8:00-17:00)</div>
                    <div class="time-slot" data-shift="evening">🌆 遅番 (12:00-21:00)</div>
                    <div class="time-slot" data-shift="night">🌙 夜勤 (21:00-8:00)</div>
                    <div class="time-slot" data-shift="custom">⚙️ カスタム</div>
                </div>
            </div>

            <div class="form-group" id="customTimeGroup" style="display: none;">
                <label>カスタム時間設定</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <input type="time" id="startTime" name="startTime" placeholder="開始時間">
                    <span>〜</span>
                    <input type="time" id="endTime" name="endTime" placeholder="終了時間">
                </div>
            </div>

            <div class="form-group">
                <label for="position">👔 役職・担当</label>
                <select id="position" name="position">
                    <option value="">選択してください</option>
                    <option value="主任">主任</option>
                    <option value="副主任">副主任</option>
                    <option value="リーダー">リーダー</option>
                    <option value="スタッフ">スタッフ</option>
                    <option value="新人">新人</option>
                    <option value="実習生">実習生</option>
                </select>
            </div>

            <div class="form-group">
                <label for="notes">📝 備考</label>
                <textarea id="notes" name="notes" rows="3" placeholder="特記事項があれば記入してください"></textarea>
            </div>

            <div style="text-align: center;">
                <button type="submit" class="btn">💾 シフトを保存</button>
                <button type="button" class="btn secondary" onclick="clearForm()">🗑️ クリア</button>
                <button type="button" class="btn" onclick="testShift()">🧪 テストデータ作成</button>
            </div>
        </form>

        <div id="resultPanel" class="result-panel">
            <h3>📊 作成結果</h3>
            <div id="resultContent"></div>
        </div>

        <div class="form-group">
            <h3>📋 既存シフト一覧</h3>
            <button type="button" class="btn" onclick="loadShifts()">🔄 シフト一覧を更新</button>
            <div id="shiftList" style="margin-top: 20px;"></div>
        </div>
    </div>

    <script>
        let selectedShift = '';
        
        // 時間帯選択
        document.querySelectorAll('.time-slot').forEach(slot => {
            slot.addEventListener('click', function() {
                document.querySelectorAll('.time-slot').forEach(s => s.classList.remove('selected'));
                this.classList.add('selected');
                selectedShift = this.dataset.shift;
                
                const customGroup = document.getElementById('customTimeGroup');
                if (selectedShift === 'custom') {
                    customGroup.style.display = 'block';
                } else {
                    customGroup.style.display = 'none';
                }
            });
        });

        // フォーム送信
        document.getElementById('shiftForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const shiftData = {
                staffName: formData.get('staffName'),
                department: formData.get('department'),
                shiftDate: formData.get('shiftDate'),
                shiftType: selectedShift,
                startTime: formData.get('startTime'),
                endTime: formData.get('endTime'),
                position: formData.get('position'),
                notes: formData.get('notes'),
                timestamp: new Date().toISOString()
            };

            try {
                const response = await fetch('/api/shifts', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(shiftData)
                });

                const result = await response.json();
                showResult(result, response.ok);
                
                if (response.ok) {
                    clearForm();
                    loadShifts();
                }
            } catch (error) {
                showResult({message: 'エラーが発生しました: ' + error.message}, false);
            }
        });

        // 結果表示
        function showResult(result, isSuccess) {
            const panel = document.getElementById('resultPanel');
            const content = document.getElementById('resultContent');
            
            content.innerHTML = `
                <div class="${isSuccess ? 'success' : 'error'}">
                    ${result.message}
                </div>
                ${isSuccess ? '<p>✅ シフトが正常に保存されました！</p>' : '<p>❌ 保存に失敗しました。'}
            `;
            
            panel.style.display = 'block';
            
            setTimeout(() => {
                panel.style.display = 'none';
            }, 5000);
        }

        // フォームクリア
        function clearForm() {
            document.getElementById('shiftForm').reset();
            document.querySelectorAll('.time-slot').forEach(s => s.classList.remove('selected'));
            selectedShift = '';
            document.getElementById('customTimeGroup').style.display = 'none';
        }

        // テストデータ作成
        function testShift() {
            document.getElementById('staffName').value = '山田花子';
            document.getElementById('department').value = '看護部';
            document.getElementById('shiftDate').value = new Date().toISOString().split('T')[0];
            document.getElementById('position').value = 'スタッフ';
            document.getElementById('notes').value = 'テストシフトデータです';
            
            // 日勤を選択
            document.querySelector('[data-shift="morning"]').click();
        }

        // シフト一覧読み込み
        async function loadShifts() {
            try {
                const response = await fetch('/api/shifts');
                const shifts = await response.json();
                
                const listDiv = document.getElementById('shiftList');
                if (shifts.length === 0) {
                    listDiv.innerHTML = '<p>まだシフトが登録されていません。</p>';
                } else {
                    listDiv.innerHTML = shifts.map(shift => `
                        <div style="background: rgba(255,255,255,0.1); padding: 15px; margin: 10px 0; border-radius: 8px;">
                            <strong>${shift.staffName}</strong> (${shift.department}) - ${shift.shiftDate}
                            <br>勤務: ${getShiftTypeName(shift.shiftType)} ${shift.position ? '/ ' + shift.position : ''}
                            ${shift.notes ? '<br>備考: ' + shift.notes : ''}
                            <br><small>登録: ${new Date(shift.timestamp).toLocaleString('ja-JP')}</small>
                        </div>
                    `).join('');
                }
            } catch (error) {
                document.getElementById('shiftList').innerHTML = '<p class="error">シフト一覧の取得に失敗しました</p>';
            }
        }

        // シフト種別名を取得
        function getShiftTypeName(type) {
            const names = {
                'morning': '🌅 日勤',
                'evening': '🌆 遅番', 
                'night': '🌙 夜勤',
                'custom': '⚙️ カスタム'
            };
            return names[type] || type;
        }

        // 初期化
        document.addEventListener('DOMContentLoaded', function() {
            loadShifts();
            
            // 今日の日付をデフォルトに設定
            document.getElementById('shiftDate').value = new Date().toISOString().split('T')[0];
        });
    </script>
</body>
</html>
        """

    def get_shift_list(self):
        """シフト一覧取得"""
        shifts_file = Path("error_logs/shifts.json")

        if not shifts_file.exists():
            return []

        try:
            with open(shifts_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.log_error(f"シフト一覧取得エラー: {str(e)}")
            return []

    def save_shift_data(self, shift_data):
        """シフトデータ保存"""
        try:
            shifts_file = Path("error_logs/shifts.json")
            shifts_file.parent.mkdir(exist_ok=True)

            # 既存のシフトデータを読み込み
            shifts = []
            if shifts_file.exists():
                with open(shifts_file, "r", encoding="utf-8") as f:
                    shifts = json.load(f)

            # 新しいシフトを追加
            shift_data["id"] = len(shifts) + 1
            shifts.append(shift_data)

            # ファイルに保存
            with open(shifts_file, "w", encoding="utf-8") as f:
                json.dump(shifts, f, ensure_ascii=False, indent=2)

            self.log_message(
                f"シフト作成: {shift_data['staffName']} - {shift_data['shiftDate']}"
            )

            return {
                "status": "success",
                "message": f"シフトが正常に保存されました (ID: {shift_data['id']})",
                "data": shift_data,
            }

        except Exception as e:
            error_msg = f"シフト保存エラー: {str(e)}"
            self.log_error(error_msg)
            return {"status": "error", "message": error_msg}
