#!/usr/bin/env python3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from datetime import datetime
import json

DATA_PATH = os.path.expanduser("~/ai_trading_bot/logs/reviewed_dataset.csv")
MODEL_PATH = os.path.expanduser("~/ai_trading_bot/ai/trade_outcome_model.pkl")
TRACKER_PATH = os.path.expanduser("~/ai_trading_bot/logs/model_tracker.json")

def retrain_model():
    try:
        df = pd.read_csv(DATA_PATH)
        df = df[df['outcome'].isin(['GOOD', 'BAD', 'NEUTRAL'])]
        features = ['rsi', 'change', 'volatility', 'volume']
        df = df.dropna(subset=features)
        X = df[features]
        y = df['outcome']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)

        # Save model
        joblib.dump(model, MODEL_PATH)

        # Track metadata
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "accuracy": round(acc, 4),
            "samples": len(df),
            "classes": list(y.unique()),
            "precision": round(report['weighted avg']['precision'], 4),
            "recall": round(report['weighted avg']['recall'], 4),
            "f1_score": round(report['weighted avg']['f1-score'], 4)
        }

        if os.path.exists(TRACKER_PATH):
            with open(TRACKER_PATH, 'r') as f:
                tracker = json.load(f)
        else:
            tracker = []

        tracker.append(log_entry)

        with open(TRACKER_PATH, 'w') as f:
            json.dump(tracker, f, indent=4)

        print(f"[RETRAIN] Model retrained — Accuracy: {acc:.2%}")

    except Exception as e:
        print(f"[RETRAIN ERROR] {e}")

if __name__ == "__main__":
    retrain_model()
