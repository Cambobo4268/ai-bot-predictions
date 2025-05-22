#!/usr/bin/env python3

import os
import time
import subprocess
from datetime import datetime, timedelta

BASE = os.path.expanduser("~/ai_trading_bot")
LOGFILE = os.path.join(BASE, "logs/orchestrator.log")
NEXT_RETRAIN = datetime.now() + timedelta(hours=24)

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGFILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def run_script(cmd, name):
    log(f"▶️ Running {name}...")
    if cmd.endswith(".sh"):
        result = os.system(f"/data/data/com.termux/files/usr/bin/bash {cmd}")
    elif cmd.endswith(".py"):
        result = os.system(f"/data/data/com.termux/files/usr/bin/python3 {cmd}")
    else:
        result = os.system(cmd)
    if result == 0:
        log(f"✅ {name} completed successfully.")
    else:
        log(f"❌ {name} failed with exit code {result}")

def start_telegram_listener():
    log("💬 Launching Telegram listener...")
    subprocess.Popen(["/data/data/com.termux/files/usr/bin/python3", f"{BASE}/tools/telegram_listener.py"])

def run_prediction_pipeline():
    run_script(f"{BASE}/pull_and_predict.sh", "pull_and_predict.sh")

def run_trade_execution():
    run_script(f"{BASE}/predict/execute_trades.py", "execute_trades.py")

def run_retrain_if_due():
    global NEXT_RETRAIN
    if datetime.now() >= NEXT_RETRAIN:
        run_script(f"{BASE}/tools/full_retrain.sh", "full_retrain.sh")
        NEXT_RETRAIN = datetime.now() + timedelta(hours=24)

def main():
    start_telegram_listener()
    while True:
        run_prediction_pipeline()
        run_trade_execution()
        run_retrain_if_due()
        log("⏳ Sleeping 60 seconds...\n")
        time.sleep(60)

if __name__ == "__main__":
    main()
