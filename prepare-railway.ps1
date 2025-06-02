# PowerShell script to prepare AgenticSeek for Railway deployment
# Run this before pushing to GitHub and deploying to Railway

Write-Host "🚀 Preparing AgenticSeek for Railway Deployment..." -ForegroundColor Green

# Backup original requirements
if (Test-Path "requirements.txt") {
    if (-not (Test-Path "requirements-original.txt")) {
        Write-Host "📦 Backing up original requirements.txt..." -ForegroundColor Yellow
        Copy-Item "requirements.txt" "requirements-original.txt"
    }
}

# Prompt user to choose requirements file
Write-Host "`n📋 Choose requirements file option:" -ForegroundColor Cyan
Write-Host "1. Use railway-optimized requirements (recommended)"
Write-Host "2. Keep original requirements.txt"
$choice = Read-Host "Enter choice (1 or 2)"

if ($choice -eq "1") {
    if (Test-Path "requirements-railway.txt") {
        Write-Host "✅ Replacing requirements.txt with railway-optimized version..." -ForegroundColor Green
        Copy-Item "requirements-railway.txt" "requirements.txt" -Force
    } else {
        Write-Host "❌ requirements-railway.txt not found!" -ForegroundColor Red
    }
} else {
    Write-Host "✅ Keeping original requirements.txt" -ForegroundColor Green
}

# Check for essential files
Write-Host "`n🔍 Checking essential files..." -ForegroundColor Cyan

$essentialFiles = @("Procfile", "railway.toml", "api.py", "config.ini")
foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "❌ $file missing!" -ForegroundColor Red
    }
}

# Display next steps
Write-Host "`n📝 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Commit and push these changes to GitHub"
Write-Host "2. Go to railway.app and create a new project"
Write-Host "3. Connect your GitHub repository"
Write-Host "4. Add Redis database service"
Write-Host "5. Configure environment variables (see railway.env.example)"
Write-Host "6. Deploy!"

Write-Host "`n📖 For detailed instructions, see railway-setup.md" -ForegroundColor Yellow
Write-Host "🎉 Preparation complete!" -ForegroundColor Green 