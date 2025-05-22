#!/data/data/com.termux/files/usr/bin/bash

cd ~/ai_trading_bot || exit 1

# Check if it's a Git repo
if [ ! -d .git ]; then
  echo "Not a git repository: ~/ai_trading_bot"
  exit 1
fi

# Pull first to avoid conflicts
git pull --rebase origin main

# Add changes and commit if any
git diff --cached --quiet || git commit -m "Auto-update: \$(date '+%Y-%m-%d %H:%M:%S')"
git add .

# Push updates
git push origin main
