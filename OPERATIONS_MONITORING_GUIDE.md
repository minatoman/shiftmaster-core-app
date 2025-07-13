# 🛠️ 運用管理・監視ガイド

## 📊 システム監視・ダッシュボード

### 🎯 監視対象メトリクス

#### アプリケーション層
- **レスポンス時間**: API・画面表示速度
- **スループット**: 同時接続数・リクエスト処理数
- **エラー率**: HTTP 4xx/5xx エラー発生率
- **可用性**: サービス稼働率・ダウンタイム
- **ユーザーセッション**: アクティブユーザー・セッション継続時間

#### インフラストラクチャ層
- **CPU使用率**: サーバー・コンテナリソース
- **メモリ使用量**: アプリケーション・システムメモリ
- **ディスク使用量**: ストレージ容量・I/O性能
- **ネットワーク**: 帯域使用率・パケット損失
- **コンテナヘルス**: Docker コンテナ稼働状況

#### データベース層
- **接続数**: アクティブ・アイドル接続
- **クエリ性能**: 実行時間・スロークエリ
- **レプリケーション**: マスター・スレーブ同期状況
- **ロック**: デッドロック・ロック待機時間
- **バックアップ**: 自動バックアップ成功・失敗

### 📈 Grafana ダッシュボード設定

```yaml
# grafana/dashboards/shiftmaster-overview.json
{
  "dashboard": {
    "title": "ShiftMaster - システム概要",
    "panels": [
      {
        "title": "アプリケーション状態",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=\"shiftmaster\"}"
          }
        ]
      },
      {
        "title": "レスポンス時間",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(django_request_duration_seconds_bucket[5m]))"
          }
        ]
      },
      {
        "title": "データベース接続",
        "type": "graph", 
        "targets": [
          {
            "expr": "pg_stat_activity_count"
          }
        ]
      }
    ]
  }
}
```

### 🚨 Prometheus アラート設定

```yaml
# prometheus/alerts/shiftmaster.yml
groups:
  - name: shiftmaster.alerts
    rules:
      # アプリケーション停止
      - alert: ShiftMasterDown
        expr: up{job="shiftmaster"} == 0
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "ShiftMaster application is down"
          description: "ShiftMaster has been down for more than 30 seconds"

      # 高レスポンス時間
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(django_request_duration_seconds_bucket[5m])) > 2
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"

      # データベース接続エラー
      - alert: DatabaseConnectionError
        expr: pg_up == 0
        for: 10s
        labels:
          severity: critical
        annotations:
          summary: "PostgreSQL database is down"

      # 高CPU使用率
      - alert: HighCPUUsage
        expr: (100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)) > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"

      # メモリ不足
      - alert: HighMemoryUsage
        expr: ((node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes) * 100 > 85
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"

      # ディスク容量不足
      - alert: DiskSpaceWarning
        expr: ((node_filesystem_size_bytes{fstype!="tmpfs"} - node_filesystem_free_bytes{fstype!="tmpfs"}) / node_filesystem_size_bytes{fstype!="tmpfs"}) * 100 > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Disk space usage is high"
```

## 🔔 アラート・通知システム

### 📧 通知チャンネル設定

```yaml
# alertmanager/config.yml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@shiftmaster.local'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
  - name: 'web.hook'
    email_configs:
      - to: 'admin@hospital.local'
        subject: '[ShiftMaster] {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          {{ end }}
    
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'
        channel: '#shiftmaster-alerts'
        title: 'ShiftMaster Alert'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname']
```

### 📱 PagerDuty 統合

```python
# monitoring/pagerduty_integration.py
import requests
import json
from django.conf import settings

class PagerDutyAlert:
    def __init__(self):
        self.integration_key = settings.PAGERDUTY_INTEGRATION_KEY
        self.api_url = "https://events.pagerduty.com/v2/enqueue"
    
    def trigger_alert(self, summary, severity, details=None):
        """緊急アラートをPagerDutyに送信"""
        payload = {
            "routing_key": self.integration_key,
            "event_action": "trigger",
            "payload": {
                "summary": summary,
                "severity": severity,
                "source": "shiftmaster",
                "custom_details": details or {}
            }
        }
        
        response = requests.post(
            self.api_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        
        return response.status_code == 202
    
    def resolve_alert(self, dedup_key):
        """アラート解決をPagerDutyに通知"""
        payload = {
            "routing_key": self.integration_key,
            "event_action": "resolve",
            "dedup_key": dedup_key
        }
        
        response = requests.post(
            self.api_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        
        return response.status_code == 202

# 使用例
def check_critical_systems():
    """重要システムの定期チェック"""
    pager = PagerDutyAlert()
    
    # データベース接続チェック
    if not check_database_connection():
        pager.trigger_alert(
            "Database connection failed",
            "critical",
            {"component": "postgresql", "timestamp": datetime.now().isoformat()}
        )
```

