import geopandas as gpd

INPUT_FILE = "data/raw/ujjain_roads.gpkg"

print("Loading Ujjain road network...")

roads = gpd.read_file(INPUT_FILE)

print("\nDataset loaded successfully!")

print("\nShape of dataset:")
print(roads.shape)

print("\nColumns:")
print(roads.columns.tolist())

print("\nFirst 5 roads:")
print(roads.head())

print("\nGeometry type:")
print(roads.geom_type.value_counts())

print("\nCoordinate Reference System:")
print(roads.crs)

print("\nRoad network inspection completed!")