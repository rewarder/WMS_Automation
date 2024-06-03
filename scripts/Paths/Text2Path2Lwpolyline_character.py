# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:07:05 2024

@author: m.buechel
"""

import ezdxf
from ezdxf.addons import text2path

# Create a DXF file object and get the current model space
doc = ezdxf.readfile("some_random_text.dxf")
msp = doc.modelspace()

# Create a function to convert a character to a path
def character_to_path(char, insertion_point, char_height, char_index):
    temp_doc = ezdxf.new("R2010", setup=True)
    temp_msp = temp_doc.modelspace()

    # Calculate the offset based on the character index
    char_offset = char_index * char_height

    # Create a temporary text entity in the temporary drawing at the adjusted insertion point
    temp_text_entity = temp_msp.add_text(char, dxfattribs={'insert': (insertion_point[0] + char_offset, insertion_point[1]),
                                                           'height': char_height})

    # Convert the inserted text entity into a path
    letter_path = text2path.make_path_from_entity(temp_text_entity)

    # Unlink the temporary text entity
    temp_text_entity.unlink_from_layout()

    # Close the temporary drawing object
    # temp_doc.close()

    # Flatten the path and get the vertices
    vertices = letter_path.flattening(100)

    return vertices

# Iterate through each text entity in the model space
for text_entity in msp.query('TEXT'):
    # Get the insertion point and height of the original text entity
    insertion_point = text_entity.dxf.insert
    char_height = text_entity.dxf.height

    # Iterate through each character in the text entity
    for char_index, char in enumerate(text_entity.dxf.text):
        # Convert each character to a path using the adjusted insertion point, character height, and index
        vertices = character_to_path(char, insertion_point, char_height, char_index)

        # Add the converted path vertices to the model space directly
        msp.add_lwpolyline(vertices)

# Save the DXF file with the converted text
doc.saveas("converted_text_separate_characters_high_accuracy.dxf")

