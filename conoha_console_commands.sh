#!/bin/bash
# ConoHaコンソールで実行するコマンド
# 新しい公開鍵を登録します

echo "=== ConoHa VPS SSH鍵登録コマンド ==="

# 1. SSHディレクトリの作成と権限設定
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# 2. 既存のauthorized_keysをバックアップ
cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup 2>/dev/null || echo "既存のauthorized_keysファイルがありません"

# 3. 新しい公開鍵を追加（改行なしで1行として）
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCmnfCVyO3aYF8qXaOHoIlH/8DAjsrceTmyaNpxoryeFYgxOXbd1vDyQ9czrQuvK516tsa+Q0y2aAp5/vQfoQqsNSdjrfBNHRyHEHHCBksuB19aBkzEySyHZYFmvcwn8iKN/rvM2G2DrXxXsrAIV5YQou7sxxZpHFjFYbGn3Q2XCKh2Fx7gqKhh/Vr4UdbLQvHCssXMvQuG9gqAgfyhPHOlF4haUPalkAr3zoDqQcKV2dNgpp4SoH0C9WLx/tvXzOAC06z55JUee9uQYc9QUGGZBZLf+Fe1MKbtuaZuPgExJOMR//g+bAx6+eP5zeV3EeIzgQkUOawbykPFcf2vZnMdo34vpEqzUhrLxZSONieVLoCCDC4aIUefl+zRRtLrW1f9O1JRRQunknTMQRQPhPt1Fn1iT4cI5OxB3iKsMWsa0tIWI6tgQDQD3QSmvN0/+TBA24D2/38YteIyNBOv72gcjPVN5yYWx6zJjOdpbWPM1xieR4sDQI3Fk9zQtdM7OOYTk8WWH2b/MSHHKvDLMLHvh6MkehQyQ6kCNBnASsqM2GFLywJmZlAPYKDxkExdqSkqXwHoR6HDSRfAA3527uk26dRqy9eSvKiNdkyfXOzZTRfIZr1Y9KOH93kH0hFiwJkC1fvXRtQ4oDeEBLLVbiZCJCH0q5y8gtwqYN5uYRZE1q6c7Hw== jinna@kikonai" > ~/.ssh/authorized_keys

# 4. 正しい権限を設定
chmod 600 ~/.ssh/authorized_keys
chown root:root ~/.ssh/authorized_keys

# 5. 設定の確認
echo "=== 設定確認 ==="
ls -la ~/.ssh/
echo ""
echo "=== authorized_keys内容確認 ==="
cat ~/.ssh/authorized_keys
echo ""
echo "=== SSH鍵登録完了 ==="
