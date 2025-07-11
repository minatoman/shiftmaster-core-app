#!/bin/bash

# SSH鍵のクリーンアップと修復スクリプト
echo "===== SSH鍵のクリーンアップと修復 ====="
echo "実行日時: $(date)"
echo

# 正しい公開鍵の内容（Windows側で生成されたもの）
CORRECT_PUBLIC_KEY="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCmnfCVyO3aYF8qXaOHoIlH/8DAjsrceTmyaNpxoryeFYgxOXbd1vDyQ9czrQuvK516tsa+Q0y2aAp5/vQfoQqsNSdjrfBNHRyHEHCBksuB19aBkzEySyHZYFmvcwn8iKN/rvM2G2DrXxXsrAIV5YQou7sxxZpHFjFYbGn3Q2XCKh2Fx7gqKhh/Vr4UdbLQvHCssXMvQuG9gqAgfyhPHOlF4haUPalkAr3zoDqQcKV2dNgpp4SoH0C9WLx/tvXzOAC06z55JUee9uQYc9QUGGZBZLf+Fe1MKbtuaZuPgExJOMR//g+bAx6+eP5zeV3EeIzgQkUOawbykPFcf2vZnMdo34vpEqzUhrLxZSONieVLoCCDC4aIUefl+zRRtLrW1f9O1JRRQunknTMQRQPhPt1Fn1iT4cI5OxB3iKsMWsa0tIWI6tgQDQD3QSmvN0/+TBA24D2/38YteIyNBOv72gcjPVN5yYWx6zJjOdpbWPM1xieR4sDQI3Fk9zQtdM7OOYTk8WWH2b/MSHHKvDLMLHvh6MkehQyQ6kCNBnASsqM2GFLywJmZlAPYKDxkExdqSkqXwHoR6HDSRfAA3527uk26dRqy9eSvKiNdkyfXOzZTRfIZr1Y9KOH93kH0hFiwJkC1fvXRtQ4oDeEBLLVbiZCJCH0q5y8gtwqYN5uYRZE1q6c7Hw== jinna@kikonai"

AUTH_KEYS_FILE="/root/.ssh/authorized_keys"
BACKUP_DIR="/root/.ssh/backups"

# バックアップディレクトリを作成
mkdir -p "$BACKUP_DIR"

echo "=== 現在の状態を確認 ==="
if [ -f "$AUTH_KEYS_FILE" ]; then
    echo "現在の authorized_keys の行数: $(wc -l < "$AUTH_KEYS_FILE")"
    echo "ファイルサイズ: $(stat -c%s "$AUTH_KEYS_FILE") bytes"
    echo
else
    echo "authorized_keys ファイルが存在しません"
    exit 1
fi

# バックアップを作成
echo "=== バックアップの作成 ==="
backup_file="$BACKUP_DIR/authorized_keys.backup.$(date +%Y%m%d_%H%M%S)"
cp "$AUTH_KEYS_FILE" "$backup_file"
echo "バックアップを作成しました: $backup_file"
echo

# 正しい鍵が存在するかチェック
echo "=== 正しい鍵の存在確認 ==="
expected_fingerprint="SHA256:q69uyJ+r62+A+7JNRmCUtqPoED2Tlz4OFm2cJEO32a8"
current_fingerprint=$(ssh-keygen -l -f "$AUTH_KEYS_FILE" 2>/dev/null | grep "$expected_fingerprint")

if [ -n "$current_fingerprint" ]; then
    echo "✓ 正しい鍵が見つかりました:"
    echo "  $current_fingerprint"
    echo
else
    echo "✗ 正しい鍵が見つかりませんでした"
    echo "現在登録されている鍵:"
    ssh-keygen -l -f "$AUTH_KEYS_FILE" 2>/dev/null || echo "  鍵を読み取れませんでした"
    echo
fi

# クリーンアップの実行確認
echo "=== クリーンアップの実行 ==="
echo "authorized_keys を正しい鍵のみで上書きしますか？"
echo "現在のファイルはバックアップされています: $backup_file"
echo
echo "実行する場合は 'yes' と入力してください:"
read -r response

if [ "$response" = "yes" ]; then
    echo "クリーンアップを実行中..."
    
    # 正しい鍵のみを設定
    echo "$CORRECT_PUBLIC_KEY" > "$AUTH_KEYS_FILE"
    
    # 権限を設定
    chmod 600 "$AUTH_KEYS_FILE"
    chmod 700 /root/.ssh
    
    # 結果を確認
    echo
    echo "=== クリーンアップ完了 ==="
    echo "新しい authorized_keys の内容:"
    echo "行数: $(wc -l < "$AUTH_KEYS_FILE")"
    echo "フィンガープリント:"
    ssh-keygen -l -f "$AUTH_KEYS_FILE" 2>/dev/null
    echo
    echo "権限:"
    ls -la /root/.ssh/authorized_keys
    echo
    
    # 接続テスト用の情報を表示
    echo "=== 接続テストの実行 ==="
    echo "Windows側から以下のコマンドで接続をテストしてください："
    echo "ssh -i C:\\Users\\jinna\\.ssh\\mednext_vps_key_new -v root@180.147.38.203"
    echo
    echo "VSCode Remote-SSH での接続もテストしてください。"
    
else
    echo "クリーンアップをキャンセルしました"
    echo "手動で確認する場合は以下を実行してください："
    echo "1. バックアップの確認: cat $backup_file"
    echo "2. 現在の鍵の確認: cat $AUTH_KEYS_FILE"
    echo "3. フィンガープリントの確認: ssh-keygen -l -f $AUTH_KEYS_FILE"
fi

echo
echo "=== SSH設定の最終確認 ==="
echo "SSHサービス状態:"
systemctl status ssh --no-pager -l
echo
echo "sshd_config の重要な設定:"
grep -E "^(PubkeyAuthentication|AuthorizedKeysFile|PermitRootLogin|PasswordAuthentication)" /etc/ssh/sshd_config | grep -v "^#"
echo
echo "===== 完了 ====="
