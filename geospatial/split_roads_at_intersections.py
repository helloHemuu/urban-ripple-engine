import geopandas as gpd
from shapely.ops import unary_union

INPUT_FILE = "data/raw/ujjain_roads.gpkg"
OUTPUT_FILE = "data/processed/ujjain_split_roads.gpkg"

print("Loading road data...")

roads = gpd.read_file(INPUT_FILE)

print("Converting coordinate system...")

roads = roads.to_crs(epsg=32643)

print("Splitting roads at intersections...")

# Combine road geometries and split at crossings
combined = unary_union(roads.geometry)

# Convert split geometry into individual road segments
segments = []

if combined.geom_type == "MultiLineString":
    segments = list(combined.geoms)

elif combined.geom_type == "LineString":
    segments = [combined]

print("Creating GeoDataFrame...")

split_roads = gpd.GeoDataFrame(
    geometry=segments,
    crs=roads.crs
)

split_roads = split_roads[split_roads.geometry.length > 1]

print("Converting back to geographic coordinates...")

split_roads = split_roads.to_crs(epsg=4326)

print("Saving split roads...")

split_roads.to_file(OUTPUT_FILE, driver="GPKG")

print("\nRoad splitting completed!")
print("Original road segments:", len(roads))
print("New road segments:", len(split_roads))
print("Saved to:", OUTPUT_FILE)