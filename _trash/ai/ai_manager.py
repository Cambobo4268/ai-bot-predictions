#!/usr/bin/env python3
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Load model
model_path = os.path.expanduser("~/ai_trading_bot/ai/trade_outcome_model.pkl")
model = joblib.load(model_path)

def ask_ai(symbol, features):
    try:
        df = pd.DataFrame([features])
        df = pd.get_dummies(df)
        
        # Align features to model
        for col in model.feature_names_in_:
            if col not in df.columns:
                df[col] = 0
        df = df[model.feature_names_in_]

        prediction = model.predict(df)[0]
        confidence = np.max(model.predict_proba(df))
        
        if prediction == 1:
            return "BUY", {"confidence": confidence}
        elif prediction == -1:
            return "SELL", {"confidence": confidence}
        else:
            return "HOLD", {"confidence": confidence}
    except Exception as e:
        print(f"[AI ERROR] {symbol}: {e}")
        return "HOLD", {"confidence": 0.0}
