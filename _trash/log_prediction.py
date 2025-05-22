#!/usr/bin/env python3
import json
from datetime import datetime
import os

PRED_PATH = os.path.expanduser("~/ai_trading_bot/data/trade_predictions.json")
LOG_PATH = os.path.expanduser("~/ai_trading_bot/logs/prediction_history.log")

with open(PRED_PATH, "r") as f:
    predictions = json.load(f)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_PATH, "a") as log:
    for p in predictions:
        if p.get("confidence", 0) >= 0.75:
            log.write(f"[{timestamp}] {p['decision']} {p['symbol']} (Confidence: {p['confidence']})\n")
