REM PowerShell Script to Push to GitHub
REM Just the basics, no fancy formatting

echo Configuring Git...
git config --global user.name "code-python-in"
echo Enter your GitHub email:
set /p email="Email: "
git config --global user.email "%email%"

echo.
echo Setting remote...
git remote set-url origin https://github.com/code-python-in/openalgo.git

echo.
echo Creating branch...
git checkout -b feature/bracket-orders

echo.
echo Staging all files...
git add .

echo.
echo Committing...
git commit -m "feat: Add bracket order implementation with REST API and TradingView webhook"

echo.
echo Pushing to GitHub...
git push -u origin feature/bracket-orders

echo.
echo DONE!
echo Your code is now at: https://github.com/code-python-in/openalgo/tree/feature/bracket-orders
echo.
echo Next steps on your server:
echo 1. git clone --branch feature/bracket-orders https://github.com/code-python-in/openalgo.git
echo 2. cd openalgo
echo 3. pip install -r requirements.txt
echo 4. systemctl restart openalgo
echo.

