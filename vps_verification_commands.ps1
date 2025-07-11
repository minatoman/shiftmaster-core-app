# VPS側での検証コマンド集
# ConoHaコンソールでVPSにログインして実行してください

Write-Host "=== VPS側での検証コマンド ===" -ForegroundColor Green
Write-Host "以下のコマンドをConoHaコンソールで実行して結果を確認してください" -ForegroundColor Yellow

Write-Host "`n1. 現在のauthorized_keysの状態確認:" -ForegroundColor Cyan
Write-Host "ls -la ~/.ssh/"
Write-Host "cat ~/.ssh/authorized_keys"

Write-Host "`n2. 行数確認（1行であることを確認）:" -ForegroundColor Cyan
Write-Host "wc -l ~/.ssh/authorized_keys"

Write-Host "`n3. 文字数確認:" -ForegroundColor Cyan
Write-Host "wc -c ~/.ssh/authorized_keys"

Write-Host "`n4. ファイルの16進ダンプ確認（改行文字チェック）:" -ForegroundColor Cyan
Write-Host "hexdump -C ~/.ssh/authorized_keys | tail -3"

Write-Host "`n5. 権限確認:" -ForegroundColor Cyan
Write-Host "ls -la ~/.ssh/authorized_keys"
Write-Host "ls -la ~/.ssh/"

Write-Host "`n6. SSHDの設定確認:" -ForegroundColor Cyan
Write-Host "grep -E '^(PubkeyAuthentication|AuthorizedKeysFile|PermitRootLogin)' /etc/ssh/sshd_config"

Write-Host "`n7. SSH認証ログをリアルタイムで確認:" -ForegroundColor Cyan
Write-Host "# 別のターミナルでこのコマンドを実行しながら、Windows側から接続を試行してください"
Write-Host "tail -f /var/log/auth.log | grep ssh"

Write-Host "`n8. もし上記で問題が見つからない場合、authorized_keysを再作成:" -ForegroundColor Yellow
Write-Host "# バックアップを作成"
Write-Host "cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup"
Write-Host ""
Write-Host "# 新しい公開鍵を直接echoで追加（改行問題を回避）"
Write-Host 'echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCmnfCVyO3aYF8qXaOHoIlH/8DAjsrceTmyaNpxoryeFYgxOXbd1vDyQ9czrQuvK516tsa+Q0y2aAp5/vQfoQqsNSdjrfBNHRyHEHHCBksuB19aBkzEySyHZYFmvcwn8iKN/rvM2G2DrXxXsrAIV5YQou7sxxZpHFjFYbGn3Q2XCKh2Fx7gqKhh/Vr4UdbLQvHCssXMvQuG9gqAgfyhPHOlF4haUPalkAr3zoDqQcKV2dNgpp4SoH0C9WLx/tvXzOAC06z55JUee9uQYc9QUGGZBZLf+Fe1MKbtuaZuPgExJOMR//g+bAx6+eP5zeV3EeIzgQkUOawbykPFcf2vZnMdo34vpEqzUhrLxZSONieVLoCCDC4aIUefl+zRRtLrW1f9O1JRRQunknTMQRQPhPt1Fn1iT4cI5OxB3iKsMWsa0tIWI6tgQDQD3QSmvN0/+TBA24D2/38YteIyNBOv72gcjPVN5yYWx6zJjOdpbWPM1xieR4sDQI3Fk9zQtdM7OOYTk8WWH2b/MSHHKvDLMLHvh6MkehQyQ6kCNBnASsqM2GFLywJmZlAPYKDxkExdqSkqXwHoR6HDSRfAA3527uk26dRqy9eSvKiNdkyfXOzZTRfIZr1Y9KOH93kH0hFiwJkC1fvXRtQ4oDeEBLLVbiZCJCH0q5y8gtwqYN5uYRZE1q6c7Hw== jinna@kikonai" > ~/.ssh/authorized_keys'
Write-Host ""
Write-Host "# 権限を再設定"
Write-Host "chmod 600 ~/.ssh/authorized_keys"
Write-Host "chmod 700 ~/.ssh"

Write-Host "`n=== 期待される結果 ===" -ForegroundColor Magenta
Write-Host "1. wc -l の結果: 1 行"
Write-Host "2. 権限: authorized_keys は 600, .ssh ディレクトリは 700"
Write-Host "3. PubkeyAuthentication yes がsshd_configに設定されている"
Write-Host "4. AuthorizedKeysFile .ssh/authorized_keys がデフォルト設定"
