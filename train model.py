

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the same dataset
df = pd.read_csv("sensor_data.csv")

# Select features and target
X = df[["temperature", "pressure", "vibration", "current"]]
y = df["fault_status"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "fault_detection_model.pkl")

print("✅ Model trained and saved successfully!")
