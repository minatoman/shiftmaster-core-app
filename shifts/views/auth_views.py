# shifts/views/auth_views.py

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import Employee
from ..utils import send_notification_email  # ← 🔄 ここを修正

def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        messages.success(request, 'ユーザー登録完了。ログインしてください。')

        # 管理者全員に通知メールを送信
        admin_emails = [emp.email for emp in Employee.objects.filter(position="管理者")]
        for email in admin_emails:
            send_notification_email(
                subject="【新規ユーザー登録】",
                message=f"新しいユーザー {user.username} さんが登録されました。",
                recipient_email=email
            )

        return redirect('login')
    elif request.method == 'POST':
        messages.error(request, '登録に失敗しました。入力内容をご確認ください。')

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'shifts/profile.html', {'user': request.user})


@login_required
def homepage(request):
    return render(request, 'shifts/homepage.html')

