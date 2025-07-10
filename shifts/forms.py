from django import forms
from .models import (
    Shift, ShiftRequest, Employee, HolidayRequest, LeaveBalance,
    Committee, OnCallShift, DialysisPatient, DialysisStaff
)
from .utils import process_uploaded_files  # ファイル処理関数のインポート

# シフトのフォーム
class ShiftForm(forms.ModelForm):
    shift_type = forms.ChoiceField(choices=Shift.SHIFT_TYPES)

    class Meta:
        model = Shift
        fields = ['employee', 'shift_date', 'shift_type', 'is_approved']

# 勤務希望のフォーム
class ShiftRequestForm(forms.ModelForm):
    shift_type = forms.ChoiceField(choices=Shift.SHIFT_TYPES)

    class Meta:
        model = ShiftRequest
        fields = ['employee', 'requested_date', 'shift_type', 'priority']

    def clean_requested_date(self):
        date = self.cleaned_data['requested_date']
        if date.day > 17:
            raise forms.ValidationError("17日以降は勤務希望の提出ができません。")
        return date

# シフト承認のフォーム
class ShiftApprovalForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['is_approved']

# 拡張された Employee モデルに対応するフォーム
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'work_constraints': forms.Textarea(attrs={'rows': 2}),
            'qualifications': forms.Textarea(attrs={'rows': 2}),
            'work_details': forms.Textarea(attrs={'rows': 2}),
            'committees': forms.Textarea(attrs={'rows': 2}),
            'teams': forms.Textarea(attrs={'rows': 2}),
            'yearly_goals': forms.Textarea(attrs={'rows': 2}),
            'career_history': forms.Textarea(attrs={'rows': 2}),
            'performance_evaluation': forms.Textarea(attrs={'rows': 2}),
            'ability_rating': forms.Textarea(attrs={'rows': 2}),
            'admin_notes': forms.Textarea(attrs={'rows': 2}),
            'interview_history': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

# 休暇希望のフォーム
class HolidayRequestForm(forms.ModelForm):
    class Meta:
        model = HolidayRequest
        fields = ['employee', 'holiday_date', 'holiday_type']

# シフト編集フォーム
class ShiftEditForm(forms.ModelForm):
    shift_type = forms.ChoiceField(choices=Shift.SHIFT_TYPES)

    class Meta:
        model = Shift
        fields = ['shift_date', 'shift_type', 'is_approved']

# 休暇残数の管理フォーム（管理者のみ編集可能）
class LeaveBalanceForm(forms.ModelForm):
    class Meta:
        model = LeaveBalance
        fields = ['annual_leave', 'compensatory_leave', 'weekend_leave', 'night_shift_leave']

# 委員会スケジュールフォーム
class CommitteeScheduleForm(forms.ModelForm):
    class Meta:
        model = Committee
        fields = ['name', 'schedule_type', 'weekday', 'day_of_month', 'time', 'description']

# 夜間透析呼び出し勤務フォーム
class OnCallShiftForm(forms.ModelForm):
    class Meta:
        model = OnCallShift
        fields = ['employee', 'shift_type', 'start_datetime', 'end_datetime']

# 透析患者フォーム
class DialysisPatientForm(forms.ModelForm):
    class Meta:
        model = DialysisPatient
        fields = ['name', 'dialysis_time', 'gender', 'area', 'remarks', 'date']

# 勤務者記録フォーム（透析）
class DialysisStaffForm(forms.ModelForm):
    class Meta:
        model = DialysisStaff
        fields = ['name', 'shift_type', 'role', 'remarks_am', 'remarks_pm', 'date']

# 勤務表アップロード用フォーム
class UploadFileForm(forms.Form):
    """
    勤務表ファイルのアップロードフォーム
    """
    file = forms.FileField(label="勤務表ファイル")

    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        # ファイルの検証処理（サイズや拡張子のチェックなど）
        if file:
            if not file.name.endswith('.csv'):
                raise forms.ValidationError("CSVファイルのみがサポートされています。")
            
            # ファイルサイズ制限（例：最大10MB）
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("ファイルサイズが大きすぎます。10MB以下のファイルをアップロードしてください。")
        
        return file

    def process_file(self):
        """
        アップロードされたファイルを処理する関数
        """
        file = self.cleaned_data.get('file')
        if file:
            # process_uploaded_files 関数を利用してファイルの処理
            data = process_uploaded_files([file])
            return data
        return None
