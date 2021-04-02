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

    try:
        MeshSize = float(dict["MeshSize"])
    except:
        MeshSize = float(dict["FineMeshSize"])


    #try:
    listOfTrajectories = model_1.getAssembly("Refinement regions").getParts(True)
    listOfAllParts = []
    for Part in model_1.getParts(True):
        if "Refinement regions" not in Part.getPath():
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
    proxSearch = apex.utility.ProximitySearch()
    listOfAllPartFaces = []
    for Part in listOfAllParts:
        for Surface in Part.getSurfaces():
            for Face in Surface.getFaces():
                listOfAllPartFaces.append(Face)

    ## Inserting the list of faces into the proximity search
    ans = proxSearch.insertList(listOfAllPartFaces)

    facesToMesh = apex.EntityCollection()

    ## Perform the search
    for Part in model_1.getAssembly('Refinement regions').getParts():  # Add spots and weld beads to perfom the search
        for Solid in Part.getSolids():
            resSearch = proxSearch.findObjectsWithinDistance(location=Solid.getLocation(), distance=1.1 * maxDiameter)
            for elem in resSearch.foundObjects():
                if elem.entityType == apex.EntityType.Face:
                    facesToMesh.append(elem)

    if listOfLengths:
        minLength = min(listOfLengths)
        ## Select everything that is smaller than the minLength * maxDiameter
        for Assy in model_1.getAssemblies():
            if "Refinement regions" not in Assy.getName():
                for Part in Assy.getParts(recursive=True):
                    for Surface in Part.getSurfaces():
                        for Face in Surface.getFaces():
                            if Face.getArea() <= (0.8 * max(listOfLengths) * maxDiameter):
                                facesToMesh.append(Face)

    else:
        ## Select everything that is smaller than the minLength * maxDiameter
        for Part in listOfAllParts:
            for Surface in Part.getSurfaces():
                for Face in Surface.getFaces():
                    if Face.getArea() <= (1.1 * 3.14159 * (maxDiameter / 2) ** 2):
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

    try:
        pass
    except:
        print("Meshing failed or not performed.")
