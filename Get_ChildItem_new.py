#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShiftMaster プロンプト生成器（デバッグ機能強化版）
GitHub Copilot Agent用の16項目必須条件自動付加＋エラーハンドリング強化

主な機能:
- 16項目の必須条件を自動付加してプロンプト生成
- サーバー自動起動（Django 8030番ポート）
- エラー発生時の詳細デバッグ情報表示・保存
- 対話式モード・コマンドライン引数モード対応
- プロンプト保存機能
"""

import sys
import os
import json
import datetime
import socket
import subprocess
import time
import traceback
import platform
from pathlib import Path
from typing import List, Optional


class ShiftMasterPromptGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.project_name = "ShiftMaster"
        self.version = "1.3.0"
        
        # 16項目の必須条件
        self.system_conditions = [
            "このシステムは勤怠管理システム「ShiftMaster」です",
            "使用技術: Django + PostgreSQL 17 + Bootstrap 5",
            "開発サーバー: http://localhost:8030 で稼働",
            "データベースポート: 5432 (PostgreSQL)",
            "データベースパス: H:\\Projects\\ShiftMaster\\db",
            "プロジェクトルート: H:\\Projects\\ShiftMaster",
            "エラー発生時は詳細なデバッグ情報を画面表示・ファイル保存",
            "利用者の操作性を最優先に設計",
            "画像リソース: H:\\Projects\\DjangoProject\\static\\assets\\images",
            "スタッフ管理・シフト管理・勤怠記録機能を提供",
            "透析患者の勤怠管理に特化した機能",
            "CSV出力・Excel出力機能を標準搭載",
            "レスポンシブデザイン対応（Bootstrap 5利用）",
            "データバックアップ・復元機能",
            "管理者権限とスタッフ権限の分離",
            "日本語UI・日本の勤怠慣習に準拠"
        ]

    def generate_system_prompt(self, user_input: str) -> str:
        """16項目の必須条件を自動付加してシステムプロンプトを生成"""
        conditions_text = "\n".join([f"- {condition}" for condition in self.system_conditions])
        
        generated_prompt = f"""# ShiftMaster 勤怠システム - GitHub Copilot Agent用プロンプト

## システム概要・必須条件（必ず遵守）:
{conditions_text}

## ユーザーからの要求:
{user_input}

## 指示:
上記のシステム概要・必須条件を必ず遵守しながら、ユーザーの要求に応えてください。
エラー発生時は詳細なデバッグ情報を表示し、修正案を提示してください。
コードの品質・保守性・操作性を最優先に考慮してください。

