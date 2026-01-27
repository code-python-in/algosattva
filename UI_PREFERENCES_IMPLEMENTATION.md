# UI Preferences Implementation Guide

## Overview
This implementation adds profile-based UI element visibility settings to the AlgoSattva application, allowing users to customize their interface experience through toggle controls.

## Features Implemented

### 1. Dashboard Quick Access Toggle
- **Location**: `/dashboard` page
- **Functionality**: Single checkbox to show/hide all Quick Access elements
- **Database Field**: `ui_dashboard_quick_access`

### 2. Platforms Page Configuration
- **Location**: `/platforms` page
- **Functionality**: Individual toggles for:
  - TradingView card (`ui_platforms_tradingview`)
  - GoCharting card (`ui_platforms_gocharting`)
  - Chartink card (`ui_platforms_chartink`)
  - Getting Started documentation (`ui_platforms_documentation`)

### 3. TradingView Page Configuration
- **Location**: `/tradingview` page
- **Functionality**: Individual toggles for:
  - Strategy Alert tab (`ui_tradingview_strategy_alert`)
  - Line Alert tab (`ui_tradingview_line_alert`)
  - Bracket Order tab (`ui_tradingview_bracket_order`)

### 4. Telegram Menu Integration
- **Location**: Main navigation menu
- **Functionality**: Added Telegram as a main menu item alongside existing navigation

## Database Schema Changes

### New Columns in `settings` Table
```sql
-- Dashboard Quick Access Elements
ui_dashboard_quick_access BOOLEAN DEFAULT TRUE

-- Platforms Page Configuration
ui_platforms_tradingview BOOLEAN DEFAULT TRUE
ui_platforms_gocharting BOOLEAN DEFAULT TRUE
ui_platforms_chartink BOOLEAN DEFAULT TRUE
ui_platforms_documentation BOOLEAN DEFAULT TRUE

-- TradingView Page Configuration
ui_tradingview_strategy_alert BOOLEAN DEFAULT TRUE
ui_tradingview_line_alert BOOLEAN DEFAULT TRUE
ui_tradingview_bracket_order BOOLEAN DEFAULT TRUE
```

## Files Modified

### Database Layer
- `database/settings_db.py`
  - Added new columns to Settings model
  - Added `get_ui_preferences()` function
  - Added `set_ui_preferences()` function

### Backend API
- `blueprints/settings.py`
  - Added `/settings/ui-preferences` GET endpoint
  - Added `/settings/ui-preferences` POST endpoint

### Blueprint Updates
- `blueprints/dashboard.py`
  - Updated to pass UI preferences to template
  
- `blueprints/platforms.py`
  - Updated to pass UI preferences to template
  
- `blueprints/tv_json.py`
  - Updated to pass UI preferences to template

### Frontend Templates
- `templates/dashboard.html`
  - Added Quick Access toggle with JavaScript handler
  
- `templates/platforms.html`
  - Added platform configuration toggles with JavaScript handlers
  
- `templates/tradingview.html`
  - Added TradingView configuration toggles with JavaScript handlers
  
- `templates/navbar.html`
  - Added Telegram menu item to main navigation

## API Endpoints

### GET /settings/ui-preferences
Returns current UI preferences:
```json
{
  "dashboard_quick_access": true,
  "platforms_tradingview": true,
  "platforms_gocharting": true,
  "platforms_chartink": true,
  "platforms_documentation": true,
  "tradingview_strategy_alert": true,
  "tradingview_line_alert": true,
  "tradingview_bracket_order": true
}
```

### POST /settings/ui-preferences
Updates UI preferences:
```json
{
  "dashboard_quick_access": false,
  "platforms_tradingview": true,
  // ... other preferences
}
```

## Rollback Instructions

### Method 1: Git Rollback (Recommended)
If you want to revert all changes:

```bash
# Check current git status
git status

# See what files were modified
git diff --name-only

# Rollback to previous commit
git reset --hard HEAD~1

# Or rollback to a specific commit
git reset --hard <commit-hash>
```

