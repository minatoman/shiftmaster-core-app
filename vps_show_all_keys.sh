#!/bin/bash
# VPS上のauthorized_keysファイル内の全ての鍵を表示・分析するスクリプト
# VPSのコンソールで実行してください

echo "🔍 VPS上のSSH公開鍵一覧表示・分析"
echo "=================================="
echo "実行日時: $(date)"
echo "ホスト名: $(hostname)"
echo "ユーザー: $(whoami)"
echo ""

# authorized_keysファイルの存在確認
AUTHORIZED_KEYS_FILE="$HOME/.ssh/authorized_keys"

if [ ! -f "$AUTHORIZED_KEYS_FILE" ]; then
    echo "❌ authorized_keysファイルが見つかりません: $AUTHORIZED_KEYS_FILE"
    exit 1
fi

echo "📁 authorized_keysファイルパス: $AUTHORIZED_KEYS_FILE"
echo "📊 ファイル情報:"
ls -la "$AUTHORIZED_KEYS_FILE"
echo ""

# ファイルの権限確認
echo "🔒 ファイル権限確認:"
echo "authorized_keys: $(stat -c '%a' "$AUTHORIZED_KEYS_FILE")"
echo ".ssh ディレクトリ: $(stat -c '%a' "$HOME/.ssh")"
echo ""

# 登録されている鍵の数をカウント
KEY_COUNT=$(grep -c "^ssh-" "$AUTHORIZED_KEYS_FILE" 2>/dev/null || echo "0")
echo "🔑 登録されている鍵の数: $KEY_COUNT"
echo ""

if [ "$KEY_COUNT" -eq 0 ]; then
    echo "⚠️ SSH鍵が登録されていません"
    echo "📋 ファイル内容:"
    cat "$AUTHORIZED_KEYS_FILE"
    exit 0
fi

# 各鍵を分析
echo "🔍 登録済みSSH鍵の詳細分析:"
echo "================================"

line_num=1
while IFS= read -r line; do
    if [[ $line =~ ^ssh- ]]; then
        echo ""
        echo "🔑 鍵 #$line_num"
        echo "--------------------"
        
        # 鍵の種類を取得
        key_type=$(echo "$line" | awk '{print $1}')
        echo "種類: $key_type"
        
        # 鍵のコメント部分を取得（通常は3番目のフィールド）
        key_comment=$(echo "$line" | awk '{print $3}')
        if [ -n "$key_comment" ]; then
            echo "コメント: $key_comment"
        else
            echo "コメント: (なし)"
        fi
        
        # フィンガープリントを生成（MD5とSHA256）
        echo "$line" > /tmp/temp_key_$line_num.pub
        
        # MD5フィンガープリント
        md5_fingerprint=$(ssh-keygen -l -E md5 -f /tmp/temp_key_$line_num.pub 2>/dev/null | awk '{print $2}')
        if [ -n "$md5_fingerprint" ]; then
            echo "MD5フィンガープリント: $md5_fingerprint"
        fi
        
        # SHA256フィンガープリント
        sha256_fingerprint=$(ssh-keygen -l -E sha256 -f /tmp/temp_key_$line_num.pub 2>/dev/null | awk '{print $2}')
        if [ -n "$sha256_fingerprint" ]; then
            echo "SHA256フィンガープリント: $sha256_fingerprint"
        fi
        
        # 鍵の長さ
        key_length=$(echo "$line" | awk '{print $2}' | wc -c)
        echo "鍵データ長: $key_length 文字"
        
        # 鍵の最初と最後の文字を表示
        key_data=$(echo "$line" | awk '{print $2}')
        echo "鍵データ開始: ${key_data:0:20}..."
        echo "鍵データ終了: ...${key_data: -20}"
        
        # 完全な鍵の内容を表示
        echo ""
        echo "📋 完全な鍵の内容:"
        echo "$line"
        
        # 一時ファイルを削除
        rm -f /tmp/temp_key_$line_num.pub
        
        ((line_num++))
    fi
done < "$AUTHORIZED_KEYS_FILE"

echo ""
echo "================================"
echo "🔍 Windows側の鍵と比較してください"
echo ""
echo "Windows側のコマンド（PowerShellで実行）:"
echo "ssh-keygen -l -E md5 -f C:\\Users\\jinna\\.ssh\\mednext_vps_key_new.pub"
echo "ssh-keygen -l -E sha256 -f C:\\Users\\jinna\\.ssh\\mednext_vps_key_new.pub"
echo ""
echo "Get-Content C:\\Users\\jinna\\.ssh\\mednext_vps_key_new.pub"
echo ""
echo "🎯 目標: 正しい鍵（mednext_vps_key_new）のみを残す"
echo "不要な鍵がある場合は、authorized_keysファイルを編集してください"
