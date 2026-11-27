from pyproj import Transformer
from pathlib import Path

import networkx as nx
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    
    title="Urban Ripple Engine",
    description="AI-powered Urban Road Network Analysis",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

GRAPH_FILE = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "ujjain_weighted_graph.graphml"
)

# Convert UTM Zone 43N coordinates into latitude/longitude
transformer = Transformer.from_crs(
    "EPSG:32643",
    "EPSG:4326",
    always_xy=True
)


def convert_coordinates(x, y):
    longitude, latitude = transformer.transform(x, y)
    return [latitude, longitude]


def get_route_coordinates(G, route):
    coordinates = []

    for node in route:
        x = float(G.nodes[node]["x"])
        y = float(G.nodes[node]["y"])

        coordinates.append(convert_coordinates(x, y))

    return coordinates


def get_edge_coordinates(G, edges):
    coordinates = []

    for u, v in edges:
        x1 = float(G.nodes[u]["x"])
        y1 = float(G.nodes[u]["y"])

        x2 = float(G.nodes[v]["x"])
        y2 = float(G.nodes[v]["y"])

        coordinates.append([
            convert_coordinates(x1, y1),
            convert_coordinates(x2, y2)
        ])

    return coordinates
@app.get("/")
def root():
    return {
        "message": "Urban Ripple Engine API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/road-impact")
def road_impact(
    closures: int = Query(default=3, ge=1, le=10)
):

    if not GRAPH_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="Road network graph file not found"
        )

    print("Loading road network...")

    G = nx.read_graphml(GRAPH_FILE)

    nodes = list(G.nodes())

    if len(nodes) <= 100:
        raise HTTPException(
            status_code=500,
            detail="Not enough nodes in road network"
        )

    source = nodes[0]
    destination = nodes[100]

    print("Calculating original route...")

    try:
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

    except nx.NetworkXNoPath:
        raise HTTPException(
            status_code=400,
            detail="No original route available"
        )

    route_length = len(original_route)
    original_route_coordinates = get_route_coordinates(G, original_route)

    block_indices = [
            route_length // 4,
            route_length // 2,
            (3 * route_length) // 4
        ]
    
    blocked_edges = []

    for index in block_indices:
        if index + 1 < route_length:
            blocked_edges.append(
                (
                    original_route[index],
                    original_route[index + 1]
                )
            )
    
    blocked_road_coordinates = get_edge_coordinates(G, blocked_edges)
    G_disrupted = G.copy()

    print("Simulating road closures...")

    for u, v in blocked_edges:

        if not G_disrupted.has_edge(u, v):
            continue

        # Remove every parallel edge for a complete closure.
        if G_disrupted.is_multigraph():
            edge_keys = list(
                G_disrupted[u][v].keys()
            )

            for key in edge_keys:
                G_disrupted.remove_edge(u, v, key)

        else:
            G_disrupted.remove_edge(u, v)

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
        alternate_route_coordinates = get_route_coordinates(G_disrupted, alternate_route)

        extra_distance = (
            alternate_distance - original_distance
        )

        increase_percent = (
            extra_distance / original_distance * 100
            if original_distance else 0
        )

        if increase_percent <= 5:
            severity = "Low"
        elif increase_percent <= 15:
            severity = "Moderate"
        elif increase_percent <= 30:
            severity = "High"
        else:
            severity = "Severe"

        return {
            "original_distance_m": round(
                original_distance, 2
            ),
            "blocked_segments": len(blocked_edges),
            "alternate_distance_m": round(
                alternate_distance, 2
            ),
            "extra_distance_m": round(
                extra_distance, 2
            ),
            "increase_percent": round(
                increase_percent, 2
            ),
            "alternate_route_available": True,
            "alternate_route_nodes": len(
                alternate_route
            ),
            "impact_severity": severity,
            "original_route_coordinates": original_route_coordinates,
"blocked_road_coordinates": blocked_road_coordinates,
"alternate_route_coordinates": alternate_route_coordinates,
        }

    except nx.NetworkXNoPath:

        return {
            "original_distance_m": round(
                original_distance, 2
            ),
            "blocked_segments": len(blocked_edges),
            "alternate_distance_m": None,
            "extra_distance_m": None,
            "increase_percent": None,
            "alternate_route_available": False,
            "alternate_route_nodes": 0,
            "impact_severity": "Critical - No Route"
        }