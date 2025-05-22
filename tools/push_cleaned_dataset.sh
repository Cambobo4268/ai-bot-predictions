#!/usr/bin/env bash

DATASET=~/ai_trading_bot/data/cleaned_dataset.csv
DEST="gdrive:/ai_trading_bot/data"

echo "⏳ Waiting 5s to ensure file is stable..."
sleep 5

if [ -f "$DATASET" ]; then
    echo "📤 Uploading cleaned dataset to Google Drive..."
    rclone copy "$DATASET" "$DEST" && echo "✅ Upload complete."
else
    echo "❌ Dataset not found at $DATASET"
fi
