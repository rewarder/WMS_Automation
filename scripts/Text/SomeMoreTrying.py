# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 15:56:23 2024

@author: m.buechel
"""

import ezdxf
from ezdxf.enums import TextEntityAlignment

# Create a DXFDocument object
doc = ezdxf.new("R2010", setup=True)
msp = doc.modelspace()

# Create a DXFText object
msp.add_text("A Simple Text").set_placement(
    (2, 3),
    align=TextEntityAlignment.MIDDLE_RIGHT
)

# Explode the text to lines
exploded_text = msp.

# Print the text objects
for line in exploded_text:
    print(line)
    
    
doc.saveas('simple_text.dxf')