# 🚀 Quick Start: Push to GitHub & Deploy

**Your GitHub**: https://github.com/code-python-in

## ⚡ 3-Minute Quick Start

### Step 1: Configure & Push to GitHub (PowerShell)

```powershell
# Navigate to project
cd D:\Appa\Markets\Code\openalgo

# Configure git (one time)
git config --global user.name "code-python-in"
git config --global user.email "your-email@gmail.com"

# Set remote to your GitHub
git remote set-url origin https://github.com/code-python-in/openalgo.git

# Create branch, add files, commit and push
git checkout -b feature/bracket-orders
git add .
git commit -m "feat: Add bracket order implementation"
git push -u origin feature/bracket-orders
```

That's it! Your code is now on GitHub.

**Note**: You may be prompted for GitHub credentials. Use your personal access token or password.

---

## 📍 Manual Alternative (If Script Doesn't Work)

```powershell
cd D:\Appa\Markets\Code\openalgo

# Configure Git (one time)
git config --global user.name "code-python-in"
git config --global user.email "your-email@gmail.com"

# Set remote
git remote add origin https://github.com/code-python-in/openalgo.git

# Create branch and push
git checkout -b feature/bracket-orders
git add .
git commit -m "feat: Add bracket order implementation"
git push -u origin feature/bracket-orders
```

---

## ✅ Verify on GitHub

1. Go to: https://github.com/code-python-in/openalgo
2. You should see your code there
3. You'll see a notification about the new branch

---

## 🖥️ Deploy to Your Server

### Option 1: On Linux Server

```bash
# SSH into your server
ssh user@your-server

# Clone your repository
git clone https://github.com/code-python-in/openalgo.git
cd openalgo

# Switch to feature branch
git checkout feature/bracket-orders

# Install dependencies
pip install -r requirements.txt

# Configure .env
cat >> .env << 'EOF'
BRACKET_ORDER_RATE_LIMIT=2 per second
BRACKET_ORDER_DELAY=0.5
EOF

# Restart Flask
sudo systemctl restart openalgo
```

### Option 2: Use Deployment Script (Automated)

```bash
cd /path/to/openalgo
bash deploy-bracket-orders.sh feature/bracket-orders production
```

### Option 3: Docker Deployment

```bash
# Pull latest code
git pull origin feature/bracket-orders

# Rebuild and restart
docker-compose down
docker-compose up -d
```

---

## 🧪 Test Your Deployment

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
```

**Expected Response:**
```json
{
    "status": "success",
    "message": "Bracket order initiated - entry order placed, GTT orders pending",
    "entry_order_id": "12345",
    "symbol": "INFY",
    "entry_price": 1500.0,
    "sl_price": 1480.0,
    "target_price": 1550.0,
    "quantity": 1,
    "action": "BUY"
}
```

---

## 📊 Check Logs

```bash
# Check database
sqlite3 db/openalgo.db "SELECT * FROM order_logs WHERE api_type='placebracketorder' LIMIT 5;"

# Check application logs
tail -f log/openalgo.log

# Check if Flask is running
curl http://localhost:5000/
```

---

## 🎯 What's Deployed

✅ **Bracket Order System**
- REST API: `/api/v1/placebracketorder/`
- Webhook: `/tradingview/webhook/bracket`
- Entry order placement
- GTT SL/Target orders
- Real-time notifications

✅ **Features**
- Price validation
- Error handling
- Database logging
- WebSocket events
- Telegram alerts

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `BRACKET_ORDER_README.md` | Getting started |
| `BRACKET_ORDER_QUICK_REFERENCE.md` | One-page reference |
| `BRACKET_ORDER_GUIDE.md` | Complete guide |
| `BRACKET_ORDER_EXAMPLES.py` | Code examples |
| `BRACKET_ORDER_DEPLOYMENT_SUMMARY.md` | Deployment guide |
| `GITHUB_PUSH_AND_DEPLOY_GUIDE.md` | This guide |

---

## ❌ Troubleshooting

### "Permission denied" when pushing
```powershell
# Use HTTPS instead
git remote set-url origin https://github.com/code-python-in/openalgo.git
```

### "fatal: could not read Username"
```powershell
# Use Personal Access Token
# Go to: https://github.com/settings/tokens
# Generate a token
# When asked for password, use the token instead
```

### "ModuleNotFoundError" after deployment
```bash
pip install -r requirements.txt
```

### Port 5000 already in use
```bash
# Find and kill the process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or use different port
export FLASK_PORT=5001
```

---

## 🎉 Summary

You now have:

1. ✅ Code pushed to GitHub
2. ✅ Branch created: `feature/bracket-orders`
3. ✅ Ready to deploy to any server
4. ✅ All documentation included
5. ✅ Automated deployment script ready

**Next: Deploy to your server and test!**

---

**GitHub Repo**: https://github.com/code-python-in/openalgo  
**Branch**: `feature/bracket-orders`  
**Status**: Ready for deployment ✅

