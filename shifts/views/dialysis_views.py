# shifts/views/dialysis_views.py

import os
import csv
import calendar
from datetime import date, datetime
from io import BytesIO

import pandas as pd

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse
from django.forms import modelformset_factory

from shifts.models import DialysisPatient, DialysisStaff
from shifts.forms import DialysisPatientForm, DialysisStaffForm

# === テスト環境判定 & PDFモジュール制御 ===
if os.environ.get("DJANGO_TEST") != "1":
    try:
        from xhtml2pdf import pisa
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False
else:
    PDF_AVAILABLE = False


@login_required
def dialysis_daily_view(request, selected_date=None):
    """透析日誌（患者とスタッフ情報）を表示"""
    selected_date = selected_date or date.today()
    patients = DialysisPatient.objects.filter(date=selected_date)
    staff = DialysisStaff.objects.filter(date=selected_date)
    return render(request, 'dialysis/daily_view.html', {
        'patients': patients,
        'staff': staff,
        'date': selected_date
    })


@login_required
def dialysis_register_view(request):
    """透析患者・スタッフ情報の一括登録"""
    if not request.user.is_staff and datetime.now().day > 17:
        raise PermissionDenied("17日以降は編集できません（スタッフ専用）")

    PatientFormSet = modelformset_factory(DialysisPatient, form=DialysisPatientForm, extra=5)
    StaffFormSet = modelformset_factory(DialysisStaff, form=DialysisStaffForm, extra=5)

    if request.method == 'POST':
        pf = PatientFormSet(request.POST, queryset=DialysisPatient.objects.none())
        sf = StaffFormSet(request.POST, queryset=DialysisStaff.objects.none())
        if pf.is_valid() and sf.is_valid():
            pf.save()
            sf.save()
            return redirect('shifts:dialysis_daily')
    else:
        pf = PatientFormSet(queryset=DialysisPatient.objects.none())
        sf = StaffFormSet(queryset=DialysisStaff.objects.none())

    return render(request, 'dialysis/register.html', {'pf': pf, 'sf': sf})


@login_required
def import_dialysis_csv(request):
    """CSV/Excelから透析患者データをインポート"""
    if request.method == "POST" and request.FILES.get('file'):
        file = request.FILES['file']
        try:
            ext = os.path.splitext(file.name)[1].lower()
            if ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file, encoding='utf-8')

            for _, row in df.iterrows():
                if not pd.isna(row.get('名前')):
                    DialysisPatient.objects.create(
                        name=row['名前'],
                        dialysis_time=row.get('透析時間'),
                        gender=row.get('性別'),
                        area=row.get('地域'),
                        remarks=row.get('備考', ''),
                        date=row.get('日付') if pd.notna(row.get('日付')) else date.today()
                    )
            messages.success(request, "透析日誌データをインポートしました。")
        except Exception as e:
            messages.error(request, f"インポート中にエラーが発生しました: {e}")

        return redirect('shifts:dialysis_daily')
    return render(request, 'dialysis/import.html')


@login_required
def dialysis_pdf_export(request, date_str):
    """透析日誌PDFをダウンロード出力"""
    if not PDF_AVAILABLE:
        return HttpResponse("PDFライブラリが未インストールです。", status=503)

    try:
        target_date = date.fromisoformat(date_str)
    except ValueError:
        return HttpResponse("日付形式が不正です。", status=400)

    patients = DialysisPatient.objects.filter(date=target_date)
    staff = DialysisStaff.objects.filter(date=target_date)

    html = get_template('dialysis/pdf_template.html').render({
        'patients': patients,
        'staff': staff,
        'date': target_date
    })

    buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer)

    if pisa_status.err:
        return HttpResponse("PDF生成中にエラーが発生しました。", status=500)

    return HttpResponse(buffer.getvalue(), content_type='application/pdf')


@login_required
def dialysis_calendar_api_events(request):
    """カレンダー表示用：透析実施日リストをJSONで返却"""
    dates = DialysisPatient.objects.values_list('date', flat=True).distinct()
    events = [{'title': '透析あり', 'start': d.isoformat()} for d in dates]
    return JsonResponse(events, safe=False)

