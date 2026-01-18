# PowerShell Script to Push Bracket Order to GitHub
# Simplified version without complex error handling

Write-Host "`n========== GitHub Push Script ==========" -ForegroundColor Cyan

# Check Git is installed
git --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Git not found. Install from https://git-scm.com/" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Git found" -ForegroundColor Green

# Check we're in git repo
if (-not (Test-Path ".git")) {
    Write-Host "ERROR: Not in a git repository!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Git repository found" -ForegroundColor Green

# Configure git if needed
$userName = git config --global user.name
if (-not $userName) {
    Write-Host "Configuring git..." -ForegroundColor Yellow
    git config --global user.name "code-python-in"
    Write-Host "Enter your GitHub email:" -ForegroundColor Cyan
    $email = Read-Host
    git config --global user.email $email
    Write-Host "✓ Git configured" -ForegroundColor Green
}

# Set remote
Write-Host "`nConfiguring remote..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/code-python-in/openalgo.git"
git remote set-url origin $remoteUrl 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote add origin $remoteUrl
}
Write-Host "✓ Remote set to: $remoteUrl" -ForegroundColor Green

# Create/switch to feature branch
Write-Host "`nCreating branch..." -ForegroundColor Yellow
git checkout -b feature/bracket-orders 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Branch created: feature/bracket-orders" -ForegroundColor Green
} else {
    git checkout feature/bracket-orders
    Write-Host "✓ Switched to branch: feature/bracket-orders" -ForegroundColor Green
}

# Stage changes
Write-Host "`nStaging changes..." -ForegroundColor Yellow
git add .
Write-Host "✓ Changes staged" -ForegroundColor Green

# Show what will be committed
Write-Host "`nChanges to commit:" -ForegroundColor Cyan
git diff --cached --name-only

# Commit
Write-Host "`nCreating commit..." -ForegroundColor Yellow
$commitMsg = "feat: Add bracket order implementation with REST API and TradingView webhook"
git commit -m $commitMsg
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Commit created" -ForegroundColor Green
} else {
    Write-Host "✗ Commit failed" -ForegroundColor Red
    exit 1
}

# Push to GitHub
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
Write-Host "This may prompt for your GitHub credentials..." -ForegroundColor Cyan
git push -u origin feature/bracket-orders

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓✓✓ SUCCESS! ✓✓✓" -ForegroundColor Green
    Write-Host "`nYour code is now on GitHub:" -ForegroundColor Cyan
    Write-Host "https://github.com/code-python-in/openalgo/tree/feature/bracket-orders" -ForegroundColor White
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "1. On your server, clone the repository:" -ForegroundColor White
    Write-Host "   git clone --branch feature/bracket-orders https://github.com/code-python-in/openalgo.git" -ForegroundColor Gray
    Write-Host "2. Install dependencies:" -ForegroundColor White
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Gray
    Write-Host "3. Configure .env file with:" -ForegroundColor White
    Write-Host "   BRACKET_ORDER_RATE_LIMIT=2 per second" -ForegroundColor Gray
    Write-Host "4. Restart Flask:" -ForegroundColor White
    Write-Host "   systemctl restart openalgo" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "`n✗ Push failed!" -ForegroundColor Red
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Check your internet connection" -ForegroundColor White
    Write-Host "2. Ensure your GitHub credentials are configured" -ForegroundColor White
    Write-Host "3. Verify the repository exists at:" -ForegroundColor White
    Write-Host "   https://github.com/code-python-in/openalgo" -ForegroundColor Gray
    exit 1
}

