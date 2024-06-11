import ezdxf
from ezdxf.addons import text2path
from ezdxf.math import Matrix44
import math

def process_dxf(input_file, output_file):
    doc = ezdxf.readfile(input_file)
    msp = doc.modelspace()

    font = text2path.FontFace(font='simplex.shx')  # Define the font

    for text_entity in msp.query('TEXT'):
        text_content = text_entity.dxf.text
        position = (text_entity.dxf.insert[0], text_entity.dxf.insert[1])
        height = text_entity.dxf.height
        rotation = text_entity.dxf.rotation

        rotation_radians = math.radians(rotation)
        transform_matrix = Matrix44.chain(
            Matrix44.translate(0, 0, 0),
            Matrix44.z_rotate(rotation_radians),
            Matrix44.translate(position[0], position[1], 0)
        )

        paths = text2path.make_paths_from_str(text_content, font=font, size=height, m=transform_matrix)
        for path in paths:
            points = []
            for segment in path:
                for start, end in zip(segment[:-1], segment[1:]):
                    points.append(start)
                    points.append(end)
            if points:
                polyline = msp.add_lwpolyline(points=points, format='xyb')

    doc.saveas(output_file)

# Input and output file paths
input_file = 'C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/Text/input.dxf'
output_file = 'C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/Text/output.dxf'

process_dxf(input_file, output_file)
