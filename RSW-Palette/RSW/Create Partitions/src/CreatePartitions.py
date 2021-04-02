import apex
from apex.construct import Point3D, Point2D
apex.disableShowOutput()

# ===================================================================
## Split the surfaces using weld beads
def SplitByTrajectories(dict={}):
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    model_1 = apex.currentModel()
    try:
        listOfParts = model_1.getParts(True)
        _target = apex.entityCollection()
        _face = apex.entityCollection()
        for Part in listOfParts:
            if 'Trajectories' in Part.getPath():
                for Solid in Part.getSolids():
                    _face += Solid.getFaces()
            else:
                _target += Part.getSurfaces()

        apex.geometry.splitOnSurface(
            target=_target,
            face=_face,
            splitBehavior=apex.geometry.GeometrySplitBehavior.Partition)
        entities_1 = apex.EntityCollection()
        assembly_1 = model_1.getAssembly( pathName = "Trajectories" )
        entities_1.append(assembly_1)
        entities_1.hide()
    except:
        print("Split failed or not performed.")
