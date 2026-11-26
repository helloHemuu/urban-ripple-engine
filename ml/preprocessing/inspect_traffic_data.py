import pandas as pd

FILE_PATH = "data/raw/Metro_Interstate_Traffic_Volume.csv.gz"

print("Loading traffic dataset...")

traffic = pd.read_csv(FILE_PATH, compression="gzip")

print("\nDataset loaded successfully!")

print("Dataset shape:", traffic.shape)

print("\nColumn names:")
print(traffic.columns.tolist())

print("\nFirst 5 records:")
print(traffic.head())

print("\nMissing values:")
print(traffic.isnull().sum())

print("\nDataset information:")
print(traffic.info())