import osmnx as ox

# Very small pilot area in central Ujjain
NORTH = 23.17
SOUTH = 23.15
EAST = 75.80
WEST = 75.78

ox.settings.overpass_url = "https://overpass-api.de/api/interpreter"
ox.settings.requests_timeout = 60

print("Downloading small Ujjain pilot road network...")

graph = ox.graph.graph_from_bbox(
    (WEST, SOUTH, EAST, NORTH),
    network_type="drive",
)

print("Download complete!")
print(f"Nodes: {len(graph.nodes)}")
print(f"Edges: {len(graph.edges)}")

ox.io.save_graphml(graph, "data/raw/ujjain_roads.graphml")

print("Saved to data/raw/ujjain_roads.graphml")