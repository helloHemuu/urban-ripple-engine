import geopandas as gpd
import matplotlib.pyplot as plt

INPUT_FILE = "data/raw/ujjain_roads.gpkg"
OUTPUT_FILE = "data/processed/ujjain_roads_map.png"

print("Loading Ujjain road data...")

roads = gpd.read_file(INPUT_FILE)

print("Visualizing road network...")

fig, ax = plt.subplots(figsize=(12, 12))

roads.plot(
    ax=ax,
    linewidth=0.6
)

ax.set_title("Ujjain Pilot Area - Road Network", fontsize=16)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

plt.show()

print("\nRoad network map generated successfully!")
print("Saved at:", OUTPUT_FILE)