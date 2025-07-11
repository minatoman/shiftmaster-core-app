# SSH接続確認スクリプト（最終版）
Write-Host "=== SSH Final Connection Test ===" -ForegroundColor Green

# SSH接続テスト
Write-Host "`nTesting SSH connection..." -ForegroundColor Yellow
$sshTest = 'ssh -i "C:\Users\jinna\.ssh\mednext_vps_key_new" -o ConnectTimeout=10 root@160.251.181.238 "echo CONNECTION_SUCCESS"'

try {
    $result = Invoke-Expression $sshTest 2>&1
    if ($LASTEXITCODE -eq 0 -and $result -match "CONNECTION_SUCCESS") {
        Write-Host "🎉 SSH CONNECTION SUCCESS!" -ForegroundColor Green
        Write-Host "Result: $result" -ForegroundColor Gray
        
        # VSCode起動確認
        Write-Host "`n💡 Launch VSCode for Remote-SSH? (y/N): " -NoNewline -ForegroundColor Yellow
        $launch = Read-Host
        if ($launch -eq "y" -or $launch -eq "Y") {
            Start-Process "code" -ArgumentList "."
            Write-Host "VSCode launched. Connect via Remote-SSH!" -ForegroundColor Green
        }
        
        Write-Host "`n🚀 Next Steps:" -ForegroundColor Cyan
        Write-Host "1. VSCode → Ctrl+Shift+P" -ForegroundColor White
        Write-Host "2. Remote-SSH: Connect to Host" -ForegroundColor White
        Write-Host "3. Select 'mednext-vps'" -ForegroundColor White
        Write-Host "4. Start Django deployment!" -ForegroundColor White
        
    } else {
        Write-Host "❌ SSH connection still failed" -ForegroundColor Red
        Write-Host "Error: $result" -ForegroundColor Red
        
        Write-Host "`n🔧 Alternative solutions:" -ForegroundColor Yellow
        Write-Host "1. Try password authentication temporarily" -ForegroundColor White
        Write-Host "2. Check VPS firewall settings" -ForegroundColor White
        Write-Host "3. Verify VPS SSH configuration" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Connection test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Green
