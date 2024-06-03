import ezdxf
import fiona
from fiona.crs import CRS
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
    line_schema = {
    'geometry': 'LineString',
    'properties': {}
    }

    point_schema = {
    'geometry': 'Point',
    'properties': {}
    }

    polygon_schema = {
    'geometry': 'Polygon',
    'properties': {}
    }


    # Define the EPSG code for your shapefile
    crs = CRS.from_epsg(2056)  # 2056 - you may need to change this

    # Then create separate Fiona objects for each type:
    with fiona.open(shp_file_path+'_lines.shp', 'w', 'ESRI Shapefile', schema=line_schema, crs=crs) as line_layer, \
    fiona.open(shp_file_path+'_points.shp', 'w', 'ESRI Shapefile', schema=point_schema, crs=crs) as point_layer, \
    fiona.open(shp_file_path+'_polygons.shp', 'w', 'ESRI Shapefile', schema=polygon_schema, crs=crs) as polygon_layer:


    # Open a Fiona object to write the SHP file
    with fiona.open(shp_file, 'w', 'ESRI Shapefile', schema, crs=crs) as layer:
        # Loop through entities in the DXF model space
        for entity in msp:
            if entity.dxftype() == 'LINE':
                # Create a Shapely LineString geometry
                start = entity.dxf.start
                end = entity.dxf.end
                line = LineString([(start.x, start.y), (end.x, end.y)])
                
                # Write the geometry to the SHP file
                line_layer.write({
                    'geometry': mapping(line),
                    'properties': {},  # Add your properties here
                })
            elif entity.dxftype() == 'POINT':
                # Create a Shapely Point geometry
                point = Point(entity.dxf.location.x, entity.dxf.location.y)
                
                # Write the geometry to the SHP file
                point_layer.write({
                    'geometry': mapping(point),
                    'properties': {},  # Add your properties here
                })
            elif entity.dxftype() == 'CIRCLE':
                # Approximate the CIRCLE with a polygon
                center = entity.dxf.center
                radius = entity.dxf.radius
                circle = approximate_circle(center.x, center.y, radius)

                # Write the geometry to the SHP file
                polygon_layer.write({
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
                polygon_layer.write({
                    'geometry': mapping(arc),
                    'properties': {},  # Add your properties here
                })
        # Add additional elif blocks for other entity types as needed

if __name__ == "__main__":
    dxf_file_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/DXFtoSHP/some_more_lines_and_a_circle_from_input.dxf"
    shp_file_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/DXFtoSHP/output_V10.shp"
    dxf_to_shp(dxf_file_path, shp_file_path)
