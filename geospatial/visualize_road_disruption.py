import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString

GRAPH_FILE = "data/processed/ujjain_weighted_graph.graphml"
ROADS_FILE = "data/processed/ujjain_split_roads.gpkg"
OUTPUT_FILE = "data/processed/road_disruption_map.png"

print("Loading weighted graph...")
G = nx.read_graphml(GRAPH_FILE)

nodes = list(G.nodes())

source = nodes[0]
destination = nodes[100]

print("Calculating original route...")

original_route = nx.shortest_path(
    G,
    source=source,
    target=destination,
    weight="length"
)

original_distance = nx.shortest_path_length(
    G,
    source=source,
    target=destination,
    weight="length"
)

# Select a road segment to block
block_index = len(original_route) // 2

blocked_node_1 = original_route[block_index]
blocked_node_2 = original_route[block_index + 1]

print("Blocking road segment...")

G_disrupted = G.copy()
G_disrupted.remove_edge(blocked_node_1, blocked_node_2)

print("Calculating alternate route...")

alternate_route = nx.shortest_path(
    G_disrupted,
    source=source,
    target=destination,
    weight="length"
)

alternate_distance = nx.shortest_path_length(
    G_disrupted,
    source=source,
    target=destination,
    weight="length"
)

print("Preparing route geometries...")

original_coordinates = [
    (float(G.nodes[node]["x"]), float(G.nodes[node]["y"]))
    for node in original_route
]

alternate_coordinates = [
    (float(G.nodes[node]["x"]), float(G.nodes[node]["y"]))
    for node in alternate_route
]

blocked_coordinates = [
    (float(G.nodes[blocked_node_1]["x"]), float(G.nodes[blocked_node_1]["y"])),
    (float(G.nodes[blocked_node_2]["x"]), float(G.nodes[blocked_node_2]["y"]))
]

original_line = LineString(original_coordinates)
alternate_line = LineString(alternate_coordinates)
blocked_line = LineString(blocked_coordinates)

original_gdf = gpd.GeoDataFrame(
    geometry=[original_line],
    crs="EPSG:32643"
)

alternate_gdf = gpd.GeoDataFrame(
    geometry=[alternate_line],
    crs="EPSG:32643"
)

blocked_gdf = gpd.GeoDataFrame(
    geometry=[blocked_line],
    crs="EPSG:32643"
)

roads = gpd.read_file(ROADS_FILE)
roads = roads.to_crs(epsg=32643)

print("Plotting disruption map...")

fig, ax = plt.subplots(figsize=(12, 12))

roads.plot(ax=ax, color="lightgray", linewidth=0.7)

original_gdf.plot(
    ax=ax,
    color="blue",
    linewidth=3,
    label="Original Route"
)

alternate_gdf.plot(
    ax=ax,
    color="green",
    linewidth=3,
    label="Alternate Route"
)

blocked_gdf.plot(
    ax=ax,
    color="red",
    linewidth=6,
    label="Blocked Road"
)

ax.set_title("Urban Ripple Engine - Road Disruption Simulation")
ax.set_xlabel("Easting (meters)")
ax.set_ylabel("Northing (meters)")

ax.legend()

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)
plt.show()

print("\nDisruption visualization completed!")
print("Saved at:", OUTPUT_FILE)

print("\nOriginal distance:", round(original_distance, 2), "meters")
print("Alternate distance:", round(alternate_distance, 2), "meters")
print("Extra distance:", round(alternate_distance - original_distance, 2), "meters")