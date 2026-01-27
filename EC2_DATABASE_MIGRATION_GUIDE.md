# EC2 Database Migration & Deployment Guide

## 🎯 Overview
This guide explains how database schema changes are automatically handled when you push to main branch and deploy to EC2.

## 🔄 Automatic Deployment Process

### What Happens When You Push to Main
1. **GitHub Actions Trigger**: Your `.github/workflows/deploy.yml` runs automatically
2. **Code Pull**: Latest changes are pulled on EC2
3. **Database Backup**: Automatic backup created before any changes
4. **Database Migration**: Schema changes applied automatically
5. **Docker Rebuild**: Container rebuilt with new code
6. **Service Restart**: Application restarts with updated schema
7. **Verification**: Deployment is verified

## 📦 Database Migration Strategy

### 1. Automatic Migrations
The `migrate_production_db.py` script handles:
- ✅ UI preferences table/column creation
- ✅ Schema verification
- ✅ Data integrity checks
- ✅ Error handling and logging

### 2. Backup Strategy
- **Before Migration**: Automatic backup created
- **Location**: `/opt/openalgo/backups/`
- **Retention**: Last 10 backups kept
- **Format**: `openalgo_backup_YYYYMMDD_HHMMSS.db`

### 3. Rollback Capability
If something goes wrong:
```bash
# SSH into EC2
ssh -i your-key.pem user@your-ec2-ip

# Rollback to latest backup
cd /opt/openalgo
./scripts/rollback-db.sh

# Or rollback to specific backup
./scripts/rollback-db.sh 20261225_143022
```

## 🛠️ Manual Database Operations

### Check Migration Status
```bash
# SSH into EC2 and run
docker compose run --rm algosattva python migrate_production_db.py
```

### Manual Backup
```bash
./scripts/backup-db.sh
```

### View Available Backups
```bash
ls -la /opt/openalgo/backups/
```

### Manual Rollback
```bash
# Rollback to latest
./scripts/rollback-db.sh

# Rollback to specific timestamp
./scripts/rollback-db.sh 20261225_143022
```

## 🔍 Migration Script Details

### What `migrate_production_db.py` Does
1. **Environment Setup**: Loads environment variables
2. **UI Preferences Migration**: Runs UI preference migrations
3. **Schema Verification**: Checks all required tables/columns exist
4. **Functionality Testing**: Verifies UI preferences work
5. **Integrity Checks**: Ensures database consistency

### Error Handling
- ✅ Graceful failure handling
- ✅ Detailed logging
- ✅ Rollback on failure
- ✅ Verification steps

## 🚨 Troubleshooting

### Migration Fails
1. **Check Logs**: `docker compose logs algosattva`
2. **Manual Rollback**: `./scripts/rollback-db.sh`
3. **Fix Issue**: Update migration script
4. **Retry**: Push fix or run manually

### Database Issues
1. **Check Backup**: Verify backup was created
2. **Verify Schema**: Check required columns exist
3. **Test Functionality**: Verify UI preferences work

### Deployment Issues
1. **Check GitHub Actions**: Review workflow logs
2. **Verify Docker**: Ensure containers build correctly
3. **Check Network**: Ensure EC2 can access Docker Hub

## 📋 Required EC2 Setup

### Directory Structure
```
/opt/openalgo/
├── db/
│   └── openalgo.db
├── backups/
│   └── openalgo_backup_*.db
├── scripts/
│   ├── backup-db.sh
│   └── rollback-db.sh
├── docker-compose.yml
└── migrate_production_db.py
```

### Permissions
```bash
# Make scripts executable
chmod +x scripts/backup-db.sh
chmod +x scripts/rollback-db.sh
chmod +x migrate_production_db.py
```

### Docker Compose Setup
Ensure your `docker-compose.yml` has:
```yaml
volumes:
  - ./db:/app/db
  - ./backups:/app/backups
```

## 🔄 Future Database Changes

### Adding New Migrations
1. Create migration script in project root
2. Add to `migrate_production_db.py`
3. Test locally
4. Push to main (auto-deploys)

### Schema Changes
- ✅ Always add migration logic
- ✅ Test with existing data
- ✅ Include rollback plan
- ✅ Update verification checks

## 🎉 Benefits

### Automatic
- ✅ No manual intervention required
- ✅ Safe deployments with backups
- ✅ Consistent environment
- ✅ Error handling built-in

### Safe
- ✅ Backups before changes
- ✅ Rollback capability
- ✅ Verification steps
- ✅ Detailed logging

### Reliable
- ✅ Tested migration process
- ✅ Error recovery
- ✅ Deployment verification
- ✅ Production-ready

Your database schema changes are now automatically and safely applied to EC2! 🚀
