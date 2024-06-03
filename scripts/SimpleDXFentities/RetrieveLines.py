# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:28:40 2023

@author: m.buechel
"""

import sys
import ezdxf
import ezdxf.path

try:
    doc = ezdxf.readfile("95_W+D_E-1_Et12_TEDA.dxf")
except IOError:
    print("Not a DXF file or a generic I/O error.")
    sys.exit(1)
except ezdxf.DXFStructureError:
    print("Invalid or corrupted DXF file.")
    sys.exit(2)
    
# helper function e
def print_entity(e):
    print("LINE on layer: %s\n" % e.dxf.layer)
    print("start point: %s\n" % e.dxf.start)
    print("end point: %s\n" % e.dxf.end)

# iterate over all entities in modelspace e
msp = doc.modelspace()
for e in msp:
    if e.dxftype() == "LINE":
        print_entity(e)

# entity query for all LINE entities in modelspace
for e in msp.query("LINE"):
    print_entity(e)
    
# entity query for all LINE entities in modelspace
for e in msp.query('LINE[layer=="Treppe"]'):
    print_entity(e)

# entity query for all LINE entities in modelspace using Extended EntityQuery Feature
for e in msp.query("LINE").layer == "Waende oberes Geschoss":
    print_entity(e)

# Checking available layers
# for layer in doc.layers:
#     if layer.dxf.name != "0":
#         layer.off() # switch all layers off except layer "0"
        
# for layer in doc.layers: 
#     if layer.dxf.name != "0":
#         layer.on() # switch all layers on except layer "0"

# for layer in doc.layers:
#     if layer.dxf.name == "Achsen":
#         layer.off() # switch layer Achsen off

# change color of a layer        
for layer in doc.layers:
    if layer.dxf.name == "Achsen":
        layer.set_color(244) # change color of a layer

doc.saveas("output.dxf")