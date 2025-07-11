#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コノハVPS SSH公開鍵自動登録スクリプト
"""

import requests
import json

class ConohaAPIClient:
    def __init__(self, username, password, tenant_id):
        self.username = username
        self.password = password
        self.tenant_id = tenant_id
        self.auth_endpoint = "https://identity.tyo1.conoha.io/v2.0"
        self.compute_endpoint = "https://compute.tyo1.conoha.io/v2"
        self.token = None
    
    def authenticate(self):
        """認証してトークンを取得"""
        auth_data = {
            "auth": {
                "passwordCredentials": {
                    "username": self.username,
                    "password": self.password
                },
                "tenantId": self.tenant_id
            }
        }
        
        try:
            response = requests.post(
                f"{self.auth_endpoint}/tokens",
                json=auth_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            self.token = result["access"]["token"]["id"]
            print("✅ 認証成功")
            return True
            
        except Exception as e:
            print(f"❌ 認証エラー: {e}")
            return False
    
    def register_ssh_key(self, key_name, public_key):
        """SSH公開鍵を登録"""
        if not self.token:
            print("❌ 認証が必要です")
            return False
        
        key_data = {
            "keypair": {
                "name": key_name,
                "public_key": public_key
            }
        }
        
        try:
            response = requests.post(
                f"{self.compute_endpoint}/{self.tenant_id}/os-keypairs",
                json=key_data,
                headers={
                    "Content-Type": "application/json",
                    "X-Auth-Token": self.token
                }
            )
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ SSH鍵登録成功: {key_name}")
            return True
            
        except Exception as e:
            print(f"❌ SSH鍵登録エラー: {e}")
            return False

def main():
    # 認証情報を設定（実際の値に置き換えてください）
    USERNAME = "YOUR_CONOHA_USERNAME"
    PASSWORD = "YOUR_CONOHA_PASSWORD"
    TENANT_ID = "YOUR_TENANT_ID"
    
    # SSH鍵情報
    KEY_NAME = "mednext-vps-key"
    PUBLIC_KEY = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC+DmzVLHtA3z0p0nyJyMgHqleZfkpB7dobgOmNHrtFZ1NqFkvXLh1EruQr+rICmduLuFiZKqcUwn9H6GvVK0Lju8/mOTFA4e2apM4iXVu5kb402cVa9jOJAsY4BW9e55Dji7hjDlrUyWrnARr6kw0t7jGXmdBSkzPWNYSK9VjXNTgcu8u257NqTWzJV/5GRKrjJRgSb18VX6y3lKtb77KBIozy8oAkToKQFTpVsux+7qLE9K+Cdgdqm7yspHvGuy8ANpWseV7NPaNo2RZiyunRm1Pe4bdM7Sb9LdDcLoynAtTSEksdb+Lgtm6ucF8mrwHISyqa6Sd5uyuo7azrUOkUS3YB0DYrA1setsIRhWlENc9/PIuKq1wQYwGmo5/ubIwyu7z2IBFqtGrnLK8c4ePVzHNsbZ4MsSsIWv60kk/boAgmbt2BtHAr/BG1Mb+WGpr+908sWK49w0p1+gH9BmBNIdssaniPg8GlutUweYPo+lIL99LnfT9mOfD01tW+KB8EDYc2ML09RzfKPKGtBJLGAcWBQb+XcANQTXEoEn/iPXLhpG00JgdDEOGpHVPsrkrJNLxfvR1x0dBx70vRdzKa49hUHVOiVIDXmUppJqHQxuV7Vc6TURHUUVvhKq33qXHty+8U4Xnh31TGSRMiMr9XwbVvNQkml/HO/xKU47oNrw== mednext-vps-key"""
    
    # API呼び出し実行
    client = ConohaAPIClient(USERNAME, PASSWORD, TENANT_ID)
    
    if client.authenticate():
        client.register_ssh_key(KEY_NAME, PUBLIC_KEY)
    else:
        print("認証に失敗しました")

if __name__ == "__main__":
    main()
