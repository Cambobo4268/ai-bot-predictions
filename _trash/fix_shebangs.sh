#!/usr/bin/env bash

echo "🔧 Fixing all shebangs to use /usr/bin/env..."

# Fix Python files
find ~/ai_trading_bot -type f -name "*.py" -exec sed -i '1s|^.*$|#!/usr/bin/env python3|' {} \;

# Fix Shell scripts
find ~/ai_trading_bot -type f -name "*.sh" -exec sed -i '1s|^.*$|#!/usr/bin/env bash|' {} \;

# Make them all executable
chmod +x ~/ai_trading_bot/**/*.py ~/ai_trading_bot/**/*.sh ~/ai_trading_bot/*.py ~/ai_trading_bot/*.sh

echo "✅ Done! You can now run: ~/ai_trading_bot/run_bot.sh"
