import joblib
import pandas as pd

MODEL_FILE = "ml/training/traffic_model.pkl"

print("Loading trained traffic model...")

model = joblib.load(MODEL_FILE)

# Sample traffic conditions
sample = pd.DataFrame([{
    "temp": 290.0,
    "rain_1h": 0.0,
    "snow_1h": 0.0,
    "clouds_all": 40,
    "hour": 17,
    "day_of_week": 4,
    "month": 11,
    "is_weekend": 0,
    "holiday": "None",
    "weather_main": "Clouds"
}])

print("\nInput traffic conditions:")
print(sample)

# Predict traffic volume
prediction = model.predict(sample)

print("\nPredicted traffic volume:")
print(round(prediction[0]), "vehicles per hour")