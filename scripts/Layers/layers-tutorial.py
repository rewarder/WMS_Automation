# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import ezdxf

doc = ezdxf.new("R2010", setup=True) # setup required for line types
msp = doc.modelspace()
doc.layers.add(name="MyLines", color=2, linetype="DASHED")
# doc.layers.add(name="MyLines")

line = msp.add_line((0.11120912, 0.34598734052345), (10, 0), dxfattribs={"layer": "MyLines"})

# Moving an entity to a different layer
# line.dxf.layer = "OtherLayer"

# Get the layer definition object from the layer table
my_lines = doc.layers.get('MyLines')

# Check the state of the layer
print(my_lines.is_off())
print(my_lines.is_on())
print(my_lines.is_locked())
layer_name = my_lines.dxf.name

# switch layer off, entities on this layer wont be shown in CAD applications
# my_lines.off()

# lock layer, entities on this layer are not editable in CAD applications
# my_lines.lock()

# changing the layer properties
# my_lines.dxf.linetype = "DOTTED"
# my_lines.color = 13 # preserves on/off state

# print(my_lines.dxf.name)

# Renaming a Layer
# my_lines = doc.layers.get("MyLines")
# my_lines.rename("SomeOtherLines")

# Deleting a Layer Definition
doc.layers.remove("MyLines")

# Deleting all entities from a layer
# key_func = doc.layers.key
# layer_key = key_func("MyLines")
# The trashcan context-manager is a safe way to delete entities from the entities DB
# with doc.entitydb.trashcan() as trash:
#     for entity in doc.entitydb.values():
#         if not entity.dxf.hasattr("layer"):
#             continue
#         if layer_key == key_func(entity.dxf.layer):
            # safe destruction while iterating
#             trash.add(entity.dxf.handle)

# jesus = doc.layers.get(name="MyLines")
# aci = jesus.set_color(2)
# gott = doc.layers.get(name="MyLines")

# Save the drawing
doc.saveas("layer_tutorial.dxf")