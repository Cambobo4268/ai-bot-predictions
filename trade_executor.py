import json

# Settings
PREDICTION_FILE = "predictions.json"
CONFIDENCE_THRESHOLD = 0.7
TRADE_PAIR = "XBTUSD"
TRADE_VOLUME = 0.001  # Simulated

# Load predictions
try:
    with open(PREDICTION_FILE, "r") as f:
        prediction = json.load(f)
except Exception as e:
    print(f"[ERROR] Could not read {PREDICTION_FILE}: {e}")
    exit(1)

label = prediction.get("prediction", "UNKNOWN")
confidence = float(prediction.get("confidence", 0))

print(f"[INFO] Prediction: {label}, Confidence: {confidence}")

# Simulated trade decision
if confidence >= CONFIDENCE_THRESHOLD:
    if label == "GOOD":
        print(f"[SIMULATION] BUY {TRADE_VOLUME} of {TRADE_PAIR}")
    elif label == "BAD":
        print(f"[SIMULATION] SELL {TRADE_VOLUME} of {TRADE_PAIR}")
    else:
        print("[SIMULATION] HOLD (Neutral signal)")
else:
    print("[SKIPPED] Confidence too low — no action taken.")
