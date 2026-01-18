# 🚀 MANUAL PUSH TO GITHUB - Step by Step

**If scripts aren't working, follow these commands manually**

---

## Step 1: Open PowerShell

1. Right-click on the Windows Start menu
2. Click "Windows PowerShell" or "Terminal"
3. Navigate to your project:
```powershell
cd D:\Appa\Markets\Code\openalgo
```

---

## Step 2: Configure Git (One Time)

```powershell
git config --global user.name "code-python-in"
```

Then enter your GitHub email:
```powershell
git config --global user.email "your-email@gmail.com"
```

---

## Step 3: Set Remote URL

```powershell
git remote set-url origin https://github.com/code-python-in/algosattva.git
```

If that fails, try:
```powershell
git remote add origin https://github.com/code-python-in/algosattva.git
```

---

## Step 4: Create Feature Branch

```powershell
git checkout -b feature/bracket-orders
```

---

## Step 5: Stage All Changes

```powershell
git add .
```

To verify what will be committed:
```powershell
git status
```

---

## Step 6: Commit

```powershell
git commit -m "feat: Add bracket order implementation with REST API and TradingView webhook"
```

---

## Step 7: Push to GitHub

```powershell
git push -u origin feature/bracket-orders
```

**You may be prompted for GitHub credentials**
- Username: `code-python-in`
- Password: Use your GitHub personal access token or password

---

## ✅ Success!

Your code is now at:
```
https://github.com/code-python-in/algosattva/tree/feature/bracket-orders
```

---

## Next: Deploy to Your Server

Once code is on GitHub, on your server run:

```bash
# Clone the repository
git clone --branch feature/bracket-orders https://github.com/code-python-in/algosattva.git /path/to/openalgo

# Or if already cloned
cd /path/to/openalgo
git fetch origin
git checkout feature/bracket-orders
git pull origin feature/bracket-orders

# Install dependencies
pip install -r requirements.txt

# Configure .env
echo "BRACKET_ORDER_RATE_LIMIT=2 per second" >> .env
echo "BRACKET_ORDER_DELAY=0.5" >> .env

# Restart Flask
sudo systemctl restart openalgo
```

---

## 🧪 Test

```bash
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

---

## ❌ If Something Goes Wrong

### Error: "Not a git repository"
Make sure you're in the correct folder:
```powershell
cd D:\Appa\Markets\Code\openalgo
```

### Error: "Permission denied"
You need to authenticate. Try:
```powershell
git config --global credential.helper wincred
```

Then try pushing again - it will prompt for credentials.

### Error: "Repository not found"
Make sure your GitHub repository exists at:
```
https://github.com/code-python-in/algosattva
```

Create it if it doesn't exist!

### Error: "Branch already exists"
You can safely ignore this and continue to `git add .`

---

## ✅ All Done!

Your bracket order implementation is now on GitHub and ready to deploy!

**Next**: Go to your server and follow the "Deploy to Your Server" section above.

---

**Remember**: 
- Your GitHub: https://github.com/code-python-in
- Your Repo: openalgo
- Your Branch: feature/bracket-orders

