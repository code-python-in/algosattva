#!/bin/bash
# Database rollback script for EC2 deployment
# Run this to rollback to a previous database backup

set -e

BACKUP_DIR="/opt/openalgo/backups"
DB_FILE="/opt/openalgo/db/openalgo.db"

echo "=== Database Rollback Script ==="

# List available backups
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Backup directory not found: $BACKUP_DIR"
    exit 1
fi

echo "📋 Available backups:"
ls -la "$BACKUP_DIR"/openalgo_backup_*.db 2>/dev/null || {
    echo "❌ No backups found"
    exit 1
}

# If no argument provided, show latest backup
if [ $# -eq 0 ]; then
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/openalgo_backup_*.db | head -1)
    echo "🔄 Rolling back to latest backup: $(basename "$LATEST_BACKUP")"
else
    BACKUP_FILE="$BACKUP_DIR/openalgo_backup_$1.db"
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "❌ Backup file not found: $BACKUP_FILE"
        exit 1
    fi
    LATEST_BACKUP="$BACKUP_FILE"
    echo "🔄 Rolling back to specified backup: $(basename "$LATEST_BACKUP")"
fi

# Create backup of current database before rollback
echo "📦 Creating backup of current database..."
CURRENT_BACKUP="$BACKUP_DIR/openalgo_before_rollback_$(date +%Y%m%d_%H%M%S).db"
if [ -f "$DB_FILE" ]; then
    cp "$DB_FILE" "$CURRENT_BACKUP"
    echo "✅ Current database backed up: $(basename "$CURRENT_BACKUP")"
fi

# Restore the backup
echo "🔄 Restoring database from backup..."
cp "$LATEST_BACKUP" "$DB_FILE"
echo "✅ Database restored successfully!"

# Restart the application
echo "🔄 Restarting application..."
cd /opt/openalgo
docker compose restart algosattva

echo "🎉 Rollback completed successfully!"
echo "📍 Database restored from: $(basename "$LATEST_BACKUP")"
