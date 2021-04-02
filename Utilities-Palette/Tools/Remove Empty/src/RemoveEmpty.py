import apex
from apex.construct import Point3D, Point2D
apex.disableShowOutput()

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
model_1 = apex.currentModel()

def RemoveEmpty(dict={}):
    entitiesToRemove = apex.EntityCollection()
    for Part in model_1.getParts(True):
        if not Part.getSolids():
            entitiesToRemove.append(Part)

    try:
        apex.deleteEntities(entitiesToRemove)
    except:
        pass

    entitiesToRemove = apex.EntityCollection()
    for Assy in model_1.getAssemblies(True):
        if not Assy.getParts(True):
            entitiesToRemove.append(Assy)
    
    try:
        apex.deleteEntities(entitiesToRemove)
    except:
        pass
