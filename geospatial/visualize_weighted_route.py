import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString

GRAPH_FILE = "data/processed/ujjain_weighted_graph.graphml"
ROADS_FILE = "data/processed/ujjain_split_roads.gpkg"
OUTPUT_FILE = "data/processed/weighted_shortest_route_map.png"

print("Loading weighted graph...")
G = nx.read_graphml(GRAPH_FILE)

nodes = list(G.nodes())

source = nodes[0]
destination = nodes[100]

print("Calculating distance-based route...")
route = nx.shortest_path(
    G,
    source=source,
    target=destination,
    weight="length"
)

print("Extracting route coordinates...")
coordinates = []

for node in route:
    data = G.nodes[node]
    coordinates.append((float(data["x"]), float(data["y"])))

route_line = LineString(coordinates)

route_gdf = gpd.GeoDataFrame(
    {"route": ["Weighted Shortest Route"]},
    geometry=[route_line],
    crs="EPSG:32643"
)

print("Loading road network...")
roads = gpd.read_file(ROADS_FILE)
roads = roads.to_crs(epsg=32643)

print("Plotting...")
fig, ax = plt.subplots(figsize=(12, 12))

roads.plot(ax=ax, linewidth=0.6)

route_gdf.plot(ax=ax, linewidth=3)

ax.set_title("Urban Ripple Engine - Distance-Based Route")
ax.set_xlabel("Easting (meters)")
ax.set_ylabel("Northing (meters)")

plt.tight_layout()

plt.savefig(OUTPUT_FILE, dpi=300)
plt.show()

print("\nRoute visualization completed!")
print("Saved at:", OUTPUT_FILE)
print("Route distance:", round(sum(
    G[u][v][key]["length"]
    for u, v, key in [
        (route[i], route[i+1], list(G[route[i]][route[i+1]].keys())[0])
        for i in range(len(route)-1)
    ]
), 2), "meters")