#!/usr/bin/env python3
import numpy as np

MODEL_PATH = "trade_outcome_model.onnx"

def predict_outcome(rsi, volatility, volume):
    try:
        session = ort.InferenceSession(MODEL_PATH)
        input_name = session.get_inputs()[0].name
        input_data = np.array([[rsi, volatility, volume]], dtype=np.float32)
        result = session.run(None, {input_name: input_data})[0]
        label = int(np.argmax(result))

        if label == 0:
            return "BAD", {"confidence": float(result[0][0])}
        elif label == 1:
            return "GOOD", {"confidence": float(result[0][1])}
        else:
            return "NEUTRAL", {"confidence": float(result[0][2])}
    except Exception as e:
        print(f"[ONNX ERROR] {e}")
        return "HOLD", {"confidence": 0.0}
