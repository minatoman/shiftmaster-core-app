#!/bin/bash
# VPS側でのSSH鍵確認スクリプト
# ConoHaコンソールで実行してください

echo "=== VPS SSH Key Status Check ==="
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "User: $(whoami)"
echo

echo "1. SSH Directory Status:"
echo "------------------------"
ls -la ~/.ssh/
echo

echo "2. Authorized Keys Content:"
echo "---------------------------"
if [ -f ~/.ssh/authorized_keys ]; then
    echo "File exists. Content:"
    cat ~/.ssh/authorized_keys
    echo
    echo "Line count: $(wc -l < ~/.ssh/authorized_keys)"
    echo "Character count: $(wc -c < ~/.ssh/authorized_keys)"
    echo "Permissions: $(ls -la ~/.ssh/authorized_keys)"
else
    echo "authorized_keys file does not exist!"
fi
echo

echo "3. SSH Directory Permissions:"
echo "-----------------------------"
ls -la ~/.ssh/
echo

echo "4. Current SSH Daemon Config (relevant parts):"
echo "-----------------------------------------------"
grep -E "^(PubkeyAuthentication|AuthorizedKeysFile|PasswordAuthentication|PermitRootLogin)" /etc/ssh/sshd_config
echo

echo "5. SSH Auth Log (last 20 lines):"
echo "---------------------------------"
tail -20 /var/log/auth.log | grep sshd
echo

echo "=== Manual Fix Instructions ==="
echo "If the key is incorrect, run these commands:"
echo "1. Backup current keys:"
echo "   cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup"
echo
echo "2. Clear authorized_keys:"
echo "   echo '' > ~/.ssh/authorized_keys"
echo
echo "3. Add the correct key (copy from Windows PC):"
echo "   nano ~/.ssh/authorized_keys"
echo "   # Paste the fixed key from Windows"
echo
echo "4. Set correct permissions:"
echo "   chmod 600 ~/.ssh/authorized_keys"
echo "   chmod 700 ~/.ssh"
echo
echo "5. Test SSH connection from Windows PC"
