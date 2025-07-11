# shifts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Committee

# ユーザー作成時または更新時に、ユーザープロフィールを作成または更新する
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # ユーザー新規作成時にプロフィールも作成
        Profile.objects.create(user=instance)
    else:
        # プロフィールが存在しない場合は作成し、存在する場合は保存
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()

# 委員会のスケジュールが更新された時に通知などを行う処理を追加
@receiver(post_save, sender=Committee)
def send_committee_schedule_notification(sender, instance, created, **kwargs):
    if created:
        # 新しい委員会が作成された時に通知
        print(f'新しい委員会「{instance.name}」が作成されました。')
        # 通知処理をここに追加可能
    else:
        # 委員会が更新された時に通知
        print(f'委員会「{instance.name}」のスケジュールが更新されました。')
        # 通知処理をここに追加可能
