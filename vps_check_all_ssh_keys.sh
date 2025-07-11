#!/bin/bash

echo "===== SSH鍵の詳細分析 ====="
echo "実行日時: $(date)"
echo

# authorized_keysファイルの基本情報
echo "=== authorized_keysファイルの基本情報 ==="
AUTH_KEYS_FILE="/root/.ssh/authorized_keys"

if [ -f "$AUTH_KEYS_FILE" ]; then
    echo "ファイルパス: $AUTH_KEYS_FILE"
    echo "ファイルサイズ: $(stat -c%s "$AUTH_KEYS_FILE") bytes"
    echo "権限: $(stat -c%a "$AUTH_KEYS_FILE")"
    echo "所有者: $(stat -c%U:%G "$AUTH_KEYS_FILE")"
    echo "最終更新: $(stat -c%y "$AUTH_KEYS_FILE")"
    echo "行数: $(wc -l < "$AUTH_KEYS_FILE")"
    echo
else
    echo "エラー: authorized_keysファイルが見つかりません"
    exit 1
fi

# 鍵の一覧表示
echo "=== 登録されている全ての鍵 ==="
echo "注: 各鍵のフィンガープリント、タイプ、コメントを表示します"
echo

# 一時ファイルを作成
TEMP_DIR="/tmp/ssh_key_analysis_$(date +%s)"
mkdir -p "$TEMP_DIR"

# 行番号付きで鍵を確認
line_num=1
while IFS= read -r line; do
    if [ -n "$line" ] && [ "${line:0:1}" != "#" ]; then
        echo "--- 鍵 #$line_num ---"
        
        # 一時ファイルに鍵を保存
        temp_key="$TEMP_DIR/key_$line_num.pub"
        echo "$line" > "$temp_key"
        
        # フィンガープリントを取得
        echo "フィンガープリント:"
        ssh-keygen -l -f "$temp_key" 2>/dev/null || echo "  エラー: フィンガープリントを取得できませんでした"
        
        # 鍵の種類とコメントを抽出
        key_type=$(echo "$line" | awk '{print $1}')
        key_data=$(echo "$line" | awk '{print $2}')
        key_comment=$(echo "$line" | awk '{for(i=3;i<=NF;i++) printf "%s ", $i; print ""}' | sed 's/ *$//')
        
        echo "タイプ: $key_type"
        echo "コメント: ${key_comment:-"(コメントなし)"}"
        
        # 鍵データの最初と最後の文字を表示（識別用）
        if [ ${#key_data} -gt 20 ]; then
            echo "鍵データ(先頭): ${key_data:0:20}..."
            echo "鍵データ(末尾): ...${key_data: -20}"
        else
            echo "鍵データ: $key_data"
        fi
        
        # 鍵の長さを推定
        key_length=$(echo "$key_data" | base64 -d 2>/dev/null | wc -c 2>/dev/null || echo "不明")
        echo "推定鍵長: $key_length bytes"
        
        echo
    elif [ -n "$line" ] && [ "${line:0:1}" == "#" ]; then
        echo "--- コメント行 #$line_num ---"
        echo "内容: $line"
        echo
    fi
    ((line_num++))
done < "$AUTH_KEYS_FILE"

# 特定の鍵パターンを検索
echo "=== 特定パターンの検索 ==="
echo "Windows (jinna@kikonai) の鍵を検索:"
grep -n "jinna@kikonai" "$AUTH_KEYS_FILE" || echo "  見つかりませんでした"
echo

echo "自宅 (home) 関連の鍵を検索:"
grep -n -i "home" "$AUTH_KEYS_FILE" || echo "  見つかりませんでした"
echo

echo "ConoHa 関連の鍵を検索:"
grep -n -i "conoha\|vps" "$AUTH_KEYS_FILE" || echo "  見つかりませんでした"
echo

# 重複チェック
echo "=== 重複鍵のチェック ==="
echo "同一の鍵データが複数回登録されているかチェック:"
awk '{print $2}' "$AUTH_KEYS_FILE" | sort | uniq -d | while read -r dup_key; do
    if [ -n "$dup_key" ]; then
        echo "重複している鍵データ: ${dup_key:0:30}..."
        grep -n "$dup_key" "$AUTH_KEYS_FILE"
    fi
done
echo "重複チェック完了"
echo

# 正しい鍵の確認
echo "=== 期待される鍵との比較 ==="
echo "Windows側で生成された正しい鍵のフィンガープリント:"
echo "SHA256:q69uyJ+r62+A+7JNRmCUtqPoED2Tlz4OFm2cJEO32a8"
echo
echo "このフィンガープリントと一致する鍵:"
ssh-keygen -l -f "$AUTH_KEYS_FILE" 2>/dev/null | grep "q69uyJ+r62+A+7JNRmCUtqPoED2Tlz4OFm2cJEO32a8" || echo "  見つかりませんでした"
echo

# ファイルの生の内容も表示
echo "=== authorized_keysの生の内容 ==="
echo "デバッグ用に改行コードも表示:"
cat -A "$AUTH_KEYS_FILE"
echo
echo

# クリーンアップ
rm -rf "$TEMP_DIR"

echo "=== 推奨されるアクション ==="
echo "1. 正しい鍵 (SHA256:q69uyJ+r62+A+7JNRmCUtqPoED2Tlz4OFm2cJEO32a8) が見つからない場合："
echo "   -> ConoHaコンソールから再度鍵を追加してください"
echo
echo "2. 複数の鍵がある場合："
echo "   -> 以下のコマンドで正しい鍵のみを残してください："
echo "   # 現在のファイルをバックアップ"
echo "   cp /root/.ssh/authorized_keys /root/.ssh/authorized_keys.backup.$(date +%s)"
echo "   # 正しい鍵のみを設定"
echo "   echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCr6... jinna@kikonai' > /root/.ssh/authorized_keys"
echo "   chmod 600 /root/.ssh/authorized_keys"
echo
echo "3. 権限の確認："
echo "   chmod 700 /root/.ssh"
echo "   chmod 600 /root/.ssh/authorized_keys"
echo
echo "===== 分析完了 ====="
