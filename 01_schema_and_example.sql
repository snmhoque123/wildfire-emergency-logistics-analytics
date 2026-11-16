/* Illustrative schema for local SQL Server testing only.
   No Sysco schema, data, rates, contracts, or customer information is included. */
CREATE TABLE dbo.DemoLocations (
  node_id varchar(12) NOT NULL PRIMARY KEY,
  node_name varchar(100) NOT NULL,
  latitude float NOT NULL,
  longitude float NOT NULL,
  node_type varchar(20) NOT NULL
);
CREATE TABLE dbo.DemoRoadEdges (
  edge_id varchar(8) NOT NULL PRIMARY KEY,
  from_node varchar(12) NOT NULL,
  to_node varchar(12) NOT NULL,
  planning_km decimal(10,2) NOT NULL,
  planning_hours decimal(10,2) NOT NULL,
  normal_status varchar(12) NOT NULL,
  wildfire_status varchar(12) NOT NULL,
  relocation_status varchar(12) NOT NULL
);
-- Import the corresponding data/*.csv files using SSMS Import Flat File.
-- Example candidate edge table for a wildfire scenario:
SELECT e.edge_id, a.node_name AS from_location, b.node_name AS to_location,
       e.planning_km, e.planning_hours
FROM dbo.DemoRoadEdges AS e
JOIN dbo.DemoLocations AS a ON a.node_id = e.from_node
JOIN dbo.DemoLocations AS b ON b.node_id = e.to_node
WHERE e.wildfire_status = 'open'
ORDER BY e.edge_id;
-- The Python script performs route graph search and cost/urgency ranking.
-- Spatial point example (SQL Server geography, WGS84):
SELECT node_id, node_name,
       geography::Point(latitude, longitude, 4326) AS map_location
FROM dbo.DemoLocations;
