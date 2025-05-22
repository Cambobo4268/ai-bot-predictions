#!/usr/bin/env python3

import json
import os

with open(os.path.expanduser("~/ai_trading_bot/data/trade_predictions.json"), "r") as f:
    predictions = json.load(f)

print("✅ High-confidence predictions:")
for trade in predictions:
    action = trade.get("decision")
    symbol = trade.get("symbol")
    confidence = trade.get("confidence")
    if confidence >= 0.8:
        print(f"{action} {symbol} (Confidence: {confidence})")
        print(f"[SIMULATED] {action} {symbol} for approx $20")
