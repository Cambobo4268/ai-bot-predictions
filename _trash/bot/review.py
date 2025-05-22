#!/usr/bin/env python3
import csv
import ccxt
from datetime import datetime, timedelta

exchange = ccxt.kraken()
LOG_PATH = os.path.expanduser('~/ai_trading_bot/logs/training_dataset.csv')
REVIEW_LOG = os.path.expanduser('~/ai_trading_bot/logs/reviewed_dataset.csv')

REVIEW_DELAY_HOURS = 6

def evaluate_trade(row):
    symbol = row['symbol']
    try:
        entry_price = float(row['price'])
        decision = row['decision']
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        change = ((current_price - entry_price) / entry_price) * 100

        if decision == "BUY" and change >= 2:
            outcome = "GOOD"
        elif decision == "SELL" and change <= -2:
            outcome = "GOOD"
        elif decision == "HOLD":
            outcome = "NEUTRAL"
        else:
            outcome = "BAD"

        print(f"[REVIEW] {symbol} | {decision} | Entry: {entry_price} | Now: {current_price} | Change: {change:.2f}% => {outcome}")
        return outcome

    except Exception as e:
        print(f"[ERROR] Could not evaluate {symbol}: {e}")
        return "UNKNOWN"

def is_trade_old_enough(row):
    try:
        trade_time = datetime.fromisoformat(row['timestamp'])
        return datetime.utcnow() - trade_time >= timedelta(hours=REVIEW_DELAY_HOURS)
    except Exception as e:
        print(f"[TIME ERROR] Could not parse timestamp: {e}")
        return False

with open(LOG_PATH, newline='') as infile, open(REVIEW_LOG, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['outcome']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        if not is_trade_old_enough(row):
            row['outcome'] = "PENDING"
            print(f"[SKIP] {row['symbol']} not old enough for review.")
        elif row['decision'] in ['BUY', 'SELL']:
            row['outcome'] = evaluate_trade(row)
        else:
            row['outcome'] = "NEUTRAL"
        writer.writerow(row)
