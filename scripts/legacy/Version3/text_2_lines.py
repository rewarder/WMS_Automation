import pathlib
import math
import ezdxf
from ezdxf.addons import text2path
from ezdxf.gfxattribs import GfxAttribs
from ezdxf.fonts import fonts
from ezdxf.math import Matrix44
from ezdxf import zoom, path

def extract_text_and_positions(input_file):
    text_content = []
    positions = []
    heights = []
    rotations = []

    doc = ezdxf.readfile(input_file)
    msp = doc.modelspace()
    text_entities = msp.query("TEXT")

    for text_entity in text_entities:
        text_content.append(text_entity.dxf.text)
        positions.append(text_entity.dxf.insert)
        heights.append(text_entity.dxf.height)
        rotations.append(text_entity.dxf.rotation)

    return text_content, positions, heights, rotations

def text_to_boundary_lines(text_content, positions, heights, rotations, doc):
    msp = doc.modelspace()
    font = fonts.FontFace(family="TXT")

    for text, position, height, rotation in zip(text_content, positions, heights, rotations):
        rotation_radians = math.radians(rotation)
        transform_matrix = Matrix44.chain(
            Matrix44.translate(0, 0, 0),
            Matrix44.z_rotate(rotation_radians),
            Matrix44.translate(position[0], position[1], 0)
        )

        paths = text2path.make_paths_from_str(text, font=font, size=height, m=transform_matrix)
        for path in paths:
            polyline = msp.add_lwpolyline(points=path.flattening(0.1), format='xyb')

    return doc


def polylines_to_lines(doc):
    msp = doc.modelspace()

    for polyline in msp.query("LWPOLYLINE"):
        vertices = list(polyline.vertices())
        # Store the color to apply it to the lines
        color = polyline.dxf.color
        # Remove the polyline after extracting its vertices
        msp.delete_entity(polyline)

        for i in range(len(vertices) - 1):
            start_point = vertices[i]
            end_point = vertices[i + 1]

            line = msp.add_line(start_point, end_point)
            line.dxf.color = color