生成日時: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return generated_prompt

    def save_prompt_to_file(self, prompt: str, filename: Optional[str] = None) -> str:
        """生成したプロンプトをファイルに保存"""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_prompt_{timestamp}.txt"
        
        filepath = self.base_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(prompt)
            return str(filepath)
        except Exception as e:
            print(f"❌ ファイル保存エラー: {e}")
            return ""

    def show_recent_error_logs(self):
        """最近のエラーログを表示"""
        try:
            error_log_dir = "error_logs"
            if not os.path.exists(error_log_dir):
                print("📋 エラーログはまだありません。")
                return
                
            log_files = [f for f in os.listdir(error_log_dir) 
                        if f.startswith('error_debug_') and f.endswith('.json')]
            
            if not log_files:
                print("📋 エラーログはまだありません。")
                return
                
            # 最新の5つのログファイルを表示
            log_files.sort(reverse=True)
            print("\n📋 最近のエラーログ (最新5件):")
            print("-" * 50)
            
            for i, log_file in enumerate(log_files[:5]):
                log_path = os.path.join(error_log_dir, log_file)
                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        log_data = json.load(f)
                    
                    print(f"{i+1}. {log_data['timestamp']} - {log_data['error_type']}")
                    print(f"   場所: {log_data['context']}")
                    print(f"   メッセージ: {log_data['error_message']}")
                    print()
                except Exception as e:
                    print(f"   ログ読み込みエラー: {log_file} - {e}")
                    
        except Exception as e:
            print(f"❌ ログ表示エラー: {e}")

    def interactive_mode(self):
        """対話式モードでプロンプト生成（エラーハンドリング強化版）"""
        print("=" * 60)
        print("🚀 ShiftMaster 勤怠システム プロンプト生成器")
        print("=" * 60)
        print()
        
        # 初期サーバー起動チェック
        self.safe_execute(
            self.ensure_server_running,
            context="interactive_mode - サーバー起動チェック"
        )
        
        while True:
            try:
                print("📝 GitHub Copilot Agentへの質問・指示を入力してください:")
                print("   (終了する場合は 'exit' または 'quit' を入力)")
                print("   (エラーログ確認は 'logs' を入力)")
                print("-" * 60)
                
                user_input = input("💬 ユーザー入力: ").strip()
                
                # 終了コマンド
                if user_input.lower() in ['exit', 'quit', '終了', 'q']:
                    print("👋 プロンプト生成器を終了します。")
                    break
                
                # ログ確認コマンド
                if user_input.lower() == 'logs':
                    self.show_recent_error_logs()
                    continue
                
                # 空入力チェック
                if not user_input:
                    print("⚠️  入力が空です。質問や指示を入力してください。")
                    continue
                
                # プロンプト生成（安全実行）
                generated_prompt = self.safe_execute(
                    self.generate_system_prompt,
                    user_input,
                    context="interactive_mode - プロンプト生成"
                )
                
                if generated_prompt is None:
                    print("❌ プロンプト生成に失敗しました。続行しますか？")
                    continue_choice = input("続行する場合はEnterキーを押してください: ")
                    continue
                
                print("\n" + "=" * 60)
                print("✅ 生成されたプロンプト:")
                print("=" * 60)
                print(generated_prompt)
                print("=" * 60)
                
                # ファイル保存の確認
                save_choice = input(
                    "\n💾 このプロンプトをファイルに保存しますか？ (y/n): "
                ).strip().lower()
                
                if save_choice in ['y', 'yes', 'はい']:
                    saved_path = self.safe_execute(
                        self.save_prompt_to_file,
                        generated_prompt,
                        context="interactive_mode - ファイル保存"
                    )
                    
                    if saved_path:
                        print(f"✅ プロンプトが保存されました: {saved_path}")
                    else:
                        print("❌ ファイル保存に失敗しました。")
                
                print("\n" + "-" * 60)
                
            except KeyboardInterrupt:
                print("\n\n⚠️  中断されました。終了しますか？ (y/n): ", end="")
                try:
                    if input().strip().lower() in ['y', 'yes', 'はい']:
                        break
                    else:
                        print("続行します...")
                except:
                    break
                    
            except Exception as e:
                self.show_error_debug_info(e, "interactive_mode - 予期しないエラー")
                print("⚠️  エラーが発生しましたが、プログラムは継続します。")
                continue

    def auto_generate_from_args(self, user_input: str) -> str:
        """コマンドライン引数からプロンプトを自動生成"""
        # サーバー自動起動チェック
        self.ensure_server_running()
        
        generated_prompt = self.generate_system_prompt(user_input)
        
        # 自動保存
        saved_path = self.save_prompt_to_file(generated_prompt)
        
        print("🚀 ShiftMaster プロンプト生成器 - 自動モード")
        print("=" * 60)
        print(generated_prompt)
        print("=" * 60)
        
        if saved_path:
            print(f"✅ プロンプトが自動保存されました: {saved_path}")
        
        return generated_prompt

    def export_conditions_json(self) -> str:
        """システム条件をJSONファイルにエクスポート"""
        conditions_data = {
            "project_name": self.project_name,
            "version": self.version,
            "generated_at": datetime.datetime.now().isoformat(),
            "system_conditions": self.system_conditions,
            "technical_stack": {
                "framework": "Django",
                "database": "PostgreSQL 17",
                "database_port": 5432,
                "development_server": "http://localhost:8030",
                "frontend": "Bootstrap 5",
                "language": "Python 3.x",
                "database_path": "H:\\Projects\\ShiftMaster\\db",
                "image_resources": "H:\\Projects\\DjangoProject\\static\\assets\\images"
            }
        }
        
        filename = "shiftmaster_conditions.json"
        filepath = self.base_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conditions_data, f, ensure_ascii=False, indent=2)
            return str(filepath)
        except Exception as e:
            print(f"❌ JSON出力エラー: {e}")
            return ""

    def is_server_running(self, host="localhost", port=8030) -> bool:
        """指定ポートでサーバーが稼働しているか確認"""
        try:
            with socket.create_connection((host, port), timeout=2):
                return True
        except Exception:
            return False

    def start_django_server(self):
        """Django開発サーバーをバックグラウンドで起動"""
        manage_py = self.base_dir / "manage.py"
        if not manage_py.exists():
            print(f"❌ manage.pyが見つかりません: {manage_py}")
            return False
        
        try:
            print("🔄 Djangoサーバーを起動しています...")
            subprocess.Popen(
                [sys.executable, str(manage_py), "runserver", "0.0.0.0:8030"],
                cwd=str(self.base_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            
            # サーバー起動待機
            for i in range(15):  # 15秒まで待機
                if self.is_server_running():
                    print("✅ Djangoサーバーが起動しました: http://localhost:8030")
                    return True
                print(f"⏳ サーバー起動中... ({i+1}/15)")
                time.sleep(1)
            
            print("⚠️ サーバー起動確認できませんでした。")
            return False
        except Exception as e:
            print(f"❌ サーバー起動エラー: {e}")
            return False

    def ensure_server_running(self):
        """サーバーが稼働していなければ自動起動"""
        if self.is_server_running():
            print("✅ サーバーは既に稼働中です: http://localhost:8030")
            return True
        else:
            print("🔄 サーバーが稼働していません。自動起動します...")
            return self.start_django_server()

    def show_error_debug_info(self, error: Exception, context: str = ""):
        """エラー発生時の詳細デバッグ情報を表示・保存"""
        error_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        debug_info = {
            'timestamp': error_time,
            'context': context,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'system_info': {
                'platform': platform.platform(),
                'python_version': sys.version,
                'working_directory': os.getcwd()
            }
        }
        
        print("\n" + "🚨" * 30)
        print("❌ エラーが発生しました - デバッグ情報")
        print("🚨" * 30)
        print(f"⏰ 発生時刻: {error_time}")
        print(f"📍 発生場所: {context}")
        print(f"🔍 エラータイプ: {debug_info['error_type']}")
        print(f"📝 エラーメッセージ: {debug_info['error_message']}")
        print("\n📋 詳細なトレースバック:")
        print("-" * 50)
        print(debug_info['traceback'])
        print("-" * 50)
        
        # 推奨修正案の表示
        self.show_suggested_fixes(error, context)
        
        # エラー情報をファイルに保存
        self.save_error_debug_info(debug_info)
        
        print("\n💡 修正後、Enterキーを押すと続行できます...")
        input()

    def show_suggested_fixes(self, error: Exception, context: str):
        """エラーに応じた推奨修正案を表示"""
        print("\n🔧 推奨修正案:")
        print("-" * 30)
        
        error_type = type(error).__name__
        error_msg = str(error).lower()
        
        if error_type == "ModuleNotFoundError":
            if "django" in error_msg:
                print("• Djangoがインストールされていません")
                print("  修正: pip install django")
            elif "psycopg2" in error_msg:
                print("• PostgreSQLドライバがインストールされていません")
                print("  修正: pip install psycopg2-binary")
            else:
                print(f"• 必要なモジュールがインストールされていません: {error}")
                print("  修正: pip install [モジュール名]")
                
        elif error_type == "ConnectionError" or "connection" in error_msg:
            if "database" in context.lower():
                print("• データベースサーバーが起動していません")
                print("  修正: PostgreSQLサーバーを起動してください")
            elif "django" in context.lower():
                print("• Djangoサーバーが起動していません")
                print("  修正: python manage.py runserver 0.0.0.0:8030")
                
        elif error_type == "FileNotFoundError":
            print("• ファイルまたはディレクトリが見つかりません")
            print(f"  修正: 指定されたパスを確認してください: {error}")
            
        elif error_type == "PermissionError":
            print("• ファイルアクセス権限エラー")
            print("  修正: 管理者権限で実行するか、ファイル権限を確認してください")
            
        elif "syntax" in error_type.lower():
            print("• Pythonコードの構文エラー")
            print("  修正: コードの記述を確認し、適切な構文に修正してください")
            
        else:
            print(f"• 一般的なエラー: {error_type}")
            print("  修正: エラーメッセージを参考に問題を特定してください")

    def save_error_debug_info(self, debug_info: dict):
        """エラーデバッグ情報をファイルに保存"""
        try:
            error_log_dir = "error_logs"
            os.makedirs(error_log_dir, exist_ok=True)
            
            timestamp = debug_info['timestamp'].replace(':', '-').replace(' ', '_')
            filename = f"{error_log_dir}/error_debug_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(debug_info, f, ensure_ascii=False, indent=2)
                
            print(f"💾 デバッグ情報が保存されました: {filename}")
            
        except Exception as save_error:
            print(f"⚠️ デバッグ情報の保存に失敗: {save_error}")

    def safe_execute(self, func, *args, context: str = "", **kwargs):
        """安全な関数実行（エラーハンドリング付き）"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.show_error_debug_info(e, context)
            return None


def main():
    """メイン実行関数"""
    generator = ShiftMasterPromptGenerator()
    
    if len(sys.argv) > 1:
        # コマンドライン引数モード
        user_input = " ".join(sys.argv[1:])
        generator.auto_generate_from_args(user_input)
    else:
        # 対話式モード
        generator.interactive_mode()


if __name__ == "__main__":
    main()
