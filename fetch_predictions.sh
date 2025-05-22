#!/usr/bin/env bash
rclone copy gdrive:trading_bot/reviewed_dataset_with_predictions.csv ~/ai_trading_bot/data/ --update --quiet
