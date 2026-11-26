import geopandas as gpd
import networkx as nx
import pandas as pd

INPUT_FILE = "data/raw/ujjain_roads.gpkg"
OUTPUT_FILE = "data/processed/ujjain_proper_graph.graphml"

print("Loading road data...")

roads = gpd.read_file(INPUT_FILE)

print("Preparing road network...")

G = nx.MultiDiGraph()

for _, row in roads.iterrows():

    geometry = row.geometry
    coordinates = list(geometry.coords)

    start_node = coordinates[0]
    end_node = coordinates[-1]

    length = row["length"]

    road_type = row["highway"]
    road_name = row["name"]

    G.add_node(start_node, x=start_node[0], y=start_node[1])
    G.add_node(end_node, x=end_node[0], y=end_node[1])

    G.add_edge(
        start_node,
        end_node,
        length=length,
        highway=str(road_type),
        name=str(road_name)
    )

    G.add_edge(
        end_node,
        start_node,
        length=length,
        highway=str(road_type),
        name=str(road_name)
    )

print("\nGraph successfully constructed!")

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

print("\nSaving graph...")

ox_placeholder = None

graph_data = nx.node_link_data(G)

import json

with open("data/processed/ujjain_graph.json", "w") as file:
    json.dump(graph_data, file, default=str)

print("\nGraph saved successfully!")