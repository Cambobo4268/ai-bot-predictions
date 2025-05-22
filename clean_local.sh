#!/usr/bin/env bash
echo "[2025-05-08T06:13:49.483291] Cleaning local data folder..."
find $HOME/ai_trading_bot/data -type f ! -name 'trade_predictions.json' \
                                 ! -name 'model_tracker.json' \
                                 ! -name '*.csv' -print -delete
echo "[2025-05-08T06:13:49.483299] Cleanup complete."