## 🔧 自動化運用スクリプト

### 📊 ヘルスチェック自動化

```python
# monitoring/health_checker.py
#!/usr/bin/env python
"""
ShiftMaster システムヘルスチェック自動化
"""

import subprocess
import requests
import psycopg2
import redis
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self):
        self.checks = [
            self.check_web_service,
            self.check_database,
            self.check_redis,
            self.check_celery,
            self.check_nginx,
            self.check_disk_space,
            self.check_memory_usage
        ]
        self.results = []
    
    def check_web_service(self):
        """Webサービス死活監視"""
        try:
            response = requests.get("http://localhost:8000/health/", timeout=10)
            if response.status_code == 200:
                return {"service": "web", "status": "healthy", "response_time": response.elapsed.total_seconds()}
            else:
                return {"service": "web", "status": "unhealthy", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"service": "web", "status": "down", "error": str(e)}
    
    def check_database(self):
        """PostgreSQL接続チェック"""
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="shiftmaster",
                user="postgres",
                password="password"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            return {"service": "database", "status": "healthy"}
        except Exception as e:
            return {"service": "database", "status": "down", "error": str(e)}
    
    def check_redis(self):
        """Redis接続チェック"""
        try:
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.ping()
            return {"service": "redis", "status": "healthy"}
        except Exception as e:
            return {"service": "redis", "status": "down", "error": str(e)}
    
    def check_celery(self):
        """Celery Worker稼働チェック"""
        try:
            result = subprocess.run(
                ["celery", "-A", "shiftmaster", "inspect", "active"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return {"service": "celery", "status": "healthy"}
            else:
                return {"service": "celery", "status": "down", "error": result.stderr}
        except Exception as e:
            return {"service": "celery", "status": "down", "error": str(e)}
    
    def check_nginx(self):
        """Nginx稼働チェック"""
        try:
            result = subprocess.run(
                ["systemctl", "is-active", "nginx"],
                capture_output=True, text=True
            )
            if result.stdout.strip() == "active":
                return {"service": "nginx", "status": "healthy"}
            else:
                return {"service": "nginx", "status": "down", "error": "Service not active"}
        except Exception as e:
            return {"service": "nginx", "status": "down", "error": str(e)}
    
    def check_disk_space(self):
        """ディスク容量チェック"""
        try:
            result = subprocess.run(
                ["df", "-h", "/"],
                capture_output=True, text=True
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                usage_line = lines[1].split()
                usage_percent = int(usage_line[4].rstrip('%'))
                
                status = "healthy"
                if usage_percent > 90:
                    status = "critical"
                elif usage_percent > 80:
                    status = "warning"
                
                return {
                    "service": "disk_space",
                    "status": status,
                    "usage_percent": usage_percent
                }
        except Exception as e:
            return {"service": "disk_space", "status": "error", "error": str(e)}
    
    def check_memory_usage(self):
        """メモリ使用量チェック"""
        try:
            result = subprocess.run(
                ["free", "-m"],
                capture_output=True, text=True
            )
            lines = result.stdout.strip().split('\n')
            mem_line = lines[1].split()
            
            total = int(mem_line[1])
            used = int(mem_line[2])
            usage_percent = (used / total) * 100
            
            status = "healthy"
            if usage_percent > 90:
                status = "critical"
            elif usage_percent > 80:
                status = "warning"
            
            return {
                "service": "memory",
                "status": status,
                "usage_percent": round(usage_percent, 2)
            }
        except Exception as e:
            return {"service": "memory", "status": "error", "error": str(e)}
    
    def run_all_checks(self):
        """全ヘルスチェック実行"""
        logger.info("Starting health checks...")
        
        for check in self.checks:
            try:
                result = check()
                result["timestamp"] = datetime.now().isoformat()
                self.results.append(result)
                logger.info(f"Check {result['service']}: {result['status']}")
            except Exception as e:
                logger.error(f"Error running check {check.__name__}: {e}")
        
        return self.results
    
    def generate_report(self):
        """ヘルスチェックレポート生成"""
        report = []
        report.append("=== ShiftMaster System Health Report ===")
        report.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        healthy_count = 0
        for result in self.results:
            status = result['status']
            service = result['service']
            
            if status == "healthy":
                healthy_count += 1
                status_icon = "✅"
            elif status == "warning":
                status_icon = "⚠️"
            elif status in ["unhealthy", "down", "critical"]:
                status_icon = "❌"
            else:
                status_icon = "❓"
            
            report.append(f"{status_icon} {service.upper()}: {status}")
            
            if "error" in result:
                report.append(f"   Error: {result['error']}")
            if "usage_percent" in result:
                report.append(f"   Usage: {result['usage_percent']}%")
            if "response_time" in result:
                report.append(f"   Response time: {result['response_time']:.3f}s")
        
        report.append("")
        report.append(f"Overall health: {healthy_count}/{len(self.results)} services healthy")
        
        return "\n".join(report)
    
    def send_alert_email(self, report):
        """アラートメール送信"""
        try:
            msg = MIMEText(report)
            msg['Subject'] = 'ShiftMaster System Health Alert'
            msg['From'] = 'system@shiftmaster.local'
            msg['To'] = 'admin@hospital.local'
            
            server = smtplib.SMTP('localhost')
            server.send_message(msg)
            server.quit()
            
            logger.info("Alert email sent successfully")
        except Exception as e:
            logger.error(f"Failed to send alert email: {e}")

if __name__ == "__main__":
    checker = HealthChecker()
    results = checker.run_all_checks()
    report = checker.generate_report()
    
    print(report)
    
    # 問題がある場合はアラートメール送信
    critical_issues = [r for r in results if r['status'] in ['down', 'critical', 'unhealthy']]
    if critical_issues:
        checker.send_alert_email(report)
```

