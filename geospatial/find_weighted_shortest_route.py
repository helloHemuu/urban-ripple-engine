import networkx as nx

INPUT_FILE = "data/processed/ujjain_weighted_graph.graphml"

print("Loading weighted road graph...")
G = nx.read_graphml(INPUT_FILE)

nodes = list(G.nodes())

source = nodes[0]
destination = nodes[100]

print("\nFinding shortest route by distance...")

route = nx.shortest_path(
    G,
    source=source,
    target=destination,
    weight="length"
)

route_distance = nx.shortest_path_length(
    G,
    source=source,
    target=destination,
    weight="length"
)

print("\nRoute successfully calculated!")
print("Source:", source)
print("Destination:", destination)
print("Number of nodes in route:", len(route))
print("Total route distance:", round(route_distance, 2), "meters")
print("Total route distance:", round(route_distance / 1000, 3), "km")

print("\nRoute nodes:")
for node in route:
    print(node)