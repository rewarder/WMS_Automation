# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 12:07:44 2024

@author: m.buechel
"""

import ezdxf
import ezdxf.path
from ezdxf.addons import text2path

# Load the DXF file
dwg = ezdxf.readfile("some_random_text.dxf")

# Get the current model space
msp = dwg.modelspace()

# Get all text entities in the model space
text_entities = msp.query('TEXT')

# Convert each text entity to paths
for text_entity in text_entities:
    # Convert the text to a Multi-Path object
    paths = text2path.make_paths_from_entity(text_entity)

    # Create a list of lines from the paths
    lines = [ezdxf.path.to_lines() for path in paths]

    # Add the lines to the model space
    for line_list in lines:
        msp.add_line_objects(line_list)

# Save the DXF file with the converted text
dwg.saveas("converted_text.dxf")