import json
import onnxruntime as ort
from pathlib import Path

INPUT_PATH = Path("../data/trade_input.json")
MODEL_PATH = Path("../models/brain.onnx")
OUTPUT_PATH = Path("../data/trade_predictions.json")

def run_prediction():
    with open(INPUT_PATH, "r") as f:
        input_data = json.load(f)

    session = ort.InferenceSession(str(MODEL_PATH))
    inputs = {session.get_inputs()[0].name: [list(input_data.values())]}
    output = session.run(None, inputs)[0]

    result = {
        "prediction": output[0],
        "confidence": float(output[1])
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print("[OK] Prediction complete. Output saved to data/trade_predictions.json")

if __name__ == "__main__":
    run_prediction()
