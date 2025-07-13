# 📋 運用チェックリスト・SOP

## 🔄 日次運用チェックリスト

### 🌅 朝のシステムチェック（8:00）

```markdown
## 日次チェックリスト - 朝 (8:00)
実施者: ___________  実施日: ___________

### システム稼働状況
- [ ] Webアプリケーション正常応答確認 (http://localhost:8000/health/)
- [ ] データベース接続確認 (PostgreSQL)
- [ ] Redis キャッシュサービス確認
- [ ] Celery Worker プロセス確認
- [ ] Nginx プロキシサーバー確認

### リソース使用状況
- [ ] CPU使用率 < 70%
- [ ] メモリ使用率 < 80%
- [ ] ディスク使用率 < 80%
- [ ] ネットワーク帯域使用率正常

### セキュリティ確認
- [ ] 不正アクセス試行ログ確認
- [ ] SSL証明書有効期限確認 (30日以上)
- [ ] バックアップファイル整合性確認
- [ ] セキュリティアップデート確認

### 業務データ確認
- [ ] 前日シフトデータ整合性確認
- [ ] 新規スタッフ登録処理確認
- [ ] システムエラーログ確認 (重要度HIGH以上)
- [ ] ユーザーからの問い合わせ確認

### アラート・通知確認
- [ ] 夜間アラート履歴確認
- [ ] 監視システム正常動作確認
- [ ] 緊急連絡体制確認
- [ ] バックアップ完了確認

コメント/注意事項:
________________________________
```

### 🌃 夜間システムチェック（22:00）

```markdown
## 日次チェックリスト - 夜 (22:00)
実施者: ___________  実施日: ___________

### 日中業務処理確認
- [ ] シフト変更要求処理状況確認
- [ ] 緊急呼出履歴確認
- [ ] システム使用統計確認
- [ ] エラー発生件数確認

### バックアップ準備
- [ ] 自動バックアップ設定確認
- [ ] バックアップ容量確認
- [ ] 前回バックアップ成功確認
- [ ] 復旧テスト計画確認

### セキュリティ点検
- [ ] 日中アクセスログ分析
- [ ] 異常な操作パターン確認
- [ ] ログイン失敗回数確認
- [ ] 権限変更履歴確認

### 翌日準備
- [ ] 予定されたメンテナンス確認
- [ ] システムアップデート計画確認
- [ ] 緊急連絡先更新確認
- [ ] 監視アラート設定確認

コメント/注意事項:
________________________________
```

## 📅 週次運用チェックリスト

### 🗓️ 毎週月曜日実施

```markdown
## 週次チェックリスト
実施者: ___________  実施週: ___________

### システム性能分析
- [ ] 過去1週間のレスポンス時間分析
- [ ] データベース性能統計確認
- [ ] ディスク使用量推移確認
- [ ] ネットワークトラフィック分析

### セキュリティ監査
- [ ] アクセスログ週次分析
- [ ] セキュリティ脆弱性スキャン実行
- [ ] ユーザー権限監査
- [ ] パスワードポリシー遵守確認

### データ整合性確認
- [ ] データベース整合性チェック
- [ ] バックアップファイル検証
- [ ] データ復旧テスト実行
- [ ] 監査ログ完全性確認

### 容量・成長計画
- [ ] ストレージ容量予測
- [ ] ユーザー数増加傾向分析
- [ ] システム拡張計画確認
- [ ] パフォーマンス最適化候補確認

### ドキュメント更新
- [ ] 運用手順書更新確認
- [ ] 緊急時対応手順更新
- [ ] ユーザーマニュアル更新
- [ ] システム構成図更新

コメント/注意事項:
________________________________
```

## 🗓️ 月次運用チェックリスト

### 📊 毎月1日実施

