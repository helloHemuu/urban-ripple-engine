import networkx as nx

GRAPH_FILE = "data/processed/ujjain_weighted_graph.graphml"

print("Loading weighted road graph...")
G = nx.read_graphml(GRAPH_FILE)

nodes = list(G.nodes())

source = nodes[0]
destination = nodes[100]

print("\nCalculating original route...")

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

print("Original route distance:", round(original_distance, 2), "meters")

# Select three road segments from the original route
route_length = len(original_route)

block_indices = [
    route_length // 4,
    route_length // 2,
    (3 * route_length) // 4
]

blocked_edges = []

for index in block_indices:

    if index + 1 < route_length:

        edge = (
            original_route[index],
            original_route[index + 1]
        )

        blocked_edges.append(edge)

print("\nSelected road segments for disruption:")

for edge in blocked_edges:
    print(edge)

# Create disrupted graph
G_disrupted = G.copy()

print("\nSimulating multiple road closures...")

for u, v in blocked_edges:

    if G_disrupted.has_edge(u, v):
        G_disrupted.remove_edge(u, v)

print("Road closures applied:", len(blocked_edges))

print("\nFinding alternate route...")

try:

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

    extra_distance = alternate_distance - original_distance

    percentage_increase = (
        extra_distance / original_distance
    ) * 100 if original_distance > 0 else 0

    print("\nAlternate route successfully found!")

    print("\n--- Multiple Disruption Analysis ---")

    print("Original route distance:",
          round(original_distance, 2), "meters")

    print("Alternate route distance:",
          round(alternate_distance, 2), "meters")

    print("Extra distance:",
          round(extra_distance, 2), "meters")

    print("Route increase:",
          round(percentage_increase, 2), "%")

    print("Original route nodes:", len(original_route))
    print("Alternate route nodes:", len(alternate_route))

    print("\nMultiple road closure simulation completed!")

except nx.NetworkXNoPath:

    print("\nNo alternate route available!")

    print("Multiple road closures disconnected the destination.")
