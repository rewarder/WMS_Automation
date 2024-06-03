# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 11:48:57 2024

@author: m.buechel
"""

import ezdxf
from ezdxf.addons import text2path, multipath

# Create a DXF file object and get the current model space
doc = ezdxf.readfile("some_random_text.dxf")
msp = doc.modelspace()

# Create a function to convert a character to a path
def character_to_path(char, insertion_point, char_height):
    temp_doc = ezdxf.new("R2010", setup=True)
    temp_msp = temp_doc.modelspace()

    # Create a temporary text entity in the temporary drawing at the adjusted insertion point
    temp_msp.add_text(char, dxfattribs={'insert': insertion_point, 'height': char_height})

    # Convert the inserted text entity into a path
    letter_path = text2path.make_path_from_entity(temp_msp.query('TEXT')[0])

    # Unlink the temporary text entity
    temp_msp.delete_all_entities()

    return letter_path

# Iterate through each text entity in the model space
for text_entity in msp.query('TEXT'):
    # Get the insertion point and height of the original text entity
    insertion_point = text_entity.dxf.insert
    char_height = text_entity.dxf.height

    # Iterate through each character in the text entity
    for char in text_entity.dxf.text:
        # Convert each character to a path using the adjusted insertion point and character height
        letter_path = character_to_path(char, insertion_point, char_height)

        # Convert the path to a polyline
        polyline = multipath.to_polylines(letter_path.flattening(0.1))[0]

        # Add the converted polyline to the model space
        msp.add_lwpolyline(points=polyline)

# Save the DXF file with the converted text
doc.saveas("converted_text_separate_characters_paths.dxf")
