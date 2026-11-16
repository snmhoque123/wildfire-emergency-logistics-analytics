# QGIS mapping recipe

1. Run `python python/analyze_routes.py`.
2. Open the generated GeoJSON layers directly in QGIS (no additional R packages).
3. Open `outputs/demo_locations.geojson` and `outputs/demo_route_segments.geojson` in QGIS.
4. Style `origin` nodes, `destination` nodes and intermediate `junction` nodes differently.
5. Filter route segments by `scenario_id`, and color by `status` or `selected`.
6. Add an annotation: **Synthetic planning graph; connectors are NOT actual roads.**
7. Export a map layout for GitHub with this disclaimer visible.

## Production adaptation (not provided by this demo)
Load road-network geometries from an approved provider; reproject into an appropriate
local projected CRS for distance calculations; verify closure and access restrictions;
use QGIS Network Analysis or an approved routing engine; validate travel times,
vehicle types, site locations, permissions, closures and freshness with operations.
Real-time emergency routing requires officially verified conditions and human oversight.
