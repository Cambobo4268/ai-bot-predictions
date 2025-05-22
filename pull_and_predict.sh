#!/usr/bin/env bash

echo "🔄 Pulling latest ONNX model from Google Drive..."
gdown 1-29cy-1eV1wo9oCbpxWrt8uHIpTjMYGE -O ~/ai_trading_bot/models/trade_outcome_model.onnx

echo "⚙️ Running predict.py..."
python3 ~/ai_trading_bot/predict/predict.py
