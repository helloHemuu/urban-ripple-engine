import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


INPUT_FILE = "data/processed/metro_traffic_cleaned.csv"
MODEL_FILE = "ml/training/traffic_model.pkl"

print("Loading cleaned traffic data...")

traffic = pd.read_csv(INPUT_FILE, keep_default_na=False)

# Remove exact duplicate records
traffic = traffic.drop_duplicates()

# Select input features
features = [
    "temp",
    "rain_1h",
    "snow_1h",
    "clouds_all",
    "hour",
    "day_of_week",
    "month",
    "is_weekend",
    "holiday",
    "weather_main"
]

X = traffic[features]
y = traffic["traffic_volume"]

# Separate numerical and categorical features
numeric_features = [
    "temp",
    "rain_1h",
    "snow_1h",
    "clouds_all",
    "hour",
    "day_of_week",
    "month",
    "is_weekend"
]

categorical_features = [
    "holiday",
    "weather_main"
]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

# Create Random Forest model
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ))
])

# Chronological train-test split
split_index = int(len(X) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining Random Forest model...")

model.fit(X_train, y_train)

print("Training completed!")

# Predictions
predictions = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\nModel Evaluation Results:")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))

# Save trained model
os.makedirs("ml/training", exist_ok=True)

joblib.dump(model, MODEL_FILE)

print("\nModel saved successfully!")
print("Location:", MODEL_FILE)