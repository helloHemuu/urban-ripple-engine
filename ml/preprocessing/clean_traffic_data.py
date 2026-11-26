import pandas as pd

INPUT_FILE = "data/raw/Metro_Interstate_Traffic_Volume.csv.gz"
OUTPUT_FILE = "data/processed/metro_traffic_cleaned.csv"

print("Loading traffic dataset...")

traffic = pd.read_csv(INPUT_FILE, compression="gzip")

print("Cleaning missing values...")

# Missing holiday values mean no holiday
traffic["holiday"] = traffic["holiday"].fillna("None")

# Convert date_time into datetime format
traffic["date_time"] = pd.to_datetime(traffic["date_time"])

# Extract time-based features
traffic["hour"] = traffic["date_time"].dt.hour
traffic["day_of_week"] = traffic["date_time"].dt.dayofweek
traffic["month"] = traffic["date_time"].dt.month
traffic["is_weekend"] = (
    traffic["day_of_week"] >= 5
).astype(int)

# Check missing values
print("\nMissing values after cleaning:")
print(traffic.isnull().sum())

# Save cleaned dataset
traffic.to_csv(OUTPUT_FILE, index=False)

print("\nCleaning completed successfully!")
print("Final dataset shape:", traffic.shape)
print("Saved to:", OUTPUT_FILE)