# 🚀 デプロイメント・インフラ自動化ガイド

## 🏗️ インフラストラクチャ自動化

### ☁️ クラウドインフラ自動化（Azure/AWS）

#### Azure Resource Manager (ARM) テンプレート

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "projectName": {
      "type": "string",
      "defaultValue": "shiftmaster",
      "metadata": {
        "description": "プロジェクト名"
      }
    },
    "environment": {
      "type": "string",
      "defaultValue": "production",
      "allowedValues": ["development", "staging", "production"],
      "metadata": {
        "description": "デプロイ環境"
      }
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]",
      "metadata": {
        "description": "リソースの場所"
      }
    }
  },
  "variables": {
    "resourcePrefix": "[concat(parameters('projectName'), '-', parameters('environment'))]",
    "appServicePlanName": "[concat(variables('resourcePrefix'), '-plan')]",
    "webAppName": "[concat(variables('resourcePrefix'), '-web')]",
    "databaseServerName": "[concat(variables('resourcePrefix'), '-dbserver')]",
    "databaseName": "[concat(parameters('projectName'), 'db')]",
    "redisName": "[concat(variables('resourcePrefix'), '-redis')]",
    "keyVaultName": "[concat(variables('resourcePrefix'), '-kv')]",
    "storageAccountName": "[concat(replace(variables('resourcePrefix'), '-', ''), 'storage')]"
  },
  "resources": [
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2021-02-01",
      "name": "[variables('appServicePlanName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "P1v2",
        "tier": "PremiumV2",
        "size": "P1v2",
        "capacity": 2
      },
      "properties": {
        "reserved": true
      }
    },
    {
      "type": "Microsoft.Web/sites",
      "apiVersion": "2021-02-01",
      "name": "[variables('webAppName')]",
      "location": "[parameters('location')]",
      "dependsOn": [
        "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]"
      ],
      "properties": {
        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', variables('appServicePlanName'))]",
        "siteConfig": {
          "linuxFxVersion": "PYTHON|3.11",
          "appSettings": [
            {
              "name": "DJANGO_SETTINGS_MODULE",
              "value": "shiftmaster.settings.production"
            },
            {
              "name": "DATABASE_URL",
              "value": "[concat('postgresql://', parameters('databaseAdminLogin'), ':', parameters('databaseAdminPassword'), '@', variables('databaseServerName'), '.postgres.database.azure.com/', variables('databaseName'))]"
            },
            {
              "name": "REDIS_URL",
              "value": "[concat('redis://', variables('redisName'), '.redis.cache.windows.net:6380?ssl=True')]"
            }
          ],
          "connectionStrings": [
            {
              "name": "DefaultConnection",
              "connectionString": "[concat('Server=', variables('databaseServerName'), '.postgres.database.azure.com;Database=', variables('databaseName'), ';')]",
              "type": "PostgreSQL"
            }
          ]
        }
      }
    },
    {
      "type": "Microsoft.DBforPostgreSQL/flexibleServers",
      "apiVersion": "2021-06-01",
      "name": "[variables('databaseServerName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "Standard_B2s",
        "tier": "Burstable"
      },
      "properties": {
        "version": "15",
        "administratorLogin": "[parameters('databaseAdminLogin')]",
        "administratorLoginPassword": "[parameters('databaseAdminPassword')]",
        "storage": {
          "storageSizeGB": 32
        },
        "backup": {
          "backupRetentionDays": 30,
          "geoRedundantBackup": "Enabled"
        },
        "highAvailability": {
          "mode": "ZoneRedundant"
        }
      }
    },
    {
      "type": "Microsoft.Cache/redis",
      "apiVersion": "2021-06-01",
      "name": "[variables('redisName')]",
      "location": "[parameters('location')]",
      "properties": {
        "sku": {
          "name": "Premium",
          "family": "P",
          "capacity": 1
        },
        "enableNonSslPort": false,
        "minimumTlsVersion": "1.2",
        "redisConfiguration": {
          "maxmemory-policy": "allkeys-lru"
        }
      }
    },
    {
      "type": "Microsoft.KeyVault/vaults",
      "apiVersion": "2021-11-01-preview",
      "name": "[variables('keyVaultName')]",
      "location": "[parameters('location')]",
      "properties": {
        "sku": {
          "family": "A",
          "name": "standard"
        },
        "tenantId": "[subscription().tenantId]",
        "accessPolicies": [],
        "enabledForDeployment": true,
        "enabledForTemplateDeployment": true,
        "enabledForDiskEncryption": true,
        "enableRbacAuthorization": true
      }
    },
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2021-09-01",
      "name": "[variables('storageAccountName')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "Standard_ZRS"
      },
      "kind": "StorageV2",
      "properties": {
        "supportsHttpsTrafficOnly": true,
        "minimumTlsVersion": "TLS1_2",
        "allowBlobPublicAccess": false,
        "encryption": {
          "services": {
            "blob": {
              "enabled": true
            },
            "file": {
              "enabled": true
            }
          },
          "keySource": "Microsoft.Storage"
        }
      }
    }
  ],
  "outputs": {
    "webAppUrl": {
      "type": "string",
      "value": "[concat('https://', variables('webAppName'), '.azurewebsites.net')]"
    },
    "databaseConnectionString": {
      "type": "string",
      "value": "[concat('postgresql://', variables('databaseServerName'), '.postgres.database.azure.com/', variables('databaseName'))]"
    }
  }
}
```

#### Terraform IaC自動化

```hcl
# infrastructure/terraform/main.tf

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
  
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstatestore"
    container_name       = "tfstate"
    key                  = "shiftmaster.terraform.tfstate"
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}

