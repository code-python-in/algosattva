#!/bin/bash

# UI Preferences Rollback Script
# This script helps rollback the UI preferences implementation

echo "=== AlgoSattva UI Preferences Rollback Script ==="
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    echo "Please run this script from the AlgoSattva root directory"
    exit 1
fi

echo "Current git status:"
git status --porcelain
echo ""

echo "Available rollback options:"
echo "1. Full rollback (revert all changes to previous commit)"
echo "2. Database only rollback (remove UI preference columns)"
echo "3. Code only rollback (revert code files, keep database)"
echo "4. Show what would be rolled back (dry run)"
echo "5. Exit"
echo ""

read -p "Choose rollback option (1-5): " choice

case $choice in
    1)
        echo "Performing full rollback..."
        echo "This will revert ALL changes to the previous commit"
        read -p "Are you sure? (y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            git reset --hard HEAD~1
            echo "Full rollback completed"
        else
            echo "Rollback cancelled"
        fi
        ;;
    
    2)
        echo "Performing database only rollback..."
        echo "This will remove UI preference columns from the database"
        read -p "Are you sure? (y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            # Create SQL rollback script
            cat > rollback_ui_preferences.sql << 'EOF'
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
EOF
            echo "SQL rollback script created: rollback_ui_preferences.sql"
            echo "Please run this script against your database"
            echo "Example: sqlite3 database.db < rollback_ui_preferences.sql"
        else
            echo "Rollback cancelled"
        fi
        ;;
    
    3)
        echo "Performing code only rollback..."
        echo "This will revert code files but keep database changes"
        read -p "Are you sure? (y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            # List of files to rollback
            files=(
                "database/settings_db.py"
                "blueprints/settings.py"
                "templates/dashboard.html"
                "templates/platforms.html"
                "templates/tradingview.html"
                "templates/navbar.html"
                "blueprints/dashboard.py"
                "blueprints/platforms.py"
                "blueprints/tv_json.py"
            )
            
            for file in "${files[@]}"; do
                if git show HEAD~1:$file > /dev/null 2>&1; then
                    git checkout HEAD~1 -- "$file"
                    echo "Reverted: $file"
                else
                    echo "File not found in previous commit: $file"
                fi
            done
            
            echo "Code rollback completed"
            echo "Database changes were preserved"
        else
            echo "Rollback cancelled"
        fi
        ;;
    
    4)
        echo "Dry run - showing what would be rolled back:"
        echo ""
        echo "Files that would be reverted:"
        git diff --name-only HEAD~1
        echo ""
        echo "Database columns that would be removed:"
        echo "- ui_dashboard_quick_access"
        echo "- ui_platforms_tradingview"
        echo "- ui_platforms_gocharting"
        echo "- ui_platforms_chartink"
        echo "- ui_platforms_documentation"
        echo "- ui_tradingview_strategy_alert"
        echo "- ui_tradingview_line_alert"
        echo "- ui_tradingview_bracket_order"
        ;;
    
    5)
        echo "Exiting rollback script"
        exit 0
        ;;
    
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac

echo ""
echo "Rollback operation completed"
echo "Please test your application to ensure everything works correctly"
