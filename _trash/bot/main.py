#!/usr/bin/env python3
import sys
sys.path.append(os.path.expanduser('~/ai_trading_bot'))

import time
import json
import csv
import ccxt
from datetime import datetime
from dotenv import load_dotenv
from ai.ai_manager import ask_ai
from utils.telegram_alert import send_telegram_alert

load_dotenv(dotenv_path=os.path.expanduser("~/ai_trading_bot/.env"))

API_KEY = os.getenv('KRAKEN_API_KEY')
API_SECRET = os.getenv('KRAKEN_API_SECRET')
LIVE_MODE = os.getenv('LIVE_MODE', 'false').lower() == 'true'

kraken = ccxt.kraken({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

BALANCE_FILE = os.path.expanduser("~/ai_trading_bot/logs/balance.json")
TRAINING_LOG = os.path.expanduser("~/ai_trading_bot/logs/training_dataset.csv")
os.makedirs(os.path.dirname(TRAINING_LOG), exist_ok=True)

if not os.path.exists(TRAINING_LOG):
    with open(TRAINING_LOG, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "symbol", "decision", "price", "volume",
            "volatility", "percent_change", "rsi", "balance_before"
        ])

START_BALANCE = None
DAILY_LOSS_THRESHOLD = 0.10
TRADE_AMOUNT_RATIO = 0.20

def load_simulated_balance():
    with open(BALANCE_FILE, 'r') as f:
        data = json.load(f)
    return data["balance"]

def save_simulated_balance(new_balance, trade_log):
    with open(BALANCE_FILE, 'r') as f:
        data = json.load(f)
    data["balance"] = new_balance
    data["history"].append(trade_log)
    with open(BALANCE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_wallet_balance():
    if not LIVE_MODE:
        balance = load_simulated_balance()
        print(f"[MODE] PAPER MODE ENABLED. Simulated Balance: ${balance}")
        return balance
    try:
        balance_info = kraken.fetch_balance()
        balance = float(balance_info['total'].get('USD', 0))
        print(f"[BALANCE] Real Kraken USD: {balance}")
        return balance
    except Exception as e:
        print(f"[ERROR] Balance fetch failed: {e}")
        send_telegram_alert(f"⚠️ Balance Error: {e}")
        return 0.0

def get_top_movers():
    try:
        tickers = kraken.fetch_tickers()
        movers = []
        for symbol, data in tickers.items():
            if '/USD' in symbol and 'open' in data and 'last' in data:
                try:
                    open_price = data['open']
                    last_price = data['last']
                    if open_price > 0:
                        change = ((last_price - open_price) / open_price) * 100
                        movers.append((symbol, change))
                except Exception:
                    continue
        top5 = sorted(movers, key=lambda x: x[1], reverse=True)[:5]
        print(f"[INFO] Top 5 movers: {top5}")
        return [coin[0] for coin in top5]
    except Exception as e:
        print(f"[ERROR] Failed to fetch tickers: {e}")
        send_telegram_alert(f"⚠️ Ticker Error: {e}")
        return []

def log_training_data(symbol, decision, price, metrics, balance_before):
    with open(TRAINING_LOG, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            symbol,
            decision,
            price,
            metrics.get("volume", ""),
            metrics.get("volatility", ""),
            metrics.get("change", ""),
            metrics.get("rsi", ""),
            balance_before
        ])

def trade_logic():
    global START_BALANCE
    if START_BALANCE is None:
        START_BALANCE = get_wallet_balance()

    current_balance = get_wallet_balance()
    if START_BALANCE <= 0 or current_balance <= 0:
        print("[WARNING] Skipping trade due to $0 balance.")
        return

    if (START_BALANCE - current_balance) / START_BALANCE >= DAILY_LOSS_THRESHOLD:
        send_telegram_alert("❗ Bot stopped due to -10% daily loss.")
        exit()

    top5 = get_top_movers()
    if not top5:
        print("[WARNING] No top movers found.")
        return

    portion = round(current_balance * TRADE_AMOUNT_RATIO, 2)
    print(f"[INFO] Simulating ${portion} per trade across top movers.")

    for symbol in top5:
        decision, metrics = ask_ai(symbol)
        print(f"[DECISION] {symbol}: {decision}")
        send_telegram_alert(f"🔍 AI Decision for {symbol}: {decision}")
        try:
            ticker = kraken.fetch_ticker(symbol)
            price = ticker['last']
            units = portion / price
            new_balance = current_balance

            if decision == 'BUY':
                if LIVE_MODE:
                    kraken.create_market_buy_order(symbol, units)
                new_balance -= portion
                print(f"[SIMULATED] Bought {symbol} worth ${portion}")
                send_telegram_alert(f"✅ Simulated BUY: {symbol} for ${portion}")

            elif decision == 'SELL':
                if LIVE_MODE:
                    kraken.create_market_sell_order(symbol, units)
                sell_return = portion * (1 + (ticker['change'] / 100 if 'change' in ticker else 0.01))
                new_balance += sell_return
                print(f"[SIMULATED] Sold {symbol} for approx ${sell_return:.2f}")
                send_telegram_alert(f"✅ Simulated SELL: {symbol} for ~${sell_return:.2f}")

            else:
                continue  # skip logging for HOLD

            if not LIVE_MODE:
                trade_log = {
                    "time": datetime.utcnow().isoformat(),
                    "symbol": symbol,
                    "decision": decision,
                    "price": price,
                    "units": round(units, 4),
                    "portion": portion,
                    "new_balance": round(new_balance, 2)
                }
                save_simulated_balance(new_balance, trade_log)
                log_training_data(symbol, decision, price, metrics, current_balance)

        except Exception as e:
            print(f"[ERROR] Trade failed for {symbol}: {e}")
            send_telegram_alert(f"❌ Trade failed for {symbol}: {e}")

def main_loop():
    while True:
        print("[LOOP] Starting trade logic cycle.")
        trade_logic()
        print("[LOOP] Sleeping 1 hour...\n")
        time.sleep(3600)

if __name__ == "__main__":
    main_loop()

import subprocess
from datetime import datetime, timedelta

RETRAIN_INTERVAL_HOURS = 336  # 14 days
LAST_RETRAIN_FILE = os.path.expanduser("~/ai_trading_bot/logs/last_retrain.txt")

def should_retrain():
    try:
        if not os.path.exists(LAST_RETRAIN_FILE):
            return True
        with open(LAST_RETRAIN_FILE, 'r') as f:
            last = datetime.fromisoformat(f.read().strip())
        return datetime.utcnow() - last >= timedelta(hours=RETRAIN_INTERVAL_HOURS)
    except:
        return True

def update_retrain_timestamp():
    with open(LAST_RETRAIN_FILE, 'w') as f:
        f.write(datetime.utcnow().isoformat())

# Add this inside your main_loop() before time.sleep()
        if should_retrain():
            subprocess.call(["python", os.path.expanduser("~/ai_trading_bot/ai/retrain_model.py")])
            update_retrain_timestamp()
            send_telegram_alert("♻️ AI Model retrained using latest reviews.")

from ai.onnx_predictor import predict_outcome

        # AI prediction
        decision, confidence = predict_outcome(rsi, volatility, volume)
        print(f"[AI DECISION] {symbol} | {decision} | Confidence: {confidence['confidence']:.2f}")
