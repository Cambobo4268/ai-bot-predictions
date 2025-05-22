#!/usr/bin/env bash
rclone copy gdrive:trading_bot/trade_outcome_model.onnx $HOME/ai_trading_bot/ai/ --update --quiet
