import geopandas as gpd
from shapely.geometry import Point

INPUT_FILE = "data/raw/ujjain_roads.gpkg"

print("Loading road data...")
roads = gpd.read_file(INPUT_FILE)

print("Checking road geometries...")

roads = roads.to_crs(epsg=32643)

intersection_points = []

for i, geom1 in enumerate(roads.geometry):

    for j in range(i + 1, len(roads.geometry)):

        geom2 = roads.geometry.iloc[j]

        intersection = geom1.intersection(geom2)

        if intersection.is_empty:
            continue

        if intersection.geom_type == "Point":
            intersection_points.append(intersection)

        elif intersection.geom_type == "MultiPoint":
            intersection_points.extend(list(intersection.geoms))

        elif intersection.geom_type == "GeometryCollection":
            for geom in intersection.geoms:
                if geom.geom_type == "Point":
                    intersection_points.append(geom)

print("\nIntersection checking completed!")

print("Road segments:", len(roads))
print("Intersection points detected:", len(intersection_points))