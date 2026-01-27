# Docker UI Preferences - Quick Start Guide

## 🚀 Fastest Setup (Recommended)

### 1. Update Your Dockerfile
Add these lines to your existing Dockerfile:

```dockerfile
# Copy UI preferences setup files
COPY docker-setup-ui-prefs.sh /app/docker-setup-ui-prefs.sh
COPY migrate_ui_preferences.py /app/migrate_ui_preferences.py
COPY scripts/ /app/scripts/

# Make setup script executable
RUN chmod +x /app/docker-setup-ui-prefs.sh

# Create scripts directory
RUN mkdir -p /app/scripts
```

### 2. Update Your Docker Compose
Modify your `docker-compose.yml` command:

```yaml
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
```

### 3. Deploy
```bash
docker-compose up --build
```

## 📋 What This Does

1. **Automatic Migration**: Runs UI preferences database migration on startup
2. **Verification**: Tests that UI preferences work correctly
3. **Error Handling**: Provides clear error messages if something goes wrong
4. **Cross-Platform**: Works on both Linux and Windows Docker

## 🔧 Alternative: Application Integration

If you prefer to integrate directly into your Flask app, add this to `app.py`:

```python
# Add this after database initialization
def ensure_ui_preferences():
    """Ensure UI preferences are set up"""
    try:
        from database.settings_db import get_ui_preferences
        prefs = get_ui_preferences()
        logger.info(f"UI preferences loaded: {len(prefs)} preferences")
    except Exception as e:
        logger.warning(f"UI preferences not set up, running migration: {e}")
        try:
            from migrate_ui_preferences import migrate_ui_preferences
            migrate_ui_preferences()
            logger.info("UI preferences migration completed")
        except Exception as migration_error:
            logger.error(f"UI preferences migration failed: {migration_error}")

# Call this after your database initialization
ensure_ui_preferences()
```

## ✅ Verification

After deployment, test the UI preferences:

1. **Visit your app**: Go to `http://localhost:5000/dashboard`
2. **Toggle Quick Access**: Turn the Quick Access toggle off/on
3. **Refresh page**: The setting should persist
4. **Navigate**: Go to `/platforms` and `/tradingview` - toggles should work there too

## 🐛 Troubleshooting

### UI preferences not working?
```bash
# Check logs
docker logs algosattva | grep -i "ui preferences"

# Run manual test
docker exec algosattva python scripts/init-ui-prefs.py --test
```

### Database issues?
```bash
# Check database file
docker exec algosattva ls -la /app/db/

# Run migration manually
docker exec algosattva python migrate_ui_preferences.py
```

## 📁 Files Created

- `docker-setup-ui-prefs.sh` - Linux/macOS setup script
- `docker-setup-ui-prefs.ps1` - Windows PowerShell setup script  
- `scripts/init-ui-prefs.py` - Python initialization script
- `DOCKER_UI_PREFERENCES.md` - Detailed documentation

## 🎯 Next Steps

1. Choose your setup method (Docker command vs app integration)
2. Update your Dockerfile and docker-compose.yml
3. Test the deployment
4. Verify UI preferences work in your browser

That's it! Your UI preferences will now work correctly in Docker! 🎉