### 🔄 自動バックアップ・復旧

```bash
#!/bin/bash
# monitoring/backup_automation.sh

set -e

# 設定
BACKUP_DIR="/var/backups/shiftmaster"
DB_NAME="shiftmaster"
DB_USER="postgres"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)
SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

# ログ設定
LOG_FILE="/var/log/shiftmaster/backup.log"
exec 1> >(tee -a $LOG_FILE)
exec 2>&1

echo "=== ShiftMaster Backup Started: $(date) ==="

# バックアップディレクトリ作成
mkdir -p $BACKUP_DIR

# データベースバックアップ
echo "Creating database backup..."
pg_dump -U $DB_USER -h localhost $DB_NAME | gzip > "$BACKUP_DIR/db_backup_$DATE.sql.gz"

if [ $? -eq 0 ]; then
    echo "✅ Database backup completed successfully"
    DB_BACKUP_STATUS="SUCCESS"
else
    echo "❌ Database backup failed"
    DB_BACKUP_STATUS="FAILED"
fi

# アプリケーションファイルバックアップ
echo "Creating application files backup..."
tar -czf "$BACKUP_DIR/app_backup_$DATE.tar.gz" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    --exclude=".git" \
    --exclude="new_env" \
    /path/to/shiftmaster/

if [ $? -eq 0 ]; then
    echo "✅ Application backup completed successfully"
    APP_BACKUP_STATUS="SUCCESS"
else
    echo "❌ Application backup failed"
    APP_BACKUP_STATUS="FAILED"
fi

# 設定ファイルバックアップ
echo "Creating configuration backup..."
tar -czf "$BACKUP_DIR/config_backup_$DATE.tar.gz" \
    /etc/nginx/sites-available/shiftmaster \
    /etc/systemd/system/shiftmaster.service \
    /etc/ssl/private/shiftmaster.key \
    /etc/ssl/certs/shiftmaster.crt

if [ $? -eq 0 ]; then
    echo "✅ Configuration backup completed successfully"
    CONFIG_BACKUP_STATUS="SUCCESS"
else
    echo "❌ Configuration backup failed"
    CONFIG_BACKUP_STATUS="FAILED"
fi

# 古いバックアップファイル削除
echo "Cleaning up old backups..."
find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -delete

# バックアップサイズ計算
BACKUP_SIZE=$(du -sh $BACKUP_DIR | cut -f1)

# Slackに結果通知
BACKUP_REPORT="ShiftMaster Backup Report
Date: $(date)
Database: $DB_BACKUP_STATUS
Application: $APP_BACKUP_STATUS
Configuration: $CONFIG_BACKUP_STATUS
Total size: $BACKUP_SIZE
Location: $BACKUP_DIR"

curl -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"$BACKUP_REPORT\"}" \
    $SLACK_WEBHOOK

echo "=== ShiftMaster Backup Completed: $(date) ==="
```

