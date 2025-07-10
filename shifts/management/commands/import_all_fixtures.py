# shifts/management/commands/import_all_fixtures.py
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = '全CSV/JSONファイルを一括でインポート'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('--- 一括インポート開始 ---'))
        call_command('import_employees')
        call_command('import_shift_requests')
        call_command('import_holiday_requests')
        self.stdout.write(self.style.SUCCESS('--- 全データのインポートが完了しました ---'))

