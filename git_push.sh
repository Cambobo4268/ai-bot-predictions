#!/data/data/com.termux/files/usr/bin/bash

cd ~/ai_trading_bot || exit 1

if [ ! -d .git ]; then
  echo "Not a git repository: ~/ai_trading_bot"
  exit 1
fi

git add .
git commit -m "Update \$(date '+%Y-%m-%d %H:%M:%S')"
