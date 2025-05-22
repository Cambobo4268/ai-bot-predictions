#!/usr/bin/env bash

echo "🔄 Pulling trade_predictions.json from Google Drive..."

mkdir -p ~/ai_trading_bot/data

FILE_ID=$(curl -s \
  "https://www.googleapis.com/drive/v3/files?q=name%3D'trade_predictions.json'&spaces=drive&fields=files(id%2Cname)&key=AIzaSyA70giD5w1bvB5-oH1GauHSlxp29pHd1M0" \
  | jq -r '.files[0].id')

if [ -z "$FILE_ID" ]; then
  echo "❌ Could not find trade_predictions.json"
  exit 1
fi

curl -L -o ~/ai_trading_bot/data/trade_predictions.json \
  "https://www.googleapis.com/drive/v3/files/$FILE_ID?alt=media&key=AIzaSyA70giD5w1bvB5-oH1GauHSlxp29pHd1M0"

echo "✅ File saved to ~/ai_trading_bot/data/trade_predictions.json"
