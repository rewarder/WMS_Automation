import math
import ezdxf

def ellipse_to_lines(ellipse):
    major_axis = ellipse.dxf.major_axis
    print('Major axis', major_axis)
    ratio = ellipse.dxf.ratio
    print('Ratio', ratio)
    minor_axis = (major_axis[0] * ratio, major_axis[1] * ratio, major_axis[2] * ratio)
    print('Minor axis', minor_axis)
    center = ellipse.dxf.center
    print('Center', center)
    extrusion = ellipse.dxf.extrusion
    print('Extrusion', extrusion)
    start_param = ellipse.dxf.start_param
    print('Start Prameter', start_param)
    end_param = ellipse.dxf.end_param
    print('End Parameter', end_param)

    # Default x-axis
    x_axis = (1, 0, 0)
    # Calculate rotation angle
    rotation = math.atan2(extrusion[1], extrusion[0])
    
    lines = []

    # Calculate the vertices of the ellipse
    vertices = []
    step = math.pi / 180  # 1 degree step
    
    # Ensure we handle angle wrapping correctly
    if start_param < end_param:
        angles = [start_param + i * step for i in range(int((end_param - start_param) / step) + 1)]
    else:
        angles = [start_param + i * step for i in range(int((2 * math.pi - start_param + end_param) / step) + 1)]
        angles = [angle if angle < 2 * math.pi else angle - 2 * math.pi for angle in angles]

    for angle in angles:
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        x = center[0] + major_axis[0] * cos_angle * math.cos(rotation) - minor_axis[0] * sin_angle * math.sin(rotation)
        y = center[1] + major_axis[1] * cos_angle * math.sin(rotation) + minor_axis[1] * sin_angle * math.cos(rotation)
        vertices.append((x, y))

    # Find visible segments of the ellipse
    for i in range(len(vertices) - 1):
        line = [vertices[i], vertices[i + 1]]
        lines.append(line)

    return lines

# Load the DXF file
doc = ezdxf.readfile("input.dxf")

# Create a new DXF file for the output
out = ezdxf.new()

# Iterate over all entities in the input DXF file
for entity in doc.modelspace():
    if entity.dxftype() == 'ELLIPSE':
        lines = ellipse_to_lines(entity)
        for line in lines:
            out.modelspace().add_line(line[0], line[1])

# Save the output DXF file
out.saveas("output.dxf")