```markdown
## 月次チェックリスト
実施者: ___________  実施月: ___________

### 包括的システム監査
- [ ] 全システムコンポーネント健全性確認
- [ ] セキュリティポリシー遵守状況確認
- [ ] データ保護規則コンプライアンス確認
- [ ] 災害復旧計画有効性確認

### パフォーマンス最適化
- [ ] データベースインデックス最適化
- [ ] アプリケーションキャッシュ効率確認
- [ ] 不要ファイル・ログクリーンアップ
- [ ] システムリソース再配分検討

### ユーザー・権限管理
- [ ] 非アクティブユーザーアカウント確認
- [ ] 権限レベル適正性確認
- [ ] アクセス権限監査
- [ ] パスワード更新推奨通知

### 法的・規制対応
- [ ] HIPAA準拠状況確認
- [ ] 個人情報保護法対応確認
- [ ] 医療機関向け規制対応確認
- [ ] 監査ログ保存期間確認

### ビジネス継続性
- [ ] 災害復旧計画テスト
- [ ] 緊急時連絡体制更新
- [ ] システム冗長性確認
- [ ] 代替手順有効性確認

コメント/注意事項:
________________________________
```

## 🚨 緊急時対応手順（SOP）

### 📞 緊急時連絡体制

```markdown
## 緊急時連絡先

### レベル1: システム障害
**対象**: アプリケーション停止、データベース障害
**対応時間**: 即座（24時間以内）

1. システム管理者: xxx-xxxx-xxxx
2. データベース管理者: xxx-xxxx-xxxx  
3. ネットワーク管理者: xxx-xxxx-xxxx
4. 病院IT責任者: xxx-xxxx-xxxx

### レベル2: セキュリティインシデント
**対象**: 不正アクセス、データ漏洩疑い
**対応時間**: 即座（1時間以内）

1. CISO (最高情報セキュリティ責任者): xxx-xxxx-xxxx
2. システム管理者: xxx-xxxx-xxxx
3. 法務担当者: xxx-xxxx-xxxx
4. 病院管理者: xxx-xxxx-xxxx

### レベル3: データ損失
**対象**: データベース破損、バックアップ失敗
**対応時間**: 即座（30分以内）

1. データベース管理者: xxx-xxxx-xxxx
2. バックアップ管理者: xxx-xxxx-xxxx
3. システム管理者: xxx-xxxx-xxxx
4. 病院IT責任者: xxx-xxxx-xxxx
```

### 🔧 システム障害対応手順

```bash
#!/bin/bash
# emergency_response.sh
# システム障害時の緊急対応手順

echo "=== ShiftMaster 緊急対応プロトコル ==="
echo "実行時刻: $(date)"
echo "実行者: $USER"
echo ""

# 1. 障害状況確認
echo "1. 障害状況確認中..."
check_system_status() {
    echo "1-1. Webアプリケーション状態確認"
    curl -s --connect-timeout 5 http://localhost:8000/health/ || echo "❌ Webアプリケーション応答なし"
    
    echo "1-2. データベース接続確認"
    sudo -u postgres psql -d shiftmaster -c "SELECT 1;" 2>/dev/null || echo "❌ データベース接続失敗"
    
    echo "1-3. Redis確認"
    redis-cli ping 2>/dev/null || echo "❌ Redis応答なし"
    
    echo "1-4. システムリソース確認"
    echo "CPU使用率: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)"
    echo "メモリ使用率: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
    echo "ディスク使用率: $(df -h / | awk 'NR==2{print $5}')"
}

# 2. 緊急復旧手順
echo "2. 緊急復旧手順実行..."
emergency_recovery() {
    echo "2-1. サービス再起動試行"
    systemctl restart shiftmaster || echo "❌ サービス再起動失敗"
    systemctl restart nginx || echo "❌ Nginx再起動失敗"
    systemctl restart postgresql || echo "❌ PostgreSQL再起動失敗"
    systemctl restart redis || echo "❌ Redis再起動失敗"
    
    echo "2-2. 緊急バックアップ作成"
    EMERGENCY_BACKUP="/tmp/emergency_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p $EMERGENCY_BACKUP
    
    # 設定ファイルバックアップ
    cp -r /etc/nginx/sites-available/shiftmaster $EMERGENCY_BACKUP/
    cp -r /var/www/shiftmaster/.env $EMERGENCY_BACKUP/
    
    # データベースダンプ（可能な場合）
    sudo -u postgres pg_dump shiftmaster > $EMERGENCY_BACKUP/emergency_db_dump.sql 2>/dev/null || echo "❌ 緊急DBダンプ失敗"
    
    echo "緊急バックアップ完了: $EMERGENCY_BACKUP"
}

# 3. ログ収集
echo "3. 障害ログ収集..."
collect_emergency_logs() {
    LOG_COLLECTION="/tmp/emergency_logs_$(date +%Y%m%d_%H%M%S)"
    mkdir -p $LOG_COLLECTION
    
    # システムログ
    journalctl -u shiftmaster --since "1 hour ago" > $LOG_COLLECTION/shiftmaster.log
    journalctl -u nginx --since "1 hour ago" > $LOG_COLLECTION/nginx.log
    journalctl -u postgresql --since "1 hour ago" > $LOG_COLLECTION/postgresql.log
    
    # アプリケーションログ
    tail -100 /var/log/shiftmaster/error.log > $LOG_COLLECTION/app_errors.log 2>/dev/null
    tail -100 /var/log/nginx/error.log > $LOG_COLLECTION/nginx_errors.log 2>/dev/null
    
    # システム状態
    ps aux > $LOG_COLLECTION/processes.log
    netstat -tulpn > $LOG_COLLECTION/network.log
    df -h > $LOG_COLLECTION/disk.log
    free -h > $LOG_COLLECTION/memory.log
    
    echo "ログ収集完了: $LOG_COLLECTION"
}

# 4. 通知送信
echo "4. 緊急通知送信..."
send_emergency_notification() {
    ALERT_MESSAGE="【緊急】ShiftMaster システム障害発生
発生時刻: $(date)
実行者: $USER
状況: 緊急復旧手順実行中
ログ: $LOG_COLLECTION
バックアップ: $EMERGENCY_BACKUP

緊急連絡先に連絡してください。"

    # メール通知（設定されている場合）
    echo "$ALERT_MESSAGE" | mail -s "【緊急】ShiftMaster障害" admin@hospital.local 2>/dev/null || echo "メール送信失敗"
    
    # Slack通知（設定されている場合）
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"$ALERT_MESSAGE\"}" \
        $SLACK_WEBHOOK_URL 2>/dev/null || echo "Slack通知失敗"
}

# メイン実行
check_system_status
echo ""
emergency_recovery
echo ""
collect_emergency_logs
echo ""
send_emergency_notification

echo "=== 緊急対応完了 ==="
echo "次のステップ:"
echo "1. 緊急連絡先に状況報告"
echo "2. 収集したログの詳細分析"
echo "3. 根本原因の調査開始"
echo "4. 恒久対策の検討・実装"
```

