#!/usr/bin/env python3
sys.path.append("/data/data/com.termux/files/home/ai_trading_bot/ai")

from onnx_predictor import predict_outcome

# Example input: RSI, volatility, volume
rsi = 68.2
volatility = 0.05
volume = 850

decision, confidence = list(predict_outcome(rsi, volatility, volume).items())[0]
print(f"Predicted Outcome: {decision} | Confidence: {confidence:.2f}")
