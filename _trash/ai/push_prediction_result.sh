#!/usr/bin/env bash
rclone copy $HOME/ai_trading_bot/ai/prediction_result.json gdrive:trading_bot/ --update --quiet
