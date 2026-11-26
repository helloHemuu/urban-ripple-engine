import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString

INPUT_FILE = "data/processed/ujjain_split_graph.graphml"
OUTPUT_FILE = "data/processed/shortest_route_map.png"

print("Loading road graph...")

G = nx.read_graphml(INPUT_FILE)

nodes = list(G.nodes())

source = nodes[0]
destination = nodes[100]

print("Calculating route...")

route = nx.shortest_path(
    G,
    source=source,
    target=destination
)

print("Preparing route geometry...")

route_coordinates = []

for node in route:
    data = G.nodes[node]

    x = float(data["x"])
    y = float(data["y"])

    route_coordinates.append((x, y))

route_line = LineString(route_coordinates)

route_gdf = gpd.GeoDataFrame(
    {"name": ["Shortest Route"]},
    geometry=[route_line],
    crs="EPSG:4326"
)

roads = gpd.read_file("data/raw/ujjain_roads.gpkg")

print("Plotting map...")

fig, ax = plt.subplots(figsize=(12, 12))

roads.plot(ax=ax, linewidth=0.5)

route_gdf.plot(
    ax=ax,
    linewidth=3
)

ax.set_title("Urban Ripple Engine - Shortest Route", fontsize=16)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)

plt.show()

print("\nRoute visualization completed!")
print("Saved at:", OUTPUT_FILE)