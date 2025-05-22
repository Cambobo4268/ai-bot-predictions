#!/usr/bin/env bash

MODEL_PATH="$HOME/ai_trading_bot/ai/trade_outcome_model.onnx"
HASH_PATH="$HOME/ai_trading_bot/ai/.model_hash"
BOT_PROCESS_NAME="orchestrator.py"

# Get current hash of model
new_hash=$(sha256sum "$MODEL_PATH" | awk '{print $1}')

# Load old hash (if exists)
old_hash=""
[ -f "$HASH_PATH" ] && old_hash=$(cat "$HASH_PATH")

# If hashes differ, restart bot
if [ "$new_hash" != "$old_hash" ]; then
    echo "$new_hash" > "$HASH_PATH"
    echo "[INFO] Model updated — restarting bot..."
    pkill -f "$BOT_PROCESS_NAME"
    nohup python3 ~/ai_trading_bot/orchestrator.py > ~/ai_trading_bot/logs/bot.log 2>&1 &
else
    echo "[INFO] No model changes — bot left running."
fi
