import ezdxf
import fiona
from fiona.crs import CRS
from shapely.geometry import mapping, LineString, Point
from shapely.geometry.polygon import Polygon
import math
from collections import defaultdict

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

def dxf_to_shp(dxf_file, output_directory):
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()

    # We will use a defaultdict to create a dictionary of shapefiles, one for each geometry type
    shapefiles = defaultdict(lambda: {
        'schema': None,
        'crs': CRS.from_epsg(2056),
        'path': None,
        'layer': None
    })

    for entity in msp:
        geom_type = entity.dxftype()
        geom = None

        # Depending on the entity type, create the appropriate Shapely geometry
        if geom_type == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            geom = LineString([(start.x, start.y), (end.x, end.y)])
            schema_type = 'LineString'
        elif geom_type == 'POINT':
            point = entity.dxf.location
            geom = Point((point.x, point.y))
            schema_type = 'Point'
        elif geom_type == 'CIRCLE':
            center = entity.dxf.center
            radius = entity.dxf.radius
            geom = approximate_circle(center.x, center.y, radius)
            schema_type = 'Polygon'
        elif geom_type == 'ARC':
            center = entity.dxf.center
            radius = entity.dxf.radius
            start_angle = entity.dxf.start_angle
            end_angle = entity.dxf.end_angle
            geom = approximate_arc(center.x, center.y, radius, start_angle, end_angle)
            schema_type = 'LineString'

        if geom:
            # If we haven't created a shapefile for this geometry type yet, do so now
            if shapefiles[geom_type]['schema'] is None:
                shapefiles[geom_type]['schema'] = {
                    'geometry': schema_type,
                    'properties': {}
                }
                shapefiles[geom_type]['path'] = f"{output_directory}/{geom_type.lower()}.shp"
                shapefiles[geom_type]['layer'] = fiona.open(
                    shapefiles[geom_type]['path'],
                    'w',
                    'ESRI Shapefile',
                    schema=shapefiles[geom_type]['schema'],
                    crs=shapefiles[geom_type]['crs']
                )

            # Write the geometry to the appropriate shapefile
            shapefiles[geom_type]['layer'].write({
                'geometry': mapping(geom),
                'properties': {}
            })

    # Close all shapefile layers
    for info in shapefiles.values():
        if info['layer']:
            info['layer'].close()

if __name__ == "__main__":
    dxf_file_path = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/DXFtoSHP/desperate_his_fater.dxf"
    output_directory = "C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/DXFtoSHP/output07"
    dxf_to_shp(dxf_file_path, output_directory)
