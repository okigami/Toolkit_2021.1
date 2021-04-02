import apex
from apex.construct import Point3D, Point2D
apex.disableShowOutput()

def SuppressFeatures(dict={}):
    #===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    model_1 = apex.currentModel()
    _target = apex.entityCollection()
    try:
        for part in model_1.getParts(True):
            if 'Trajectories' not in part.getPath():
                for surface in part.getSurfaces():
                    _target.extend(surface.getEdges())
                    _target.extend(surface.getVertices())

        result = apex.geometry.suppressOnly(
            target = _target,
            maxEdgeAngle = 1.745329251994330e-01,
            maxFaceAngle = 8.726646259971650e-02,
            keepVerticesAtCurvatureChange = False,
            cleanupTol = 1.000000000000000)
    except:
        print("Simplification not performed or failed.")
