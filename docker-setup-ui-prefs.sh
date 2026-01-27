#!/bin/bash
# Docker setup script for UI Preferences
# This script ensures the database is properly configured for UI preferences in Docker

set -e

echo "=== Docker UI Preferences Setup ==="

# Wait for database to be ready (if using external database)
echo "Waiting for database to be ready..."
sleep 5

# Run the migration script
echo "Running UI preferences migration..."
python migrate_ui_preferences.py

# Verify the migration
echo "Verifying UI preferences setup..."
python -c "
import os
from utils.env_check import load_and_check_env_variables
load_and_check_env_variables()

from database.settings_db import get_ui_preferences, set_ui_preferences

# Test UI preferences
prefs = get_ui_preferences()
print(f'UI Preferences loaded: {len(prefs)} preferences')

# Test setting a preference
set_ui_preferences(dashboard_quick_access=True)
print('UI Preferences test: PASSED')
"

echo "✅ Docker UI Preferences setup complete!"
echo "You can now start your Flask application."
