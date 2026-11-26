import geopandas as gpd
import matplotlib.pyplot as plt

INPUT_FILE = "data/processed/ujjain_split_roads.gpkg"
OUTPUT_FILE = "data/processed/ujjain_split_roads_map.png"

print("Loading split road network...")

roads = gpd.read_file(INPUT_FILE)

print("Visualizing roads...")

fig, ax = plt.subplots(figsize=(12, 12))

roads.plot(ax=ax, linewidth=0.7)

ax.set_title("Ujjain - Improved Split Road Network", fontsize=16)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

plt.show()

print("\nMap generated successfully!")
print("Saved at:", OUTPUT_FILE)