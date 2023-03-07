import arcpy

# Set the workspace environment to the folder containing the shapefiles
arcpy.env.workspace = "D:/Airports"

# Define the input and output shapefile names
polygons_name = "provinces/mn871sp9778.shp"
airports_name = "airport/italy_airport_point.shp"
output_name = "polygons_with_counts.shp"

# Read in the polygon shapefile
polygons = arcpy.MakeFeatureLayer_management(polygons_name)

# Read in the point shapefile
points = arcpy.MakeFeatureLayer_management(airports_name)

# Add a new field to the polygons feature class to hold the point count
arcpy.AddField_management(polygons, "air_count", "LONG")

# Loop through each polygon and update the point count field
with arcpy.da.UpdateCursor(polygons, ["SHAPE@", "air_count"]) as cursor:
    for row in cursor:
        polygon_geometry = row[0]
        selected_points = arcpy.SelectLayerByLocation_management(points, "WITHIN", polygon_geometry)
        point_count = int(arcpy.GetCount_management(selected_points).getOutput(0))
        row[1] = point_count
        cursor.updateRow(row)

# Copy the polygons feature class to a new feature class with the point count field
arcpy.CopyFeatures_management(polygons, output_name)


