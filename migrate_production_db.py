#!/usr/bin/env python3
"""
Production Database Migration Script for EC2 Deployment
This script handles all database schema changes for production deployment
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_migrations():
    """Run all database migrations in production"""
    
    logger.info("Starting production database migrations...")
    
    try:
        # Add project root to Python path
        project_root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_root)
        
        # Load environment variables
        from utils.env_check import load_and_check_env_variables
        load_and_check_env_variables()
        logger.info("Environment variables loaded")
        
        # 1. Run UI preferences migration
        logger.info("Running UI preferences migration...")
        try:
            from migrate_ui_preferences import migrate_ui_preferences
            migrate_ui_preferences()
            logger.info("✅ UI preferences migration completed")
        except Exception as e:
            logger.warning(f"UI preferences migration failed or already run: {e}")
        
        # 2. Verify database schema
        logger.info("Verifying database schema...")
        try:
            from database.settings_db import get_ui_preferences, set_ui_preferences
            
            # Test UI preferences functionality
            prefs = get_ui_preferences()
            logger.info(f"✅ UI preferences verified: {len(prefs)} preferences found")
            
            # Test setting a preference
            set_ui_preferences(dashboard_quick_access=True)
            logger.info("✅ UI preferences functionality verified")
            
        except Exception as e:
            logger.error(f"❌ Database schema verification failed: {e}")
            raise
        
        # 3. Check for any missing tables or columns
        logger.info("Checking database integrity...")
        try:
            from sqlalchemy import text
            from database.settings_db import engine
            
            with engine.connect() as conn:
                # Check settings table exists
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='settings'"))
                if not result.fetchone():
                    logger.error("❌ Settings table not found")
                    raise Exception("Settings table missing")
                
                # Check UI preference columns exist
                result = conn.execute(text("PRAGMA table_info(settings)"))
                columns = [row[1] for row in result.fetchall()]
                ui_columns = [col for col in columns if col.startswith('ui_')]
                
                expected_ui_columns = [
                    'ui_dashboard_quick_access',
                    'ui_platforms_tradingview', 
                    'ui_platforms_gocharting',
                    'ui_platforms_chartink',
                    'ui_platforms_documentation',
                    'ui_tradingview_strategy_alert',
                    'ui_tradingview_line_alert',
                    'ui_tradingview_bracket_order'
                ]
                
                missing_columns = [col for col in expected_ui_columns if col not in ui_columns]
                if missing_columns:
                    logger.error(f"❌ Missing UI columns: {missing_columns}")
                    raise Exception(f"Missing UI columns: {missing_columns}")
                
                logger.info(f"✅ Database integrity verified: {len(ui_columns)} UI columns found")
                
        except Exception as e:
            logger.error(f"❌ Database integrity check failed: {e}")
            raise
        
        logger.info("🎉 All database migrations completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
