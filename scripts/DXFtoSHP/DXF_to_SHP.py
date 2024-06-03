import math
import ezdxf
import fiona
from fiona.crs import from_epsg
from shapely.geometry import mapping, LineString, Point, Polygon

# Define the schema for the shapefile
# We'll use 'LineString' for lines and arcs, 'Polygon' for circles
schema = {
    'geometry': 'Unknown',  # 'Unknown' allows for different geometry types
    'properties': {'ID': 'int'},
}

# Define the EPSG code for your shapefile
crs = from_epsg(2056)  # 2056, you should change this to your coordinate system

# Read the DXF file
dxf = ezdxf.readfile('C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/DXFtoSHP/modified_input.dxf')

# Function to approximate a circle as a polygon
def approximate_circle(center, radius, num_points=64):
    angle_step = 2 * math.pi / num_points
    points = [
        (center.x + math.cos(i * angle_step) * radius,
         center.y + math.sin(i * angle_step) * radius)
        for i in range(num_points + 1)  # +1 to close the polygon
    ]
    return Polygon(points)

# Function to approximate an arc as a linestring
def approximate_arc(center, radius, start_angle, end_angle, num_points=64):
    angle_step = (end_angle - start_angle) / num_points
    points = [
        (center.x + math.cos(math.radians(start_angle + i * angle_step)) * radius,
         center.y + math.sin(math.radians(start_angle + i * angle_step)) * radius)
        for i in range(num_points + 1)
    ]
    return LineString(points)

# Prepare a function to extract geometries from the DXF, depending on the entity type
def extract_geometry(entity):
    if entity.dxftype() == 'LINE':
        return LineString([(entity.dxf.start.x, entity.dxf.start.y), (entity.dxf.end.x, entity.dxf.end.y)])
    elif entity.dxftype() == 'CIRCLE':
        center = entity.dxf.center
        radius = entity.dxf.radius
        return approximate_circle(center, radius)
    elif entity.dxftype() == 'ARC':
        center = entity.dxf.center
        radius = entity.dxf.radius
        start_angle = entity.dxf.start_angle
        end_angle = entity.dxf.end_angle
        return approximate_arc(center, radius, start_angle, end_angle)
    return None

# Create a new shapefile with Fiona
with fiona.open('C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/DXFtoSHP/DXF_to_SHP_output.shp', 'w', 'ESRI Shapefile', schema=schema, crs=crs) as output:
    # Iterate through all entities in the DXF model space
    for entity in dxf.modelspace():
        geom = extract_geometry(entity)
        if geom:
            output.write({
                'geometry': mapping(geom),
                'properties': {'ID': 0},  # You can populate this with real data if needed
            })

print("Conversion completed!")
