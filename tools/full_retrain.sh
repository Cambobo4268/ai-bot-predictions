#!/usr/bin/env bash

echo "📤 Syncing latest cleaned dataset to Google Drive..."
rclone copy ~/ai_trading_bot/data/cleaned_dataset.csv gdrive:/ai_trading_bot/data/ --update

echo "✅ Dataset pushed successfully."

echo ""
echo "🔗 Click this link to open retrain notebook in Colab:"
echo "https://colab.research.google.com/drive/1AJKuJ8NJXbFozW17YKR-7hlC9o4WN4jfj"
echo ""
echo "👉 In Colab: just click 'Runtime > Run all' to retrain and sync model."
