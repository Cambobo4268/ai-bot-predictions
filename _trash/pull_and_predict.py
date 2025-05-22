#!/usr/bin/env python3

import os
import subprocess
import json

print("🔄 Pulling latest ONNX model from Google Drive...")
model_cmd = [
    "gdown",
    "--id", "1-29cy-1eV1wo9oCbpxWrt8uHIpTjMYGE",
    "-O", os.path.expanduser("~/ai_trading_bot/models/trade_outcome_model.onnx")
]
subprocess.run(model_cmd, check=True)

print("⚙️ Running predict.py...")
predict_result = subprocess.run(["python3", os.path.expanduser("~/ai_trading_bot/predict/predict.py")])
if predict_result.returncode != 0:
    print("❌ Prediction script failed.")
