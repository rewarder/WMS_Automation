# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 16:08:25 2024

@author: m.buechel
"""

import ezdxf
from ezdxf.gfxattribs import GfxAttribs

doc = ezdxf.new()
doc.layers.add("ENTITY", color=2)
msp = doc.modelspace()
attribs = GfxAttribs(layer="ENTITY")

# create a point
point = msp.add_point((10, 10), dxfattribs=attribs)

# create a line
line = msp.add_line((0, 0), (10, 10), dxfattribs=attribs)

# create a circle
circle = msp.add_circle((10, 10), radius=3, dxfattribs=attribs)

# create an arc
arc = msp.add_arc((10, 10), radius=3, start_angle=30, end_angle=120, dxfattribs=attribs)

#create an ellipse
ellipse = msp.add_ellipse(
    (10, 10), major_axis=(5, 0), ratio=0.5, start_param=0, end_param=3.14, dxfattribs=attribs
    )
                  
doc.saveas("SimpleDXFentities.dxf")
