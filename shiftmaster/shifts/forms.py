from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Employee, Shift, ShiftRequest, ShiftType
from datetime import date, timedelta


class CustomUserCreationForm(UserCreationForm):
    """カスタムユーザー作成フォーム"""
    email = forms.EmailField(required=True, label='メールアドレス')
    first_name = forms.CharField(max_length=30, required=True, label='名')
    last_name = forms.CharField(max_length=30, required=True, label='姓')

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # スマホ対応のCSSクラスを追加
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-lg',
                'placeholder': field.label
            })


class CustomAuthenticationForm(AuthenticationForm):
    """カスタム認証フォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # スマホ対応のCSSクラスを追加
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-lg',
                'placeholder': field.label
            })


class EmployeeForm(forms.ModelForm):
    """従業員フォーム"""
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'position', 'department', 'phone_number', 'email', 'hire_date', 'profile_image']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '従業員ID'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '氏名'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '職種'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '部署'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '電話番号'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'メールアドレス'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control-file'})
        }


class ShiftForm(forms.ModelForm):
    """シフトフォーム"""
    class Meta:
        model = Shift
        fields = ['employee', 'shift_date', 'shift_type', 'notes']
        widgets = {
            'shift_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'shift_type': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '備考'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # デフォルトで今日以降の日付のみ選択可能
        self.fields['shift_date'].widget.attrs['min'] = date.today().isoformat()


class ShiftRequestForm(forms.ModelForm):
    """シフト申請フォーム"""
    class Meta:
        model = ShiftRequest
        fields = ['request_type', 'original_shift', 'new_shift_type', 'swap_with_employee', 'reason']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'original_shift': forms.Select(attrs={'class': 'form-control'}),
            'new_shift_type': forms.Select(attrs={'class': 'form-control'}),
            'swap_with_employee': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '申請理由を入力してください'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and hasattr(user, 'employee'):
            # 自分のシフトのみ表示
            self.fields['original_shift'].queryset = Shift.objects.filter(
                employee=user.employee,
                shift_date__gte=date.today()
            )
            # 交換相手から自分を除外
            self.fields['swap_with_employee'].queryset = Employee.objects.exclude(
                id=user.employee.id
            ).filter(is_active=True)


class ShiftTypeForm(forms.ModelForm):
    """シフトタイプフォーム"""
    class Meta:
        model = ShiftType
        fields = ['name', 'start_time', 'end_time', 'break_time', 'color_code', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'シフト名'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'color_code': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class DateRangeForm(forms.Form):
    """日付範囲フォーム"""
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=lambda: date.today() - timedelta(days=7),
        label='開始日'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=lambda: date.today() + timedelta(days=7),
        label='終了日'
    )


class QuickShiftForm(forms.Form):
    """クイックシフト作成フォーム（スマホ対応）"""
    employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='従業員'
    )
    shift_type = forms.ModelChoiceField(
        queryset=ShiftType.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
        label='シフトタイプ'
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
        initial=date.today,
        label='開始日'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
        initial=lambda: date.today() + timedelta(days=6),
        label='終了日'
    )


class AttendanceForm(forms.Form):
    """出勤打刻フォーム（スマホ対応）"""
    action = forms.ChoiceField(
        choices=[
            ('check_in', 'チェックイン'),
            ('break_start', '休憩開始'),
            ('break_end', '休憩終了'),
            ('check_out', 'チェックアウト')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='アクション'
    )
    location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '勤務場所'}),
        label='勤務場所'
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '備考'}),
        label='備考'
    )
