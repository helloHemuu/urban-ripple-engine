import geopandas as gpd
import pandas as pd

INPUT_FILE = "data/raw/ujjain_roads.gpkg"
OUTPUT_FILE = "data/processed/ujjain_road_features.csv"

print("Loading Ujjain road network...")

roads = gpd.read_file(INPUT_FILE)

# Select useful ML features
features = roads[
    [
        "id",
        "highway",
        "lanes",
        "maxspeed",
        "oneway",
        "junction",
        "bridge",
        "surface",
        "length",
    ]
].copy()

# Convert numeric columns
features["lanes"] = pd.to_numeric(features["lanes"], errors="coerce")
features["maxspeed"] = pd.to_numeric(features["maxspeed"], errors="coerce")
features["length"] = pd.to_numeric(features["length"], errors="coerce")

# Fill missing numeric values
features["lanes"] = features["lanes"].fillna(1)
features["maxspeed"] = features["maxspeed"].fillna(40)

# Convert categorical values to strings
for column in ["highway", "oneway", "junction", "bridge", "surface"]:
    features[column] = features[column].fillna("unknown").astype(str)

print(f"Road features created: {len(features)}")

features.to_csv(OUTPUT_FILE, index=False)

print(f"Saved to: {OUTPUT_FILE}")