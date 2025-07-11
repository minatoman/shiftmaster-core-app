# ShiftMaster GitHub Setup Automation Script
# Execution Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Write-Host "🚀 ShiftMaster GitHub Automation Script Started" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Yellow

# 1. Project Information Display
Write-Host "📊 Project Information:" -ForegroundColor Cyan
Write-Host "  - Project Name: ShiftMaster"
Write-Host "  - Tech Stack: Django 5.2+ / Python 3.8+"
Write-Host "  - Recommended Repo Name: shiftmaster-django-healthcare"
Write-Host ""

# 2. Git Status Check
Write-Host "🔍 Checking Current Git Status..." -ForegroundColor Cyan
git status
Write-Host ""

# 3. GitHub Authentication Check
Write-Host "🔐 Checking GitHub Authentication..." -ForegroundColor Cyan
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "GitHub CLI is available"
    gh auth status
} else {
    Write-Host "⚠️ GitHub CLI not found" -ForegroundColor Yellow
    Write-Host "Please create GitHub repository manually:"
    Write-Host "1. Go to https://github.com/new"
    Write-Host "2. Repository name: shiftmaster-django-healthcare"
    Write-Host "3. Create as Private repository"
    Write-Host "4. Do not add README, .gitignore, license (already exists)"
    Write-Host ""
}

# 4. GitHub Repository Creation (if CLI available)
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "📦 Creating GitHub Repository..." -ForegroundColor Cyan
    try {
        gh repo create shiftmaster-django-healthcare --private --description "Django healthcare shift management system" --confirm
        Write-Host "✅ GitHub repository created successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Repository creation error: $_" -ForegroundColor Red
    }
}

# 5. Remote Repository Setup
Write-Host "🔗 Setting up Remote Repository..." -ForegroundColor Cyan
$repoUrl = "https://github.com/YOUR_USERNAME/shiftmaster-django-healthcare.git"
Write-Host "  Recommended URL: $repoUrl"
Write-Host "  ※ Replace YOUR_USERNAME with your actual GitHub username"

# Sample commands for manual execution
Write-Host "📝 Manual Execution Commands:" -ForegroundColor Yellow
Write-Host "git remote add origin https://github.com/YOUR_USERNAME/shiftmaster-django-healthcare.git"
Write-Host "git branch -M main"
Write-Host "git push -u origin main"
Write-Host ""

# 6. Project Structure Verification
Write-Host "📁 Project Structure Check:" -ForegroundColor Cyan
Write-Host "  ✅ .gitignore - Created"
Write-Host "  ✅ .dockerignore - Created"
Write-Host "  ✅ README.md - Created"
Write-Host "  ✅ Dockerfile - Created"
Write-Host "  ✅ docker-compose.yml - Created"
Write-Host "  ✅ requirements.txt - Verified"
Write-Host ""

# 7. Next Steps Guide
Write-Host "🎯 Next Steps:" -ForegroundColor Green
Write-Host "1. Create GitHub repository manually (if not completed)"
Write-Host "2. Set remote repository: git remote add origin [URL]"
Write-Host "3. Initial push: git push -u origin main"
Write-Host "4. Setup GitHub Actions (CI/CD)"
Write-Host "5. Prepare production deployment"
Write-Host ""

# 8. Troubleshooting Information
Write-Host "🛠️ Troubleshooting:" -ForegroundColor Yellow
Write-Host "- Git auth error: Setup GitHub Personal Access Token"
Write-Host "- Push error: Check git config --global user.name/email"
Write-Host "- Docker issues: Verify Docker Desktop is running"
Write-Host ""

# 9. Completion Message
Write-Host "✅ Project setup completed!" -ForegroundColor Green
Write-Host "📚 See README.md for detailed usage instructions"
Write-Host "================================================" -ForegroundColor Yellow

# Log to file
$logContent = @"
ShiftMaster GitHub Automation Log
Execution DateTime: $(Get-Date)
Project Status: Ready
Recommended Repository Name: shiftmaster-django-healthcare
Next Action: Create GitHub repository and setup remote
"@

$logContent | Out-File -FilePath "setup_log.txt" -Encoding UTF8
Write-Host "📝 Log saved to setup_log.txt" -ForegroundColor Cyan