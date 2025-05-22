#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.expanduser("~/ai_trading_bot/.env"))

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }
    requests.post(url, data=payload)
