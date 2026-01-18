# 🚀 How to Push & Deploy Bracket Order Changes to Your GitHub

**Your GitHub**: https://github.com/code-python-in  
**Current Project**: OpenAlgo with Bracket Order Implementation

---

## 📍 Step 1: Create a New Repository on GitHub

### Option A: Fork the OpenAlgo Repository (Recommended)
1. Go to the original OpenAlgo repo on GitHub
2. Click the **Fork** button
3. This creates your own copy at: `https://github.com/code-python-in/openalgo`

### Option B: Create a New Repository
1. Go to https://github.com/new
2. Repository name: `openalgo`
3. Description: "OpenAlgo with Bracket Order Implementation"
4. Make it **Private** (recommended) or **Public**
5. Click **Create repository**

---

## 🔑 Step 2: Configure Git with Your GitHub Credentials

```bash
# Set your GitHub username
git config --global user.name "code-python-in"

# Set your GitHub email (use your GitHub account email)
git config --global user.email "your-email@github.com"

# Configure git to store credentials (Windows)
git config --global credential.helper wincred
```

Or create a Personal Access Token (better security):

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Select scopes: `repo` (full control of private repositories)
4. Copy the token (you'll use this as password)

---

## 📤 Step 3: Push Your Changes to GitHub

Run these commands in PowerShell from your project directory:

```powershell
# Navigate to your project
cd D:\Appa\Markets\Code\openalgo

# Check remote URL
git remote -v

# If you don't have a remote, add your GitHub repository
# Replace 'code-python-in' and 'openalgo' with your actual values
git remote add origin https://github.com/code-python-in/openalgo.git

# Or if remote exists, update it
git remote set-url origin https://github.com/code-python-in/openalgo.git

# Create a feature branch for bracket orders
git checkout -b feature/bracket-orders

# Stage all changes
git add .

# Commit with a descriptive message
git commit -m "feat: Add complete bracket order implementation

Features:
- Entry order placement with LIMIT pricing
- GTT OCO (One Cancels Other) order scheduling
- REST API endpoint at /api/v1/placebracketorder/
- TradingView webhook at /tradingview/webhook/bracket
- Comprehensive price validation (SL < Entry < Target)
- WebSocket real-time event emission
- Telegram notifications
- Database logging to order_logs table
- Rate limiting (2 per second, configurable)
- Complete error handling

Files Added:
- services/bracket_order_service.py (Core service)
- restx_api/bracket_order.py (REST API)
- BRACKET_ORDER_*.md (8 documentation files)

Files Modified:
- blueprints/tv_json.py (Added webhook endpoint)
- restx_api/__init__.py (Added namespace registration)"

# Push to GitHub
git push -u origin feature/bracket-orders
```

---

## ✅ Step 3b: Verify on GitHub

1. Go to https://github.com/code-python-in/openalgo
2. You should see a notification: **"Compare & pull request"**
3. Optionally create a Pull Request to your main branch
4. Or just keep it on the feature branch

---

## 🖥️ Step 4: Deploy to Your Server

### Option 1: Deploy from GitHub (Recommended)

**On your production server:**

```bash
# Clone your repository
git clone https://github.com/code-python-in/openalgo.git
cd openalgo

# Or if already cloned, update it
git pull origin feature/bracket-orders

# Switch to the feature branch
git checkout feature/bracket-orders

# Install/update dependencies
pip install -r requirements.txt

# Create/update .env file
cp .env.example .env
# Edit .env and add:
# BRACKET_ORDER_RATE_LIMIT=2 per second
# BRACKET_ORDER_DELAY=0.5

# Restart the Flask application
# (How you do this depends on your setup - see below)
```

### Option 2: Manual Deployment

Copy the files directly from your local machine to the server:

```powershell
# From your local machine, copy files to server
# If using SSH/SCP:
scp -r D:\Appa\Markets\Code\openalgo\services\bracket_order_service.py user@server:/path/to/openalgo/services/
scp -r D:\Appa\Markets\Code\openalgo\restx_api\bracket_order.py user@server:/path/to/openalgo/restx_api/

# Then SSH into server and restart Flask
ssh user@server
cd /path/to/openalgo
sudo systemctl restart openalgo  # Or your Flask service name
```

---

## 🔄 Step 5: Restart Your Flask Application

### If using systemd (Linux):
```bash
sudo systemctl restart openalgo
sudo systemctl status openalgo
```

### If using Docker:
```bash
docker-compose down
docker-compose up -d
docker-compose logs -f
```

### If running directly:
```bash
# Stop the current process (Ctrl+C)
# Then restart:
python app.py
# Or if using gunicorn:
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### If using Windows with Flask development server:
```powershell
# Stop current process
# Ctrl+C

# Restart
python app.py
```

---

## ✨ Step 6: Verify Deployment

Test your bracket order endpoints:

```bash
# Test REST API
curl -X POST http://your-server:5000/api/v1/placebracketorder/ \
  -H "Content-Type: application/json" \
  -d '{
    "apikey": "YOUR_API_KEY",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500,
    "sl_price": 1480,
    "target_price": 1550
  }'

