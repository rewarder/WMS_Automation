# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:56:57 2024

@author: m.buechel
"""

import ezdxf
from ezdxf.addons import text2path

# Define a function to convert a character to a path
def character_to_path(char, doc):
    # Create a model space object in the temporary drawing
    temp_msp = doc.modelspace()

    # Create a temporary text entity in the temporary drawing
    temp_text_entity = temp_msp.add_text(char, dxfattribs={'height': 1})  

    # Insert the temporary text entity into the main drawing
    letter_path = text2path.make_path_from_entity(temp_text_entity)  

    # Erase the temporary text entity
    # temp_text_entity.unlink_from_layout()

    return letter_path

# Define a function to extract the path for a single letter
def extract_path(text_entity, character, doc):
    # Convert the character to a path
    letter_path = character_to_path(character, doc)
    return letter_path

# Create a DXF file object and get the current model space
doc = ezdxf.readfile("some_random_text.dxf")
msp = doc.modelspace()

# Convert paths to lines
paths = []
for text_entity in msp.query('TEXT'):
    letter_paths = []

    # Extract the paths for each letter of the text
    for char in text_entity.dxf.text:
        letter_path = extract_path(text_entity, char, doc)
        letter_paths.append(letter_path)

    # Add the converted paths to the model space
    paths.append(letter_paths)

# Add the converted paths to the model space
for path_group in paths:
    for path in path_group:
        msp.add_lwpolyline(points=path.flattening(1))

# Save the DXF file with the converted text
doc.saveas("converted_text.dxf")
