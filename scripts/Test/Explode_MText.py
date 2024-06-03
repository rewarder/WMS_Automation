# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 11:45:50 2024

@author: m.buechel
"""

import ezdxf
from ezdxf.addons import MTextExplode

doc = ezdxf.readfile("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Test/Test_Exploded_Dimensions.dxf")
msp = doc.modelspace()
with MTextExplode(msp) as xpl:
    for mtext in msp.query("MTEXT"):
        xpl.explode(mtext)
doc.saveas("C:/Users/mbuechel/Desktop/ToDo/Automation/DXFAutomation/Scripts/Test/Test_Exploded_MText.dxf")