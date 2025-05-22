#!/usr/bin/env bash

echo "🔥 FINAL SHEBANG + PERMISSION RESET"

# Fix all .py files
find ~/ai_trading_bot -type f -name "*.py" -exec sed -i '1s|^#!.*|#!/usr/bin/env python3|' {} \;

# Fix all .sh files
find ~/ai_trading_bot -type f -name "*.sh" -exec sed -i '1s|^#!.*|#!/usr/bin/env bash|' {} \;

# Set +x on all .py and .sh files
find ~/ai_trading_bot -type f -name "*.py" -o -name "*.sh" -exec chmod +x {} \;

echo "✅ Final fix complete. Try this now:"
echo "   ~/ai_trading_bot/run_bot.sh"
