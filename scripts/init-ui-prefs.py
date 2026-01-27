#!/usr/bin/env python3
"""
Docker initialization script for UI preferences
This script ensures UI preferences are properly set up in Docker containers
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_ui_preferences():
    """Initialize UI preferences for Docker deployment"""
    
    logger.info("Initializing UI preferences for Docker environment...")
    
    try:
        # Add project root to Python path
        project_root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_root)
        
        # Load environment variables
        from utils.env_check import load_and_check_env_variables
        load_and_check_env_variables()
        logger.info("Environment variables loaded")
        
        # Check if we need to run migration
        try:
            from database.settings_db import get_ui_preferences
            
            # Test if UI preferences work
            prefs = get_ui_preferences()
            logger.info(f"UI preferences already configured: {len(prefs)} preferences")
            
            # Test setting a preference to ensure it works
            from database.settings_db import set_ui_preferences
            set_ui_preferences(dashboard_quick_access=prefs.get('dashboard_quick_access', True))
            logger.info("UI preferences functionality verified")
            
        except Exception as pref_error:
            logger.warning(f"UI preferences test failed: {pref_error}")
            logger.info("Running UI preferences migration...")
            
            # Run migration
            from migrate_ui_preferences import migrate_ui_preferences
            migrate_ui_preferences()
            logger.info("UI preferences migration completed")
            
            # Test again after migration
            from database.settings_db import get_ui_preferences, set_ui_preferences
            prefs = get_ui_preferences()
            set_ui_preferences(dashboard_quick_access=True)
            logger.info(f"UI preferences initialized: {len(prefs)} preferences")
        
        logger.info("✅ UI preferences initialization successful!")
        return True
        
    except Exception as e:
        logger.error(f"❌ UI preferences initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_ui_preferences():
    """Verify UI preferences are working correctly"""
    
    logger.info("Verifying UI preferences...")
    
    try:
        from database.settings_db import get_ui_preferences, set_ui_preferences
        
        # Test getting preferences
        prefs = get_ui_preferences()
        logger.info(f"Retrieved {len(prefs)} preferences")
        
        # Test setting a preference
        original_value = prefs.get('dashboard_quick_access', True)
        new_value = not original_value
        
        set_ui_preferences(dashboard_quick_access=new_value)
        
        # Verify the change
        updated_prefs = get_ui_preferences()
        if updated_prefs.get('dashboard_quick_access') == new_value:
            logger.info("✅ UI preferences verification passed!")
            
            # Reset to original value
            set_ui_preferences(dashboard_quick_access=original_value)
            return True
        else:
            logger.error("❌ UI preferences verification failed - changes not persisting")
            return False
            
    except Exception as e:
        logger.error(f"❌ UI preferences verification error: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize UI preferences for Docker')
    parser.add_argument('--verify-only', action='store_true', 
                       help='Only verify existing UI preferences, skip initialization')
    parser.add_argument('--test', action='store_true',
                       help='Run comprehensive tests')
    
    args = parser.parse_args()
    
    if args.verify_only:
        success = verify_ui_preferences()
    elif args.test:
        success = init_ui_preferences() and verify_ui_preferences()
    else:
        success = init_ui_preferences()
    
    sys.exit(0 if success else 1)
