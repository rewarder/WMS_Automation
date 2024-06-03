# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:28:40 2023

@author: m.buechel
"""

import sys
import ezdxf
from ezdxf.addons import r12export

try:
    doc = ezdxf.readfile("Test-input.dxf")
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

# Collect all anonymous block references starting with '*U'
anonymous_block_refs = msp.query('INSERT[name ? "^\*.*"]')

# Collect the references of the 'FLAG' block
flag_refs = []
for block_ref in anonymous_block_refs:
    # Get the block layout of the anonymous block
    block = doc.blocks.get(block_ref.dxf.name)
    # Find all block references to 'FLAG' in the anonymous block
    flag_refs.extend(block.query('INSERT[name=="FLAG"]'))

# Evaluation example: collect all flag names.
flag_numbers = [
    flag.get_attrib_text("NAME")
    for flag in flag_refs
    if flag.has_attrib("NAME")
]

print(flag_numbers)

#for e in msp:
#    if e.dxftype() == "LINE":
#        print_entity(e)
        
# entity query for all LINE entities in modelspace
#for e in msp.query("LINE"):
#    print_entity(e)
    
# entity query for all LINE entities in modelspace
#for e in msp.query('LINE[layer=="Treppe"]'):
#    print_entity(e)

# entity query for all LINE entities in modelspace using Extended EntityQuery Feature
#for e in msp.query("LINE").layer == "Waende oberes Geschoss":
#    print_entity(e)
    
r12export.saveas(doc, "Test-output.dxf")