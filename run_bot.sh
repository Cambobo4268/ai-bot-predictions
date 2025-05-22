#!/data/data/com.termux/files/usr/bin/bash
cd ~/ai_trading_bot

echo "[STEP 1] Fetching AI prediction from Drive..."
bash fetch_prediction.sh

echo "[STEP 2] Executing trade logic based on prediction..."
python3 trade_executor.py

echo "[COMPLETE] Termux bot cycle finished. Lightweight and synced."
