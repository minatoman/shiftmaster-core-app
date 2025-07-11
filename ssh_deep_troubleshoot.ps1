# SSH Deep Troubleshooting Script for Company PC
# 会社PCでのSSH接続問題の詳細診断

Write-Host "=== SSH Deep Troubleshooting for Company PC ===" -ForegroundColor Green
Write-Host "診断開始: $(Get-Date)" -ForegroundColor Yellow

$PRIVATE_KEY = "C:\Users\jinna\.ssh\mednext_vps_key_new"
$PUBLIC_KEY = "C:\Users\jinna\.ssh\mednext_vps_key_new.pub"
$SSH_CONFIG = "C:\Users\jinna\.ssh\config"
$VPS_IP = "160.251.181.238"
$VPS_USER = "root"

Write-Host "`n1. SSH Key Files Status Check" -ForegroundColor Cyan
Write-Host "Private Key: $PRIVATE_KEY"
if (Test-Path $PRIVATE_KEY) {
    $privKeyInfo = Get-ChildItem $PRIVATE_KEY
    Write-Host "  Exists: YES" -ForegroundColor Green
    Write-Host "  Size: $($privKeyInfo.Length) bytes"
    Write-Host "  Modified: $($privKeyInfo.LastWriteTime)"
    
    # Check permissions
    $acl = Get-Acl $PRIVATE_KEY
    Write-Host "  Permissions:"
    $acl.Access | ForEach-Object {
        Write-Host "    $($_.IdentityReference): $($_.FileSystemRights)" -ForegroundColor Gray
    }
} else {
    Write-Host "  Exists: NO" -ForegroundColor Red
}

Write-Host "`nPublic Key: $PUBLIC_KEY"
if (Test-Path $PUBLIC_KEY) {
    $pubKeyInfo = Get-ChildItem $PUBLIC_KEY
    Write-Host "  Exists: YES" -ForegroundColor Green
    Write-Host "  Size: $($pubKeyInfo.Length) bytes"
    Write-Host "  Modified: $($pubKeyInfo.LastWriteTime)"
    
    # Display fingerprint
    Write-Host "  Fingerprint:"
    ssh-keygen -l -f $PUBLIC_KEY
} else {
    Write-Host "  Exists: NO" -ForegroundColor Red
}

Write-Host "`n2. SSH Config Check" -ForegroundColor Cyan
if (Test-Path $SSH_CONFIG) {
    Write-Host "SSH Config exists. Content:" -ForegroundColor Green
    Get-Content $SSH_CONFIG
} else {
    Write-Host "SSH Config does not exist" -ForegroundColor Red
}

Write-Host "`n3. SSH Agent Status" -ForegroundColor Cyan
try {
    $sshAgentStatus = ssh-add -l 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SSH Agent is running with keys:" -ForegroundColor Green
        Write-Host $sshAgentStatus
    } else {
        Write-Host "SSH Agent status: $sshAgentStatus" -ForegroundColor Yellow
    }
} catch {
    Write-Host "SSH Agent not available or error occurred" -ForegroundColor Red
}

Write-Host "`n4. Network Connectivity Test" -ForegroundColor Cyan
Write-Host "Testing connectivity to VPS..."
$pingResult = Test-NetConnection -ComputerName $VPS_IP -Port 22
if ($pingResult.TcpTestSucceeded) {
    Write-Host "Port 22 is reachable on $VPS_IP" -ForegroundColor Green
} else {
    Write-Host "Port 22 is NOT reachable on $VPS_IP" -ForegroundColor Red
}

Write-Host "`n5. SSH Connection Test with Maximum Verbosity" -ForegroundColor Cyan
Write-Host "Attempting SSH connection with verbose output..."
Write-Host "Command: ssh -vvv -i `"$PRIVATE_KEY`" $VPS_USER@$VPS_IP 'echo Connection successful'" -ForegroundColor Gray

# Run SSH with maximum verbosity
$sshCmd = "ssh -vvv -i `"$PRIVATE_KEY`" $VPS_USER@$VPS_IP 'echo Connection successful'"
Write-Host "`nExecuting SSH command..." -ForegroundColor Yellow
Invoke-Expression $sshCmd

Write-Host "`n6. Public Key Content Analysis" -ForegroundColor Cyan
if (Test-Path $PUBLIC_KEY) {
    $pubKeyContent = Get-Content $PUBLIC_KEY -Raw
    Write-Host "Public key length: $($pubKeyContent.Length) characters"
    Write-Host "First 50 characters: $($pubKeyContent.Substring(0, [Math]::Min(50, $pubKeyContent.Length)))"
    Write-Host "Last 50 characters: $($pubKeyContent.Substring([Math]::Max(0, $pubKeyContent.Length - 50)))"
    
    # Check for line endings
    if ($pubKeyContent.Contains("`r`n")) {
        Write-Host "Line ending type: CRLF (Windows)" -ForegroundColor Yellow
    } elseif ($pubKeyContent.Contains("`n")) {
        Write-Host "Line ending type: LF (Unix)" -ForegroundColor Yellow
    } else {
        Write-Host "Line ending type: None (single line)" -ForegroundColor Green
    }
    
    # Check for trailing whitespace
    if ($pubKeyContent.EndsWith(" ") -or $pubKeyContent.EndsWith("`t")) {
        Write-Host "WARNING: Public key has trailing whitespace" -ForegroundColor Red
    } else {
        Write-Host "No trailing whitespace detected" -ForegroundColor Green
    }
}

Write-Host "`n7. Environment Variables Check" -ForegroundColor Cyan
Write-Host "SSH_AUTH_SOCK: $env:SSH_AUTH_SOCK"
Write-Host "SSH_AGENT_PID: $env:SSH_AGENT_PID"
Write-Host "HOME: $env:HOME"
Write-Host "USERPROFILE: $env:USERPROFILE"

Write-Host "`n8. OpenSSH Version" -ForegroundColor Cyan
ssh -V

Write-Host "`n=== Troubleshooting Complete ===" -ForegroundColor Green
Write-Host "診断完了: $(Get-Date)" -ForegroundColor Yellow

Write-Host "`n=== Recommendations ===" -ForegroundColor Magenta
Write-Host "1. SSHエージェントが動作している場合は、一度クリアしてから再試行してください:"
Write-Host "   ssh-add -D"
Write-Host "   ssh-add `"$PRIVATE_KEY`""
Write-Host ""
Write-Host "2. SSH接続を試す前に、明示的に鍵を指定してください:"
Write-Host "   ssh -o IdentitiesOnly=yes -i `"$PRIVATE_KEY`" $VPS_USER@$VPS_IP"
Write-Host ""
Write-Host "3. 上記のverbose出力を確認し、どの段階で失敗しているかを特定してください"
