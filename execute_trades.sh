#!/data/data/com.termux/files/usr/bin/bash

# === CONFIG ===
PREDICTION_PATH="$HOME/storage/shared/Download/predictions.json"
KRAKEN_KEYS="$HOME/ai_trading_bot/kraken_api.json"
LOG_PATH="$HOME/ai_trading_bot/trade_log.csv"

# === READ API KEYS ===
API_KEY=$(jq -r .api_key "$KRAKEN_KEYS")
API_SECRET=$(jq -r .api_secret "$KRAKEN_KEYS")

# === RUN TRADES ===
python3 -u - <<EOF2
import json, time, csv, hmac, hashlib, base64
import urllib.parse
import requests
from datetime import datetime

with open("$PREDICTION_PATH") as f:
    predictions = json.load(f)

with open("$KRAKEN_KEYS") as f:
    keys = json.load(f)

api_key = keys["api_key"]
api_sec = base64.b64decode(keys["api_secret"])

def kraken_request(uri_path, data, api_key, api_sec):
    url = "https://api.kraken.com" + uri_path
    nonce = str(int(1000*time.time()))
    data["nonce"] = nonce
    post_data = urllib.parse.urlencode(data)
    message = (nonce + post_data).encode()
    sha256 = hashlib.sha256(message).digest()
    hmac_key = hmac.new(api_sec, uri_path.encode() + sha256, hashlib.sha512)
    headers = {
        "API-Key": api_key,
        "API-Sign": base64.b64encode(hmac_key.digest()),
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Symbol Mapping
symbol_map = {
    "XBT/USD": "XXBTZUSD",
    "ETH/USD": "XETHZUSD",
    "ADA/USD": "ADAUSD",
    "SOL/USD": "SOLUSD",
    "DOT/USD": "DOTUSD"
}

# Log header
try:
    with open("$LOG_PATH", "r") as f:
        next(csv.reader(f))
except:
    with open("$LOG_PATH", "w") as f:
        csv.writer(f).writerow(["timestamp","symbol","action","confidence"])

# Execute trades
for item in predictions:
    if isinstance(item["prediction"], str):
        continue

    if item["confidence"] >= 0.8:
        symbol = item["symbol"]
        pair = symbol_map.get(symbol, symbol)
        action = "buy" if item["prediction"] == 1 else "sell"
        volume = "5.0"

        print(f"[SIMULATED] Would execute {action.upper()} {pair} @ confidence {item['confidence']}")
        response = {"result": "dry_run"}  # Simulation mode

        with open("$LOG_PATH", "a") as f:
            csv.writer(f).writerow([datetime.utcnow(), pair, action.upper(), item["confidence"]])
EOF2
