#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import os, json, datetime

def generate_dashboard_image():
    predictions_path = os.path.expanduser("~/ai_trading_bot/data/trade_predictions.json")
    retrain_info = "24h ago"
    status = "✅ Online"
    mode = "Dry-run [Simulated trades]"

    try:
        with open(predictions_path) as f:
            predictions = json.load(f)
    except:
        predictions = []

    lines = [
        "AI Bot Dashboard:",
        f"├─ Status: {status}",
        f"├─ Predictions:"
    ]
    for p in predictions:
        lines.append(f"│  ├─ {p['pair']}: {p['action']} ({p['confidence']})")
    lines.append(f"├─ Last Retrain: {retrain_info}")
    lines.append(f"└─ Mode: {mode}")

    img = Image.new("RGB", (600, 300), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    font_path = "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono.ttf"
    font = ImageFont.truetype(font_path, 18)

    y = 10
    for line in lines:
        draw.text((20, y), line, font=font, fill=(255, 255, 255))
        y += 30

    path = os.path.expanduser("~/ai_trading_bot/data/dashboard.png")
    img.save(path)
    return path

def send_dashboard():
    with open(os.path.expanduser("~/ai_trading_bot/config/chat_id.txt")) as f:
        chat_id = f.read().strip()

    path = generate_dashboard_image()
    TOKEN = "8019495081:AAFXLKAczA-UtsTTK5AKVHU_CquQ1BhqQc8"
    URL = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    with open(path, "rb") as photo:
        requests.post(
            URL,
            data={"chat_id": chat_id, "caption": "📊 AI Bot Dashboard"},
            files={"photo": photo}
        )

if __name__ == "__main__":
    send_dashboard()
