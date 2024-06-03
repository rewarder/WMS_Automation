# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 16:43:18 2024

@author: m.buechel
"""

import ezdxf 
import random # need for random placing points

def get_random_point():
    """Returns random x, y coordinates."""
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    return x, y

# Create a new drawing AutoCAD 2010
doc = ezdxf.new('R2010')

# Create a block with the name 'FLAG'
flag = doc.blocks.new(name='FLAG')

# Add DXF entities to the block 'FLAG'
# The default base point (= insertion point) of the block is (0, 0)
flag.add_lwpolyline([(0, 0), (0, 5), (4, 3), (0, 3)]) # the flag symbol as 2D polyline
flag.add_circle((0, 0), .4, dxfattribs={'color': 2}) # mark the base point with a circle

# Get the modelspace of the drawing
msp = doc.modelspace()

# Get 50 random placing points
placing_points = [get_random_point() for _ in range(50)]

for point in placing_points:
    # Every flag has a different scaling and a rotation of -15deg
    random_scale = 0.5 + random.random() * 2.0
    # Add a block reference to the block named 'FLAG' at the coordinates 'point'
    msp.add_blockref('FLAG', point, dxfattribs={
        'xscale': random_scale,
        'yscale': random_scale,
        'rotation': -30
    })

doc.saveas('Blocks_30deg.dxf')