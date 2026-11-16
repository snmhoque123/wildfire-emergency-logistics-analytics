"""Synthetic wildfire delivery scenario comparison. Standard library only.
Run: python python/analyze_routes.py from repository root.
NOT a real routing engine, live wildfire feed, or operational recommendation.
"""
import csv
import heapq
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(exist_ok=True)


def read_csv(name):
    with (DATA / name).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_csv(name, rows, columns):
    with (OUTPUT / name).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def shortest_path(start, end, edges, status_field):
    """Dijkstra weighted by illustrative travel hours; bidirectional graph."""
    graph = {}
    for edge in edges:
        if edge[status_field].lower() != "open":
            continue
        for u, v in [(edge["from_node"], edge["to_node"]),
                     (edge["to_node"], edge["from_node"])]:
            graph.setdefault(u, []).append((v, float(edge["planning_hours"]), edge))
    queue = [(0.0, start, [], [])]
    best = {}
    while queue:
        hours, node, path, used_edges = heapq.heappop(queue)
        if hours >= best.get(node, float("inf")):
            continue
        best[node] = hours
        if node == end:
            return path + [node], used_edges, hours
        for neighbor, edge_hours, edge in graph.get(node, []):
            if hours + edge_hours < best.get(neighbor, float("inf")):
                heapq.heappush(queue, (hours + edge_hours, neighbor,
                                       path + [node], used_edges + [edge]))
    return None, [], None


def main():
    nodes = read_csv("nodes.csv")
    edges = read_csv("road_edges.csv")
    origins = read_csv("origins.csv")
    scenarios = read_csv("scenarios.csv")
    node_lookup = {n["node_id"]: n for n in nodes}
    assert len(node_lookup) == len(nodes), "Duplicate node IDs"
    assert len({e["edge_id"] for e in edges}) == len(edges), "Duplicate edge IDs"
    for edge in edges:
        assert edge["from_node"] in node_lookup and edge["to_node"] in node_lookup
        assert float(edge["planning_hours"]) > 0 and float(edge["planning_km"]) > 0

    comparisons, routes, segments = [], [], []
    for scenario in scenarios:
        sid = scenario["scenario_id"]
        status_field = scenario["edge_status_field"]
        destination = scenario["destination_id"]
        required = int(scenario["required_cases"])
        deadline = float(scenario["max_delivery_hours"])
        candidates = []
        for origin in origins:
            oid = origin["origin_id"]
            stock = int(origin["available_cases"])
            path, path_edges, travel = shortest_path(oid, destination, edges, status_field)
            record = dict(scenario_id=sid, origin_id=oid,
                          destination_id=destination, required_cases=required,
                          route_path="", route_km="", travel_hours="",
                          estimated_delivery_hours="", delivered_cost_per_case="",
                          estimated_total_cost="", status="", selected=False)
            if stock < required:
                record["status"] = "INSUFFICIENT_STOCK"
            elif path is None:
                record["status"] = "NO_OPEN_ROUTE"
            else:
                km = sum(float(e["planning_km"]) for e in path_edges)
                dispatch = float(origin["dispatch_hours"])
                hours = travel + dispatch
                unit = (float(origin["dead_net_per_case"])
                        - float(origin["pickup_allowance_per_case"])
                        + float(origin["handling_per_case"])
                        + km * float(origin["freight_rate_per_km"]) / required)
                cost = unit * required
                record.update(route_path=" > ".join(path), route_km=round(km, 2),
                              travel_hours=round(travel, 2),
                              estimated_delivery_hours=round(hours, 2),
                              delivered_cost_per_case=round(unit, 2),
                              estimated_total_cost=round(cost, 2),
                              status="FEASIBLE" if hours <= deadline else "LATE")
                for a, b, edge in zip(path[:-1], path[1:], path_edges):
                    segments.append(dict(scenario_id=sid, origin_id=oid,
                                         from_node=a, to_node=b,
                                         edge_id=edge["edge_id"],
                                         from_lat=node_lookup[a]["latitude"],
                                         from_lon=node_lookup[a]["longitude"],
                                         to_lat=node_lookup[b]["latitude"],
                                         to_lon=node_lookup[b]["longitude"],
                                         selected=False))
                candidates.append(record)
            comparisons.append(record)
        feasible = [r for r in candidates if r["status"] == "FEASIBLE"]
        if feasible:
            selected = min(feasible, key=lambda r: (r["estimated_delivery_hours"],
                                                   r["estimated_total_cost"]))
            selected["selected"] = True
            routes.append(dict(scenario_id=sid, origin_id=selected["origin_id"],
                               destination_id=destination, route_path=selected["route_path"],
                               route_km=selected["route_km"],
                               estimated_delivery_hours=selected["estimated_delivery_hours"],
                               estimated_total_cost=selected["estimated_total_cost"]))
            for segment in segments:
                if segment["scenario_id"] == sid and segment["origin_id"] == selected["origin_id"]:
                    segment["selected"] = True
        else:
            routes.append(dict(scenario_id=sid, origin_id="NO_FEASIBLE_OPTION",
                               destination_id=destination, route_path="", route_km="",
                               estimated_delivery_hours="", estimated_total_cost=""))

    write_csv("scenario_comparison.csv", comparisons,
              list(comparisons[0]))
    write_csv("selected_routes.csv", routes, list(routes[0]))
    write_csv("route_segments.csv", segments, list(segments[0]))

    locations = []
    for n in nodes:
        locations.append(dict(type="Feature", properties={k:v for k,v in n.items() if k not in ("latitude","longitude")},
                              geometry=dict(type="Point", coordinates=[float(n["longitude"]),float(n["latitude"])])))
    (OUTPUT / "demo_locations.geojson").write_text(json.dumps(dict(type="FeatureCollection",features=locations),indent=2))
    lines = []
    for s in segments:
        lines.append(dict(type="Feature", properties={k:v for k,v in s.items() if k not in ("from_lat","from_lon","to_lat","to_lon")},
                          geometry=dict(type="LineString", coordinates=[
                              [float(s["from_lon"]),float(s["from_lat"])],
                              [float(s["to_lon"]),float(s["to_lat"])]])))
    (OUTPUT / "demo_route_segments.geojson").write_text(json.dumps(dict(type="FeatureCollection",features=lines),indent=2))
    for r in routes:
        print(f"{r['scenario_id']}: {r['origin_id']} -> {r['destination_id']}; {r['estimated_delivery_hours']} hr; ${r['estimated_total_cost']}")


if __name__ == "__main__":
    main()