### Method 2: Manual Database Rollback
If you want to keep code changes but remove database columns:

```sql
-- Remove UI preference columns from settings table
ALTER TABLE settings 
DROP COLUMN IF EXISTS ui_dashboard_quick_access,
DROP COLUMN IF EXISTS ui_platforms_tradingview,
DROP COLUMN IF EXISTS ui_platforms_gocharting,
DROP COLUMN IF EXISTS ui_platforms_chartink,
DROP COLUMN IF EXISTS ui_platforms_documentation,
DROP COLUMN IF EXISTS ui_tradingview_strategy_alert,
DROP COLUMN IF EXISTS ui_tradingview_line_alert,
DROP COLUMN IF EXISTS ui_tradingview_bracket_order;
```

### Method 3: Selective File Rollback
If you want to revert specific files:

```bash
# Revert specific files to previous commit
git checkout HEAD~1 -- database/settings_db.py
git checkout HEAD~1 -- blueprints/settings.py
git checkout HEAD~1 -- templates/dashboard.html
git checkout HEAD~1 -- templates/platforms.html
git checkout HEAD~1 -- templates/tradingview.html
git checkout HEAD~1 -- templates/navbar.html
git checkout HEAD~1 -- blueprints/dashboard.py
git checkout HEAD~1 -- blueprints/platforms.py
git checkout HEAD~1 -- blueprints/tv_json.py
```

## Testing Checklist

### Dashboard Functionality
- [ ] Quick Access toggle shows/hides all elements
- [ ] Preference persists after page refresh
- [ ] Preference persists after logout/login
- [ ] Toggle state matches database value

### Platforms Page Functionality
- [ ] Individual platform toggles work correctly
- [ ] Documentation toggle works correctly
- [ ] All preferences persist after refresh
- [ ] Card visibility matches toggle states

### TradingView Page Functionality
- [ ] Tab toggles show/hide correctly
- [ ] Tab switching logic works when tabs are hidden
- [ ] Form fields update correctly with tab changes
- [ ] Preferences persist after refresh

### Navigation
- [ ] Telegram menu item appears in main navigation
- [ ] Telegram menu item highlights correctly when active
- [ ] Mobile navigation works correctly

### Error Handling
- [ ] Network errors revert toggle changes
- [ ] Invalid responses from API are handled gracefully
- [ ] JavaScript errors don't break functionality

## Browser Compatibility
- [ ] Chrome/Chromium: Full support
- [ ] Firefox: Full support
- [ ] Safari: Full support
- [ ] Edge: Full support
- [ ] Mobile browsers: Full support

## Performance Considerations
- UI preferences are cached for 1 hour to reduce database queries
- Toggle changes provide immediate visual feedback
- Failed API calls revert UI changes to maintain consistency
- JavaScript uses async/await for non-blocking operations

## Security Notes
- All UI preference endpoints require valid session authentication
- CSRF protection is enabled for all preference updates
- No sensitive data is stored in UI preferences
- All preferences are server-validated before storage

## Future Enhancements
Potential improvements for future versions:
1. Per-user theme customization
2. Dashboard widget arrangement
3. Customizable navigation menu items
4. Notification preferences
5. Language and locale settings
6. Accessibility preferences (font sizes, contrast)

## Troubleshooting

### Common Issues

**Toggle changes not persisting**
- Check browser console for JavaScript errors
- Verify network requests are successful
- Check session authentication status

**Database errors**
- Ensure database migrations have run
- Check database connection status
- Verify table schema matches expectations

**UI elements not updating**
- Clear browser cache
- Check CSS specificity issues
- Verify JavaScript is loading correctly

**Performance issues**
- Check database query performance
- Monitor cache hit rates
- Review JavaScript execution time

## Support
For issues or questions about this implementation:
1. Check the troubleshooting section above
2. Review browser console for errors
3. Verify database connectivity
4. Check application logs for detailed error messages