### 🛡️ セキュリティインシデント対応

```python
#!/usr/bin/env python
# security_incident_response.py
"""
セキュリティインシデント対応自動化スクリプト
"""

import datetime
import subprocess
import os
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityIncidentResponse:
    def __init__(self):
        self.incident_id = self.generate_incident_id()
        self.response_dir = f"/var/log/security/incident_{self.incident_id}"
        self.ensure_response_directory()
    
    def generate_incident_id(self):
        """インシデントID生成"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"SEC_{timestamp}"
    
    def ensure_response_directory(self):
        """対応ディレクトリ作成"""
        os.makedirs(self.response_dir, exist_ok=True)
        logger.info(f"インシデント対応ディレクトリ作成: {self.response_dir}")
    
    def isolate_affected_systems(self):
        """影響システムの隔離"""
        logger.info("影響システムの隔離開始...")
        
        try:
            # 緊急アクセス制限
            subprocess.run([
                "iptables", "-A", "INPUT", "-p", "tcp", "--dport", "8000", "-j", "DROP"
            ], check=True)
            
            # 疑わしいセッション切断
            subprocess.run([
                "pkill", "-f", "suspicious_process"
            ])
            
            logger.info("✅ システム隔離完了")
            return True
        except Exception as e:
            logger.error(f"❌ システム隔離失敗: {e}")
            return False
    
    def preserve_evidence(self):
        """証拠保全"""
        logger.info("証拠保全開始...")
        
        evidence_files = [
            "/var/log/auth.log",
            "/var/log/syslog", 
            "/var/log/shiftmaster/access.log",
            "/var/log/nginx/access.log",
            "/var/log/postgresql/postgresql.log"
        ]
        
        for file_path in evidence_files:
            if os.path.exists(file_path):
                # ハッシュ値計算
                hash_value = self.calculate_file_hash(file_path)
                
                # 証拠ファイルコピー
                evidence_copy = f"{self.response_dir}/{os.path.basename(file_path)}"
                subprocess.run(["cp", file_path, evidence_copy])
                
                # ハッシュ値記録
                with open(f"{evidence_copy}.hash", "w") as f:
                    f.write(f"{hash_value}  {os.path.basename(file_path)}\n")
                
                logger.info(f"証拠保全完了: {file_path}")
    
    def calculate_file_hash(self, file_path):
        """ファイルハッシュ値計算"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def analyze_security_logs(self):
        """セキュリティログ分析"""
        logger.info("セキュリティログ分析開始...")
        
        analysis_results = {
            "failed_logins": self.count_failed_logins(),
            "suspicious_ips": self.identify_suspicious_ips(),
            "unusual_access_patterns": self.analyze_access_patterns(),
            "privilege_escalations": self.check_privilege_escalations()
        }
        
        # 分析結果保存
        with open(f"{self.response_dir}/analysis_results.txt", "w") as f:
            for category, results in analysis_results.items():
                f.write(f"=== {category.upper()} ===\n")
                for result in results:
                    f.write(f"{result}\n")
                f.write("\n")
        
        return analysis_results
    
    def count_failed_logins(self):
        """ログイン失敗回数カウント"""
        try:
            result = subprocess.run([
                "grep", "Failed password", "/var/log/auth.log"
            ], capture_output=True, text=True)
            
            failed_logins = result.stdout.strip().split('\n')
            return [f"ログイン失敗総数: {len(failed_logins)}"] + failed_logins[-10:]
        except:
            return ["ログイン失敗ログ分析エラー"]
    
    def identify_suspicious_ips(self):
        """疑わしいIPアドレス特定"""
        # 実装例: アクセスログから異常なアクセスパターンを検出
        suspicious_ips = []
        
        try:
            result = subprocess.run([
                "awk", '{print $1}', "/var/log/nginx/access.log"
            ], capture_output=True, text=True)
            
            # IP別アクセス数集計（簡易版）
            ip_counts = {}
            for ip in result.stdout.strip().split('\n'):
                ip_counts[ip] = ip_counts.get(ip, 0) + 1
            
            # 異常に多いアクセスのIPを抽出
            for ip, count in ip_counts.items():
                if count > 1000:  # 閾値は環境に応じて調整
                    suspicious_ips.append(f"高頻度アクセスIP: {ip} ({count} 回)")
        
        except:
            suspicious_ips.append("疑わしいIP分析エラー")
        
        return suspicious_ips
    
    def analyze_access_patterns(self):
        """アクセスパターン分析"""
        patterns = []
        
        try:
            # 時間外アクセス検出
            result = subprocess.run([
                "grep", "$(date -d '23:00' +%H)", "/var/log/shiftmaster/access.log"
            ], capture_output=True, text=True)
            
            if result.stdout:
                patterns.append(f"深夜アクセス検出: {len(result.stdout.strip().split())} 件")
            
            # 管理者権限アクセス検出
            result = subprocess.run([
                "grep", "admin", "/var/log/shiftmaster/access.log"
            ], capture_output=True, text=True)
            
            if result.stdout:
                patterns.append(f"管理者アクセス: {len(result.stdout.strip().split())} 件")
        
        except:
            patterns.append("アクセスパターン分析エラー")
        
        return patterns
    
    def check_privilege_escalations(self):
        """権限昇格チェック"""
        escalations = []
        
        try:
            result = subprocess.run([
                "grep", "sudo", "/var/log/auth.log"
            ], capture_output=True, text=True)
            
            sudo_attempts = result.stdout.strip().split('\n')
            escalations.append(f"sudo実行総数: {len(sudo_attempts)}")
            
            # 最近のsudo実行（最新10件）
            escalations.extend(sudo_attempts[-10:])
        
        except:
            escalations.append("権限昇格チェックエラー")
        
        return escalations
    
    def generate_incident_report(self, analysis_results):
        """インシデントレポート生成"""
        report_path = f"{self.response_dir}/incident_report.md"
        
        report_content = f"""# セキュリティインシデント報告書

## インシデント基本情報
- **インシデントID**: {self.incident_id}
- **発生日時**: {datetime.datetime.now().strftime('%Y年%m月%d日 %H時%M分')}
- **検出方法**: 自動監視システム
- **対応者**: {os.getenv('USER', '不明')}

## 対応状況
- **隔離措置**: 実施済み
- **証拠保全**: 実施済み
- **ログ分析**: 実施済み

## 分析結果サマリー
"""
        
        for category, results in analysis_results.items():
            report_content += f"\n### {category.replace('_', ' ').title()}\n"
            for result in results[:5]:  # 上位5件のみ表示
                report_content += f"- {result}\n"
        
        report_content += f"""
## 推奨事項
1. 影響範囲の詳細調査
2. 脆弱性の特定・修正
3. セキュリティポリシー見直し
4. スタッフへのセキュリティ教育

## 添付ファイル
- 証拠ログファイル: {self.response_dir}/
- 分析結果詳細: {self.response_dir}/analysis_results.txt

---
**報告者**: システム管理者  
**作成日時**: {datetime.datetime.now().strftime('%Y年%m月%d日 %H時%M分')}
"""
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        logger.info(f"インシデントレポート生成完了: {report_path}")
        return report_path
    
    def execute_full_response(self):
        """完全インシデント対応実行"""
        logger.info(f"セキュリティインシデント対応開始: {self.incident_id}")
        
        # 1. システム隔離
        self.isolate_affected_systems()
        
        # 2. 証拠保全
        self.preserve_evidence()
        
        # 3. ログ分析
        analysis_results = self.analyze_security_logs()
        
        # 4. レポート生成
        report_path = self.generate_incident_report(analysis_results)
        
        logger.info("セキュリティインシデント対応完了")
        return {
            "incident_id": self.incident_id,
            "response_directory": self.response_dir,
            "report_path": report_path
        }

if __name__ == "__main__":
    response = SecurityIncidentResponse()
    result = response.execute_full_response()
    
    print(f"=== セキュリティインシデント対応完了 ===")
    print(f"インシデントID: {result['incident_id']}")
    print(f"対応ディレクトリ: {result['response_directory']}")
    print(f"報告書: {result['report_path']}")
    print("\n次のステップ:")
    print("1. CISO・管理者への即座報告")
    print("2. 法執行機関への通報検討")
    print("3. 影響を受けた関係者への通知")
    print("4. 恒久対策の検討・実装")
```

