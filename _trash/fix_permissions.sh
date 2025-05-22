#!/usr/bin/env bash

echo "🔧 Fixing shebangs..."
find ~/ai_trading_bot -type f -name "*.py" -exec sed -i '1s|^.*$|#!/data/data/com.termux/files/usr/bin/python3|' {} \;
find ~/ai_trading_bot -type f -name "*.sh" -exec sed -i '1s|^.*$|#!/data/data/com.termux/files/usr/bin/bash|' {} \;

echo "🔐 Making scripts executable..."
find ~/ai_trading_bot -type f -name "*.py" -o -name "*.sh" -exec chmod +x {} \;

echo "✅ All scripts fixed."
echo "👉 You can now run:"
echo "   python3 ~/ai_trading_bot/tools/telegram_listener.py"
