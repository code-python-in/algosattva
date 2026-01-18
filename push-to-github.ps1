# PowerShell Script to Push Bracket Order Implementation to GitHub
# Run this script from your project root directory: D:\Appa\Markets\Code\openalgo

param(
    [string]$GitHubUsername = "code-python-in",
    [string]$RepositoryName = "openalgo",
    [string]$BranchName = "feature/bracket-orders",
    [string]$CommitMessage = "feat: Add bracket order implementation with REST API and TradingView webhook"
)

# Color output functions
function Write-Header {
    param([string]$Text)
    Write-Host "`n$('=' * 80)" -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "$('=' * 80)`n" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host "✓ $Text" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Text)
    Write-Host "✗ $Text" -ForegroundColor Red
}

function Write-Warning-Custom {
    param([string]$Text)
    Write-Host "⚠ $Text" -ForegroundColor Yellow
}

# Main script
Write-Header "GitHub Push and Deploy Script for Bracket Orders"

# Check if Git is installed
Write-Host "Checking prerequisites..."
$gitVersion = git --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Success "Git is installed: $gitVersion"
} else {
    Write-Error-Custom "Git is not installed. Please install Git from https://git-scm.com/"
    exit 1
}

# Check current directory
$currentDir = Get-Location
Write-Host "Current directory: $currentDir"

if (-not (Test-Path ".git")) {
    Write-Error-Custom "Not in a Git repository. Please run this script from the openalgo root directory."
    exit 1
}

Write-Success "Git repository found"

# Step 1: Configure Git
Write-Header "Step 1: Configuring Git"

$gitUserName = git config --global user.name
if ([string]::IsNullOrEmpty($gitUserName)) {
    Write-Host "Setting Git username to: $GitHubUsername"
    git config --global user.name $GitHubUsername
    Write-Success "Git username configured"
} else {
    Write-Success "Git username already set: $gitUserName"
}

$gitUserEmail = git config --global user.email
if ([string]::IsNullOrEmpty($gitUserEmail)) {
    $emailInput = Read-Host "Enter your GitHub email"
    git config --global user.email $emailInput
    Write-Success "Git email configured: $emailInput"
} else {
    Write-Success "Git email already set: $gitUserEmail"
}

# Step 2: Check remote URL
Write-Header "Step 2: Checking Remote Configuration"

$remotes = git remote -v
if ($LASTEXITCODE -eq 0 -and $remotes) {
    Write-Host "Current remote(s):"
    Write-Host $remotes

    $changeRemote = Read-Host "Change remote URL? (y/n)"
    if ($changeRemote -eq 'y') {
        $newUrl = "https://github.com/$GitHubUsername/$RepositoryName.git"
        Write-Host "Setting remote to: $newUrl"
        git remote set-url origin $newUrl
        Write-Success "Remote URL updated"
    }
} else {
    Write-Warning-Custom "No remote found. Adding origin..."
    $newUrl = "https://github.com/$GitHubUsername/$RepositoryName.git"
    git remote add origin $newUrl
    Write-Success "Origin added: $newUrl"
}

# Step 3: Create branch
Write-Header "Step 3: Creating Feature Branch"

$currentBranch = git rev-parse --abbrev-ref HEAD
Write-Host "Current branch: $currentBranch"

$branches = git branch
if ($branches -like "*$BranchName*") {
    Write-Host "Branch '$BranchName' already exists"
    git checkout $BranchName
    Write-Success "Switched to branch: $BranchName"
} else {
    Write-Host "Creating new branch: $BranchName"
    git checkout -b $BranchName
    Write-Success "Branch created and switched: $BranchName"
}

# Step 4: Check for changes
Write-Header "Step 4: Checking for Changes"

$status = git status --porcelain
if ([string]::IsNullOrEmpty($status)) {
    Write-Warning-Custom "No changes to commit"
    $continueAnyway = Read-Host "Continue with push anyway? (y/n)"
    if ($continueAnyway -ne 'y') {
        exit 0
    }
} else {
    Write-Host "Changes found:"
    Write-Host $status
}

# Step 5: Stage changes
Write-Header "Step 5: Staging Changes"

Write-Host "Running: git add ."
git add .

if ($LASTEXITCODE -eq 0) {
    Write-Success "All changes staged"

    $stagedFiles = git diff --cached --name-only
    Write-Host "Staged files:"
    Write-Host $stagedFiles
} else {
    Write-Error-Custom "Failed to stage changes"
    exit 1
}

# Step 6: Commit
Write-Header "Step 6: Creating Commit"

Write-Host "Commit message:"
Write-Host $CommitMessage
Write-Host ""

$proceedWithCommit = Read-Host "Proceed with commit? (y/n)"
if ($proceedWithCommit -eq 'y') {
    git commit -m $CommitMessage

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Commit created successfully"
    } else {
        Write-Error-Custom "Failed to create commit"
        exit 1
    }
} else {
    Write-Host "Commit cancelled"
    exit 0
}

# Step 7: Push to GitHub
Write-Header "Step 7: Pushing to GitHub"

Write-Host "Repository URL: https://github.com/$GitHubUsername/$RepositoryName"
Write-Host "Branch: $BranchName"
Write-Host ""
Write-Host "Running: git push -u origin $BranchName"
Write-Host ""

$proceedWithPush = Read-Host "Proceed with push to GitHub? (y/n)"
if ($proceedWithPush -eq 'y') {
    git push -u origin $BranchName

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Successfully pushed to GitHub!"
        Write-Host ""
        Write-Host "Your code is now at:"
        Write-Host "https://github.com/$GitHubUsername/$RepositoryName/tree/$BranchName"
    } else {
        Write-Error-Custom "Failed to push to GitHub"
        Write-Host ""
        Write-Host "Troubleshooting:"
        Write-Host "1. Make sure you have GitHub credentials configured"
        Write-Host "2. Check your internet connection"
        Write-Host "3. Verify the repository exists at: https://github.com/$GitHubUsername/$RepositoryName"
        exit 1
    }
} else {
    Write-Host "Push cancelled"
    exit 0
}

# Step 8: Next steps
Write-Header "Next Steps"

Write-Host @"
✓ Code pushed to GitHub successfully!

Next steps to deploy:

1. On your production server, clone the repository:
   git clone https://github.com/$GitHubUsername/$RepositoryName.git
   cd $RepositoryName
   git checkout $BranchName

2. Or if already cloned, update it:
   cd /path/to/$RepositoryName
   git pull origin $BranchName

3. Install dependencies:
   pip install -r requirements.txt

4. Configure .env file:
   BRACKET_ORDER_RATE_LIMIT=2 per second
   BRACKET_ORDER_DELAY=0.5

5. Restart Flask application:
   systemctl restart openalgo
   # or
   docker-compose restart

6. Test the endpoints:
   curl -X POST http://localhost:5000/api/v1/placebracketorder/ ...

7. Verify in database:
   SELECT * FROM order_logs WHERE api_type='placebracketorder'

For detailed information, see:
- GITHUB_PUSH_AND_DEPLOY_GUIDE.md (Complete guide)
- BRACKET_ORDER_README.md (Getting started)
- BRACKET_ORDER_DEPLOYMENT_SUMMARY.md (Deployment details)

"@

Write-Success "Script completed successfully!"

