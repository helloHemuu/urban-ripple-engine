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

# Select a road from the original route to block
block_index = len(original_route) // 2

blocked_node_1 = original_route[block_index]
blocked_node_2 = original_route[block_index + 1]

print("\nSimulating road closure...")
print("Blocked road:")
print("From:", blocked_node_1)
print("To:", blocked_node_2)

# Create a copy of the graph
G_disrupted = G.copy()

# Remove the selected road
G_disrupted.remove_edge(blocked_node_1, blocked_node_2)

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

    print("\nAlternate route found!")
    print("Alternate route nodes:", len(alternate_route))
    print("Alternate route distance:", round(alternate_distance, 2), "meters")

    difference = alternate_distance - original_distance

    print("\n--- Disruption Analysis ---")
    print("Original distance:", round(original_distance, 2), "meters")
    print("Alternate distance:", round(alternate_distance, 2), "meters")
    print("Extra distance:", round(difference, 2), "meters")

    if original_distance > 0:
        percentage = (difference / original_distance) * 100
        print("Route increase:", round(percentage, 2), "%")

except nx.NetworkXNoPath:

    print("\nNo alternate route available!")
    print("The road closure disconnects the destination.")

print("\nRoad disruption simulation completed!")