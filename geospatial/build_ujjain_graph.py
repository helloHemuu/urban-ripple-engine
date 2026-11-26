import geopandas as gpd
import networkx as nx

INPUT_FILE = "data/raw/ujjain_roads.gpkg"

print("Loading road data...")

roads = gpd.read_file(INPUT_FILE)

print("Building road network graph...")

G = nx.Graph()

for _, row in roads.iterrows():

    geometry = row.geometry

    coordinates = list(geometry.coords)

    start_node = coordinates[0]
    end_node = coordinates[-1]

    length = row["length"]

    G.add_node(start_node)
    G.add_node(end_node)

    G.add_edge(
        start_node,
        end_node,
        length=length,
        highway=row["highway"],
        name=row["name"]
    )

print("\nGraph created successfully!")

print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

print("\nGraph construction completed!")