import apex
from apex.construct import Point3D, Point2D

apex.disableShowOutput()


def CreateMeshPartitions(dict={}):
    # ===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName=r'''mm-kg-s-N''')
    model_1 = apex.currentModel()

    ## Collect faces to mesh
    _targetFine = apex.entityCollection()
    listOfLengths = []
    listOfDiameters = []

    MeshSize = float(dict["MeshSize"])

    try:
        listOfTrajectories = model_1.getAssembly("Trajectories").getParts(True)
        listOfAllParts = []
        for Part in model_1.getParts(True):
            if "Trajectories" not in Part.getPath():
                listOfAllParts.append(Part)

        for Part in listOfTrajectories:
            if 'RefDiam' in Part.getName():
                _, Diam = Part.getName().split('_')
                listOfDiameters.append(float(Diam))
            else:
                if len(Part.getCurves()) > 0:
                    listOfLengths.append(Part.getCurves()[0].getLength())

        maxDiameter = max(listOfDiameters) #Getting the max diameter to use as search range

        ## Getting all faces from all parts that are not under 'Trajectories'
        facesToMesh = apex.EntityCollection()
        for Part in listOfAllParts:
            for Surface in Part.getSurfaces():
                for Face in Surface.getFaces():
                    if Face.getArea() <= (1.1 * 3.14159 * maxDiameter * maxDiameter):
                        facesToMesh.append(Face)


        apex.mesh.createSurfaceMesh(
            name="",
            target=facesToMesh,
            meshSize=MeshSize,
            meshType=apex.mesh.SurfaceMeshElementShape.Mixed,
            meshMethod=apex.mesh.SurfaceMeshMethod.Pave,
            mappedMeshDominanceLevel=2,
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


    except:
        print("Meshing failed or not performed.")
