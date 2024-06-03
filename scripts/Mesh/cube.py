# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 13:42:16 2023

@author: m.buechel
"""

import pyautocad

def draw_3d_cube(side_length):
    acad = pyautocad.Autocad(create_if_not_exists=True)
    acad.prompt("Hello, Autocad from Python\n")
    print(acad.doc.Name)

    # Define the corner points of the cube
    base_point = (0, 0, 0)
    opposite_point = (side_length, side_length, side_length)

    # Draw the 3D cube using lines
    acad.model.AddLine(base_point, (side_length, 0, 0))
    acad.model.AddLine(base_point, (0, side_length, 0))
    acad.model.AddLine(base_point, (0, 0, side_length))

    acad.model.AddLine((side_length, 0, 0), opposite_point)
    acad.model.AddLine((0, side_length, 0), opposite_point)
    acad.model.AddLine((0, 0, side_length), opposite_point)

    acad.model.AddLine(opposite_point, (0, side_length, side_length))
    acad.model.AddLine(opposite_point, (side_length, 0, side_length))
    acad.model.AddLine(opposite_point, (side_length, side_length, 0))

    # Specify the side length of the cube
    cube_side_length = 200

    # Draw the 3D cube
    draw_3d_cube(cube_side_length)

    print("3D cube drawn successfully.")