## 📊 運用KPI・メトリクス

### 📈 システム可用性KPI

```python
# monitoring/kpi_calculator.py
"""
ShiftMaster 運用KPI計算・レポート生成
"""

import datetime
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class KPIMetrics:
    """KPIメトリクス定義"""
    availability: float  # 可用性 (%)
    response_time_p95: float  # 応答時間95パーセンタイル (ms)
    error_rate: float  # エラー率 (%)
    throughput: float  # スループット (req/sec)
    mttr: float  # 平均復旧時間 (minutes)
    mtbf: float  # 平均故障間隔 (hours)

class KPICalculator:
    def __init__(self):
        self.sla_targets = {
            "availability": 99.9,  # 99.9%
            "response_time_p95": 200,  # 200ms
            "error_rate": 0.1,  # 0.1%
            "throughput": 1000,  # 1000 req/sec
            "mttr": 15,  # 15分
            "mtbf": 720  # 30日
        }
    
    def calculate_monthly_kpi(self, year: int, month: int) -> KPIMetrics:
        """月次KPI計算"""
        # 実際の実装では、監視システムからデータを取得
        # ここでは例示的な計算を示す
        
        # 可用性計算
        total_minutes = self.get_total_minutes_in_month(year, month)
        downtime_minutes = self.get_downtime_minutes(year, month)
        availability = ((total_minutes - downtime_minutes) / total_minutes) * 100
        
        # レスポンス時間（95パーセンタイル）
        response_times = self.get_response_times(year, month)
        response_time_p95 = self.calculate_percentile(response_times, 95)
        
        # エラー率
        total_requests = self.get_total_requests(year, month)
        error_requests = self.get_error_requests(year, month)
        error_rate = (error_requests / total_requests) * 100 if total_requests > 0 else 0
        
        # スループット
        throughput = total_requests / (total_minutes * 60)  # req/sec
        
        # MTTR（平均復旧時間）
        incidents = self.get_incidents(year, month)
        mttr = sum(incident['resolution_time'] for incident in incidents) / len(incidents) if incidents else 0
        
        # MTBF（平均故障間隔）
        mtbf = total_minutes / len(incidents) if incidents else total_minutes
        
        return KPIMetrics(
            availability=availability,
            response_time_p95=response_time_p95,
            error_rate=error_rate,
            throughput=throughput,
            mttr=mttr,
            mtbf=mtbf / 60  # 時間単位に変換
        )
    
    def generate_kpi_report(self, metrics: KPIMetrics, year: int, month: int) -> str:
        """KPIレポート生成"""
        report = f"""
# ShiftMaster 月次運用KPIレポート
**対象期間**: {year}年{month}月

## 📊 主要KPI

| メトリクス | 実績値 | SLA目標 | 達成状況 |
|-----------|--------|---------|----------|
| **可用性** | {metrics.availability:.3f}% | {self.sla_targets['availability']}% | {'✅' if metrics.availability >= self.sla_targets['availability'] else '❌'} |
| **応答時間(P95)** | {metrics.response_time_p95:.1f}ms | {self.sla_targets['response_time_p95']}ms | {'✅' if metrics.response_time_p95 <= self.sla_targets['response_time_p95'] else '❌'} |
| **エラー率** | {metrics.error_rate:.3f}% | {self.sla_targets['error_rate']}% | {'✅' if metrics.error_rate <= self.sla_targets['error_rate'] else '❌'} |
| **スループット** | {metrics.throughput:.1f} req/sec | {self.sla_targets['throughput']} req/sec | {'✅' if metrics.throughput >= self.sla_targets['throughput'] else '❌'} |
| **MTTR** | {metrics.mttr:.1f}分 | {self.sla_targets['mttr']}分 | {'✅' if metrics.mttr <= self.sla_targets['mttr'] else '❌'} |
| **MTBF** | {metrics.mtbf:.1f}時間 | {self.sla_targets['mtbf']}時間 | {'✅' if metrics.mtbf >= self.sla_targets['mtbf'] else '❌'} |

## 📈 パフォーマンス分析

### 可用性分析
- **稼働時間**: {self.get_total_minutes_in_month(year, month) - self.get_downtime_minutes(year, month):.0f}分
- **停止時間**: {self.get_downtime_minutes(year, month):.0f}分
- **主要停止原因**: {self.get_top_downtime_causes(year, month)}

### レスポンス時間分析
- **平均応答時間**: {self.get_avg_response_time(year, month):.1f}ms
- **最大応答時間**: {self.get_max_response_time(year, month):.1f}ms
- **改善傾向**: {self.get_response_time_trend(year, month)}

## 🎯 SLA達成度サマリー

**SLA達成率**: {self.calculate_sla_achievement_rate(metrics):.1f}%

### 目標達成項目
{self.get_achieved_targets(metrics)}

### 要改善項目
{self.get_improvement_targets(metrics)}

## 📋 改善アクションプラン

{self.generate_improvement_plan(metrics)}

---
**レポート作成日**: {datetime.datetime.now().strftime('%Y年%m月%d日')}  
**作成者**: システム運用チーム
"""
        return report
    
    def get_total_minutes_in_month(self, year: int, month: int) -> float:
        """月の総分数を取得"""
        import calendar
        days = calendar.monthrange(year, month)[1]
        return days * 24 * 60
    
    def get_downtime_minutes(self, year: int, month: int) -> float:
        """停止時間を取得（実装例）"""
        # 実際の実装では監視システムから取得
        return 30  # 例: 30分の停止時間
    
    def calculate_sla_achievement_rate(self, metrics: KPIMetrics) -> float:
        """SLA達成率計算"""
        achievements = [
            metrics.availability >= self.sla_targets['availability'],
            metrics.response_time_p95 <= self.sla_targets['response_time_p95'],
            metrics.error_rate <= self.sla_targets['error_rate'],
            metrics.throughput >= self.sla_targets['throughput'],
            metrics.mttr <= self.sla_targets['mttr'],
            metrics.mtbf >= self.sla_targets['mtbf']
        ]
        return (sum(achievements) / len(achievements)) * 100
```

---

このガイドにより、ShiftMasterの包括的な運用管理体制が確立され、医療機関での安定的な24時間365日運用が実現されます。

**最終更新**: 2024年1月20日  
**対象バージョン**: ShiftMaster 2.0.0  
**運用担当**: システム運用管理チーム
