import ezdxf

# Create a new DXF drawing
doc = ezdxf.new('R2000')
msp = doc.modelspace()

ellipse = msp.add_ellipse(
    (2217.429, 1365.415), major_axis=(2.137, 0.573), ratio=0.268, start_param=0, end_param=4.450364573332983
)

print('Major Axis', ellipse.dxf.major_axis)

# Save the drawing to a file

doc.saveas('ellipse.dxf')
