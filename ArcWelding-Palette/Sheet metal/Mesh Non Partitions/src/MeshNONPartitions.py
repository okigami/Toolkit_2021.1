import apex
from apex.construct import Point3D, Point2D
apex.disableShowOutput()

def CreateMeshNONPartitions(dict={}):
    #===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    model_1 = apex.currentModel()

    try:
        MeshSize = float(dict["CoarseMeshSize"])
    except:
        MeshSize = float(dict["MeshSize"])
         
    listOfAllParts = []
    for Part in model_1.getParts(True):
        if "Trajectories" not in Part.getPath():
            listOfAllParts.append(Part)
            
    ## Getting all faces from all parts that are not under 'Trajectories'
    listOfNonMeshedFaces = apex.EntityCollection()
    for Part in listOfAllParts:
        for Surface in Part.getSurfaces():
            for Face in Surface.getFaces():
                if not Face.getElements():
                    listOfNonMeshedFaces.append(Face)
    
    ## -----------------------------------------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------------------------------------

    apex.mesh.createSurfaceMesh(
        name="",
        target=listOfNonMeshedFaces,
        meshSize= MeshSize,
        meshType=apex.mesh.SurfaceMeshElementShape.Mixed,
        meshMethod=apex.mesh.SurfaceMeshMethod.Pave,
        mappedMeshDominanceLevel=0,
        elementOrder=apex.mesh.ElementOrder.Linear,
        meshUsingPrincipalAxes=False,
        refineMeshUsingCurvature=True,
        elementGeometryDeviationRatio=0.10,
        elementMinEdgeLengthRatio=0.50,
        createFeatureMeshOnFillets=False,
        createFeatureMeshOnChamfers=False,
        createFeatureMeshOnWashers=False,
        createFeatureMeshOnQuadFaces=False
    )

                    