# 変数定義
variable "project_name" {
  description = "プロジェクト名"
  type        = string
  default     = "shiftmaster"
}

variable "environment" {
  description = "環境名"
  type        = string
  default     = "production"
}

variable "location" {
  description = "Azureリージョン"
  type        = string
  default     = "Japan East"
}

variable "database_admin_login" {
  description = "データベース管理者ユーザー名"
  type        = string
  sensitive   = true
}

variable "database_admin_password" {
  description = "データベース管理者パスワード"
  type        = string
  sensitive   = true
}

# ローカル変数
locals {
  resource_prefix = "${var.project_name}-${var.environment}"
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    CreatedDate = timestamp()
  }
}

# ランダムパスワード生成
resource "random_password" "database_password" {
  count   = var.database_admin_password == "" ? 1 : 0
  length  = 32
  special = true
}

# リソースグループ
resource "azurerm_resource_group" "main" {
  name     = "${local.resource_prefix}-rg"
  location = var.location
  tags     = local.common_tags
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "${local.resource_prefix}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  os_type            = "Linux"
  sku_name           = "P1v2"
  
  tags = local.common_tags
}

# App Service
resource "azurerm_linux_web_app" "main" {
  name                = "${local.resource_prefix}-web"
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  service_plan_id    = azurerm_service_plan.main.id
  
  site_config {
    linux_fx_version = "PYTHON|3.11"
    
    application_stack {
      python_version = "3.11"
    }
    
    app_command_line = "gunicorn --bind=0.0.0.0 --workers=2 shiftmaster.wsgi"
  }
  
  app_settings = {
    "DJANGO_SETTINGS_MODULE" = "shiftmaster.settings.production"
    "DATABASE_URL"          = "postgresql://${var.database_admin_login}:${var.database_admin_password}@${azurerm_postgresql_flexible_server.main.fqdn}/${azurerm_postgresql_flexible_server_database.main.name}"
    "REDIS_URL"             = "redis://${azurerm_redis_cache.main.hostname}:${azurerm_redis_cache.main.ssl_port}?ssl=True"
    "SECRET_KEY"            = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.django_secret.id})"
    "ALLOWED_HOSTS"         = "${local.resource_prefix}-web.azurewebsites.net"
  }
  
  identity {
    type = "SystemAssigned"
  }
  
  tags = local.common_tags
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "${local.resource_prefix}-dbserver"
  resource_group_name    = azurerm_resource_group.main.name
  location              = azurerm_resource_group.main.location
  version               = "15"
  administrator_login    = var.database_admin_login
  administrator_password = var.database_admin_password
  
  storage_mb   = 32768
  sku_name     = "B_Standard_B2s"
  
  backup_retention_days        = 30
  geo_redundant_backup_enabled = true
  
  high_availability {
    mode = "ZoneRedundant"
  }
  
  tags = local.common_tags
}

# PostgreSQL Database
resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = "${var.project_name}db"
  server_id = azurerm_postgresql_flexible_server.main.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# Redis Cache
