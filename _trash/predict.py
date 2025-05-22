import onnxruntime as ort
import numpy as np
import json

# Load the model
session = ort.InferenceSession("models/brain.onnx")

# Load trade input (simulated or from JSON)
with open("trade_input.json", "r") as f:
    data = json.load(f)

# Prepare input
x = np.array([[data["rsi"], data["volatility"], data["volume"], data["percent_change"]]], dtype=np.float32)

# Predict
inputs = {session.get_inputs()[0].name: x}
outputs = session.run(None, inputs)[0]
prediction = np.argmax(outputs)

labels = {0: "GOOD", 1: "NEUTRAL", 2: "BAD"}
print("Predicted Outcome:", labels[prediction])
