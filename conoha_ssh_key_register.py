#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コノハVPS SSH公開鍵登録コマンド生成器
共有キー対応版
"""

import json
import datetime
import requests
import base64


class ConohaSSHKeyRegister:
    def __init__(self):
        self.api_endpoint = "https://identity.tyo1.conoha.io/v2.0"
        self.compute_endpoint = "https://compute.tyo1.conoha.io/v2"
        
        # 提供された情報
        self.server_ip = "160.251.181.238"
        self.username = "root"
        self.key_name = "mednext-vps-key"
        self.public_key = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC+DmzVLHtA3z0p0nyJyMgHqleZfkpB7dobgOmNHrtFZ1NqFkvXLh1EruQr+rICmduLuFiZKqcUwn9H6GvVK0Lju8/mOTFA4e2apM4iXVu5kb402cVa9jOJAsY4BW9e55Dji7hjDlrUyWrnARr6kw0t7jGXmdBSkzPWNYSK9VjXNTgcu8u257NqTWzJV/5GRKrjJRgSb18VX6y3lKtb77KBIozy8oAkToKQFTpVsux+7qLE9K+Cdgdqm7yspHvGuy8ANpWseV7NPaNo2RZiyunRm1Pe4bdM7Sb9LdDcLoynAtTSEksdb+Lgtm6ucF8mrwHISyqa6Sd5uyuo7azrUOkUS3YB0DYrA1setsIRhWlENc9/PIuKq1wQYwGmo5/ubIwyu7z2IBFqtGrnLK8c4ePVzHNsbZ4MsSsIWv60kk/boAgmbt2BtHAr/BG1Mb+WGpr+908sWK49w0p1+gH9BmBNIdssaniPg8GlutUweYPo+lIL99LnfT9mOfD01tW+KB8EDYc2ML09RzfKPKGtBJLGAcWBQb+XcANQTXEoEn/iPXLhpG00JgdDEOGpHVPsrkrJNLxfvR1x0dBx70vRdzKa49hUHVOiVIDXmUppJqHQxuV7Vc6TURHUUVvhKq33qXHty+8U4Xnh31TGSRMiMr9XwbVvNQkml/HO/xKU47oNrw== mednext-vps-key"""

    def generate_curl_commands(self):
        """cURLコマンドを生成"""
        print("🔧 コノハVPS SSH公開鍵登録 cURLコマンド")
        print("=" * 60)
        
        # 1. 認証トークン取得コマンド
        auth_command = f'''curl -X POST "{self.api_endpoint}/tokens" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "auth": {{
      "passwordCredentials": {{
        "username": "YOUR_CONOHA_USERNAME",
        "password": "YOUR_CONOHA_PASSWORD"
      }},
      "tenantId": "YOUR_TENANT_ID"
    }}
  }}'
'''
        
        # 2. SSH鍵登録コマンド
        key_register_command = f'''curl -X POST "{self.compute_endpoint}/YOUR_TENANT_ID/os-keypairs" \\
  -H "Content-Type: application/json" \\
  -H "X-Auth-Token: YOUR_AUTH_TOKEN" \\
  -d '{{
    "keypair": {{
      "name": "{self.key_name}",
      "public_key": "{self.public_key.strip()}"
    }}
  }}'
'''
        
        print("📋 手順1: 認証トークンを取得")
        print("-" * 40)
        print(auth_command)
        print()
        
        print("📋 手順2: SSH公開鍵を登録")
        print("-" * 40)
        print(key_register_command)
        print()
        
        return auth_command, key_register_command

    def generate_powershell_commands(self):
        """PowerShellコマンドを生成"""
        print("🔧 PowerShell版コマンド")
        print("=" * 60)
        
        # PowerShell用のJSON文字列をエスケープ
        escaped_public_key = self.public_key.strip().replace('"', '""')
        
        ps_auth_command = f'''$authBody = @{{
    auth = @{{
        passwordCredentials = @{{
            username = "YOUR_CONOHA_USERNAME"
            password = "YOUR_CONOHA_PASSWORD"
        }}
        tenantId = "YOUR_TENANT_ID"
    }}
}} | ConvertTo-Json -Depth 3

$authResponse = Invoke-RestMethod -Uri "{self.api_endpoint}/tokens" -Method POST -Body $authBody -ContentType "application/json"
$token = $authResponse.access.token.id
$tenantId = $authResponse.access.token.tenant.id
'''

        ps_key_command = f'''$keyBody = @{{
    keypair = @{{
        name = "{self.key_name}"
        public_key = @"
{self.public_key.strip()}
"@
    }}
}} | ConvertTo-Json -Depth 2

$keyResponse = Invoke-RestMethod -Uri "{self.compute_endpoint}/$tenantId/os-keypairs" -Method POST -Body $keyBody -ContentType "application/json" -Headers @{{"X-Auth-Token" = $token}}
'''
        
        print("📋 PowerShell手順1: 認証とトークン取得")
        print("-" * 40)
        print(ps_auth_command)
        print()
        
        print("📋 PowerShell手順2: SSH鍵登録")
        print("-" * 40)
        print(ps_key_command)
        print()
        
        return ps_auth_command, ps_key_command

    def generate_python_script(self):
        """Python API呼び出しスクリプトを生成（改行修正版）"""
        # 公開鍵から改行を完全に除去
        clean_public_key = self.public_key.replace('\n', '').replace('\r', '').strip()
        
        python_script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コノハVPS SSH公開鍵自動登録スクリプト（改行修正版）