### 🚀 自動デプロイメント・ロールバック

```python
# monitoring/deployment_automation.py
#!/usr/bin/env python
"""
ShiftMaster 自動デプロイメント・ロールバック
"""

import subprocess
import sys
import os
import time
import requests
from datetime import datetime

class DeploymentManager:
    def __init__(self):
        self.app_path = "/var/www/shiftmaster"
        self.service_name = "shiftmaster"
        self.backup_path = "/var/backups/shiftmaster/deployments"
        
    def backup_current_deployment(self):
        """現在のデプロイメントをバックアップ"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"{self.backup_path}/backup_{timestamp}"
        
        print(f"Creating deployment backup: {backup_dir}")
        
        subprocess.run([
            "cp", "-r", self.app_path, backup_dir
        ], check=True)
        
        return backup_dir
    
    def health_check(self, max_attempts=5, delay=10):
        """デプロイ後のヘルスチェック"""
        for attempt in range(max_attempts):
            try:
                response = requests.get("http://localhost:8000/health/", timeout=10)
                if response.status_code == 200:
                    print("✅ Health check passed")
                    return True
            except Exception as e:
                print(f"Health check attempt {attempt + 1} failed: {e}")
                
            if attempt < max_attempts - 1:
                print(f"Waiting {delay} seconds before next attempt...")
                time.sleep(delay)
        
        print("❌ Health check failed")
        return False
    
    def deploy(self, git_branch="main"):
        """新しいバージョンをデプロイ"""
        print(f"=== Starting deployment from branch: {git_branch} ===")
        
        # バックアップ作成
        backup_dir = self.backup_current_deployment()
        
        try:
            # GitプルしてアップデートKa
            print("Updating application code...")
            subprocess.run([
                "git", "-C", self.app_path, "fetch", "origin"
            ], check=True)
            
            subprocess.run([
                "git", "-C", self.app_path, "checkout", git_branch
            ], check=True)
            
            subprocess.run([
                "git", "-C", self.app_path, "pull", "origin", git_branch
            ], check=True)
            
            # 依存関係更新
            print("Installing dependencies...")
            subprocess.run([
                "pip", "install", "-r", f"{self.app_path}/requirements.txt"
            ], check=True)
            
            # データベースマイグレーション
            print("Running database migrations...")
            subprocess.run([
                "python", f"{self.app_path}/manage.py", "migrate"
            ], check=True)
            
            # 静的ファイル収集
            print("Collecting static files...")
            subprocess.run([
                "python", f"{self.app_path}/manage.py", "collectstatic", "--noinput"
            ], check=True)
            
            # サービス再起動
            print("Restarting application service...")
            subprocess.run([
                "systemctl", "restart", self.service_name
            ], check=True)
            
            # Nginx再読み込み
            subprocess.run([
                "systemctl", "reload", "nginx"
            ], check=True)
            
            # ヘルスチェック
            print("Performing health check...")
            if self.health_check():
                print("✅ Deployment completed successfully!")
                return True
            else:
                print("❌ Deployment failed health check")
                self.rollback(backup_dir)
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Deployment failed: {e}")
            self.rollback(backup_dir)
            return False
    
    def rollback(self, backup_dir):
        """前のバージョンにロールバック"""
        print(f"=== Starting rollback to: {backup_dir} ===")
        
        try:
            # バックアップから復元
            subprocess.run([
                "rm", "-rf", f"{self.app_path}.old"
            ])
            
            subprocess.run([
                "mv", self.app_path, f"{self.app_path}.old"
            ], check=True)
            
            subprocess.run([
                "mv", backup_dir, self.app_path
            ], check=True)
            
            # サービス再起動
            subprocess.run([
                "systemctl", "restart", self.service_name
            ], check=True)
            
            subprocess.run([
                "systemctl", "reload", "nginx"
            ], check=True)
            
            # ヘルスチェック
            if self.health_check():
                print("✅ Rollback completed successfully!")
                return True
            else:
                print("❌ Rollback failed health check")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Rollback failed: {e}")
            return False

if __name__ == "__main__":
    manager = DeploymentManager()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "deploy":
            branch = sys.argv[2] if len(sys.argv) > 2 else "main"
            success = manager.deploy(branch)
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "rollback":
            backup_dir = sys.argv[2] if len(sys.argv) > 2 else None
            if backup_dir:
                success = manager.rollback(backup_dir)
                sys.exit(0 if success else 1)
            else:
                print("Please specify backup directory for rollback")
                sys.exit(1)
    else:
        print("Usage: python deployment_automation.py [deploy|rollback] [branch|backup_dir]")
        sys.exit(1)
```

