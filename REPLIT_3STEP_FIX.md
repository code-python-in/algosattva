# ✅ REPLIT .env FIX - ACTION GUIDE

**Status**: Fixed! ✅  
**What to do**: Follow these 3 simple steps

---

## 🚀 3-STEP FIX (5 minutes)

### Step 1️⃣: Get Your Replit URL

1. In Replit, click **"Run"** button
2. Wait for app to load
3. Look for the **"Open in new tab"** button (or check browser URL bar)
4. Copy the URL - it looks like: `https://your-project-name.username.replit.dev`
5. **Keep this URL - you'll need it next**

---

### Step 2️⃣: Add HOST_SERVER Secret

1. In Replit, click the **🔐 Secrets** icon (left sidebar)
2. Click **"New Secret"** button
3. Fill in:
   - **Key**: `HOST_SERVER`
   - **Value**: Paste your Replit URL from Step 1
4. Click **"Add Secret"**
5. **Done!** Now you have HOST_SERVER configured

---

### Step 3️⃣: Restart & Run

1. **Stop** the current process (press Ctrl+C)
2. Click **"Run"** again
3. **The script will now auto-generate .env file!** ✅

---

## ✨ What Happens Next

When you click Run:
- ✅ Script detects HOST_SERVER secret
- ✅ Auto-generates .env file with all your secrets
- ✅ App starts successfully
- ✅ Bracket orders work! 🎉

---

## 📋 Make Sure You Have These Secrets Too

In addition to HOST_SERVER, make sure these secrets are set:

```
BROKER_API_KEY = (your broker API key)
BROKER_API_SECRET = (your broker API secret)
REDIRECT_URL = (your broker callback URL)
APP_KEY = (generate with: python -c "import secrets; print(secrets.token_hex(32))")
API_KEY_PEPPER = (generate another: python -c "import secrets; print(secrets.token_hex(32))")
DATABASE_URL = sqlite:///db/openalgo.db
FLASK_ENV = production
```

---

## 🔑 How to Generate APP_KEY & API_KEY_PEPPER

If you haven't generated these yet:

1. In Replit, open the **Console** (bottom panel)
2. Type: `python`
3. Type: `import secrets`
4. Type: `print(secrets.token_hex(32))` and copy the output → use as APP_KEY
5. Type: `print(secrets.token_hex(32))` again and copy → use as API_KEY_PEPPER
6. Type: `exit()`

Then add these as secrets in Replit.

---

## 📁 If Manual .env Works Better

If you prefer to create .env manually:

1. Click **Files** (📁) in Replit
2. Right-click in root directory
3. Select **"New File"**
4. Name it: `.env`
5. Paste and fill this template:

```
BROKER_API_KEY='your_api_key'
BROKER_API_SECRET='your_api_secret'
REDIRECT_URL='your_redirect_url'
APP_KEY='your_generated_key'
API_KEY_PEPPER='your_generated_key_2'
HOST_SERVER='https://your-replit-url.replit.dev'
DATABASE_URL='sqlite:///db/openalgo.db'
LATENCY_DATABASE_URL='sqlite:///db/latency.db'
LOGS_DATABASE_URL='sqlite:///db/logs.db'
SANDBOX_DATABASE_URL='sqlite:///db/sandbox.db'
FLASK_HOST_IP='0.0.0.0'
FLASK_PORT='5000'
FLASK_DEBUG='False'
FLASK_ENV='production'
VALID_BROKERS='fivepaisa,aliceblue,angel,zerodha,upstox'
WEBSOCKET_HOST='0.0.0.0'
WEBSOCKET_PORT='8765'
NGROK_ALLOW='FALSE'
LOG_LEVEL='INFO'
```

6. Save the file
7. Click **Run**

---

## ✅ You're Done!

After following the 3 steps above:

- ✅ .env file will be auto-generated
- ✅ All secrets will be loaded
- ✅ App will start without errors
- ✅ Bracket orders will work
- ✅ TradingView webhook will work
- ✅ Everything is live! 🚀

---

## 🆘 Still Getting Error?

**Checklist:**

- [ ] Did you get your Replit URL correctly?
- [ ] Did you add HOST_SERVER with the correct URL?
- [ ] Did you restart the app (Ctrl+C then Run)?
- [ ] Are all other required secrets set?
- [ ] Is the URL format correct? (https://...replit.dev)

If still stuck:
1. Try manual .env creation (step above)
2. Check Replit console for error messages
3. Make sure all secrets are in 🔐 Secrets list

---

**That's it! Follow the 3 steps and you're good to go!** 🎉

