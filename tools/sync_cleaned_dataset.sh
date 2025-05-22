#!/usr/bin/env bash

echo "🔄 Pulling cleaned dataset from Google Drive..."
rclone copy gdrive:/ai_trading_bot/data/cleaned_dataset.csv ~/ai_trading_bot/data/ --update

echo "⏳ Waiting 5s before pushing..."
sleep 5

echo "📤 Pushing updated cleaned dataset..."
rclone copy ~/ai_trading_bot/data/cleaned_dataset.csv gdrive:/ai_trading_bot/data/ && echo "✅ Sync complete."
