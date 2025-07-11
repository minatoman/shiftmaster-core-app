#!/bin/bash
# VPS側でのSSH認証詳細ログ確認スクリプト

echo "🔍 VPS側 SSH認証ログ詳細確認"
echo "=================================="

# 現在の時刻を記録
echo "📅 現在時刻: $(date)"
echo ""

# SSH関連プロセス確認
echo "🔄 SSHサービス状態確認:"
echo "------------------------"
systemctl status ssh --no-pager -l
echo ""

# authorized_keys詳細確認
echo "🔑 authorized_keys詳細確認:"
echo "----------------------------"
echo "📁 /root/.ssh/ ディレクトリ権限:"
ls -la /root/.ssh/
echo ""

echo "📄 authorized_keys ファイル詳細:"
if [ -f /root/.ssh/authorized_keys ]; then
    echo "✅ ファイル存在: /root/.ssh/authorized_keys"
    echo "📊 ファイル統計:"
    stat /root/.ssh/authorized_keys
    echo ""
    echo "📏 行数とサイズ:"
    wc -l /root/.ssh/authorized_keys
    wc -c /root/.ssh/authorized_keys
    echo ""
    echo "🔍 ファイル内容（最初の100文字）:"
    head -c 100 /root/.ssh/authorized_keys
    echo ""
    echo "🔍 ファイル内容（最後の100文字）:"
    tail -c 100 /root/.ssh/authorized_keys
    echo ""
    echo "🔍 ファイル内容（16進数で確認、改行や隠し文字チェック）:"
    hexdump -C /root/.ssh/authorized_keys | head -5
    echo ""
else
    echo "❌ authorized_keys ファイルが存在しません"
fi

# SSH設定ファイル確認
echo "⚙️ SSH設定確認:"
echo "----------------"
echo "📋 sshd_config の重要な設定:"
grep -E "^(PubkeyAuthentication|PermitRootLogin|AuthorizedKeysFile|PasswordAuthentication)" /etc/ssh/sshd_config
echo ""

# 最新のSSH認証ログ
echo "📋 最新のSSH認証ログ（直近20行）:"
echo "----------------------------------"
tail -20 /var/log/auth.log | grep -E "(sshd|SSH)"
echo ""

# リアルタイムログ監視の準備
echo "🔄 リアルタイムSSHログ監視の準備完了"
echo "------------------------------------"
echo "📋 Windows側からSSH接続を試行してください。"
echo "   以下のコマンドでリアルタイムログを監視できます:"
echo ""
echo "   tail -f /var/log/auth.log | grep sshd"
echo ""
echo "🎯 次のステップ:"
echo "1. 別のターミナルで上記のログ監視コマンドを実行"
echo "2. Windows側からSSH接続を試行"
echo "3. ログに表示されるエラーメッセージを確認"
echo ""

# ログ監視コマンドを自動実行するかどうか確認
read -p "🤔 今すぐリアルタイムログ監視を開始しますか？ (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 リアルタイムSSHログ監視開始（Ctrl+Cで停止）:"
    echo "================================================"
    tail -f /var/log/auth.log | grep --line-buffered sshd
fi
