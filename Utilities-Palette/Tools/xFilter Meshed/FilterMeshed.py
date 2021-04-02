import apex
from apex.construct import Point3D, Point2D
apex.disableShowOutput()

def ShowSurfMeshedOnly(dict={}):
    #===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    model_1 = apex.currentModel()

    # ===================================================================
    for Part in model_1.getParts(recursive = True):
        if 'Trajectories' not in Part.getPathName():
            _target = apex.entityCollection()
            for Mesh in Part.getMeshes():
                print(Mesh.entityType)
                if Mesh.entityType == apex.EntityType.SurfaceMesh:
                    _target.extend(Part)

    _target.hide()

"""
def ShowVolMeshedOnly(dict={}):
    #===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    model_1 = apex.currentModel()

    # ===================================================================
    for Part in model_1.getParts(recursive = True):
        if 'Trajectories' not in Part.getPathName():
            _target = apex.entityCollection()
            for Mesh in Part.getMeshes():
                if Mesh.entityType == apex.EntityType.SolidMesh:
                    _target.append(Part)
                    Part.hide()
                if Mesh.entityType == apex.EntityType.HexMesh:
                    _target.append(Part)
    _target.hide()
"""

def ShowAnyMeshed(dict={}):
    #===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    model_1 = apex.currentModel()

    # ===================================================================
    for Part in model_1.getParts(recursive = True):
        if 'Trajectories' not in Part.getPathName():
            _target = apex.entityCollection()
            if Part.getMeshes():
                Part.show()
            else:
                Part.hide()

def ShowNoMeshed(dict={}):
    #===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    model_1 = apex.currentModel()

    # ===================================================================
    for Part in model_1.getParts(recursive = True):
        if 'Trajectories' not in Part.getPathName():
            _target = apex.entityCollection()
            if Part.getMeshes():
                Part.hide()
            else:
                Part.show()