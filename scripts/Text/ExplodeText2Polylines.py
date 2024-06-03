# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 10:05:45 2024

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
    lines = ezdxf.path.to_lines(text_entity)
    
    # Add the exploded polylines to the model space
    for line in lines:
        msp.add_line(line[0], line[1])
    

# Save the DXF file with the converted text
dwg.saveas("converted_text.dxf")