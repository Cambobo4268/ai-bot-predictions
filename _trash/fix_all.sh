#!/usr/bin/env bash

echo "🔧 Fixing shebangs to use /usr/bin/env..."

# Rewrite all .py and .sh headers
find ~/ai_trading_bot -type f -name "*.py" -exec sed -i '1s|^.*$|#!/usr/bin/env python3|' {} \;
find ~/ai_trading_bot -type f -name "*.sh" -exec sed -i '1s|^.*$|#!/usr/bin/env bash|' {} \;

echo "🔐 Making scripts executable..."
find ~/ai_trading_bot -type f -name "*.py" -o -name "*.sh" -exec chmod +x {} \;

echo "📦 Installing Pillow from Termux repo (if not already installed)..."
pkg install -y python-pillow

echo "✅ All fixed. You can now run: ~/ai_trading_bot/run_bot.sh"