resource "azurerm_redis_cache" "main" {
  name                = "${local.resource_prefix}-redis"
  location           = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  capacity           = 1
  family             = "P"
  sku_name           = "Premium"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"
  
  redis_configuration {
    maxmemory_policy = "allkeys-lru"
  }
  
  tags = local.common_tags
}

# Key Vault
resource "azurerm_key_vault" "main" {
  name                       = "${local.resource_prefix}-kv"
  location                  = azurerm_resource_group.main.location
  resource_group_name       = azurerm_resource_group.main.name
  tenant_id                 = data.azurerm_client_config.current.tenant_id
  sku_name                  = "standard"
  soft_delete_retention_days = 7
  
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id
    
    secret_permissions = [
      "Get", "List", "Set", "Delete", "Purge", "Recover"
    ]
  }
  
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = azurerm_linux_web_app.main.identity[0].principal_id
    
    secret_permissions = [
      "Get"
    ]
  }
  
  tags = local.common_tags
}

# Key Vault Secret
resource "azurerm_key_vault_secret" "django_secret" {
  name         = "django-secret-key"
  value        = random_password.django_secret.result
  key_vault_id = azurerm_key_vault.main.id
  
  depends_on = [azurerm_key_vault.main]
}

resource "random_password" "django_secret" {
  length  = 50
  special = true
}

# Storage Account
resource "azurerm_storage_account" "main" {
  name                     = "${replace(local.resource_prefix, "-", "")}storage"
  resource_group_name      = azurerm_resource_group.main.name
  location                = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "ZRS"
  min_tls_version         = "TLS1_2"
  
  blob_properties {
    delete_retention_policy {
      days = 30
    }
  }
  
  tags = local.common_tags
}

# データソース
data "azurerm_client_config" "current" {}

