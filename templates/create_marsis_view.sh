#!/bin/bash
# $1 -> dbname

PSQL_COMMAND="psql -U marsis -w -d $1 -c "

# Points view with -180 < lon < 180
$PSQL_COMMAND "CREATE MATERIALIZED VIEW orbit_points_180 AS SELECT ST_Shift_Longitude(wkb_geometry) as  hhh  FROM orbit_point;"

$PSQL_COMMAND "CREATE UNIQUE INDEX orbit_points_180_u_idx ON orbit_points_180 (orbitnumber, operationmode, point_id)"

$PSQL_COMMAND "CREATE INDEX orbit_points_180_idx ON orbit_points_180 using gist (points_geometry)"

$PSQL_COMMAND "GRANT SELECT ON orbit_points_180 TO marsisuser"

# Lines view
$PSQL_COMMAND "CREATE MATERIALIZED VIEW orbit_lines AS SELECT orbitnumber, operationmode, ST_MakeLine(wkb_geometry) as lines_geometry  FROM orbit_point GROUP BY orbitnumber,  operationmode"

$PSQL_COMMAND "CREATE UNIQUE INDEX orbit_lines_u_idx ON orbit_lines (orbitnumber, operationmode)"

$PSQL_COMMAND "CREATE INDEX orbit_lines_idx ON orbit_lines using gist (lines_geometry)"

$PSQL_COMMAND "GRANT SELECT ON orbit_lines TO marsisuser"

# Lines view 180
$PSQL_COMMAND "CREATE MATERIALIZED VIEW orbit_lines_180 AS SELECT orbitnumber, operationmode, ST_Shift_Longitude(ST_MakeLine(wkb_geometry)) as lines_geometry  FROM orbit_point GROUP BY orbitnumber,  operationmode"

$PSQL_COMMAND "CREATE UNIQUE INDEX orbit_lines_180_u_idx ON orbit_lines_180 (orbitnumber, operationmode)"

$PSQL_COMMAND "CREATE INDEX orbit_lines_180_idx ON orbit_lines_180 using gist (lines_geometry)"

$PSQL_COMMAND "GRANT SELECT ON orbit_lines_180 TO marsisuser"

# Medusae Fossae
. create_roi_views.sh $1 medusaefossae -167.97704 -8.12635 -153.19333 1.83659


