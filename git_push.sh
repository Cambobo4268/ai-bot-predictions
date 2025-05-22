#!/data/data/com.termux/files/usr/bin/bash
cd ~/ai_trading_bot || exit 1

# Check if it's a git repo
if [ ! -d .git ]; then
  echo "Not a git repository: ~/ai_trading_bot"
  exit 1
fi

# Add changes and commit if there are any
git add .
git diff --cached --quiet || git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')"

# Push to main
git push origin main