# 出力値
output "web_app_url" {
  description = "WebアプリのURL"
  value       = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "database_connection_string" {
  description = "データベース接続文字列"
  value       = "postgresql://${azurerm_postgresql_flexible_server.main.fqdn}/${azurerm_postgresql_flexible_server_database.main.name}"
  sensitive   = true
}

output "redis_connection_string" {
  description = "Redis接続文字列"
  value       = "redis://${azurerm_redis_cache.main.hostname}:${azurerm_redis_cache.main.ssl_port}?ssl=True"
  sensitive   = true
}
```

### 🐳 Kubernetes自動化

#### Helm Chart設定

```yaml
# infrastructure/helm/shiftmaster/Chart.yaml
apiVersion: v2
name: shiftmaster
description: Medical Shift Management System
type: application
version: 2.0.0
appVersion: "2.0.0"
keywords:
  - medical
  - shift-management
  - healthcare
  - django
home: https://github.com/minatoman/shiftmaster-core-app
sources:
  - https://github.com/minatoman/shiftmaster-core-app
maintainers:
  - name: ShiftMaster Team
    email: team@shiftmaster.dev
```

```yaml
# infrastructure/helm/shiftmaster/values.yaml
# ShiftMaster Helm Chart設定

global:
  imageRegistry: "registry.example.com"
  imagePullSecrets: []
  
image:
  repository: shiftmaster/app
  tag: "2.0.0"
  pullPolicy: IfNotPresent

replicaCount: 3

service:
  type: LoadBalancer
  port: 80
  targetPort: 8000
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"

ingress:
  enabled: true
  className: "nginx"
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
  hosts:
    - host: shiftmaster.hospital.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: shiftmaster-tls
      hosts:
        - shiftmaster.hospital.com

resources:
  limits:
    cpu: 1000m
    memory: 2Gi
  requests:
    cpu: 500m
    memory: 1Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

postgresql:
  enabled: true
  auth:
    database: shiftmaster
    username: shiftmaster
    existingSecret: postgresql-secret
  architecture: replication
  primary:
    persistence:
      enabled: true
      size: 100Gi
      storageClass: premium-ssd
  readReplicas:
    replicaCount: 2
    persistence:
      enabled: true
      size: 100Gi

redis:
  enabled: true
  architecture: replication
  auth:
    enabled: true
    existingSecret: redis-secret
  master:
    persistence:
      enabled: true
      size: 10Gi
  replica:
    replicaCount: 2
    persistence:
      enabled: true
      size: 10Gi

celery:
  enabled: true
  worker:
    replicaCount: 2
    resources:
      limits:
        cpu: 500m
        memory: 1Gi
      requests:
        cpu: 250m
        memory: 512Mi
  beat:
    enabled: true
    resources:
      limits:
        cpu: 100m
        memory: 256Mi

monitoring:
  enabled: true
  prometheus:
    enabled: true
  grafana:
    enabled: true
  alerts:
    enabled: true

backup:
  enabled: true
  schedule: "0 2 * * *"  # 毎日2時
  retention: 30
  storage:
    enabled: true
    size: 500Gi
    storageClass: standard

security:
  networkPolicies:
    enabled: true
  podSecurityPolicy:
    enabled: true
  rbac:
    enabled: true

configMap:
  data:
    DJANGO_SETTINGS_MODULE: "shiftmaster.settings.production"
    ALLOWED_HOSTS: "shiftmaster.hospital.com,localhost"
    DEBUG: "False"
    USE_TZ: "True"
    TIME_ZONE: "Asia/Tokyo"

secrets:
  secretKey: ""  # K8s Secret から取得
  databaseUrl: ""  # K8s Secret から取得
  redisUrl: ""  # K8s Secret から取得
```

```yaml
# infrastructure/helm/shiftmaster/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "shiftmaster.fullname" . }}
  labels:
    {{- include "shiftmaster.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "shiftmaster.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
      labels:
        {{- include "shiftmaster.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.global.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "shiftmaster.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      initContainers:
        - name: db-migrate
          image: "{{ .Values.global.imageRegistry }}/{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["python", "manage.py", "migrate"]
          envFrom:
            - configMapRef:
                name: {{ include "shiftmaster.fullname" . }}-config
            - secretRef:
                name: {{ include "shiftmaster.fullname" . }}-secret
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.global.imageRegistry }}/{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health/
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready/
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          envFrom:
            - configMapRef:
                name: {{ include "shiftmaster.fullname" . }}-config
            - secretRef:
                name: {{ include "shiftmaster.fullname" . }}-secret
          volumeMounts:
            - name: static-files
              mountPath: /app/staticfiles
            - name: media-files
              mountPath: /app/media
      volumes:
        - name: static-files
          persistentVolumeClaim:
            claimName: {{ include "shiftmaster.fullname" . }}-static
        - name: media-files
          persistentVolumeClaim:
            claimName: {{ include "shiftmaster.fullname" . }}-media
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

## 🔄 CI/CDパイプライン自動化

### 🔧 GitHub Actions完全ワークフロー

```yaml
# .github/workflows/ci-cd-pipeline.yml
name: ShiftMaster CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]

env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'
  DOCKER_REGISTRY: 'ghcr.io'
  IMAGE_NAME: 'minatoman/shiftmaster'

jobs:
  # 1. コード品質・セキュリティチェック
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          
      - name: Cache Python dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
          
      - name: Lint with flake8
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
          
      - name: Security scan with bandit
        run: |
          bandit -r . -f json -o bandit-report.json
          
      - name: Type checking with mypy
        run: |
          mypy . --ignore-missing-imports
          
      - name: Check code formatting with black
        run: |
          black --check .
          
      - name: Import sorting with isort
        run: |
          isort --check-only .
          
      - name: Upload security scan results
        uses: actions/upload-artifact@v3
        with:
          name: security-report
          path: bandit-report.json

  # 2. テスト実行
  test:
    runs-on: ubuntu-latest
    needs: quality-check
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_shiftmaster
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
          
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-test.txt
          
      - name: Run unit tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_shiftmaster
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key-for-github-actions
        run: |
          python manage.py migrate
          pytest --cov=. --cov-report=xml --cov-report=html --junitxml=pytest.xml
          
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
          
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: |
            pytest.xml
            htmlcov/

  # 3. セキュリティスキャン
  security-scan:
    runs-on: ubuntu-latest
    needs: quality-check
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
          
      - name: Upload Trivy scan results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  # 4. Dockerイメージビルド
  build-image:
    runs-on: ubuntu-latest
    needs: [test, security-scan]
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.DOCKER_REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
            
      - name: Build and push Docker image
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile.prod
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64
          
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          image: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: spdx-json
          output-file: sbom.spdx.json
          
      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.spdx.json

  # 5. ステージングデプロイ
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build-image
    if: github.ref == 'refs/heads/develop'
    environment: staging
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Deploy to Azure App Service (Staging)
        uses: azure/webapps-deploy@v2
        with:
          app-name: 'shiftmaster-staging-web'
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE_STAGING }}
          images: ${{ needs.build-image.outputs.image-tag }}
          
      - name: Run smoke tests
        run: |
          sleep 30  # アプリケーション起動待機
          curl -f https://shiftmaster-staging-web.azurewebsites.net/health/ || exit 1
          
      - name: Notify Slack
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: '#deployments'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        if: always()

  # 6. プロダクションデプロイ
  deploy-production:
    runs-on: ubuntu-latest
    needs: build-image
    if: github.event_name == 'release'
    environment: production
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: '1.28.0'
          
      - name: Set up Helm
        uses: azure/setup-helm@v3
        with:
          version: '3.12.0'
          
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
          
      - name: Set AKS context
        uses: azure/aks-set-context@v3
        with:
          resource-group: 'shiftmaster-production-rg'
          cluster-name: 'shiftmaster-aks'
          
      - name: Deploy with Helm
        run: |
          helm upgrade --install shiftmaster ./infrastructure/helm/shiftmaster \
            --namespace production \
            --create-namespace \
            --set image.tag=${{ github.sha }} \
            --set global.imageRegistry=${{ env.DOCKER_REGISTRY }} \
            --wait --timeout=10m
            
      - name: Run production health check
        run: |
          kubectl wait --for=condition=available --timeout=300s deployment/shiftmaster -n production
          kubectl get pods -n production
          
      - name: Run production smoke tests
        run: |
          EXTERNAL_IP=$(kubectl get service shiftmaster -n production -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
          curl -f http://$EXTERNAL_IP/health/ || exit 1
          
      - name: Notify success
        uses: 8398a7/action-slack@v3
        with:
          status: success
          channel: '#production-deployments'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
          text: "🚀 ShiftMaster ${{ github.event.release.tag_name }} deployed to production successfully!"

  # 7. パフォーマンステスト
  performance-test:
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.ref == 'refs/heads/develop'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Run Locust performance tests
        run: |
          pip install locust
          locust -f tests/performance/locustfile.py \
            --host https://shiftmaster-staging-web.azurewebsites.net \
            --users 50 \
            --spawn-rate 5 \
            --run-time 5m \
            --headless \
            --html performance-report.html
            
      - name: Upload performance report
        uses: actions/upload-artifact@v3
        with:
          name: performance-report
          path: performance-report.html
```

### 🔧 Azure DevOps Pipeline

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
  tags:
    include:
      - v*

pr:
  branches:
    include:
      - main

variables:
  pythonVersion: '3.11'
  vmImageName: 'ubuntu-latest'
  projectName: 'shiftmaster'
  
stages:
  # Build & Test Stage
  - stage: BuildAndTest
    displayName: 'Build and Test'
    jobs:
      - job: Test
        displayName: 'Run Tests'
        pool:
          vmImage: $(vmImageName)
        
        services:
          postgres:
            image: postgres:15
            env:
              POSTGRES_PASSWORD: postgres
              POSTGRES_DB: test_shiftmaster
            ports:
              - 5432:5432
          redis:
            image: redis:7
            ports:
              - 6379:6379
        
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '$(pythonVersion)'
            displayName: 'Use Python $(pythonVersion)'
            
          - script: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt
              pip install -r requirements-test.txt
            displayName: 'Install dependencies'
            
          - script: |
              export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/test_shiftmaster"
              export REDIS_URL="redis://localhost:6379/0"
              export SECRET_KEY="test-secret-key"
              python manage.py migrate
              pytest --cov=. --cov-report=xml --junitxml=pytest.xml
            displayName: 'Run tests'
            
          - task: PublishTestResults@2
            condition: succeededOrFailed()
            inputs:
              testResultsFiles: 'pytest.xml'
              testRunTitle: 'Publish test results for Python $(pythonVersion)'
              
          - task: PublishCodeCoverageResults@1
            inputs:
              codeCoverageTool: Cobertura
              summaryFileLocation: 'coverage.xml'

  # Build Docker Image
  - stage: BuildImage
    displayName: 'Build Docker Image'
    dependsOn: BuildAndTest
    condition: succeeded()
    jobs:
      - job: BuildAndPush
        displayName: 'Build and Push Docker Image'
        pool:
          vmImage: $(vmImageName)
        steps:
          - task: Docker@2
            displayName: 'Build and push Docker image'
            inputs:
              containerRegistry: 'ACR Connection'
              repository: '$(projectName)'
              command: 'buildAndPush'
              Dockerfile: 'Dockerfile.prod'
              tags: |
                $(Build.BuildId)
                latest

  # Deploy to Staging
  - stage: DeployStaging
    displayName: 'Deploy to Staging'
    dependsOn: BuildImage
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/develop'))
    jobs:
      - deployment: DeployStaging
        displayName: 'Deploy to Staging Environment'
        pool:
          vmImage: $(vmImageName)
        environment: 'staging'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureWebApp@1
                  displayName: 'Deploy to Azure Web App'
                  inputs:
                    azureSubscription: 'Azure Subscription'
                    appType: 'webAppContainer'
                    appName: '$(projectName)-staging-web'
                    deployToSlotOrASE: true
                    resourceGroupName: '$(projectName)-staging-rg'
                    slotName: 'staging'
                    imageName: 'yourregistry.azurecr.io/$(projectName):$(Build.BuildId)'

  # Deploy to Production
  - stage: DeployProduction
    displayName: 'Deploy to Production'
    dependsOn: BuildImage
    condition: and(succeeded(), startsWith(variables['Build.SourceBranch'], 'refs/tags/v'))
    jobs:
      - deployment: DeployProduction
        displayName: 'Deploy to Production Environment'
        pool:
          vmImage: $(vmImageName)
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: HelmDeploy@0
                  displayName: 'Deploy with Helm'
                  inputs:
                    connectionType: 'Azure Resource Manager'
                    azureSubscription: 'Azure Subscription'
                    azureResourceGroup: '$(projectName)-production-rg'
                    kubernetesCluster: '$(projectName)-aks'
                    namespace: 'production'
                    command: 'upgrade'
                    chartType: 'FilePath'
                    chartPath: 'infrastructure/helm/shiftmaster'
                    releaseName: 'shiftmaster'
                    arguments: '--set image.tag=$(Build.BuildId) --wait --timeout=10m'
```

## 🚀 デプロイメント自動化スクリプト

### 📦 ワンクリックデプロイスクリプト

```powershell
# scripts/deploy-production.ps1
<#
.SYNOPSIS
    ShiftMaster プロダクション環境への自動デプロイ
.DESCRIPTION
    本番環境への完全自動デプロイを実行します
.PARAMETER Environment
    デプロイ先環境 (staging/production)
.PARAMETER Version
    デプロイするバージョンタグ
.PARAMETER SkipTests
    テストをスキップするかどうか
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("staging", "production")]
    [string]$Environment,
    
    [Parameter(Mandatory=$false)]
    [string]$Version = "latest",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipTests = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$DryRun = $false
)

# エラー時停止設定
$ErrorActionPreference = "Stop"

# ログ設定
$LogFile = "deploy-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
$LogPath = ".\logs\$LogFile"

function Write-Log {
    param($Message, $Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Write-Host $LogEntry
    $LogEntry | Out-File -FilePath $LogPath -Append -Encoding UTF8
}

function Test-Prerequisites {
    Write-Log "前提条件チェック開始..."
    
    # 必要なツールの確認
    $RequiredTools = @("docker", "kubectl", "helm", "az")
    foreach ($Tool in $RequiredTools) {
        if (-not (Get-Command $Tool -ErrorAction SilentlyContinue)) {
            throw "$Tool が見つかりません。インストールしてください。"
        }
        Write-Log "$Tool: OK"
    }
    
    # Azure CLI ログイン確認
    $AzAccount = az account show --output json 2>$null | ConvertFrom-Json
    if (-not $AzAccount) {
        throw "Azure CLI にログインしていません。'az login' を実行してください。"
    }
    Write-Log "Azure CLI ログイン: OK ($($AzAccount.user.name))"
    
    # Kubernetes接続確認
    try {
        kubectl cluster-info --request-timeout=5s | Out-Null
        Write-Log "Kubernetes 接続: OK"
    }
    catch {
        throw "Kubernetes クラスターに接続できません。"
    }
}

function Invoke-PreDeploymentTests {
    if ($SkipTests) {
        Write-Log "テストをスキップします"
        return
    }
    
    Write-Log "デプロイ前テスト実行..."
    
    # 単体テスト
    Write-Log "単体テスト実行中..."
    & python -m pytest tests/unit/ --junitxml=test-results.xml
    if ($LASTEXITCODE -ne 0) {
        throw "単体テストが失敗しました"
    }
    
    # 統合テスト
    Write-Log "統合テスト実行中..."
    & python -m pytest tests/integration/ --junitxml=integration-results.xml
    if ($LASTEXITCODE -ne 0) {
        throw "統合テストが失敗しました"
    }
    
    # セキュリティスキャン
    Write-Log "セキュリティスキャン実行中..."
    & bandit -r . -f json -o security-report.json
    if ($LASTEXITCODE -ne 0) {
        Write-Log "セキュリティ警告が検出されました" "WARNING"
    }
    
    Write-Log "全テスト完了"
}

function Build-DockerImage {
    Write-Log "Docker イメージビルド開始..."
    
    $ImageTag = "shiftmaster:$Version"
    $RegistryImage = "yourregistry.azurecr.io/$ImageTag"
    
    if ($DryRun) {
        Write-Log "[DRY RUN] Docker build $RegistryImage"
        return $RegistryImage
    }
    
    # イメージビルド
    Write-Log "Building image: $RegistryImage"
    & docker build -t $ImageTag -f Dockerfile.prod .
    if ($LASTEXITCODE -ne 0) {
        throw "Docker イメージビルドが失敗しました"
    }
    
    # タグ付け
    & docker tag $ImageTag $RegistryImage
    
    # プッシュ
    Write-Log "Pushing image to registry..."
    & docker push $RegistryImage
    if ($LASTEXITCODE -ne 0) {
        throw "Docker イメージプッシュが失敗しました"
    }
    
    Write-Log "Docker イメージビルド完了: $RegistryImage"
    return $RegistryImage
}

function Invoke-DatabaseMigration {
    param($ImageName)
    
    Write-Log "データベースマイグレーション実行..."
    
    if ($DryRun) {
        Write-Log "[DRY RUN] Database migration"
        return
    }
    
    # マイグレーションジョブ実行
    $MigrationJob = @"
apiVersion: batch/v1
kind: Job
metadata:
  name: migration-$(Get-Date -Format 'yyyymmdd-hhmmss')
  namespace: $Environment
spec:
  template:
    spec:
      containers:
      - name: migration
        image: $ImageName
        command: ["python", "manage.py", "migrate"]
        envFrom:
        - configMapRef:
            name: shiftmaster-config
        - secretRef:
            name: shiftmaster-secret
      restartPolicy: Never
  backoffLimit: 3
"@
    
    $MigrationJob | kubectl apply -f -
    
    # ジョブ完了待機
    Write-Log "マイグレーション完了待機中..."
    & kubectl wait --for=condition=complete --timeout=300s job/migration-$(Get-Date -Format 'yyyymmdd-hhmmss') -n $Environment
    
    if ($LASTEXITCODE -ne 0) {
        throw "データベースマイグレーションが失敗しました"
    }
    
    Write-Log "データベースマイグレーション完了"
}

function Deploy-Application {
    param($ImageName)
    
    Write-Log "アプリケーションデプロイ開始..."
    
    if ($DryRun) {
        Write-Log "[DRY RUN] Application deployment"
        return
    }
    
    # Helm値準備
    $HelmValues = @{
        "image.tag" = $Version
        "image.repository" = "shiftmaster"
        "global.imageRegistry" = "yourregistry.azurecr.io"
        "environment" = $Environment
    }
    
    # Helm引数構築
    $HelmArgs = @()
    foreach ($Key in $HelmValues.Keys) {
        $HelmArgs += "--set"
        $HelmArgs += "$Key=$($HelmValues[$Key])"
    }
    
    # Helmデプロイ実行
    Write-Log "Helm デプロイ実行中..."
    & helm upgrade --install shiftmaster ./infrastructure/helm/shiftmaster `
        --namespace $Environment `
        --create-namespace `
        $HelmArgs `
        --wait `
        --timeout=10m
        
    if ($LASTEXITCODE -ne 0) {
        throw "Helm デプロイが失敗しました"
    }
    
    Write-Log "アプリケーションデプロイ完了"
}

function Test-PostDeployment {
    Write-Log "デプロイ後テスト開始..."
    
    # Pod稼働状態確認
    Write-Log "Pod 状態確認中..."
    & kubectl get pods -n $Environment -l app.kubernetes.io/name=shiftmaster
    
    # ヘルスチェック
    Write-Log "ヘルスチェック実行中..."
    $MaxAttempts = 10
    $Attempt = 0
    
    do {
        $Attempt++
        try {
            $ServiceIP = kubectl get service shiftmaster -n $Environment -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
            if ($ServiceIP) {
                $Response = Invoke-WebRequest -Uri "http://$ServiceIP/health/" -TimeoutSec 10
                if ($Response.StatusCode -eq 200) {
                    Write-Log "ヘルスチェック成功"
                    return
                }
            }
        }
        catch {
            Write-Log "ヘルスチェック試行 $Attempt/$MaxAttempts 失敗: $($_.Exception.Message)" "WARNING"
        }
        
        if ($Attempt -lt $MaxAttempts) {
            Start-Sleep -Seconds 30
        }
    } while ($Attempt -lt $MaxAttempts)
    
    throw "ヘルスチェックが失敗しました"
}

function Invoke-Rollback {
    param($PreviousVersion)
    
    Write-Log "ロールバック開始..." "WARNING"
    
    if ($DryRun) {
        Write-Log "[DRY RUN] Rollback to $PreviousVersion"
        return
    }
    
    & helm rollback shiftmaster --namespace $Environment
    
    if ($LASTEXITCODE -eq 0) {
        Write-Log "ロールバック完了" "WARNING"
    } else {
        Write-Log "ロールバック失敗" "ERROR"
    }
}

function Send-Notification {
    param($Success, $Message)
    
    $Status = if ($Success) { "SUCCESS" } else { "FAILED" }
    $Color = if ($Success) { "good" } else { "danger" }
    $Icon = if ($Success) { "✅" } else { "❌" }
    
    $SlackMessage = @{
        text = "$Icon ShiftMaster Deployment $Status"
        attachments = @(
            @{
                color = $Color
                fields = @(
                    @{
                        title = "Environment"
                        value = $Environment
                        short = $true
                    }
                    @{
                        title = "Version"
                        value = $Version
                        short = $true
                    }
                    @{
                        title = "Status"
                        value = $Message
                        short = $false
                    }
                )
                footer = "ShiftMaster DevOps"
                ts = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
            }
        )
    } | ConvertTo-Json -Depth 10
    
    try {
        $WebhookUrl = $env:SLACK_WEBHOOK_URL
        if ($WebhookUrl) {
            Invoke-RestMethod -Uri $WebhookUrl -Method Post -Body $SlackMessage -ContentType "application/json"
            Write-Log "Slack通知送信完了"
        }
    }
    catch {
        Write-Log "Slack通知送信失敗: $($_.Exception.Message)" "WARNING"
    }
}

# メイン実行
try {
    Write-Log "=== ShiftMaster Deployment Started ==="
    Write-Log "Environment: $Environment"
    Write-Log "Version: $Version"
    Write-Log "DryRun: $DryRun"
    
    # 前提条件チェック
    Test-Prerequisites
    
    # デプロイ前テスト
    Invoke-PreDeploymentTests
    
    # Dockerイメージビルド
    $ImageName = Build-DockerImage
    
    # データベースマイグレーション
    Invoke-DatabaseMigration -ImageName $ImageName
    
    # アプリケーションデプロイ
    Deploy-Application -ImageName $ImageName
    
    # デプロイ後テスト
    Test-PostDeployment
    
    Write-Log "=== Deployment Completed Successfully ==="
    Send-Notification -Success $true -Message "Deployment completed successfully"
    
}
catch {
    $ErrorMessage = $_.Exception.Message
    Write-Log "デプロイメントエラー: $ErrorMessage" "ERROR"
    
    # ロールバック実行
    if (-not $DryRun -and $Environment -eq "production") {
        Write-Log "プロダクション環境でエラー発生。ロールバックを実行します..." "WARNING"
        Invoke-Rollback
    }
    
    Send-Notification -Success $false -Message $ErrorMessage
    
    Write-Log "=== Deployment Failed ==="
    exit 1
}
```

---

このガイドにより、ShiftMasterの完全自動化されたデプロイメント・インフラ管理が実現され、企業レベルの CI/CD パイプラインによる安定した運用が可能になります。

**最終更新**: 2024年1月20日  
**対象バージョン**: ShiftMaster 2.0.0  
**DevOps担当**: インフラ・デプロイメントチーム
