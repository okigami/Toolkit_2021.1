# coding: utf-8


import apex
from apex.construct import Point3D, Point2D

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
model_1 = apex.currentModel()

# 
# Start of recorded operations
# 

def createAssy(dict={}):
    apex.disableShowOutput()
    model_1 = apex.currentModel()
    if dict["assyName"]:
        newAssy = model_1.createAssembly(name=dict["assyName"])
    else:
        newAssy = model_1.createAssembly()

    for selElem in apex.selection.getCurrentSelection():
        res = selElem.getParent().setParent(parent=newAssy)
