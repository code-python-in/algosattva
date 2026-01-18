# ⚡ QUICK COPY-PASTE SOLUTION

Just copy these lines and paste them into PowerShell. Do it one block at a time.

---

## BLOCK 1: Navigate to Project

```powershell
cd D:\Appa\Markets\Code\openalgo
```

---

## BLOCK 2: Configure Git (First Time Only)

```powershell
git config --global user.name "code-python-in"
git config --global user.email "your-email@gmail.com"
```

---

## BLOCK 3: Set Remote

```powershell
git remote set-url origin https://github.com/code-python-in/openalgo.git
```

---

## BLOCK 4: Create Branch

```powershell
git checkout -b feature/bracket-orders
```

---

## BLOCK 5: Stage Everything

```powershell
git add .
```

---

## BLOCK 6: Commit

```powershell
git commit -m "feat: Add bracket order implementation with REST API and TradingView webhook"
```

---

## BLOCK 7: Push to GitHub

```powershell
git push -u origin feature/bracket-orders
```

**This will prompt for GitHub credentials**

---

## ✅ DONE!

Your code is now on GitHub at:
```
https://github.com/code-python-in/openalgo/tree/feature/bracket-orders
```

---

## 📍 NEXT: Deploy to Server

```bash
git clone --branch feature/bracket-orders https://github.com/code-python-in/openalgo.git
cd openalgo
pip install -r requirements.txt
systemctl restart openalgo
```

---

**That's it! You're done!** 🎉

