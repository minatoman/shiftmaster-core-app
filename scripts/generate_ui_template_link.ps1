# generate_ui_template_link.ps1
# 📂 保存先: H:\Projects\ShiftMaster\scripts

$projectRoot = "H:\Projects\ShiftMaster"
$templateSource = "$projectRoot\shifts\static\templates_generated\template_shift_3block_colored.html"
$templateDestDir = "$projectRoot\shifts\templates\templates_generated"
$templateDestFile = "$templateDestDir\template_shift_3block_colored.html"

# フォルダがなければ作成
if (-not (Test-Path $templateDestDir)) {
    New-Item -ItemType Directory -Force -Path $templateDestDir
}

# テンプレートファイルをコピー
if (Test-Path $templateSource) {
    Copy-Item $templateSource $templateDestFile -Force
    Write-Host "✅ HTMLテンプレートをテンプレートフォルダへコピーしました。"
} else {
    Write-Host "❌ ソースファイルが見つかりません: $templateSource"
}

# DjangoビューとURLへの連携情報
Write-Host "`n📌 Django側で以下を追加してください：`n"
Write-Host "`n📄 views.py:"
Write-Host "--------------------------------------"
Write-Host "@login_required"
Write-Host "def view_generated_shift_template(request):"
Write-Host "    return render(request, 'templates_generated/template_shift_3block_colored.html')"
Write-Host "--------------------------------------"

Write-Host "`n📄 urls.py:"
Write-Host "--------------------------------------"
Write-Host "path('shifts/template/3block/', views.view_generated_shift_template, name='shift_template_3block'),"
Write-Host "--------------------------------------"
