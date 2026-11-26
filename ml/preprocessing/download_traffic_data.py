
from ucimlrepo import fetch_ucirepo
import pandas as pd
from pathlib import Path

print("Downloading Metro Interstate Traffic Dataset...")

# Fetch dataset from UCI
dataset = fetch_ucirepo(id=492)

# Combine features and target
traffic = pd.concat(
    [dataset.data.features, dataset.data.targets],
    axis=1
)

print("\nDataset downloaded successfully!")
print("Shape:", traffic.shape)
print("\nColumns:")
print(traffic.columns.tolist())

# Save dataset
output_path = Path("data/raw/metro_interstate_traffic_volume.csv")
traffic.to_csv(output_path, index=False)

print("\nDataset saved at:", output_path)
print("\nFirst five records:")
print(traffic.head())
