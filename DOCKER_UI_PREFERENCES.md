# Docker UI Preferences Setup Guide

## Overview
This guide explains how to set up UI preferences for your Docker deployment of AlgoSattva.

## Prerequisites
- Docker and Docker Compose installed
- AlgoSattva codebase with UI preferences implemented

## Option 1: Using the Setup Script (Recommended)

### 1. Add to Dockerfile
Add these lines to your `Dockerfile` before the CMD:

```dockerfile
# Copy UI preferences setup script
COPY docker-setup-ui-prefs.sh /app/docker-setup-ui-prefs.sh
RUN chmod +x /app/docker-setup-ui-prefs.sh

# Copy migration script
COPY migrate_ui_preferences.py /app/migrate_ui_preferences.py
```

### 2. Update Docker Compose
Modify your `docker-compose.yml` to run the setup script:

```yaml
version: '3.8'

services:
  algosattva:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=sqlite:///db/openalgo.db
    volumes:
      - ./db:/app/db
    command: >
      sh -c "
        ./docker-setup-ui-prefs.sh &&
        python app.py
      "
    depends_on:
      - db

  db:
    image: sqlite:latest
    volumes:
      - ./db:/app/db
```

## Option 2: Manual Setup

### 1. Update Dockerfile
```dockerfile
# Add UI preferences migration to Dockerfile
COPY migrate_ui_preferences.py /app/migrate_ui_preferences.py

# Run migration during build
RUN python migrate_ui_preferences.py
```

### 2. Add to Application Startup
Add this to your `app.py` before the Flask app starts:

```python
# Ensure UI preferences are set up
try:
    from migrate_ui_preferences import migrate_ui_preferences
    migrate_ui_preferences()
    logger.info("UI preferences migration completed")
except Exception as e:
    logger.error(f"UI preferences migration failed: {e}")
```

## Option 3: Database Initialization Hook

### 1. Create Init Script
Create `scripts/init-ui-prefs.py`:

```python
#!/usr/bin/env python3
"""
Initialize UI preferences for Docker deployment
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def init_ui_preferences():
    """Initialize UI preferences in Docker environment"""
    
    print("Initializing UI preferences for Docker...")
    
    try:
        # Load environment variables
        from utils.env_check import load_and_check_env_variables
        load_and_check_env_variables()
        
        # Run migration
        from migrate_ui_preferences import migrate_ui_preferences
        migrate_ui_preferences()
        
        # Test functionality
        from database.settings_db import get_ui_preferences, set_ui_preferences
        
        prefs = get_ui_preferences()
        print(f"✅ UI preferences initialized: {len(prefs)} preferences")
        
        return True
        
    except Exception as e:
        print(f"❌ UI preferences initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_ui_preferences()
    sys.exit(0 if success else 1)
```

### 2. Update Docker Compose
```yaml
services:
  algosattva:
    build: .
    command: >
      sh -c "
        python scripts/init-ui-prefs.py &&
        python app.py
      "
```

## Database Considerations

### SQLite (Default)
- Ensure the `db/` directory is mounted as a volume
- Database file: `db/openalgo.db`

### PostgreSQL/MySQL
Update your `DATABASE_URL` environment variable:
```yaml
environment:
  - DATABASE_URL=postgresql://user:password@db:5432/algosattva
  # or
  - DATABASE_URL=mysql://user:password@db:3306/algosattva
```

## Verification

After deployment, verify UI preferences work:

1. **Check Application Logs:**
   ```bash
   docker logs algosattva | grep -i "ui preferences"
   ```

2. **Test API Endpoints:**
   ```bash
   curl -X POST http://localhost:5000/settings/ui_preferences \
     -H "Content-Type: application/json" \
     -d '{"dashboard_quick_access": false}'
   ```

3. **Check Database:**
   ```bash
   docker exec algosattva python -c "
   from database.settings_db import get_ui_preferences
   print(get_ui_preferences())
   "
   ```

## Troubleshooting

### Issue: Database not found
```bash
# Ensure database directory exists
docker exec algosattva mkdir -p /app/db

# Check permissions
docker exec algosattva ls -la /app/db/
```

### Issue: Migration fails
```bash
# Run migration manually
docker exec algosattva python migrate_ui_preferences.py
```

### Issue: UI preferences not persisting
```bash
# Check database file location
docker exec algosattva python -c "
import os
print('DATABASE_URL:', os.getenv('DATABASE_URL'))
"
```

## Production Considerations

1. **Database Backups:** Ensure your database volume is backed up
2. **Environment Variables:** Use Docker secrets for sensitive data
3. **Health Checks:** Add health check to verify UI preferences work
4. **Monitoring:** Monitor UI preference API endpoints

## Example Complete Docker Compose

```yaml
version: '3.8'

services:
  algosattva:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=sqlite:///db/openalgo.db
      - FLASK_ENV=production
    volumes:
      - ./db:/app/db
      - ./logs:/app/logs
    command: >
      sh -c "
        ./docker-setup-ui-prefs.sh &&
        python app.py
      "
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

volumes:
  db:
  logs:
```

This setup ensures UI preferences work correctly in your Docker environment!
