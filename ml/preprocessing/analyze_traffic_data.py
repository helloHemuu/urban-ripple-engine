import pandas as pd

FILE_PATH = "data/processed/metro_traffic_cleaned.csv"

print("Loading cleaned traffic data...")

traffic = pd.read_csv(FILE_PATH)

print("\nDataset shape:")
print(traffic.shape)

print("\nTraffic volume statistics:")
print(traffic["traffic_volume"].describe())

print("\nTraffic volume by hour:")
print(traffic.groupby("hour")["traffic_volume"].mean().round(2))

print("\nTraffic volume by day:")
print(traffic.groupby("day_of_week")["traffic_volume"].mean().round(2))

print("\nDuplicate records:")
print(traffic.duplicated().sum())

print("\nAnalysis completed!")