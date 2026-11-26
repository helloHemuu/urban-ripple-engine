from pyrosm import OSM

PBF_FILE = "data/raw/central-zone-latest.osm.pbf"

# Small Ujjain pilot area
BBOX = [75.78, 23.15, 75.80, 23.17]

print("Reading only the Ujjain pilot area...")

osm = OSM(
    PBF_FILE,
    bounding_box=BBOX
)

print("Extracting driving roads...")

roads = osm.get_network(
    network_type="driving"
)

print(f"Road segments found: {len(roads)}")

roads.to_file(
    "data/raw/ujjain_roads.gpkg",
    driver="GPKG"
)

print("Ujjain road network saved successfully!")