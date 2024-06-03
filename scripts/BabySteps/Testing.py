# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 11:04:07 2023

@author: m.buechel
"""

from pyautocad import Autocad, APoint

acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello, Autocad from Python\n")
print(acad.doc.Name)

# Creating a line
p1 = APoint(0, 0)
p2 = APoint(50, 25)
line1 = acad.model.AddLine(p1, p2)

# Creating another line
p3 = APoint(0, 10)
p4 = APoint(25, 40)
line2 = acad.model.AddLine(p3, p4)

# Create circles
circle_center = APoint(5, 5)
radius1 = 10

draw_circle1 = acad.model.AddCircle(circle_center, radius1)

draw_polyline = acad.model.AddLine(p1, p2)