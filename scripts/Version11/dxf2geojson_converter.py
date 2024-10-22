import ezdxf
from shapely.geometry import LineString
import geojson
import math

def convert_dxf_to_geojson(dxf_data, geojson_file):
    """
    Convert DXF entities to GeoJSON format and save to a file.

    :param dxf_data: Path to the DXF file.
    :param geojson_file: Path to the output GeoJSON file.
    """
    COLOR_INDEX_TO_HEX = {
        1: "#FF0000",      # red
        2: "#FFFF00",      # yellow
        3: "#00FF00",      # green
        4: "#00FFFF",      # cyan
        5: "#0000FF",      # blue
        6: "#FF00FF",      # magenta
        7: "#FFFFFF",      # white
        256: "bylayer",    # Special index meaning "by layer"
    }

    def get_color_hex(color_index):
        return COLOR_INDEX_TO_HEX.get(color_index, "#000000")  # Default to black for unknown colors

    def sample_circle(center, radius, num_points=75):
        return [
            (
                center[0] + radius * math.cos(2 * math.pi * i / num_points),
                center[1] + radius * math.sin(2 * math.pi * i / num_points),
            )
            for i in range(num_points)
        ]

    def sample_arc(center, radius, start_angle, end_angle, num_points=75):
        return [
            (
                center[0] + radius * math.cos(math.radians(start_angle + (end_angle - start_angle) * i / num_points)),
                center[1] + radius * math.sin(math.radians(start_angle + (end_angle - start_angle) * i / num_points)),
            )
            for i in range(num_points)
        ]

    def sample_ellipse(center, major_axis, minor_axis, start_param, end_param, num_points=75):
        return [
            (
                center[0] + major_axis * math.cos(param) * math.cos(end_param) - minor_axis * math.sin(param) * math.sin(end_param),
                center[1] + major_axis * math.cos(param) * math.sin(end_param) + minor_axis * math.sin(param) * math.cos(end_param),
            )
            for param in [start_param + (end_param - start_param) * i / num_points for i in range(num_points + 1)]
        ]

    # Read the DXF data from the file
    doc = ezdxf.readfile(dxf_data)
    features = []

    for entity in doc.entities:
        if entity.dxftype() == 'LINE':
            start = (entity.dxf.start.x, entity.dxf.start.y)
            end = (entity.dxf.end.x, entity.dxf.end.y)
            line = LineString([start, end])
        elif entity.dxftype() == 'CIRCLE':
            center = (entity.dxf.center.x, entity.dxf.center.y)
            radius = entity.dxf.radius
            points = sample_circle(center, radius)
            line = LineString(points)
        elif entity.dxftype() == 'ARC':
            center = (entity.dxf.center.x, entity.dxf.center.y)
            radius = entity.dxf.radius
            start_angle = entity.dxf.start_angle
            end_angle = entity.dxf.end_angle
            points = sample_arc(center, radius, start_angle, end_angle)
            line = LineString(points)
        elif entity.dxftype() == 'ELLIPSE':
            center = (entity.dxf.center.x, entity.dxf.center.y)
            major_axis = math.sqrt(entity.dxf.major_axis.x**2 + entity.dxf.major_axis.y**2)
            ratio = float(entity.dxf.ratio)
            minor_axis = major_axis * ratio
            start_param = entity.dxf.start_param
            end_param = entity.dxf.end_param
            points = sample_ellipse(center, major_axis, minor_axis, start_param, end_param)
            line = LineString(points)
        else:
            continue

        color_index = entity.dxf.color
        color_hex = get_color_hex(color_index)

        if color_hex == "bylayer" or color_hex == "#000000":
            layer_name = entity.dxf.layer
            layer = doc.layers.get(layer_name)
            if layer:
                layer_color_index = layer.dxf.color
                color_hex = get_color_hex(layer_color_index) if layer_color_index in COLOR_INDEX_TO_HEX else "#000000"

        feature = geojson.Feature(geometry=line, properties={"color": color_hex})
        features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    with open(geojson_file, 'w') as f:
        geojson.dump(feature_collection, f)
