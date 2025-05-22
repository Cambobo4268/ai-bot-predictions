#!/usr/bin/env python3

import os
import subprocess

dataset = os.path.expanduser("~/ai_trading_bot/data/cleaned_dataset.csv")
dest = "gdrive:/ai_trading_bot/data/cleaned_dataset.csv"

print("📤 Syncing latest cleaned dataset to Google Drive...")
subprocess.run(["rclone", "copy", dataset, dest], check=True)

print("""
✅ Dataset pushed successfully.

🔗 Click this link to open retrain notebook in Colab:
https://colab.research.google.com/drive/1AJKuJ8NJXbFozW17YKR-7hlC9o4WN4jfj

👉 In Colab: just click 'Runtime > Run all' to retrain and sync model.
""")
