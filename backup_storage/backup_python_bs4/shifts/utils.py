import re
import requests
from django.core.mail import send_mail
from django.conf import settings

def normalize_name(name):
    """
    氏名の正規化処理：
    - 全角スペース（\u3000）を半角に変換
    - 複数スペースを1つに統一
    - 前後の不要な空白を除去

    Args:
        name (str): 元の名前（氏名）

    Returns:
        str: 正規化された名前
    """
    if not name:
        return ''
    
    # 全角スペースを半角に変換
    name = name.replace('\u3000', ' ')
    # 複数スペースを1つに統一
    name = re.sub(r'\s+', ' ', name)
    # 前後のスペースを削除
    return name.strip()

def send_notification_email(subject, message, recipient_email):
    """
    管理者への通知メール送信処理。
    設定されている送信元から受信先へメールを送信します。

    Args:
        subject (str): メールの件名
        message (str): 本文
        recipient_email (str): 宛先メールアドレス

    Returns:
        bool: メール送信の成否
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email]
        )
        return True
    except Exception as e:
        print(f"メール送信失敗: {e}")
        return False

def send_line_notification(message, token):
    """
    LINE通知を送信する関数。

    Args:
        message (str): 通知メッセージ
        token (str): LINE Notifyのアクセストークン

    Returns:
        bool: 通知成功でTrue、失敗でFalse
    """
    try:
        url = "https://notify-api.line.me/api/notify"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        data = {"message": message}
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return True
        else:
            print(f"LINE通知失敗: {response.text}")
            return False
    except Exception as e:
        print(f"LINE通知送信エラー: {e}")
        return False
