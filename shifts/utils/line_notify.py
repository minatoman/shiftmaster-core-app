import requests
import json

def send_line_notify(message: str, token: str, user_id: str) -> bool:
    """
    LINE Messaging APIを使って、指定されたユーザーにメッセージを送信する。

    :param message: 送信するメッセージ
    :param token: LINE Messaging APIのアクセストークン
    :param user_id: 受信者のLINEユーザーID
    :return: メッセージ送信が成功したかどうか
    """
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {
        "to": user_id,  # 受信者のLINEユーザーID
        "messages": [{"type": "text", "text": message}]
    }

    try:
        # POSTリクエストをLINE Messaging APIに送信
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            print("LINE通知送信成功")
            return True
        else:
            print(f"LINE通知エラー: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"LINE通知エラー: {e}")
        return False

