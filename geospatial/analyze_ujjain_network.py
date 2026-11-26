import geopandas as gpd
import networkx as nx
import pandas as pd

INPUT_FILE = "data/raw/ujjain_roads.gpkg"
OUTPUT_FILE = "data/processed/ujjain_network_analysis.csv"

print("Loading Ujjain road data...")
roads = gpd.read_file(INPUT_FILE)

print("Building road network graph...")

G = nx.Graph()

for _, row in roads.iterrows():
    geometry = row.geometry
    coordinates = list(geometry.coords)

    start_node = coordinates[0]
    end_node = coordinates[-1]

    G.add_edge(
        start_node,
        end_node,
        length=row["length"],
        road_name=row["name"],
        road_type=row["highway"]
    )

print("\nCalculating network statistics...")

degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G, weight="length")

results = []

for node in G.nodes():
    results.append({
        "node": str(node),
        "degree_centrality": degree_centrality[node],
        "betweenness_centrality": betweenness_centrality[node]
    })

df = pd.DataFrame(results)

df = df.sort_values(
    by="betweenness_centrality",
    ascending=False
)

df.to_csv(OUTPUT_FILE, index=False)

print("\nNetwork Analysis Completed!")
print("Total Nodes:", G.number_of_nodes())
print("Total Edges:", G.number_of_edges())

print("\nTop 10 Important Network Nodes:")
print(df.head(10).to_string(index=False))

print("\nAnalysis saved to:", OUTPUT_FILE)