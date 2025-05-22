#!/usr/bin/env python3

import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID_FILE = os.path.expanduser("~/ai_trading_bot/config/chat_id.txt")

def get_chat_id():
    try:
        with open(CHAT_ID_FILE) as f:
            return f.read().strip()
    except:
        return None

def notify(text):
    chat_id = get_chat_id()
    if chat_id and TOKEN:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        notify(" ".join(sys.argv[1:]))
