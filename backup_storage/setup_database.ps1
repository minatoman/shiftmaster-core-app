# setup_database.ps1
$ErrorActionPreference = "Stop"

# PostgreSQL設定
$pgDbName = "shiftmaster_db"
$pgUser = "postgres"
$pgPassword = "yourpassword"

# データベースの削除と再作成
psql -U $pgUser -d postgres -c "DROP DATABASE IF EXISTS $pgDbName;"
psql -U $pgUser -d postgres -c "CREATE DATABASE $pgDbName;"

# マイグレーションの実行
python manage.py makemigrations
python manage.py migrate
