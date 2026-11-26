import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import LineString

ROADS_FILE = "data/processed/ujjain_split_roads.gpkg"
CRITICAL_FILE = "data/processed/critical_roads.csv"
OUTPUT_FILE = "data/processed/critical_roads_map.png"

print("Loading roads...")
roads = gpd.read_file(ROADS_FILE)
roads = roads.to_crs(epsg=32643)

print("Loading criticality data...")
critical = pd.read_csv(CRITICAL_FILE)

# Select top 100 segments
top_roads = critical.nlargest(100, "criticality_score")

print("Creating road geometries...")

geometries = []

for _, row in top_roads.iterrows():

    u = eval(row["node_u"])
    v = eval(row["node_v"])

    geometries.append(
        LineString([u, v])
    )

critical_gdf = gpd.GeoDataFrame(
    top_roads,
    geometry=geometries,
    crs="EPSG:32643"
)

print("Plotting map...")

fig, ax = plt.subplots(figsize=(12, 12))

roads.plot(
    ax=ax,
    color="lightgray",
    linewidth=0.6
)

critical_gdf.plot(
    ax=ax,
    column="criticality_score",
    cmap="hot",
    linewidth=2,
    legend=True
)

ax.set_title(
    "Urban Ripple Engine - Critical Road Segments",
    fontsize=16
)

ax.set_xlabel("Easting (meters)")
ax.set_ylabel("Northing (meters)")

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)
plt.show()

print("\nCritical road visualization completed!")
print("Saved at:", OUTPUT_FILE)
print("Highlighted road segments:", len(critical_gdf))