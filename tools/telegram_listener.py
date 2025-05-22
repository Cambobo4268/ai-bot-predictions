#!/usr/bin/env python3

import os, time, json, requests, subprocess

TOKEN = "8019495081:AAFXLKAczA-UtsTTK5AKVHU_CquQ1BhqQc8"
URL = f"https://api.telegram.org/bot{TOKEN}"

CHAT_ID_FILE = os.path.expanduser("~/ai_trading_bot/config/chat_id.txt")
LOG_FILE = os.path.expanduser("~/ai_trading_bot/logs/orchestrator.log")

def send_message(chat_id, text):
    print(f"➡️ Sending to Telegram: {text}")
    requests.post(URL + "/sendMessage", data={"chat_id": chat_id, "text": text})

def send_dashboard(chat_id):
    subprocess.run(["python3", os.path.expanduser("~/ai_trading_bot/tools/send_dashboard.py")])
    with open(os.path.expanduser("~/ai_trading_bot/data/dashboard.png"), "rb") as photo:
        requests.post(
            f"{URL}/sendPhoto",
            data={"chat_id": chat_id, "caption": "📊 AI Bot Dashboard"},
            files={"photo": photo},
        )

def read_log_tail():
    if not os.path.exists(LOG_FILE): return "No logs yet."
    with open(LOG_FILE, "r") as f:
        return "\n".join(f.readlines()[-10:])

def handle_command(command, chat_id):
    if command == "/status":
        send_message(chat_id, "✅ Bot is online and running.")
    elif command == "/log":
        send_message(chat_id, f"🧠 Last logs:\n{read_log_tail()}")
    elif command == "/retrain":
        send_message(chat_id, "⏳ Starting retraining...")
        os.system("bash ~/ai_trading_bot/tools/full_retrain.sh")
        send_message(chat_id, "✅ Retraining complete.")
    elif command == "/dashboard":
        send_message(chat_id, "🖼️ Generating dashboard...")
        send_dashboard(chat_id)
    else:
        send_message(chat_id, "❌ Unknown command.")

def get_updates(offset=None):
    params = {"timeout": 30}
    if offset: params["offset"] = offset
    return requests.get(URL + "/getUpdates", params=params).json()

def main():
    print("👂 Listening for Telegram commands...")
    last_update_id = None
    while True:
        try:
            updates = get_updates(last_update_id).get("result", [])
            for update in updates:
                last_update_id = update["update_id"] + 1
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "").strip()
                if chat_id:
                    with open(CHAT_ID_FILE, "w") as f:
                        f.write(str(chat_id))
                    if text.startswith("/"):
                        handle_command(text.lower(), chat_id)
        except Exception as e:
            print(f"⚠️ Error: {e}")
        time.sleep(3)

if __name__ == "__main__":
    main()