## 📈 パフォーマンス監視・最適化

### 🔍 APM（Application Performance Monitoring）

```python
# monitoring/apm_integration.py
from django.middleware.base import BaseMiddleware
from django.utils.deprecation import MiddlewareMixin
import time
import logging
import psutil
from datetime import datetime

logger = logging.getLogger(__name__)

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """アプリケーション性能監視ミドルウェア"""
    
    def process_request(self, request):
        request.start_time = time.time()
        request.start_memory = psutil.Process().memory_info().rss
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            memory_used = psutil.Process().memory_info().rss - request.start_memory
            
            # パフォーマンスメトリクス記録
            performance_data = {
                'timestamp': datetime.now().isoformat(),
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': round(duration * 1000, 2),
                'memory_mb': round(memory_used / 1024 / 1024, 2),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'remote_addr': request.META.get('REMOTE_ADDR', ''),
            }
            
            # 警告レベルの性能問題をログ
            if duration > 2.0:  # 2秒以上
                logger.warning(f"Slow request detected: {performance_data}")
            elif duration > 1.0:  # 1秒以上
                logger.info(f"Performance concern: {performance_data}")
            
            # Prometheusメトリクス更新（実装時）
            # self.update_prometheus_metrics(performance_data)
        
        return response
    
    def update_prometheus_metrics(self, data):
        """Prometheusメトリクス更新"""
        # from prometheus_client import Counter, Histogram
        # REQUEST_COUNT.labels(method=data['method'], endpoint=data['path']).inc()
        # REQUEST_LATENCY.observe(data['duration_ms'] / 1000)
        pass
```

### 📊 データベース性能監視

```sql
-- monitoring/db_performance_queries.sql

-- 実行時間の長いクエリ
SELECT 
    query,
    mean_time,
    calls,
    total_time,
    (total_time/calls) as avg_time_ms
FROM pg_stat_statements 
WHERE mean_time > 100  -- 100ms以上
ORDER BY mean_time DESC 
LIMIT 10;

-- テーブルサイズ監視
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY size_bytes DESC;

-- インデックス使用状況
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE idx_scan < 100  -- あまり使われていないインデックス
ORDER BY idx_scan;

-- アクティブ接続監視
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    state_change,
    query
FROM pg_stat_activity 
WHERE state != 'idle';
```

## 🔧 トラブルシューティング・問題解決

### 🚨 一般的な問題と解決策

