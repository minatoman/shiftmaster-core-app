# コノハVPS SSH鍵登録 PowerShellスクリプト
# 認証情報を設定してください
$username = "YOUR_CONOHA_USERNAME"
$password = "YOUR_CONOHA_PASSWORD" 
$tenantId = "YOUR_TENANT_ID"

$authBody = @{
    auth = @{
        passwordCredentials = @{
            username = "YOUR_CONOHA_USERNAME"
            password = "YOUR_CONOHA_PASSWORD"
        }
        tenantId = "YOUR_TENANT_ID"
    }
} | ConvertTo-Json -Depth 3

$authResponse = Invoke-RestMethod -Uri "https://identity.tyo1.conoha.io/v2.0/tokens" -Method POST -Body $authBody -ContentType "application/json"
$token = $authResponse.access.token.id
$tenantId = $authResponse.access.token.tenant.id

$keyBody = @{
    keypair = @{
        name = "mednext-vps-key"
        public_key = @"
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC+DmzVLHtA3z0p0nyJyMgHqleZfkpB7dobgOmNHrtFZ1NqFkvXLh1EruQr+rICmduLuFiZKqcUwn9H6GvVK0Lju8/mOTFA4e2apM4iXVu5kb402cVa9jOJAsY4BW9e55Dji7hjDlrUyWrnARr6kw0t7jGXmdBSkzPWNYSK9VjXNTgcu8u257NqTWzJV/5GRKrjJRgSb18VX6y3lKtb77KBIozy8oAkToKQFTpVsux+7qLE9K+Cdgdqm7yspHvGuy8ANpWseV7NPaNo2RZiyunRm1Pe4bdM7Sb9LdDcLoynAtTSEksdb+Lgtm6ucF8mrwHISyqa6Sd5uyuo7azrUOkUS3YB0DYrA1setsIRhWlENc9/PIuKq1wQYwGmo5/ubIwyu7z2IBFqtGrnLK8c4ePVzHNsbZ4MsSsIWv60kk/boAgmbt2BtHAr/BG1Mb+WGpr+908sWK49w0p1+gH9BmBNIdssaniPg8GlutUweYPo+lIL99LnfT9mOfD01tW+KB8EDYc2ML09RzfKPKGtBJLGAcWBQb+XcANQTXEoEn/iPXLhpG00JgdDEOGpHVPsrkrJNLxfvR1x0dBx70vRdzKa49hUHVOiVIDXmUppJqHQxuV7Vc6TURHUUVvhKq33qXHty+8U4Xnh31TGSRMiMr9XwbVvNQkml/HO/xKU47oNrw== mednext-vps-key
"@
    }
} | ConvertTo-Json -Depth 2

$keyResponse = Invoke-RestMethod -Uri "https://compute.tyo1.conoha.io/v2/$tenantId/os-keypairs" -Method POST -Body $keyBody -ContentType "application/json" -Headers @{"X-Auth-Token" = $token}


Write-Host "SSH鍵登録完了" -ForegroundColor Green
