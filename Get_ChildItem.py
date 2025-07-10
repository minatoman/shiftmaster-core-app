#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
勤怠システム自動プロンプト生成器
GitHub Copilot Agentに指示する際の条件を自動で付加するプログラム

Author: ShiftMaster System
Date: 2025年6月23日
"""

import sys
import json
import datetime
import subprocess
import threading
import time
import requests
from pathlib import Path
from typing import List, Optional


class ShiftMasterPromptGenerator:
    """勤怠システム用プロンプト自動生成クラス"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.project_name = "ShiftMaster"
        self.version = "2.0.0"
        self.system_conditions = self._load_system_conditions()
        self.templates_dir = self.base_dir / "prompt_templates"
        self.history_dir = self.base_dir / "prompt_history"
        self._ensure_directories()
        
    def _ensure_directories(self):
        """必要なディレクトリを作成"""
        self.templates_dir.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)
        
    def _load_prompt_templates(self) -> dict:
        """プロンプトテンプレートを読み込み"""
        templates = {
            "新機能追加": "新しい機能を追加したい：",
            "バグ修正": "以下のエラーを修正してください：",
            "UI改善": "ユーザーインターフェースを改善したい：",
            "データベース": "データベース関連の処理を実装したい：",
            "API開発": "API機能を開発したい：",
            "セキュリティ": "セキュリティを強化したい：",
            "パフォーマンス": "パフォーマンスを最適化したい：",
            "テスト": "テストコードを作成したい："
        }
        
        # カスタムテンプレートファイルがあれば読み込み
        custom_template_file = self.templates_dir / "custom_templates.json"
        if custom_template_file.exists():
            try:
                with open(custom_template_file, 'r', encoding='utf-8') as f:
                    custom_templates = json.load(f)
                    templates.update(custom_templates)
            except Exception:
                pass
                
        return templates
    
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
    
    def _check_server_status(self, url: str = "http://localhost:8030") -> bool:
        """サーバーの稼働状況を確認"""
        try:
            response = requests.get(url, timeout=3)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def _start_django_server(self, port: int = 8030) -> bool:
        """Django開発サーバーを起動"""
        try:
            print("🚀 Django開発サーバーを起動中...")
            
            # manage.pyの場所を確認
            manage_py = self.base_dir / "manage.py"
            if not manage_py.exists():
                print(f"❌ manage.pyが見つかりません: {manage_py}")
                return False
            
            # サーバー起動コマンド
            cmd = [
                sys.executable, "manage.py", "runserver", f"0.0.0.0:{port}"
            ]
            
            # バックグラウンドでサーバーを起動
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            
            # サーバー起動の待機
            print("⏳ サーバー起動を待機中...")
            for i in range(10):  # 最大10秒待機
                time.sleep(1)
                if self._check_server_status(f"http://localhost:{port}"):
                    print(f"✅ サーバーが正常に起動しました: http://localhost:{port}")
                    return True
                print(f"   待機中... ({i+1}/10)")
            
            print("⚠️  サーバー起動の確認ができませんでした")
            return False
            
        except Exception as e:
            print(f"❌ サーバー起動エラー: {e}")
            return False
    
    def _auto_start_server_if_needed(self) -> str:
        """必要に応じてサーバーを自動起動し、URLを返す"""
        server_url = "http://localhost:8030"
        
        if self._check_server_status(server_url):
            print(f"✅ サーバーは既に稼働中です: {server_url}")
            return server_url
        
        print("🔄 サーバーが稼働していません。自動起動を試行します...")
        
        if self._start_django_server(8030):
            return server_url
        else:
            print("⚠️  自動起動に失敗しました。手動でサーバーを起動してください:")
            print("   python manage.py runserver 0.0.0.0:8030")
            return server_url
