# UI Preferences Rollback Script (PowerShell)
# This script helps rollback the UI preferences implementation

Write-Host "=== AlgoSattva UI Preferences Rollback Script ===" -ForegroundColor Cyan
Write-Host ""

# Check if we're in a git repository
try {
    $null = git rev-parse --git-dir 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Not in a git repository" -ForegroundColor Red
        Write-Host "Please run this script from the AlgoSattva root directory"
        exit 1
    }
} catch {
    Write-Host "Error: Git not found or not in a git repository" -ForegroundColor Red
    exit 1
}

Write-Host "Current git status:" -ForegroundColor Yellow
git status --porcelain
Write-Host ""

Write-Host "Available rollback options:" -ForegroundColor Yellow
Write-Host "1. Full rollback (revert all changes to previous commit)"
Write-Host "2. Database only rollback (remove UI preference columns)"
Write-Host "3. Code only rollback (revert code files, keep database)"
Write-Host "4. Show what would be rolled back (dry run)"
Write-Host "5. Exit"
Write-Host ""

$choice = Read-Host "Choose rollback option (1-5)"

switch ($choice) {
    "1" {
        Write-Host "Performing full rollback..." -ForegroundColor Yellow
        Write-Host "This will revert ALL changes to the previous commit"
        $confirm = Read-Host "Are you sure? (y/N)"
        if ($confirm -match '^[Yy]$') {
            git reset --hard HEAD~1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Full rollback completed" -ForegroundColor Green
            } else {
                Write-Host "Rollback failed" -ForegroundColor Red
            }
        } else {
            Write-Host "Rollback cancelled" -ForegroundColor Yellow
        }
    }
    
    "2" {
        Write-Host "Performing database only rollback..." -ForegroundColor Yellow
        Write-Host "This will remove UI preference columns from the database"
        $confirm = Read-Host "Are you sure? (y/N)"
        if ($confirm -match '^[Yy]$') {
            # Create SQL rollback script
            $sqlContent = @"
-- Rollback UI Preferences Database Changes
-- Run this SQL script to remove UI preference columns

ALTER TABLE settings 
DROP COLUMN IF EXISTS ui_dashboard_quick_access,
DROP COLUMN IF EXISTS ui_platforms_tradingview,
DROP COLUMN IF EXISTS ui_platforms_gocharting,
DROP COLUMN IF EXISTS ui_platforms_chartink,
DROP COLUMN IF EXISTS ui_platforms_documentation,
DROP COLUMN IF EXISTS ui_tradingview_strategy_alert,
DROP COLUMN IF EXISTS ui_tradingview_line_alert,
DROP COLUMN IF EXISTS ui_tradingview_bracket_order;
"@
            $sqlContent | Out-File -FilePath "rollback_ui_preferences.sql" -Encoding UTF8
            Write-Host "SQL rollback script created: rollback_ui_preferences.sql" -ForegroundColor Green
            Write-Host "Please run this script against your database"
            Write-Host "Example: sqlite3 database.db < rollback_ui_preferences.sql"
        } else {
            Write-Host "Rollback cancelled" -ForegroundColor Yellow
        }
    }
    
    "3" {
        Write-Host "Performing code only rollback..." -ForegroundColor Yellow
        Write-Host "This will revert code files but keep database changes"
        $confirm = Read-Host "Are you sure? (y/N)"
        if ($confirm -match '^[Yy]$') {
            # List of files to rollback
            $files = @(
                "database/settings_db.py",
                "blueprints/settings.py",
                "templates/dashboard.html",
                "templates/platforms.html",
                "templates/tradingview.html",
                "templates/navbar.html",
                "blueprints/dashboard.py",
                "blueprints/platforms.py",
                "blueprints/tv_json.py"
            )
            
            foreach ($file in $files) {
                try {
                    $null = git show HEAD~1:$file 2>$null
                    if ($LASTEXITCODE -eq 0) {
                        git checkout HEAD~1 -- $file
                        if ($LASTEXITCODE -eq 0) {
                            Write-Host "Reverted: $file" -ForegroundColor Green
                        } else {
                            Write-Host "Failed to revert: $file" -ForegroundColor Red
                        }
                    } else {
                        Write-Host "File not found in previous commit: $file" -ForegroundColor Yellow
                    }
                } catch {
                    Write-Host "Error checking file: $file" -ForegroundColor Red
                }
            }
            
            Write-Host "Code rollback completed" -ForegroundColor Green
            Write-Host "Database changes were preserved" -ForegroundColor Yellow
        } else {
            Write-Host "Rollback cancelled" -ForegroundColor Yellow
        }
    }
    
    "4" {
        Write-Host "Dry run - showing what would be rolled back:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Files that would be reverted:" -ForegroundColor Cyan
        git diff --name-only HEAD~1
        Write-Host ""
        Write-Host "Database columns that would be removed:" -ForegroundColor Cyan
        Write-Host "- ui_dashboard_quick_access"
        Write-Host "- ui_platforms_tradingview"
        Write-Host "- ui_platforms_gocharting"
        Write-Host "- ui_platforms_chartink"
        Write-Host "- ui_platforms_documentation"
        Write-Host "- ui_tradingview_strategy_alert"
        Write-Host "- ui_tradingview_line_alert"
        Write-Host "- ui_tradingview_bracket_order"
    }
    
    "5" {
        Write-Host "Exiting rollback script" -ForegroundColor Yellow
        exit 0
    }
    
    default {
        Write-Host "Invalid option. Exiting." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Rollback operation completed" -ForegroundColor Green
Write-Host "Please test your application to ensure everything works correctly" -ForegroundColor Yellow
