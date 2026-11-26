import networkx as nx

INPUT_FILE = "data/processed/ujjain_split_graph.graphml"

print("Loading road graph...")

G = nx.read_graphml(INPUT_FILE)

print("Graph loaded!")

print("\nSample nodes for routing:\n")

nodes = list(G.nodes(data=True))

for i, (node_id, data) in enumerate(nodes[:20]):

    print(f"Node {i + 1}")
    print("Node ID:", node_id)
    print("Coordinates:", data)
    print("-" * 40)

print("\nTotal nodes:", G.number_of_nodes())