#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
勤怠システム自動プロンプト生成器 (シンプル版)
GitHub Copilot Agentに指示する際の条件を自動で付加し、サーバーも自動起動

Author: ShiftMaster System
Date: 2025年6月24日
Version: 1.0.1 Simple
"""

import sys
import subprocess
import socket
import time
import datetime
from pathlib import Path
from typing import List, Optional


class ShiftMasterPromptGenerator:
    """勤怠システム用プロンプト自動生成クラス (シンプル版)"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.project_name = "ShiftMaster"
        self.version = "1.0.1-Simple"
        self.system_conditions = self._load_system_conditions()
        
    def _load_system_conditions(self) -> List[str]:
        """システム構築条件を定義"""
        conditions = [
            ("①勤怠システム：https://www.mtrx.co.jp/の中核に記載されている"
             "すべての機能、システムを組み込んで最高の勤怠自動システムの構築"),
            ("②無料AIを組み込んで自動勤務表管理と構築と"
             "個人勤務管理システムとする。"),
            ("③現在のレイアウトをこちらからレイアウト変更の指示を出すまで"
             "変更しないでもらいたい。"),
            ("④できる限り、安定したプログラムの重複がない管理のしやすい"
             "拡張性のあるサイトを目指して作成してほしい。"),
            "⑤毎回タスク画面にエラーの表示を出すようにしてほしい。",
            ("⑥毎回タスクに出たエラーを元にデバッグを行い、"
             "適切なエラー修正を自動で行ってほしい。"),
            "⑦毎回修正が終わったら確認のためのサイトURL（http://localhost:8030）を表示してほしい。",
            ("⑧修正、エラー発見、エラーの追求のためのデバッグ、実行ボタン"
             "継続ボタン続行ボタンが出た場合の自動実行。"),
            ("⑨djangoのviews、URLs、forms、admin、テンプレートが連携されているか"
             "システム上問題はないかを毎回確認する"),
            ("⑩django、Python、PostgreSQL17、使用テンプレートは"
             "Bootstrap 5中心で"),
            ("⑪毎回修正後のレイアウト提案やシステム提案がある場合は、"
             "まず提案文章を掲示してからこちらの実行を待って次に移ってください"),
            ("⑫SQLはH:\\db\\PostgreSQL-17\\pgsql\\binを使って"
             "H:\\Projects\\ShiftMaster\\dbにデータ収納でポートは5333"),
            "⑬現在のシステムを再利用しながらシステム、機能を追加していく",
            ("⑭画像はH:\\Projects\\DjangoProject\\static\\assets\\images内"
             "下層のフォルダ内すべてからマッチするものを選び使用してはめ込んでいって"),
            ("⑮すべてのクリックイベントに関連するフロントエンドエラーまたは"
             "リンク切れ・ナビゲーションエラーの詳細エラーデバッグと確認後の修正を"
             "実施して全ページのクリックイベントに関連するフロントエンドエラーまたは"
             "リンク切れ・ナビゲーションエラーがないようにする"),
            ("⑯自動実行、自動続行、自動継続、自動エラーデバッグ、自動修正、"
             "自動AI構築、自動学習、自動成長のシステムを作成して最高のシステムを"
             "構築して実行してすべての自動化")
        ]
        return conditions
    
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
            print("   Djangoプロジェクトルートで実行してください")
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
            
            print("⚠️ サーバー起動確認できませんでした。手動で起動してください。")
            print("   コマンド: python manage.py runserver 0.0.0.0:8030")
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
    
    def generate_system_prompt(self, user_input: str = "") -> str:
        """
        ユーザー入力にシステム条件を自動付加したプロンプトを生成
        
        Args:
            user_input (str): ユーザーからの質問・指示
            
        Returns:
            str: 条件付きプロンプト
        """
        timestamp = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        # プロンプトヘッダー
        prompt_header = f"""
【勤怠システム開発プロンプト】
生成日時: {timestamp}
プロジェクト: {self.project_name} v{self.version}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【ユーザーからの指示・質問】
{user_input}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【システム構築必須条件】
GitHub Copilot Agentへの指示において、以下の条件を常に満たすこと：
"""
        
        # 条件部分を構築
        conditions_text = "\n".join(self.system_conditions)
        
        # プロンプトフッター
        prompt_footer = """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【技術スタック】
- フレームワーク: Django (最新版)
- データベース: PostgreSQL 17 (ポート: 5333)
- 開発サーバー: http://localhost:8030 (自動起動対応)
- フロントエンド: Bootstrap 5
- 言語: Python 3.x
- データベース場所: H:\\Projects\\ShiftMaster\\db
- 画像リソース: H:\\Projects\\DjangoProject\\static\\assets\\images

【自動化要件】
全てのプロセスを自動化し、エラー検出・修正・継続実行を自動で行う高度なシステムを構築する。

【生成プログラム】
このプロンプトは Get_ChildItem_simple.py により自動生成されました。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return prompt_header + conditions_text + prompt_footer
    
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
    
    def run_simple_mode(self, user_input: str = ""):
        """シンプルモードでプロンプト生成とサーバー起動"""
        print("🚀 ShiftMaster プロンプト生成器 (シンプル版)")
        print("=" * 60)
        
        # サーバー自動起動チェック
        self.ensure_server_running()
        
        if not user_input:
            print("\n📝 GitHub Copilot Agentへの質問・指示を入力してください:")
            user_input = input("💬 ユーザー入力: ").strip()
        
        if not user_input:
            print("⚠️ 入力が空です。")
            return
        
        # プロンプト生成
        generated_prompt = self.generate_system_prompt(user_input)
        
        print("\n" + "=" * 60)
        print("✅ 生成されたプロンプト:")
        print("=" * 60)
        print(generated_prompt)
        print("=" * 60)
        
        # 自動保存
        saved_path = self.save_prompt_to_file(generated_prompt)
        if saved_path:
            print(f"✅ プロンプトが保存されました: {saved_path}")
        
        print("\n🌐 確認用サイト: http://localhost:8030")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


def main():
    """メイン実行関数"""
    generator = ShiftMasterPromptGenerator()
    
    # コマンドライン引数の確認
    if len(sys.argv) > 1:
        # 引数があれば自動モード
        user_input = " ".join(sys.argv[1:])
        generator.run_simple_mode(user_input)
    else:
        # 引数がなければ対話モード
        generator.run_simple_mode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 ユーザーによって中断されました。")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}")
        sys.exit(1)
