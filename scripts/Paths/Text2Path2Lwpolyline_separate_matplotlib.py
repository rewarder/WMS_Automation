# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 11:22:46 2024

@author: m.buechel
"""

import ezdxf
import matplotlib.pyplot as plt
from io import BytesIO

# Create a DXF file object and get the current model space
doc = ezdxf.readfile("some_random_text.dxf")
msp = doc.modelspace()

# Function to convert a character to a path
def character_to_path(char, insertion_point, char_height, char_index):
    # Create a figure and axis for plotting
    fig, ax = plt.subplots(figsize=(char_height, char_height))
    ax.text(0.5, 0.5, char, fontsize=char_height, ha='center', va='center', transform=ax.transAxes)

    # Save the figure to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight', pad_inches=0)
    buf.seek(0)

    # Read the SVG content from the buffer
    svg_content = buf.getvalue().decode('utf-8')

    # Use the svg2paths library to convert SVG to paths
    from svg2paths import svg2paths
    paths, attributes = svg2paths(svg_content)

    # Extract vertices from the paths
    vertices = []
    for path in paths:
        for segment in path:
            vertices.extend(segment)

    # Adjust the insertion point based on the character index
    char_offset = char_index * char_height
    vertices = [(x + insertion_point[0] + char_offset, y + insertion_point[1]) for x, y in vertices]

    return vertices

# Iterate through each text entity in the model space
for text_entity in msp.query('TEXT'):
    insertion_point = text_entity.dxf.insert
    char_height = text_entity.dxf.height

    # Iterate through each character in the text entity
    for char_index, char in enumerate(text_entity.dxf.text):
        # Convert each character to a path using the adjusted insertion point, character height, and index
        vertices = character_to_path(char, insertion_point, char_height, char_index)

        # Add the converted path vertices to the model space directly
        msp.add_lwpolyline(vertices)

# Save the DXF file with the converted text
doc.saveas("converted_text_high_accuracy_matplotlib.dxf")