```bash
# monitoring/troubleshooting_guide.sh

#!/bin/bash
echo "=== ShiftMaster トラブルシューティングガイド ==="

# 1. アプリケーションが起動しない
check_application_startup() {
    echo "1. アプリケーション起動問題の診断..."
    
    # サービス状態確認
    systemctl status shiftmaster
    
    # ログ確認
    echo "最新のエラーログ:"
    tail -50 /var/log/shiftmaster/error.log
    
    # ポート使用状況
    echo "ポート8000の使用状況:"
    netstat -tulpn | grep 8000
    
    # 仮想環境確認
    echo "Python仮想環境:"
    which python
    python --version
}

# 2. データベース接続エラー
check_database_connection() {
    echo "2. データベース接続問題の診断..."
    
    # PostgreSQL状態確認
    systemctl status postgresql
    
    # 接続テスト
    sudo -u postgres psql -c "SELECT version();"
    
    # 接続数確認
    sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"
    
    # データベース存在確認
    sudo -u postgres psql -c "\l" | grep shiftmaster
}

# 3. 高CPU使用率
check_high_cpu() {
    echo "3. 高CPU使用率の診断..."
    
    # プロセス別CPU使用率
    ps aux --sort=-%cpu | head -10
    
    # システム負荷
    uptime
    
    # Djangoプロセス詳細
    ps aux | grep python | grep manage.py
    
    # 実行中のクエリ
    sudo -u postgres psql -d shiftmaster -c "SELECT pid, query_start, state, query FROM pg_stat_activity WHERE state = 'active';"
}

# 4. メモリ不足
check_memory_issues() {
    echo "4. メモリ使用状況の診断..."
    
    # メモリ使用量詳細
    free -h
    cat /proc/meminfo | grep -E "(MemTotal|MemFree|MemAvailable|Cached|Buffers)"
    
    # プロセス別メモリ使用量
    ps aux --sort=-%mem | head -10
    
    # スワップ使用状況
    swapon --show
    
    # OOM Killer履歴
    dmesg | grep -i "killed process"
}

# 5. ディスク容量問題
check_disk_space() {
    echo "5. ディスク容量の診断..."
    
    # ディスク使用量
    df -h
    
    # 大きなファイル・ディレクトリ
    du -sh /var/log/* | sort -hr | head -10
    du -sh /var/lib/postgresql/* | sort -hr | head -10
    
    # ログローテーション状況
    ls -la /var/log/shiftmaster/
    
    # inodeの使用状況
    df -i
}

# 6. ネットワーク問題
check_network_issues() {
    echo "6. ネットワーク問題の診断..."
    
    # リスニングポート
    netstat -tulpn | grep -E "(80|443|8000|5432|6379)"
    
    # ファイアウォール状態
    ufw status
    iptables -L
    
    # 外部接続テスト
    curl -I http://localhost:8000/health/
    
    # DNS解決テスト
    nslookup $(hostname)
}

# メイン診断実行
run_full_diagnosis() {
    echo "ShiftMaster システム完全診断開始: $(date)"
    echo "=================================================="
    
    check_application_startup
    echo ""
    check_database_connection
    echo ""
    check_high_cpu
    echo ""
    check_memory_issues
    echo ""
    check_disk_space
    echo ""
    check_network_issues
    
    echo "=================================================="
    echo "診断完了: $(date)"
}

# コマンドライン引数に応じて実行
case "${1:-all}" in
    "app") check_application_startup ;;
    "db") check_database_connection ;;
    "cpu") check_high_cpu ;;
    "memory") check_memory_issues ;;
    "disk") check_disk_space ;;
    "network") check_network_issues ;;
    "all") run_full_diagnosis ;;
    *) 
        echo "Usage: $0 [app|db|cpu|memory|disk|network|all]"
        echo "  app     - アプリケーション起動問題"
        echo "  db      - データベース接続問題"
        echo "  cpu     - 高CPU使用率問題"
        echo "  memory  - メモリ不足問題"
        echo "  disk    - ディスク容量問題"
        echo "  network - ネットワーク問題"
        echo "  all     - 全項目診断（デフォルト）"
        ;;
esac
```

## 📝 ログ管理・分析

### 🗂️ ログ統合・集約

```yaml
# monitoring/log_aggregation.yml
# ELK Stack (Elasticsearch, Logstash, Kibana) 設定

version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.5.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5044:5044"
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.5.0
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_HOSTS: http://elasticsearch:9200
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.5.0
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/log/shiftmaster:/var/log/shiftmaster:ro
    depends_on:
      - logstash

volumes:
  elasticsearch_data:
```

```yaml
# monitoring/filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/shiftmaster/*.log
  fields:
    service: shiftmaster
    environment: production
  multiline.pattern: '^\d{4}-\d{2}-\d{2}'
  multiline.negate: true
  multiline.match: after

output.logstash:
  hosts: ["logstash:5044"]

processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
```

```ruby
# monitoring/logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][service] == "shiftmaster" {
    grok {
      match => { 
        "message" => "%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:level}\] %{DATA:logger}: %{GREEDYDATA:message}" 
      }
    }
    
    date {
      match => [ "timestamp", "yyyy-MM-dd HH:mm:ss,SSS" ]
    }
    
    if [level] in ["ERROR", "CRITICAL"] {
      mutate {
        add_tag => [ "alert" ]
      }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "shiftmaster-logs-%{+YYYY.MM.dd}"
  }
}
```

---

このガイドにより、ShiftMasterシステムの包括的な運用管理・監視体制が確立されます。24時間365日の安定稼働を実現し、医療機関での安心・安全な運用を支援します。

**最終更新**: 2024年1月20日  
**対象バージョン**: ShiftMaster 2.0.0  
**メンテナンス担当**: システム管理者チーム
