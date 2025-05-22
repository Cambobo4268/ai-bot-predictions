#!/data/data/com.termux/files/usr/bin/bash

while true; do
  echo "=== Executing at $(date) ==="
  bash ~/ai_trading_bot/fetch_prediction.sh
  bash ~/ai_trading_bot/execute_trades.sh
  echo "=== Sleeping 30s ==="
  sleep 30
done
