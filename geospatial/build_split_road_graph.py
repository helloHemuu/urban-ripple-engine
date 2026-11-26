import geopandas as gpd
import networkx as nx

INPUT_FILE = "data/processed/ujjain_split_roads.gpkg"
OUTPUT_FILE = "data/processed/ujjain_weighted_graph.graphml"

print("Loading split roads...")
roads = gpd.read_file(INPUT_FILE)

print("Projecting roads to metric coordinate system...")
roads = roads.to_crs(epsg=32643)

print("Building weighted road graph...")
G = nx.MultiGraph()

for _, row in roads.iterrows():

    geometry = row.geometry

    if geometry is None:
        continue

    coordinates = list(geometry.coords)

    if len(coordinates) < 2:
        continue

    start = coordinates[0]
    end = coordinates[-1]

    start_node = (round(start[0], 3), round(start[1], 3))
    end_node = (round(end[0], 3), round(end[1], 3))

    length_m = geometry.length

    G.add_node(start_node, x=start_node[0], y=start_node[1])
    G.add_node(end_node, x=end_node[0], y=end_node[1])

    G.add_edge(
        start_node,
        end_node,
        length=length_m
    )

print("Saving weighted graph...")
nx.write_graphml(G, OUTPUT_FILE)

print("\nWeighted graph created successfully!")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print("Graph saved at:", OUTPUT_FILE)