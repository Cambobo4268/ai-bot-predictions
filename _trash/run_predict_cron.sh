#!/usr/bin/env bash
echo ">>> Running predict at \$(date)" >> ~/ai_trading_bot/predict/cron.log
python3 ~/ai_trading_bot/predict/predict.py >> ~/ai_trading_bot/predict/cron.log 2>&1
