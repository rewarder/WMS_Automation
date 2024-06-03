# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 11:31:11 2024

@author: m.buechel
"""

import ezdxf
from ezdxf.addons import text2path
from ezdxf.enums import TextEntityAlignment

# Create a new DXF file
dwg = ezdxf.new("R12", setup=True)

# Get the current model space
msp = dwg.modelspace()

# Add Text
text_entity = msp.add_text("A Simple Text").set_placement(
    (2, 3),
    align=TextEntityAlignment.MIDDLE_RIGHT
)

# Create a text entity and set its properties
# text_entity = dwg.entities.new('TEXT', insert=(0, 0), text='Hello, World!', height=2, layer='TEXT')

# Create a path object from the text entity
line = text2path.path.to_lines(text_entity)

# Add the path to the model space
msp.add_line(line[0], line[1])

# Save the DXF file
dwg.saveas("paths.dxf")