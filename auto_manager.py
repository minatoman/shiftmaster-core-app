#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShiftMaster 自動実行・デバッグマネージャー
プロンプト生成器と連携してシステムの自動監視・修正を行う

Author: ShiftMaster System  
Date: 2025年6月23日
"""

import sys
import json
import datetime
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional


class AutoExecutionManager:
    """自動実行・デバッグ管理クラス"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.project_dir = self.base_dir
        self.logs_dir = self.base_dir / "auto_logs"
        self.logs_dir.mkdir(exist_ok=True)
        
    def check_django_status(self) -> Dict[str, bool]:
        """Djangoシステムの状態をチェック"""
        status = {
            "database_connection": False,
            "migrations_applied": False,
            "static_files_collected": False,
            "urls_valid": False,
            "templates_exist": False
        }
        
        try:
            # データベース接続チェック
            result = subprocess.run([
                sys.executable, "manage.py", "check", "--database"
            ], cwd=self.project_dir, capture_output=True, text=True)
            status["database_connection"] = result.returncode == 0
            
            # マイグレーション状態チェック  
            result = subprocess.run([
                sys.executable, "manage.py", "showmigrations"
            ], cwd=self.project_dir, capture_output=True, text=True)
            status["migrations_applied"] = "[ ]" not in result.stdout
            
            # URL設定チェック
            result = subprocess.run([
                sys.executable, "manage.py", "check", "--deploy"
            ], cwd=self.project_dir, capture_output=True, text=True)
            status["urls_valid"] = "ERRORS" not in result.stdout
            
        except Exception as e:
            self._log_error(f"Django状態チェックエラー: {e}")
            
        return status
    
    def auto_fix_issues(self, status: Dict[str, bool]) -> List[str]:
        """検出された問題を自動修正"""
        fixes_applied = []
        
        # マイグレーション未適用の場合
        if not status["migrations_applied"]:
            try:
                subprocess.run([
                    sys.executable, "manage.py", "makemigrations"
                ], cwd=self.project_dir, check=True)
                
                subprocess.run([
                    sys.executable, "manage.py", "migrate"
                ], cwd=self.project_dir, check=True)
                
                fixes_applied.append("✅ データベースマイグレーションを実行")
            except Exception as e:
                self._log_error(f"マイグレーション実行エラー: {e}")
        
        # 静的ファイル収集
        if not status["static_files_collected"]:
            try:
                subprocess.run([
                    sys.executable, "manage.py", "collectstatic", "--noinput"
                ], cwd=self.project_dir, check=True)
                
                fixes_applied.append("✅ 静的ファイルを収集")
            except Exception as e:
                self._log_error(f"静的ファイル収集エラー: {e}")
        
        return fixes_applied
    
    def generate_error_report(self) -> str:
        """エラーレポートを生成"""
        status = self.check_django_status()
        report_lines = [
            "🔍 ShiftMaster システム診断レポート",
            "=" * 50,
            f"生成日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
            "",
            "📊 システム状態:"
        ]
        
        for check, result in status.items():
            icon = "✅" if result else "❌"
            check_name = check.replace("_", " ").title()
            report_lines.append(f"   {icon} {check_name}: {'OK' if result else 'NG'}")
        
        # 自動修正の実行
        fixes = self.auto_fix_issues(status)
        if fixes:
            report_lines.extend([
                "",
                "🔧 自動修正を実行:",
                *[f"   {fix}" for fix in fixes]
            ])
        
        return "\\n".join(report_lines)
    
    def start_auto_monitoring(self, interval: int = 300):
        """自動監視を開始（デフォルト5分間隔）"""
        print(f"🤖 自動監視を開始します（間隔: {interval}秒）")
        print("   Ctrl+C で停止")
        
        try:
            while True:
                print(f"\\n⏰ {datetime.datetime.now().strftime('%H:%M:%S')} - システムチェック実行中...")
                
                report = self.generate_error_report()
                print(report)
                
                # レポートをファイルに保存
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                report_file = self.logs_dir / f"system_report_{timestamp}.txt"
                
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                
                print(f"📝 レポート保存: {report_file}")
                print(f"⏳ {interval}秒後に次回チェック...")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\\n🛑 自動監視を停止しました。")
    
    def _log_error(self, error_message: str):
        """エラーをログファイルに記録"""
        log_file = self.logs_dir / "error.log"
        timestamp = datetime.datetime.now().isoformat()
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {error_message}\\n")


def main():
    """メイン実行関数"""
    manager = AutoExecutionManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "check":
            print("🔍 システム状態をチェック中...")
            report = manager.generate_error_report()
            print(report)
            
        elif command == "monitor":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
            manager.start_auto_monitoring(interval)
            
        elif command == "fix":
            print("🔧 問題の自動修正を実行中...")
            status = manager.check_django_status()
            fixes = manager.auto_fix_issues(status)
            
            if fixes:
                print("✅ 以下の修正を実行しました:")
                for fix in fixes:
                    print(f"   {fix}")
            else:
                print("✅ 修正が必要な問題は見つかりませんでした。")
                
        else:
            print_help()
    else:
        print_help()


def print_help():
    """ヘルプを表示"""
    help_text = """
🤖 ShiftMaster 自動実行・デバッグマネージャー

使用方法:
  python auto_manager.py check           # システム状態をチェック
  python auto_manager.py fix             # 問題を自動修正
  python auto_manager.py monitor [秒]    # 自動監視を開始（デフォルト300秒間隔）

機能:
  ✅ Djangoシステムの状態監視
  ✅ データベース接続チェック
  ✅ マイグレーション状態確認
  ✅ URL設定検証
  ✅ 自動修正機能
  ✅ 定期監視機能
  ✅ エラーログ記録

例:
  python auto_manager.py check
  python auto_manager.py monitor 600    # 10分間隔で監視
  python auto_manager.py fix
"""
    print(help_text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n🛑 処理を中断しました。")
        sys.exit(0)
    except Exception as e:
        print(f"\\n❌ エラーが発生しました: {e}")
        sys.exit(1)
