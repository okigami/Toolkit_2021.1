import apex
from apex.construct import Point3D, Point2D
apex.disableShowOutput()

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
model_1 = apex.currentModel()

def NameAfterAssy(dict={}):
    entities_1 = apex.EntityCollection()

    for Part in model_1.getParts(True):
        if len(Part.getParent().getParts(True)) == 1:
            Part.update(name=Part.getParent().getName())
