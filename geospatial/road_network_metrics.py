import networkx as nx
import json

INPUT_FILE = "data/processed/ujjain_graph.json"

print("Loading graph data...")

with open(INPUT_FILE, "r") as file:
    graph_data = json.load(file)

G = nx.node_link_graph(graph_data, directed=True, multigraph=True)

print("\nCalculating network metrics...")

nodes = G.number_of_nodes()
edges = G.number_of_edges()

density = nx.density(G)

average_degree = sum(dict(G.degree()).values()) / nodes

undirected_graph = G.to_undirected()

components = list(nx.connected_components(undirected_graph))

largest_component = max(components, key=len)

print("\n===== ROAD NETWORK REPORT =====")
print("Total Nodes:", nodes)
print("Total Edges:", edges)
print("Network Density:", round(density, 6))
print("Average Degree:", round(average_degree, 2))
print("Connected Components:", len(components))
print("Largest Component Size:", len(largest_component))
print("==============================")