"""

import requests
import json

class ConohaAPIClient:
    def __init__(self, username, password, tenant_id):
        self.username = username
        self.password = password
        self.tenant_id = tenant_id
        self.auth_endpoint = "{self.api_endpoint}"
        self.compute_endpoint = "{self.compute_endpoint}"
        self.token = None
    
    def authenticate(self):
        """認証してトークンを取得"""
        auth_data = {{
            "auth": {{
                "passwordCredentials": {{
                    "username": self.username,
                    "password": self.password
                }},
                "tenantId": self.tenant_id
            }}
        }}
        
        try:
            response = requests.post(
                f"{{self.auth_endpoint}}/tokens",
                json=auth_data,
                headers={{"Content-Type": "application/json"}}
            )
            response.raise_for_status()
            
            result = response.json()
            self.token = result["access"]["token"]["id"]
            print("✅ 認証成功")
            return True
            
        except Exception as e:
            print(f"❌ 認証エラー: {{e}}")
            return False
    
    def delete_existing_key(self, key_name):
        """既存のSSH鍵を削除"""
        if not self.token:
            print("❌ 認証が必要です")
            return False
        
        try:
            response = requests.delete(
                f"{{self.compute_endpoint}}/{{self.tenant_id}}/os-keypairs/{{key_name}}",
                headers={{
                    "X-Auth-Token": self.token
                }}
            )
            
            if response.status_code == 202:
                print(f"✅ 既存のSSH鍵削除成功: {{key_name}}")
                return True
            elif response.status_code == 404:
                print(f"ℹ️ SSH鍵が見つかりません: {{key_name}} (新規登録)")
                return True
            else:
                print(f"⚠️ SSH鍵削除で予期しないレスポンス: {{response.status_code}}")
                return False
                
        except Exception as e:
            print(f"❌ SSH鍵削除エラー: {{e}}")
            return False
    
    def register_ssh_key(self, key_name, public_key):
        """SSH公開鍵を登録（改行完全除去版）"""
        if not self.token:
            print("❌ 認証が必要です")
            return False
        
        # 改行と余分なスペースを完全に除去
        clean_key = public_key.replace('\\n', '').replace('\\r', '').replace(' \\n', '').strip()
        
        print(f"🔍 鍵の長さ: {{len(clean_key)}} 文字")
        print(f"🔍 鍵の開始: {{clean_key[:50]}}...")
        print(f"🔍 鍵の終了: ...{{clean_key[-50:]}}")
        
        key_data = {{
            "keypair": {{
                "name": key_name,
                "public_key": clean_key
            }}
        }}
        
        try:
            response = requests.post(
                f"{{self.compute_endpoint}}/{{self.tenant_id}}/os-keypairs",
                json=key_data,
                headers={{
                    "Content-Type": "application/json",
                    "X-Auth-Token": self.token
                }}
            )
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ SSH鍵登録成功: {{key_name}}")
            print(f"🔑 登録された鍵のフィンガープリント: {{result.get('keypair', {{}}).get('fingerprint', 'N/A')}}")
            return True
            
        except Exception as e:
            print(f"❌ SSH鍵登録エラー: {{e}}")
            if hasattr(e, 'response') and e.response:
                print(f"📋 エラー詳細: {{e.response.text}}")
            return False
    
    def list_ssh_keys(self):
        """登録済みのSSH鍵一覧を取得"""
        if not self.token:
            print("❌ 認証が必要です")
            return False
        
        try:
            response = requests.get(
                f"{{self.compute_endpoint}}/{{self.tenant_id}}/os-keypairs",
                headers={{
                    "X-Auth-Token": self.token
                }}
            )
            response.raise_for_status()
            
            result = response.json()
            print("📋 登録済みSSH鍵一覧:")
            for keypair in result.get("keypairs", []):
                kp = keypair.get("keypair", {{}})
                print(f"  - 名前: {{kp.get('name')}}")
                print(f"    フィンガープリント: {{kp.get('fingerprint')}}")
            
            return True
            
        except Exception as e:
            print(f"❌ SSH鍵一覧取得エラー: {{e}}")
            return False

    def generate_new_ssh_key_pair(self, private_key_path="mednext_vps_key", public_key_path="mednext_vps_key.pub", key_comment=None):
        """新しいRSA SSH鍵ペアを生成し、ファイルに保存する（cryptography利用）"""
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.backends import default_backend
        except ImportError:
            print("[ERROR] cryptographyライブラリが必要です。pip install cryptography を実行してください。")
            return False

        # 鍵ペア生成
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        # 秘密鍵保存
        with open(private_key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        print(f"✅ 秘密鍵を保存: {private_key_path}")

        # 公開鍵OpenSSH形式で保存
        public_key = private_key.public_key()
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )
        if key_comment:
            pub_bytes += b" " + key_comment.encode("utf-8")
        with open(public_key_path, "wb") as f:
            f.write(pub_bytes)
        print(f"✅ 公開鍵を保存: {public_key_path}")

        # self.public_keyにもセット
        self.public_key = pub_bytes.decode("utf-8")
        print(f"🔑 公開鍵内容: {self.public_key}")
        return True

def main():
    # 認証情報を設定（実際の値に置き換えてください）
    USERNAME = "YOUR_CONOHA_USERNAME"
    PASSWORD = "YOUR_CONOHA_PASSWORD"
    TENANT_ID = "YOUR_TENANT_ID"
    
    # SSH鍵情報（改行完全除去版）
    KEY_NAME = "{self.key_name}"
    PUBLIC_KEY = """{clean_public_key}"""
    
    print("🚀 コノハVPS SSH鍵登録（改行修正版）")
    print("=" * 50)
    
    # API呼び出し実行
    client = ConohaAPIClient(USERNAME, PASSWORD, TENANT_ID)
    
    if client.authenticate():
        # 既存の鍵があれば削除
        print("\\n🗑️ 既存鍵の削除を試行...")
        client.delete_existing_key(KEY_NAME)
        
        # 新しい鍵を登録
        print("\\n📝 新しい鍵を登録...")
        if client.register_ssh_key(KEY_NAME, PUBLIC_KEY):
            print("\\n📋 登録確認...")
            client.list_ssh_keys()
            print("\\n🔗 SSH接続テスト:")
            print("ssh -i C:\\\\Users\\\\jinna\\\\.ssh\\\\mednext_vps_key root@{self.server_ip}")
        else:
            print("❌ SSH鍵登録に失敗しました")
    else:
        print("❌ 認証に失敗しました")

if __name__ == "__main__":
    register = ConohaSSHKeyRegister()
    # Windowsの絶対パスで新しい鍵を作成
    private_key_path = "C:\\Users\\jinna\\.ssh\\mednext_vps_key"
    public_key_path = "C:\\Users\\jinna\\.ssh\\mednext_vps_key.pub"
    register.generate_new_ssh_key_pair(private_key_path=private_key_path, public_key_path=public_key_path, key_comment="mednext-vps-key")
    print(f"\n✅ 新しいSSH鍵ペアを {private_key_path}, {public_key_path} に作成しました")

    # 公開鍵をセット
    with open(public_key_path, encoding="utf-8") as f:
        register.public_key = f.read().strip()

    # コノハVPSへ登録
    print("\n--- コノハVPSへ公開鍵を登録 ---")
    # 認証情報を入力してください
    USERNAME = "YOUR_CONOHA_USERNAME"
    PASSWORD = "YOUR_CONOHA_PASSWORD"
    TENANT_ID = "YOUR_TENANT_ID"
    # API呼び出し
    client = ConohaAPIClient(USERNAME, PASSWORD, TENANT_ID)
    if client.authenticate():
        print("\n🗑️ 既存鍵の削除を試行...")
        client.delete_existing_key(register.key_name)
        print("\n📝 新しい鍵を登録...")
        if client.register_ssh_key(register.key_name, register.public_key):
            print("\n🔗 SSH接続テスト:")
            print(f"ssh -i {private_key_path} {register.username}@{register.server_ip}")
        else:
            print("❌ SSH鍵登録に失敗しました")
    else:
        print("❌ 認証に失敗しました")
