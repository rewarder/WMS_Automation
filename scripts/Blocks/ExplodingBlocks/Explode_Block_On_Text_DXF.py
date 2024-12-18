# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 11:36:14 2024

@author: m.buechel
"""
import ezdxf

# Load the DXF file
doc = ezdxf.readfile('C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/Text.dxf')

# Get the modelspace of the drawing
msp = doc.modelspace()

# Get all block references
blocks = msp.query('ACAD_BLOCK_RECORD')

# Explode each block reference
for block in blocks:
    msp.explode(block, True)

# Save the DXF file
doc.saveas('C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Blocks/Exploded_Text.dxf')