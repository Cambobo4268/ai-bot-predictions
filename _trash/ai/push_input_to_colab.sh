#!/usr/bin/env bash

# Prepare input JSON for the model
cat <<EOL > ~/ai_trading_bot/ai/input_data.json
{
  "rsi": 45.7,
  "volatility": 0.03,
  "volume": 1020
}
EOL

# Upload to Drive using gdown reverse (simulate upload via web)
rclone copy ~/ai_trading_bot/ai/input_data.json remote:MyDrive/trading_bot/
