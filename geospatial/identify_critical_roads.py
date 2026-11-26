import networkx as nx
import pandas as pd

GRAPH_FILE = "data/processed/ujjain_weighted_graph.graphml"
OUTPUT_FILE = "data/processed/critical_roads.csv"

print("Loading weighted graph...")

G = nx.read_graphml(GRAPH_FILE)

print("Converting MultiGraph to Graph...")
simple_G = nx.Graph(G)

print("Calculating edge betweenness centrality...")

edge_betweenness = nx.edge_betweenness_centrality(
    simple_G,
    weight="length",
    normalized=True
)

print("Preparing road analysis...")

results = []

for u, v in simple_G.edges():

    edge_data = simple_G[u][v]

    length = edge_data.get("length", 0)

    betweenness = edge_betweenness.get((u, v))

    if betweenness is None:
        betweenness = edge_betweenness.get((v, u), 0)

    degree_u = simple_G.degree(u)
    degree_v = simple_G.degree(v)

    connectivity = degree_u + degree_v

    results.append({
        "node_u": str(u),
        "node_v": str(v),
        "length_m": length,
        "edge_betweenness": betweenness,
        "endpoint_connectivity": connectivity
    })

df = pd.DataFrame(results)

print("Normalizing metrics...")

def normalize(column):

    maximum = column.max()

    if maximum == 0:
        return column * 0

    return column / maximum

df["normalized_betweenness"] = normalize(
    df["edge_betweenness"]
)

df["normalized_length"] = normalize(
    df["length_m"]
)

df["normalized_connectivity"] = normalize(
    df["endpoint_connectivity"]
)

print("Calculating criticality score...")

df["criticality_score"] = (
    0.60 * df["normalized_betweenness"] +
    0.25 * df["normalized_length"] +
    0.15 * df["normalized_connectivity"]
)

df = df.sort_values(
    "criticality_score",
    ascending=False
)

df.to_csv(OUTPUT_FILE, index=False)

print("\n--- Critical Road Analysis ---")

print("Total road segments analyzed:", len(df))

print("\nTop 10 Critical Road Segments:")

print(
    df[[
        "node_u",
        "node_v",
        "length_m",
        "edge_betweenness",
        "criticality_score"
    ]].head(10).to_string(index=False)
)

print("\nCritical road analysis completed!")
print("Saved at:", OUTPUT_FILE)