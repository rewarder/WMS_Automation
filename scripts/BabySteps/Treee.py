# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 11:28:43 2023

@author: m.buechel
"""

import pyautocad

def draw_tree_in_existing_drawing(trunk_base, trunk_top, canopy_radius, num_canopy_circles):
    try:
        acad = pyautocad.Autocad()
        doc = acad.doc
        if not doc.Name == "Zeichnung1.dwg":
            raise ValueError("The active drawing is not 'Zeichnung1.dwg'.")
    except pyautocad.api.exception.RuntimeError:
        raise RuntimeError("AutoCAD is not running or an error occurred.")

    # Draw trunk as a polyline
    trunk = acad.model.AddLine(trunk_base, trunk_top)

    # Draw canopy as circles
    canopy_center = trunk_top
    for _ in range(num_canopy_circles):
        canopy = acad.model.AddCircle(canopy_center, canopy_radius)
        canopy_center = (canopy_center[0], canopy_center[1] + 2 * canopy_radius)  # Move vertically for the next circle

if __name__ == "__main__":
    # Specify parameters for the tree
    trunk_base = (5, 0)
    trunk_top = (5, 10)
    canopy_radius = 3
    num_canopy_circles = 5

    # Draw the tree in the existing drawing
    draw_tree_in_existing_drawing(trunk_base, trunk_top, canopy_radius, num_canopy_circles)

    print("Tree drawn successfully in the existing drawing.")
