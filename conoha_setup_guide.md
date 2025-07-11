# ConoHa VPS SSH公開鍵登録 作業指示書

## 📋 作業前の確認事項
- ConoHaコントロールパネルのログイン情報を準備
- VPSが起動していることを確認
- ブラウザでConoHaコントロールパネルにアクセス可能

## 🛠️ 手順1: ConoHaコンソールへのアクセス

1. **ConoHaコントロールパネル**にログインしてください
   - URL: https://manage.conoha.jp/
   
2. **VPS**メニューをクリック

3. **サーバー一覧**から対象のVPS (160.251.181.238) を選択

4. **コンソール**タブをクリック

5. コンソール画面が表示されるまで待機

## 🔑 手順2: SSH公開鍵の登録

コンソール画面で以下のコマンドを**順番に**実行してください：

### A. SSHディレクトリの作成と権限設定
```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

### B. 既存ファイルのバックアップ（エラーが出ても問題ありません）
```bash
cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup 2>/dev/null || echo "No existing authorized_keys file"
```

### C. 新しい公開鍵の登録（⚠️重要：以下の長い行を改行なしで全てコピー&ペースト）
```bash
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCmnfCVyO3aYF8qXaOHoIlH/8DAjsrceTmyaNpxoryeFYgxOXbd1vDyQ9czrQuvK516tsa+Q0y2aAp5/vQfoQqsNSdjrfBNHRyHEHHCBksuB19aBkzEySyHZYFmvcwn8iKN/rvM2G2DrXxXsrAIV5YQou7sxxZpHFjFYbGn3Q2XCKh2Fx7gqKhh/Vr4UdbLQvHCssXMvQuG9gqAgfyhPHOlF4haUPalkAr3zoDqQcKV2dNgpp4SoH0C9WLx/tvXzOAC06z55JUee9uQYc9QUGGZBZLf+Fe1MKbtuaZuPgExJOMR//g+bAx6+eP5zeV3EeIzgQkUOawbykPFcf2vZnMdo34vpEqzUhrLxZSONieVLoCCDC4aIUefl+zRRtLrW1f9O1JRRQunknTMQRQPhPt1Fn1iT4cI5OxB3iKsMWsa0tIWI6tgQDQD3QSmvN0/+TBA24D2/38YteIyNBOv72gcjPVN5yYWx6zJjOdpbWPM1xieR4sDQI3Fk9zQtdM7OOYTk8WWH2b/MSHHKvDLMLHvh6MkehQyQ6kCNBnASsqM2GFLywJmZlAPYKDxkExdqSkqXwHoR6HDSRfAA3527uk26dRqy9eSvKiNdkyfXOzZTRfIZr1Y9KOH93kH0hFiwJkC1fvXRtQ4oDeEBLLVbiZCJCH0q5y8gtwqYN5uYRZE1q6c7Hw== jinna@kikonai" > ~/.ssh/authorized_keys
```

### D. 権限の設定
```bash
chmod 600 ~/.ssh/authorized_keys
chown root:root ~/.ssh/authorized_keys
```

### E. 設定の確認
```bash
ls -la ~/.ssh/
cat ~/.ssh/authorized_keys
```

## ✅ 手順3: 登録確認

最後のコマンド実行後、以下が表示されることを確認してください：

1. **ディレクトリ一覧**に`authorized_keys`ファイルが表示される
2. **ファイル権限**が`-rw-------`（600）になっている
3. **公開鍵の内容**が正しく表示される（ssh-rsaで始まる長い文字列）

## 🔄 手順4: 接続テスト

VPSコンソールでの作業完了後、Windows側で以下のコマンドを実行してください：

```powershell
PowerShell -ExecutionPolicy Bypass -File h:\Projects\ShiftMaster\vscode_remote_connect.ps1
```

## 🚀 手順5: VSCode Remote-SSH接続

接続テストが成功したら：

1. **VSCode**を起動
2. **Ctrl+Shift+P**でコマンドパレットを開く
3. **「Remote-SSH: Connect to Host」**と入力
4. **「mednext-vps」**を選択
5. 新しいVSCodeウィンドウが開くまで待機
6. **ターミナル**を開いて`pwd`コマンドで接続確認

## ❌ トラブルシューティング

### 公開鍵登録でエラーが発生した場合：
```bash
# 手動で1行ずつ入力
cd ~/.ssh
nano authorized_keys
# 公開鍵をコピー&ペーストして保存 (Ctrl+X, Y, Enter)
chmod 600 authorized_keys
```

### SSH接続テストが失敗する場合：
1. VPSの再起動を試行
2. ファイアウォール設定の確認
3. SSH設定ファイルの再確認

## 📞 サポート

問題が解決しない場合は、エラーメッセージを含めてお知らせください。
