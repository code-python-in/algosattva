# 🔧 FIX: .env File Configuration for Replit

**Problem**: Getting "Error: .env file not found" on Replit  
**Solution**: Set the `HOST_SERVER` environment variable in Replit Secrets

---

## ✅ QUICK FIX (5 minutes)

### Step 1: Get Your Replit URL

1. Click **"Run"** to start your project
2. Wait for it to load
3. Click the **"Open in new tab"** button (or look at the browser tab)
4. Copy the URL (example: `https://openalgo.username.replit.dev`)

### Step 2: Add HOST_SERVER Secret in Replit

1. In Replit, click the **🔐 Secrets** icon on the left sidebar
2. Click **"New Secret"**
3. Fill in:
   - **Key**: `HOST_SERVER`
   - **Value**: `https://your-replit-url.replit.dev` (paste your URL)
4. Click **"Add Secret"**

### Step 3: Restart Your Project

1. Stop the current process (Ctrl+C)
2. Click **"Run"** again
3. The `.env` file will be auto-generated!

---

## 📋 ALL REQUIRED REPLIT SECRETS

Make sure these are set in Replit Secrets:

```
HOST_SERVER = https://your-project-name.username.replit.dev
BROKER_API_KEY = your_broker_api_key_here
BROKER_API_SECRET = your_broker_api_secret_here
REDIRECT_URL = your_broker_redirect_url
APP_KEY = (generate: python -c "import secrets; print(secrets.token_hex(32))")
API_KEY_PEPPER = (generate another: python -c "import secrets; print(secrets.token_hex(32))")
DATABASE_URL = sqlite:///db/openalgo.db
FLASK_ENV = production
```

---

## 🔑 HOW TO GENERATE APP_KEY & API_KEY_PEPPER

### In Replit Console:

```bash
python
```

Then in Python:

```python
import secrets
print(secrets.token_hex(32))  # Run twice to get two keys
```

Copy each output and use them for APP_KEY and API_KEY_PEPPER.

---

## 📁 ALTERNATIVE: Manual .env Creation

If you prefer to create `.env` manually in Replit:

1. Click **📁 Files**
2. Click the **"+"** button to create a new file
3. Name it: `.env`
4. Copy this template and fill in your values:

```bash
# Broker Configuration
BROKER_API_KEY='your_api_key'
BROKER_API_SECRET='your_api_secret'
REDIRECT_URL='your_redirect_url'

# Security
APP_KEY='your_app_key'
API_KEY_PEPPER='your_api_key_pepper'

# Host
HOST_SERVER='https://your-replit-url.replit.dev'

# Database
DATABASE_URL='sqlite:///db/openalgo.db'
LATENCY_DATABASE_URL='sqlite:///db/latency.db'
LOGS_DATABASE_URL='sqlite:///db/logs.db'
SANDBOX_DATABASE_URL='sqlite:///db/sandbox.db'

# Flask
FLASK_HOST_IP='0.0.0.0'
FLASK_PORT='5000'
FLASK_DEBUG='False'
FLASK_ENV='production'

# Brokers
VALID_BROKERS='fivepaisa,aliceblue,angel,zerodha,upstox'

# WebSocket
WEBSOCKET_HOST='0.0.0.0'
WEBSOCKET_PORT='8765'
WEBSOCKET_URL='wss://your-replit-url.replit.dev/ws'
```

5. Click **"Run"** to start the app

---

## 🚀 UPDATED start.sh

The `start.sh` script has been updated to:

1. ✅ Check for `HOST_SERVER` environment variable
2. ✅ If found, auto-generate `.env` from secrets
3. ✅ If not found, try to copy from `.sample.env`
4. ✅ Provide clear error messages with solutions

---

## ✨ WHAT HAPPENS NOW

1. **With HOST_SERVER set**: `.env` is auto-generated ✅
2. **Without HOST_SERVER**: Script copies `.sample.env` ✅
3. **Without either**: Clear error message with solutions ✅

---

## 📍 IF IT STILL FAILS

Check these in Replit:

1. **Verify Secrets are Set**:
   - Click 🔐 Secrets
   - Make sure `HOST_SERVER` appears in the list
   - Make sure all other secrets are there

2. **Check Your Replit URL**:
   - Run the project
   - Get the actual URL from browser tab or "Open in new tab" button
   - It should be: `https://[project-name].[username].replit.dev`

3. **Restart Everything**:
   - Stop the process
   - Close and reopen Replit
   - Click Run again

---

## 🎯 FINAL CHECKLIST

- [ ] I got my Replit URL
- [ ] I added HOST_SERVER secret with my Replit URL
- [ ] I have all other secrets configured
- [ ] I restarted the project
- [ ] The `.env` file was auto-generated
- [ ] The app is running without errors

---

**Once this is done, your bracket order system will work perfectly on Replit!** 🚀

