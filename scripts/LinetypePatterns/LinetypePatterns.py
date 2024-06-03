# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 14:47:50 2024

@author: m.buechel
"""

import ezdxf
from ezdxf.tools.standards import linetypes # some predefined linetypes

doc = ezdxf.new()
msp = doc.modelspace()


# creating my own linetypes
my_line_types = [
    (
         "DOTTED",
         "Dotted .  .  .  .  .",
         [0.2, 0.0, -0.2],
    ),
    (
         "DOTTEDX2",
         "Dotted (2x) .    .    .    .    . ",
         [0.4, 0.0, -0.4],
    ),
    (
         "DOTTED2",
         "Dotted (.5) . . . . . ",
        [0.1, 0.0, -0.1],
    ),
]
for name, desc, pattern in my_line_types:
    if name not in doc.linetypes:
        doc.linetypes.add(
            name=name,
            pattern=pattern,
            description=desc,
        )
        
# setting up predefined linetypes
for name, desc, pattern in linetypes():
    if name not in doc.linetypes:
        doc.linetypes.add(
            name=name, 
            pattern=pattern,
            description=desc,
        )

# check available linetypes
print("available linetypes:")
for lt in doc.linetypes:
    print(f"{lt.dxf.name}: {lt.dxf.description}")
    
# check for existing linetype
if "DOTTED" in doc.linetypes:
    pass

count = len(doc.linetypes) # total count of linetypes

# delete a linetype
doc.layers.remove("DASHED")
