import networkx as nx

INPUT_FILE = "data/processed/ujjain_split_graph.graphml"

print("Loading split road graph...")

G = nx.read_graphml(INPUT_FILE)

print("Graph loaded successfully!")

print("\nAnalyzing connectivity...")

nodes = G.number_of_nodes()
edges = G.number_of_edges()

components = list(nx.connected_components(G))

largest_component = max(components, key=len)

density = nx.density(G)

average_degree = sum(dict(G.degree()).values()) / nodes

print("\n===== IMPROVED ROAD NETWORK REPORT =====")
print("Total Nodes:", nodes)
print("Total Edges:", edges)
print("Network Density:", round(density, 6))
print("Average Degree:", round(average_degree, 2))
print("Connected Components:", len(components))
print("Largest Component Size:", len(largest_component))
print("Largest Component Percentage:", round((len(largest_component) / nodes) * 100, 2), "%")
print("======================================")