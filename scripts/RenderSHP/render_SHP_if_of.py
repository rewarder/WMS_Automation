import ezdxf
from ezdxf import path, zoom
from ezdxf.fonts import fonts
from ezdxf.document import Drawing
from ezdxf.path import Path
from ezdxf.render import forms
from ezdxf.addons import text2path
from ezdxf.math import Matrix44
import math

# Hard coded link to the directory that contains the fonts which are to be rendered
ezdxf.options.support_dirs = ["C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/dxfsupport"]

# System font cache needs to be rebuilt
fonts.build_system_font_cache()

def render_txt(fontname: str, text: str, cap_height: float = 3.5):
    font = fonts.make_font(fontname, cap_height=cap_height)
    text_path = font.text_path(text)
    return text_path

def convert_text_in_dxf(input_dxf: str, output_dxf: str, fontname: str):
    doc = ezdxf.readfile(input_dxf)
    msp = doc.modelspace()

    # Collect all text entities to be converted
    text_entities = msp.query("TEXT")

    for text_entity in text_entities:
        text = text_entity.dxf.text
        cap_height = text_entity.dxf.height
        rotation = text_entity.dxf.rotation  # Rotation angle in degrees

        # Render text to path
        text_path = render_txt(fontname, text, cap_height)

        # Ensure text_path is a list of Path objects
        if not isinstance(text_path, list):
            text_path = [text_path]

        # Get the insertion point of the text entity
        insert_point = text_entity.dxf.insert

        # Create transformation matrix for rotation around the insertion point
        rotation_radians = math.radians(rotation) # roataion angle in radians
        transform = Matrix44.chain(
            Matrix44.translate(0, 0, 0),
            Matrix44.z_rotate(rotation_radians),
            Matrix44.translate(insert_point[0], insert_point[1], 0)
        )

        # Render polylines
        try:
            for path_item in text_path:
                for sub_path in path_item.sub_paths():
                    polyline = msp.add_lwpolyline(sub_path.control_vertices(), dxfattribs={'layer': text_entity.dxf.layer})
                    polyline.transform(transform)
        except Exception as e:
            print(f"Error rendering polylines: {e}")
            continue

        # Remove the original text entity
        msp.delete_entity(text_entity)

    # Adjust the view to fit the new content
    zoom.extents(msp)

    # Save the modified DXF
    doc.saveas(output_dxf)

# Example usage
input_dxf = "C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/RenderSHP/splines_text_only.dxf"
output_dxf = "C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/RenderSHP/output_isocp.dxf"
fontname = "isocp.shx"

convert_text_in_dxf(input_dxf, output_dxf, fontname)
