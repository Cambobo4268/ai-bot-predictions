#!/usr/bin/env python3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load cleaned dataset
df = pd.read_csv("cleaned_dataset.csv")

# Encode 'outcome' column
df['outcome'] = df['outcome'].map({'GOOD': 1, 'BAD': -1, 'PENDING': 0})

# One-hot encode 'symbol' and 'decision'
df = pd.get_dummies(df, columns=['symbol', 'decision'], drop_first=True)

# Split data
X = df.drop(columns=['timestamp', 'outcome'])
y = df['outcome']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "../ai/trade_outcome_model.pkl")

# Accuracy
print("Training accuracy:", model.score(X_train, y_train))
print("Testing accuracy:", model.score(X_test, y_test))
