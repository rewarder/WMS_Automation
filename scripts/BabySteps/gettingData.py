# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:28:40 2023

@author: m.buechel
"""

import sys
import ezdxf

try:
    doc = ezdxf.readfile("95_W+D_E-1_Et12_TEDA.dxf")
except IOError:
    print("Not a DXF file or a generic I/O error.")
    sys.exit(1)
except ezdxf.DXFStructureError:
    print("Invalid or corrupted DXF file.")
    sys.exit(2)
    
# helper function
def print_entity(e):
    print("LINE on layer: %s\n" % e.dxf.layer)
    print("start point: %s\n" % e.dxf.start)
    print("end point: %s\n" % e.dxf.end)
 #   print("POINT on Layer: %s\n" % e.dxf.point)

# iterate over all entities in modelspace
msp = doc.modelspace()
for e in msp:
    if e.dxftype() == "LINE":
        print_entity(e)

#for e in msp:
#    if e.dxftype() == "POINT":
#        print_entity(e)

# entity query for all LINE entities in modelspace
for e in msp.query("LINE"):
    print_entity(e)