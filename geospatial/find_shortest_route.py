import networkx as nx

INPUT_FILE = "data/processed/ujjain_split_graph.graphml"

print("Loading road graph...")

G = nx.read_graphml(INPUT_FILE)

print("Graph loaded successfully!")

# Select two sample nodes
nodes = list(G.nodes())

source = nodes[0]
destination = nodes[100]

print("\nStarting route calculation...")

try:
    route = nx.shortest_path(
        G,
        source=source,
        target=destination
    )

    print("\nRoute found successfully!")

    print("Starting Node:", source)
    print("Destination Node:", destination)
    print("Number of nodes in route:", len(route))

    print("\nRoute nodes:")

    for node in route:
        print(node)

except nx.NetworkXNoPath:
    print("No route found between these nodes.")

print("\nRouting process completed!")