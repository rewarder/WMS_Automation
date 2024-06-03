import ezdxf
from ezdxf.math import Vec3

def spline_to_lines(spline, segments=100):
    """
    Convert a spline to individual lines by sampling points along the spline.
    
    :param spline: The spline entity to convert.
    :param segments: Number of segments to approximate the spline.
    :return: A list of new line entities approximating the spline.
    """
    points = [Vec3(spline.point_at(t / segments)) for t in range(segments + 1)]
    lines = []
    for start, end in zip(points[:-1], points[1:]):
        line = spline.doc.modelspace().add_line(start, end, dxfattribs={
            'layer': spline.dxf.layer,
            'color': spline.dxf.color,
            'linetype': spline.dxf.linetype,
            'lineweight': spline.dxf.lineweight,
        })
        lines.append(line)
    return lines

def convert_splines_to_lines(doc, segments=100):
    """
    Convert all splines in the document to individual lines.
    
    :param doc: The DXF document.
    :param segments: Number of segments to approximate each spline.
    """
    modelspace = doc.modelspace()
    splines = modelspace.query('SPLINE')
    for spline in splines:
        lines = spline_to_lines(spline, segments)
        modelspace.delete_entity(spline)

# Load the DXF document
doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Splines/modified_GD1_ELE_RUB_Ausführung GD1 7.OG 50__GEOREF.dxf")

# Convert all splines to lines
convert_splines_to_lines(doc)

# Save the modified DXF document
doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Splines/converted_modified_GD1_ELE_RUB_Ausführung GD1 7.OG 50__GEOREF.dxf")
