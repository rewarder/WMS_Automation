import ezdxf
from ezdxf import path, zoom
from ezdxf.fonts import fonts
from ezdxf.document import Drawing
from ezdxf.path import Path
from ezdxf.render import forms
from ezdxf.addons import text2path
from ezdxf.math import Matrix44
import math
from concurrent.futures import ThreadPoolExecutor

# Hard coded link to the directory that contains the fonts which are to be rendered
ezdxf.options.support_dirs = ["C:/Users/mbuechel/Desktop/ToDo/Automation/WMS_Automation/scripts/Version9/font"]

# System font cache needs to be rebuilt
fonts.build_system_font_cache()

def render_txt(fontname: str, text: str, cap_height: float = 3.5):
    font = fonts.make_font(fontname, cap_height=cap_height)
    text_path = font.text_path(text)
    return text_path

def process_text_entity(msp, text_entity, fontname, kerning):
    text = text_entity.dxf.text
    cap_height = text_entity.dxf.height
    rotation = text_entity.dxf.rotation  # Rotation angle in degrees
    insert_point = text_entity.dxf.insert

    # Initialize X offset for character positioning
    x_offset = 0.0
    transforms = []

    for char in text:
        # Render individual character to path
        char_path = render_txt(fontname, char, cap_height)

        # Ensure char_path is a list of Path objects
        if not isinstance(char_path, list):
            char_path = [char_path]

        # Create transformation matrix for positioning and rotation around the insertion point
        rotation_radians = math.radians(rotation)  # Rotation angle in radians
        transform = Matrix44.chain(
            Matrix44.translate(0 + x_offset, 0, 0),
            Matrix44.z_rotate(rotation_radians),
            Matrix44.translate(insert_point[0], insert_point[1], 0)
        )

        # Store the transformations and character paths for later processing
        transforms.append((char_path, transform))

        # Update X offset for the next character, apply kerning
        x_offset += cap_height * kerning

    # Render polylines in the main thread after processing
    for char_path, transform in transforms:
        for path_item in char_path:
            for sub_path in path_item.sub_paths():
                polyline = msp.add_lwpolyline(sub_path.control_vertices(), dxfattribs={'layer': text_entity.dxf.layer})
                polyline.transform(transform)

    # Remove the original text entity
    msp.delete_entity(text_entity)

def convert_text_in_dxf(doc: Drawing) -> Drawing:
    fontname = "isocp.shx"
    kerning = 0.8  # Adjust the kerning factor as needed

    msp = doc.modelspace()

    # Collect all text entities to be converted
    text_entities = msp.query("TEXT")

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_text_entity, msp, text_entity, fontname, kerning)
            for text_entity in text_entities
        ]

        # Wait for all futures to complete
        for future in futures:
            future.result()  # You can handle exceptions here if needed

    # Adjust the view to fit the new content
    zoom.extents(msp)

    return doc
