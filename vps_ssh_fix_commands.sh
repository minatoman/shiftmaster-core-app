#!/bin/bash
# ConoHaコンソールで実行：authorized_keys確認・修正コマンド

echo "=== SSH設定診断・修正コマンド ==="

echo "1. 現在のauthorized_keysファイルの確認"
ls -la ~/.ssh/authorized_keys
echo ""

echo "2. authorized_keysファイルの内容確認"
cat ~/.ssh/authorized_keys
echo ""

echo "3. 鍵の行数確認"
wc -l ~/.ssh/authorized_keys
echo ""

echo "4. 権限の再設定"
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chown -R root:root ~/.ssh
echo "権限設定完了"

echo "5. 再度権限確認"
ls -la ~/.ssh/
echo ""

echo "6. SSH設定ファイルの確認"
grep -E "^(PubkeyAuthentication|PasswordAuthentication|PermitRootLogin)" /etc/ssh/sshd_config
echo ""

echo "7. SSHサービスの再起動"
systemctl restart ssh
echo "SSH再起動完了"

echo "8. 新しいauthorized_keysファイルを作成（必要に応じて）"
echo "# 以下のコマンドで正しい公開鍵のみを設定"
echo "# バックアップを作成してから実行してください"
echo ""
echo "cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup.$(date +%Y%m%d_%H%M%S)"
echo ""
echo "# 新しい公開鍵のみを設定（以下の長い行を全てコピー）"
echo 'echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCmnfCVyO3aYF8qXaOHoIlH/8DAjsrceTmyaNpxoryeFYgxOXbd1vDyQ9czrQuvK516tsa+Q0y2aAp5/vQfoQqsNSdjrfBNHRyHEHHCBksuB19aBkzEySyHZYFmvcwn8iKN/rvM2G2DrXxXsrAIV5YQou7sxxZpHFjFYbGn3Q2XCKh2Fx7gqKhh/Vr4UdbLQvHCssXMvQuG9gqAgfyhPHOlF4haUPalkAr3zoDqQcKV2dNgpp4SoH0C9WLx/tvXzOAC06z55JUee9uQYc9QUGGZBZLf+Fe1MKbtuaZuPgExJOMR//g+bAx6+eP5zeV3EeIzgQkUOawbykPFcf2vZnMdo34vpEqzUhrLxZSONieVLoCCDC4aIUefl+zRRtLrW1f9O1JRRQunknTMQRQPhPt1Fn1iT4cI5OxB3iKsMWsa0tIWI6tgQDQD3QSmvN0/+TBA24D2/38YteIyNBOv72gcjPVN5yYWx6zJjOdpbWPM1xieR4sDQI3Fk9zQtdM7OOYTk8WWH2b/MSHHKvDLMLHvh6MkehQyQ6kCNBnASsqM2GFLywJmZlAPYKDxkExdqSkqXwHoR6HDSRfAA3527uk26dRqy9eSvKiNdkyfXOzZTRfIZr1Y9KOH93kH0hFiwJkC1fvXRtQ4oDeEBLLVbiZCJCH0q5y8gtwqYN5uYRZE1q6c7Hw== jinna@kikonai" > ~/.ssh/authorized_keys'
echo ""
echo "chmod 600 ~/.ssh/authorized_keys"
echo "chown root:root ~/.ssh/authorized_keys"
