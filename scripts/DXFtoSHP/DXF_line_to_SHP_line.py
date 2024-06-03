import ezdxf
import fiona
from fiona.crs import from_epsg
from shapely.geometry import mapping, LineString, Point
from shapely.geometry.polygon import Polygon
import math

def approximate_circle(center_x, center_y, radius, num_points=64):
    """Approximate a circle with a polygon with a given number of points."""
    angle_step = 2 * math.pi / num_points
    return Polygon(
        [(center_x + math.cos(angle) * radius, center_y + math.sin(angle) * radius)
         for angle in (i * angle_step for i in range(num_points))]
    )

def approximate_arc(center_x, center_y, radius, start_angle, end_angle, num_points=64):
    """Approximate an arc with a LineString with a given number of points."""
    angle_step = (end_angle - start_angle) / max(num_points, 1)
    return LineString(
        [(center_x + math.cos(math.radians(start_angle + angle)) * radius, 
          center_y + math.sin(math.radians(start_angle + angle)) * radius)
         for angle in (i * angle_step for i in range(num_points + 1))]
    )

def dxf_to_shp(dxf_file, shp_file):
    # Read the DXF file
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()

    # Define the schema for the SHP file
    schema = {
        'geometry': 'Unknown',
        'properties': {}  # Add your properties here
    }

    # Define the EPSG code for your shapefile
    crs = from_epsg(2056)  # WGS84 - you may need to change this

    # Open a Fiona object to write the SHP file
    with fiona.open(shp_file, 'w', 'ESRI Shapefile', schema, crs=crs) as layer:
        # Loop through entities in the DXF model space
        for entity in msp:
            if entity.dxftype() == 'LINE':
                # Handle LINE entity as before
                # Create a Shapely LineString geometry
                start = entity.dxf.start
                end = entity.dxf.end
                line = LineString([(start.x, start.y), (end.x, end.y)])

                # Write the geometry to the SHP file
                layer.write({
                    'geometry': mapping(line),
                    'properties': {},  # Add your properties here
                })
            elif entity.dxftype() == 'POINT':
                # Handle POINT entity as before
                # Create a Shapely Point geometry
                point = Point(entity.dxf.location.x, entity.dxf.location.y)

            elif entity.dxftype() == 'CIRCLE':
                # Approximate the CIRCLE with a polygon
                center = entity.dxf.center
                radius = entity.dxf.radius
                circle = approximate_circle(center.x, center.y, radius)

                # Write the geometry to the SHP file
                layer.write({
                    'geometry': mapping(circle),
                    'properties': {},  # Add your properties here
                })
            elif entity.dxftype() == 'ARC':
                # Approximate the ARC with a LineString
                center = entity.dxf.center
                radius = entity.dxf.radius
                start_angle = entity.dxf.start_angle
                end_angle = entity.dxf.end_angle
                arc = approximate_arc(center.x, center.y, radius, start_angle, end_angle)
                layer.write({
                    'geometry': mapping(arc),
                    'properties': {},  # Add your properties here
                })
        # Add additional elif blocks for other entity types as needed

if __name__ == "__main__":
    dxf_file_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/DXFtoSHP/multiple_Lines.dxf"
    shp_file_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/DXFtoSHP/ouput_V6.shp"
    dxf_to_shp(dxf_file_path, shp_file_path)