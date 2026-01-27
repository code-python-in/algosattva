# Docker UI Preferences Setup Script
# PowerShell version for Windows Docker environments

param(
    [switch]$SkipMigration,
    [switch]$TestOnly
)

Write-Host "=== Docker UI Preferences Setup (PowerShell) ===" -ForegroundColor Green

try {
    # Load environment variables like Flask does
    Write-Host "Loading environment variables..." -ForegroundColor Yellow
    python -c "
import sys
import os
sys.path.insert(0, os.getcwd())
from utils.env_check import load_and_check_env_variables
load_and_check_env_variables()
print('Environment variables loaded')
"

    if (-not $SkipMigration) {
        # Run the migration script
        Write-Host "Running UI preferences migration..." -ForegroundColor Yellow
        python migrate_ui_preferences.py
        
        if ($LASTEXITCODE -ne 0) {
            throw "Migration script failed with exit code $LASTEXITCODE"
        }
    }

    if ($TestOnly) {
        # Test the UI preferences functionality
        Write-Host "Testing UI preferences functionality..." -ForegroundColor Yellow
        $testResult = python -c "
import sys
import os
sys.path.insert(0, os.getcwd())
from utils.env_check import load_and_check_env_variables
load_and_check_env_variables()

try:
    from database.settings_db import get_ui_preferences, set_ui_preferences
    
    # Test getting preferences
    prefs = get_ui_preferences()
    print(f'UI Preferences loaded: {len(prefs)} preferences')
    
    # Test setting a preference
    set_ui_preferences(dashboard_quick_access=True)
    print('UI Preferences test: PASSED')
    
    # Test getting updated preferences
    updated_prefs = get_ui_preferences()
    print(f'Updated preferences: dashboard_quick_access = {updated_prefs[\"dashboard_quick_access\"]}')
    
except Exception as e:
    print(f'UI Preferences test: FAILED - {e}')
    exit(1)
"
        
        if ($LASTEXITCODE -ne 0) {
            throw "UI preferences test failed"
        }
        
        Write-Host "✅ UI preferences test completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "✅ Docker UI preferences setup complete!" -ForegroundColor Green
        Write-Host "You can now start your Flask application." -ForegroundColor Cyan
    }

} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
