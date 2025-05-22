#!/usr/bin/env python3
import pandas as pd

# Load saved model
model = joblib.load("trade_outcome_model.pkl")

# Example trade to predict
trade = pd.DataFrame([{
    "rsi": 43.5,
    "balance_before": 6500.0,
    "percent_change": 8.3
}])

# Predict
pred = model.predict(trade)[0]
print("Predicted Outcome:", "GOOD" if pred == 1 else "BAD")
