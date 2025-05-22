#!/usr/bin/env bash

echo "🧹 Full cleanup: rewriting shebangs + permissions..."

# Rewrite all .py and .sh shebangs to use /usr/bin/env
find ~/ai_trading_bot -type f -name "*.py" -exec sed -i '1s|^.*$|#!/usr/bin/env python3|' {} \;
find ~/ai_trading_bot -type f -name "*.sh" -exec sed -i '1s|^.*$|#!/usr/bin/env bash|' {} \;

# Reset permissions
find ~/ai_trading_bot -type f -name "*.py" -o -name "*.sh" -exec chmod +x {} \;

echo "✅ Cleaned. Now run: ~/ai_trading_bot/run_bot.sh"
