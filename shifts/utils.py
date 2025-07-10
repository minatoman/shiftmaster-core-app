import os
import re
import requests
import csv
from io import StringIO
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

def process_uploaded_files(files):
    """
    アップロードされたファイルを処理する関数。
    ここではファイルのバリデーションやパース処理を行うことができます。

    Args:
        files (list): アップロードされたファイルのリスト

    Returns:
        list: 処理されたデータ
    """
    processed_data = []
    
    for file in files:
        # ここでファイルを処理します。例えばCSVの読み込みや検証など。
        if file.name.endswith('.csv'):
            try:
                file_data = StringIO(file.read().decode('utf-8'))
                csv_reader = csv.DictReader(file_data)
                for row in csv_reader:
                    # 行データを処理してリストに追加
                    processed_data.append(row)
            except Exception as e:
                print(f"ファイル {file.name} の処理中にエラーが発生しました: {e}")
        else:
            print(f"ファイル {file.name} はCSVファイルではありません。")
    
    return processed_data

def save_file(file, save_dir):
    """
    アップロードされたファイルを指定したディレクトリに保存する関数。
    
    Args:
        file (UploadedFile): アップロードされたファイルオブジェクト
        save_dir (str): 保存先ディレクトリ
    
    Returns:
        str: 保存されたファイルのパス
    """
    try:
        # ディレクトリが存在しない場合は作成
        os.makedirs(save_dir, exist_ok=True)

        # 保存するファイルのパス
        file_path = os.path.join(save_dir, file.name)
        
        # ファイルを保存
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        
        return file_path
    except Exception as e:
        print(f"ファイル {file.name} の保存中にエラーが発生しました: {e}")
        raise ValueError("ファイル保存に失敗しました")
