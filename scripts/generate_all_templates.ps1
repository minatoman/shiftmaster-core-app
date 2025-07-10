
param (
    [int]$Year = 2025,
    [int]$Month = 4
)

$targetDir = "shifts/static/templates_generated"
$venvPython = "env/Scripts/python.exe"

$pyScript = @"
import pandas as pd
import calendar
from datetime import datetime
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from fpdf import FPDF

output_dir = Path("shifts/static/templates_generated")
output_dir.mkdir(parents=True, exist_ok=True)

year = $Year
month = $Month
days_in_month = calendar.monthrange(year, month)[1]
dates = [datetime(year, month, d+1) for d in range(days_in_month)]
shift_blocks = ["午前", "午後", "夜間"]
weekday_map = ["月", "火", "水", "木", "金", "土", "日"]

staff = ["神 道人", "大谷 興", "木村 陽子", "渥美 大五", "丸谷 啓彰"]
positions = ["Ns", "CE", "Ns", "Ns", "CE"]

records = []
for name, pos in zip(staff, positions):
    for dt in dates:
        for block in shift_blocks:
            shift = "勤務" if block != "夜間" else ("当直" if pos == "Ns" else "")
            records.append([name, dt.strftime("%Y-%m-%d"), block, pos, shift, ""])

df = pd.DataFrame(records, columns=["名前", "日付", "区分", "職種", "勤務内容", "備考"])
df.to_csv(output_dir / "template_shift_3block.csv", index=False, encoding="utf-8-sig")
df.to_excel(output_dir / "template_shift_3block.xlsx", index=False)

# 色付きExcel
wb = Workbook()
ws = wb.active
ws.append(df.columns.tolist())
color_map = {"Ns": "CCE5FF", "CE": "F0C8FF", "中材": "FFFACD"}
for row in records:
    ws.append(row)
    color = color_map.get(row[3], None)
    if color:
        for col in range(1, 7):
            ws.cell(row=ws.max_row, column=col).fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
wb.save(output_dir / "template_shift_3block_colored.xlsx")

# AI割当
df["割当済"] = df["勤務内容"].apply(lambda x: "○" if x in ["勤務", "当直"] else "")
df.to_excel(output_dir / "template_shift_3block_ai.xlsx", index=False)

# カウント集計
summary = df.groupby(["名前", "職種", "勤務内容"])["割当済"].apply(lambda x: (x=="○").sum()).unstack().fillna(0)
summary.to_excel(output_dir / "template_shift_3block_summary.xlsx")

# PDF出力
pdf = FPDF(orientation='L', unit='mm', format='A4')
pdf.add_page()
pdf.set_font("Arial", size=8)
pdf.cell(0, 10, f"勤務表: {year}年 {month}月", ln=True)
pdf.set_fill_color(200, 220, 255)
for col in df.columns:
    pdf.cell(45, 8, str(col), 1, 0, 'C', 1)
pdf.ln()
for _, row in df.iterrows():
    for val in row:
        pdf.cell(45, 8, str(val), 1)
    pdf.ln()
pdf.output(str(output_dir / "template_shift_3block.pdf"))
"@

$pyFile = "generate_shift_templates.py"
$pyScript | Out-File -Encoding UTF8 $pyFile
& $venvPython $pyFile
Remove-Item $pyFile
Write-Host "✅ すべてのテンプレート生成完了 ($Year年 $Month月)"
