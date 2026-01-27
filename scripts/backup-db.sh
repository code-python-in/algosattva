#!/bin/bash
# Database backup script for EC2 deployment
# Run this before migrations to create a backup

set -e

BACKUP_DIR="/opt/openalgo/backups"
DB_FILE="/opt/openalgo/db/openalgo.db"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/openalgo_backup_$TIMESTAMP.db"

echo "=== Database Backup Script ==="

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if database file exists
if [ ! -f "$DB_FILE" ]; then
    echo "⚠️  Database file not found at $DB_FILE"
    echo "Creating empty database backup placeholder..."
    touch "$BACKUP_FILE"
else
    echo "📦 Creating database backup..."
    cp "$DB_FILE" "$BACKUP_FILE"
    echo "✅ Backup created: $BACKUP_FILE"
fi

# Keep only last 10 backups
echo "🧹 Cleaning up old backups (keeping last 10)..."
cd "$BACKUP_DIR"
ls -t openalgo_backup_*.db | tail -n +11 | xargs -r rm

echo "🎉 Backup completed successfully!"
echo "📍 Backup location: $BACKUP_FILE"
