#!/data/data/com.termux/files/usr/bin/bash

echo "=== Checking AI Bot Files in Termux ==="
FILES=(
  "predict.py"
  "fetch_prediction.sh"
  "trade_executor.py"
  "trade_input.json"
  "predictions.json"
  ".env"
  "telegram_bot.py"
)

cd ~/ai_trading_bot || exit 1

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "[OK] $file exists"
  else
    echo "[MISSING] $file not found"
  fi
done
