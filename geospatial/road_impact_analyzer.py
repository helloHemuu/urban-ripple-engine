import networkx as nx
import pandas as pd

GRAPH_FILE = "data/processed/ujjain_weighted_graph.graphml"
OUTPUT_FILE = "data/processed/road_impact_report.csv"

print("Loading weighted road network...")
G = nx.read_graphml(GRAPH_FILE)

nodes = list(G.nodes())

source = nodes[0]
destination = nodes[100]

print("\nCalculating baseline route...")

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

# Select 3 road segments along the baseline route
route_length = len(original_route)

block_indices = [
    route_length // 4,
    route_length // 2,
    (3 * route_length) // 4
]

blocked_edges = []

for index in block_indices:

    if index + 1 < route_length:

        blocked_edges.append(
            (original_route[index], original_route[index + 1])
        )

print("\nSelected roads for disruption:", len(blocked_edges))

G_disrupted = G.copy()

for u, v in blocked_edges:

    if G_disrupted.has_edge(u, v):
        G_disrupted.remove_edge(u, v)

print("Analyzing disrupted network...")

report = {}

report["original_distance_m"] = original_distance
report["blocked_segments"] = len(blocked_edges)

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

    increase_percent = (
        extra_distance / original_distance * 100
    ) if original_distance else 0

    if increase_percent <= 5:
        severity = "Low"

    elif increase_percent <= 15:
        severity = "Moderate"

    elif increase_percent <= 30:
        severity = "High"

    else:
        severity = "Severe"

    report["alternate_distance_m"] = alternate_distance
    report["extra_distance_m"] = extra_distance
    report["increase_percent"] = increase_percent
    report["alternate_route_available"] = True
    report["alternate_route_nodes"] = len(alternate_route)
    report["impact_severity"] = severity

except nx.NetworkXNoPath:

    report["alternate_distance_m"] = None
    report["extra_distance_m"] = None
    report["increase_percent"] = None
    report["alternate_route_available"] = False
    report["alternate_route_nodes"] = 0
    report["impact_severity"] = "Critical - No Route"

print("\n--- ROAD IMPACT REPORT ---")

for key, value in report.items():

    if isinstance(value, float):
        value = round(value, 2)

    print(f"{key}: {value}")

print("\nSaving report...")

df = pd.DataFrame([report])

df.to_csv(OUTPUT_FILE, index=False)

print("\nRoad impact analysis completed!")
print("Report saved at:", OUTPUT_FILE)