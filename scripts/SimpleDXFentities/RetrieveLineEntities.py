# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 15:28:47 2023

@author: m.buechel
"""

import sys
import ezdxf 
import ezdxf.groupby

try:
    doc = ezdxf.readfile("95_W+D_E-1_Et12_TEDA.dxf")
except IOError:
    print("Not a DXF file or a generic I/O error.")
    sys.exit(1)
except ezdxf.DXFStructureError:
    print("Invalid or corrupted DXF file.")
    sys.exit(2)
    
msp = doc.modelspace()
    
group = groupby(entities=msp, dxfattrib="layer")

def layer_and_color_key(entity):
    # return None to exclude entities from the result container
    if entity.dxf.layer == "0":  # exclude entities from default layer "0"
        return None
    else:
        return entity.dxf.layer, entity.dxf.color

group = msp.groupby(key=layer_and_color_key)
for key, entities in group.items():
    print(f'Grouping criteria "{key}" matches following entities:')
    for entity in entities:
        print(f"    {entity}")
    print("-"*40)