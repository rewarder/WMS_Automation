# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 09:12:21 2024

@author: m.buechel
"""

import ezdxf
from ezdxf.addons import text2path
import os

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the file path using the script directory
file_path = os.path.join(script_dir, "some__more_random_text.dxf")  # Update filename if needed

# Read the DXF file
doc = ezdxf.readfile(file_path)
msp = doc.modelspace()

# Convert paths to lines
paths = []
for text_entity in msp.query('TEXT'):
    paths.append(text2path.make_path_from_entity(text_entity))

# Add the converted paths to the model space
for path in paths:
    msp.add_lwpolyline(points=path.flattening(1))

# Build the save path using the script directory and a new filename
save_path = os.path.join(script_dir, "converted_text.dxf")  # Update filename if desired

# Save the DXF file with the converted text
doc.saveas(save_path)