# Test TradingView Webhook
curl -X POST http://your-server:5000/tradingview/webhook/bracket \
  -H "Content-Type: application/json" \
  -d '{
    "apikey": "YOUR_API_KEY",
    "symbol": "INFY",
    "exchange": "NSE",
    "product": "MIS",
    "action": "BUY",
    "quantity": 1,
    "entry_price": 1500,
    "sl_price": 1480,
    "target_price": 1550
  }'
```

Expected response:
```json
{
    "status": "success",
    "message": "Bracket order initiated - entry order placed, GTT orders pending",
    "entry_order_id": "12345",
    ...
}
```

---

## 📊 Step 7: Monitor in Production

```bash
# Check database logs
sqlite3 db/openalgo.db "SELECT * FROM order_logs WHERE api_type='placebracketorder' ORDER BY created_at DESC LIMIT 5;"

# Or with PostgreSQL
psql -c "SELECT * FROM order_logs WHERE api_type='placebracketorder' ORDER BY created_at DESC LIMIT 5;"

# Check application logs
tail -f log/openalgo.log
```

---

## 🔑 Important: Protect Your Credentials

### Never commit these files:
```
.env                    (contains API keys, secrets)
keys/                   (broker credentials)
*.log                   (logs with sensitive data)
__pycache__/           (compiled Python files)
*.pyc                   (compiled Python files)
```

### Make sure .gitignore includes:
```
.env
.env.local
keys/
*.log
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.venv/
venv/
```

If you accidentally committed sensitive data, revoke it immediately and regenerate API keys.

---

## 🚨 Troubleshooting

### Issue: Permission denied (git@github.com)
**Solution**: Use HTTPS instead of SSH, or set up SSH keys
```bash
git remote set-url origin https://github.com/code-python-in/openalgo.git
```

### Issue: Can't push to GitHub
**Solution**: Make sure you're on a branch first
```bash
git branch  # Check current branch
git checkout feature/bracket-orders
git push -u origin feature/bracket-orders
```

### Issue: ModuleNotFoundError after deployment
**Solution**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Port already in use
**Solution**: Kill the old process or use a different port
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port
export FLASK_PORT=5001
python app.py
```

---

## 📋 Quick Checklist

Before deploying to production:

- [ ] Push all code to GitHub
- [ ] Code is on `feature/bracket-orders` branch
- [ ] `.env` file configured (BRACKET_ORDER_RATE_LIMIT, BRACKET_ORDER_DELAY)
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Tested locally with cURL
- [ ] No sensitive data in git commits
- [ ] Database initialized
- [ ] Flask application restarted
- [ ] Endpoint tested: `/api/v1/placebracketorder/`
- [ ] Webhook tested: `/tradingview/webhook/bracket`
- [ ] Database logs checked
- [ ] WebSocket events verified
- [ ] Telegram notifications configured (optional)

---

## 🎯 Summary: Your Action Items

1. **Push to GitHub**:
   ```bash
   git checkout -b feature/bracket-orders
   git add .
   git commit -m "feat: Add bracket order implementation"
   git push -u origin feature/bracket-orders
   ```

2. **Deploy to Server**:
   - Clone/pull from `https://github.com/code-python-in/openalgo.git`
   - Switch to `feature/bracket-orders` branch
   - Install dependencies
   - Restart Flask application

3. **Verify**:
   - Test API endpoints
   - Check database logs
   - Monitor WebSocket events

---

## 📞 Need Help?

If you get stuck:
1. Check `BRACKET_ORDER_README.md` for quick reference
2. Review `BRACKET_ORDER_GUIDE.md` for complete documentation
3. Check `BRACKET_ORDER_DEPLOYMENT_SUMMARY.md` for deployment steps
4. Review error logs: `log/openalgo.log`
5. Check database logs: `db/openalgo.db`

---

**GitHub Account**: https://github.com/code-python-in  
**Next**: Create the repo and push your code!

