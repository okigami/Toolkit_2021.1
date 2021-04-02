# coding: utf-8

import apex
from apex.construct import Point3D, Point2D
apex.disableShowOutput()

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
applicationSettingsGeometry = apex.setting.ApplicationSettingsGeometry()
applicationSettingsGeometry.createGeometryInNewPart =  apex.setting.CreateGeometryInNewPart.CurrentPart
apex.setting.setApplicationSettingsGeometry(applicationSettingsGeometry = applicationSettingsGeometry)
model_1 = apex.currentModel()

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
def buildFlushCorner(dict={}):
    # - Get the data from the dictionary
    HorizWidth = float(dict["HorizWidth"])
    HorizLength = float(dict["HorizLength"])
    HorizThick = float(dict["HorizThick"])
    VertHeight = float(dict["VertHeight"])
    VertLength = float(dict["VertLength"])
    VertThick = float(dict["VertThick"])

    ## Define max and min thickness
    if VertThick >= HorizThick:
        maxThick = VertThick
        minThick = HorizThick
    else:
        maxThick = HorizThick
        minThick = VertThick

    Sheet01 = apex.createPart()

    ParentAssy = model_1.createAssembly(name="FlushCorner")

    # - Build the horizontal plate
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet01',
        description='',
        length=HorizLength, #Length
        height=HorizWidth,  #Width
        depth=HorizThick,   #Thickness
        origin=apex.Coordinate(0.0, 0.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet01.setParent(ParentAssy)
    res = Sheet01.update(name='Plate')

    # - Build the vertical plate
    Sheet02 = apex.createPart()
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet02',
        description='',
        length=VertLength,  # Length
        height=VertThick,  # Width
        depth=VertHeight,    # Thickness
        origin=apex.Coordinate(0.0, 0.0, HorizThick),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet02.setParent(ParentAssy)
    res = Sheet02.update(name='Web')
    

    # Save joint info for reference
    JointInfoAssy = model_1.createAssembly("Joint info")
    res = JointInfoAssy.createPart( name="Sheet 01 = {0}mm".format(HorizThick))
    res = JointInfoAssy.createPart( name="Sheet 02 = {0}mm".format(VertThick))
    res = JointInfoAssy.createPart( name="Width = {0}mm".format(HorizWidth))
    res = JointInfoAssy.createPart( name="Length = {0}mm".format(HorizLength))


    # Creating split regions
    ## Split sheet 01 (horizontal sheet)
    _target = apex.EntityCollection()
    _target.append( Sheet01.getSolids()[0] )
    _plane = apex.construct.Plane(
        apex.construct.Point3D(0.0, (VertThick + 1.5*maxThick), 0.0), # Where it should cut
        apex.construct.Vector3D(0.0, 1.0, 0.0)
    )
    result = apex.geometry.splitWithPlane(
        target = _target,
        plane = _plane, 
        splitBehavior = apex.geometry.GeometrySplitBehavior.Partition
    )
    _plane = apex.construct.Plane(
        apex.construct.Point3D(0.0, 1.5*(VertThick + 1.5*maxThick), 0.0), # Where it should cut
        apex.construct.Vector3D(0.0, 1.0, 0.0)
    )
    result = apex.geometry.splitWithPlane(
        target = _target,
        plane = _plane, 
        splitBehavior = apex.geometry.GeometrySplitBehavior.Partition
    )
    _plane = apex.construct.Plane(
        apex.construct.Point3D(0.0, 2.0 * (VertThick + 1.5 * maxThick), 0.0),  # Where it should cut
        apex.construct.Vector3D(0.0, 1.0, 0.0)
    )
    result = apex.geometry.splitWithPlane(
        target=_target,
        plane=_plane,
        splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
    )

    ## Split sheet 02 (vertical sheet)
    _target = apex.EntityCollection()
    _target.append( Sheet02.getSolids()[0] )
    _plane = apex.construct.Plane(
        apex.construct.Point3D(0, 0, (HorizThick + 1.5*maxThick)), # Where it should cut
        apex.construct.Vector3D(0.0, 0.0, 1.0)
    )
    result = apex.geometry.splitWithPlane(
        target = _target,
        plane = _plane, 
        splitBehavior = apex.geometry.GeometrySplitBehavior.Partition
    )
    _plane = apex.construct.Plane(
        apex.construct.Point3D(0, 0, 1.5*(HorizThick + 1.5*maxThick)), # Where it should cut
        apex.construct.Vector3D(0.0, 0.0, 1.0)
    )
    result = apex.geometry.splitWithPlane(
        target = _target,
        plane = _plane, 
        splitBehavior = apex.geometry.GeometrySplitBehavior.Partition
    )
    _plane = apex.construct.Plane(
        apex.construct.Point3D(0, 0, 2.0 * (HorizThick + 1.5 * maxThick)),  # Where it should cut
        apex.construct.Vector3D(0.0, 0.0, 1.0)
    )
    result = apex.geometry.splitWithPlane(
        target=_target,
        plane=_plane,
        splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
    )


    ## - Perform meshing if requested
    if dict["MeshForMe"] == 'True':
        # - Meshing Sheet 01
        refPoint = apex.Coordinate( HorizLength / 2.0, 0.0, 0.0 )
        proxSearch = apex.utility.ProximitySearch()
        ans = proxSearch.insertList(list(Sheet01.getSolids()[0].getCells()))
        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=2) # Nearest 2 cells

        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            cellsToMesh.append(elem)

        _SweepFace = apex.EntityCollection()
        result = apex.mesh.createHexMesh(
            name="",
            target=cellsToMesh,
            meshSize=(min([VertThick, HorizThick]) / 2),
            surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
            mappedMeshDominanceLevel=2,
            elementOrder=apex.mesh.ElementOrder.Linear,
            refineMeshUsingCurvature=False,
            elementGeometryDeviationRatio=0.10,
            elementMinEdgeLengthRatio=0.20,
            createFeatureMeshOnWashers=False,
            createFeatureMeshOnArbitraryHoles=False,
            preserveWasherThroughMesh=True,
            sweepFace=_SweepFace,
            hexMeshMethod=apex.mesh.HexMeshMethod.Auto
        )

        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=4)
        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            if len(elem.getElements()) > 0:  # Check if it has a mesh already
                pass
            else:
                cellsToMesh.append(elem)
                seedEdge = apex.EntityCollection()
                for Edge in elem.getEdges():
                    if (Edge.getLength() == minThick) or (Edge.getLength() == maxThick):
                        seedEdge.append(Edge)
                result = apex.mesh.createEdgeSeedUniformByNumber(
                    target=seedEdge,
                    numberElementEdges=1
                )
        for Cell in cellsToMesh:
            vecFaces = Cell.getFaces()
            for Face in vecFaces:
                paramU = Face.evaluatePointOnFace(Face.getCentroid()).u
                paramV = Face.evaluatePointOnFace(Face.getCentroid()).v
                normalAtPoint = Face.evaluateNormal(paramU, paramV)
                if abs(normalAtPoint.z) == 1:
                    _SweepFace = apex.EntityCollection()
                    _SweepFace.append(Face)
                    meshCell = apex.EntityCollection()
                    meshCell.append(Cell)
                    result = apex.mesh.createHexMesh(
                        name="",
                        target=meshCell,
                        meshSize=maxThick,
                        surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
                        mappedMeshDominanceLevel=2,
                        elementOrder=apex.mesh.ElementOrder.Linear,
                        refineMeshUsingCurvature=False,
                        elementGeometryDeviationRatio=0.10,
                        elementMinEdgeLengthRatio=0.20,
                        createFeatureMeshOnWashers=False,
                        createFeatureMeshOnArbitraryHoles=False,
                        preserveWasherThroughMesh=True,
                        sweepFace=_SweepFace,
                        hexMeshMethod=apex.mesh.HexMeshMethod.Auto
                    )
                    break

        # - Meshing Sheet 02
        refPoint = apex.Coordinate(HorizLength / 2.0, 0.0, 0.0)
        proxSearch = apex.utility.ProximitySearch()
        ans = proxSearch.insertList(list(Sheet02.getSolids()[0].getCells()))
        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=2)

        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            cellsToMesh.append(elem)

        _SweepFace = apex.EntityCollection()
        result = apex.mesh.createHexMesh(
            name="",
            target=cellsToMesh,
            meshSize=(min([VertThick, HorizThick]) / 2),
            surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
            mappedMeshDominanceLevel=2,
            elementOrder=apex.mesh.ElementOrder.Linear,
            refineMeshUsingCurvature=False,
            elementGeometryDeviationRatio=0.10,
            elementMinEdgeLengthRatio=0.20,
            createFeatureMeshOnWashers=False,
            createFeatureMeshOnArbitraryHoles=False,
            preserveWasherThroughMesh=True,
            sweepFace=_SweepFace,
            hexMeshMethod=apex.mesh.HexMeshMethod.Auto
        )

        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=4)
        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            if len(elem.getElements()) > 0:  # Check if it has a mesh already
                pass
            else:
                cellsToMesh.append(elem)
                seedEdge = apex.EntityCollection()
                for Edge in elem.getEdges():
                    if (Edge.getLength() == minThick) or (Edge.getLength() == maxThick):
                        seedEdge.append(Edge)
                result = apex.mesh.createEdgeSeedUniformByNumber(
                    target=seedEdge,
                    numberElementEdges=1
                )
        for Cell in cellsToMesh:
            vecFaces = Cell.getFaces()
            for Face in vecFaces:
                paramU = Face.evaluatePointOnFace(Face.getCentroid()).u
                paramV = Face.evaluatePointOnFace(Face.getCentroid()).v
                normalAtPoint = Face.evaluateNormal(paramU, paramV)
                if abs(normalAtPoint.y) == 1:
                    _SweepFace = apex.EntityCollection()
                    _SweepFace.append(Face)
                    meshCell = apex.EntityCollection()
                    meshCell.append(Cell)
                    result = apex.mesh.createHexMesh(
                        name="",
                        target=meshCell,
                        meshSize=maxThick,
                        surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
                        mappedMeshDominanceLevel=2,
                        elementOrder=apex.mesh.ElementOrder.Linear,
                        refineMeshUsingCurvature=False,
                        elementGeometryDeviationRatio=0.10,
                        elementMinEdgeLengthRatio=0.20,
                        createFeatureMeshOnWashers=False,
                        createFeatureMeshOnArbitraryHoles=False,
                        preserveWasherThroughMesh=True,
                        sweepFace=_SweepFace,
                        hexMeshMethod=apex.mesh.HexMeshMethod.Auto
                    )
                    break


#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
def buildTJoint(dict={}):
    # - Get the data from the dictionary
    HorizWidth = float(dict["HorizWidth"])
    HorizLength = float(dict["HorizLength"])
    HorizThick = float(dict["HorizThick"])
    VertHeight = float(dict["VertHeight"])
    VertLength = float(dict["VertLength"])
    VertThick = float(dict["VertThick"])

    ## Define max and min thickness
    if VertThick >= HorizThick:
        maxThick = VertThick
        minThick = HorizThick
    else:
        maxThick = HorizThick
        minThick = VertThick

    avgThick = (maxThick + minThick) / 2.0

    Sheet01 = apex.createPart()

    ParentAssy = model_1.createAssembly(name="T-Joint")

    # - Build the horizontal plate
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet01',
        description='',
        length=HorizLength,  # Length
        height=HorizWidth,  # Width
        depth=HorizThick,  # Thickness
        origin=apex.Coordinate(0.0, 0.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet01.setParent(ParentAssy)
    res = Sheet01.update(name='Plate')

    # - Build the vertical plate
    Sheet02 = apex.createPart()
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet02',
        description='',
        length=VertLength,  # Length
        height=VertThick,  # Width
        depth=VertHeight,  # Thickness
        origin=apex.Coordinate(0.0, 0.0, HorizThick),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet02.setParent(ParentAssy)
    res = Sheet02.update(name='Web')

    # - Translate vertical plate to the middle of horizontal plate
    _translateSheet = apex.EntityCollection()
    _translateSheet.append(Sheet02.getSolids()[0])
    newEntities = apex.transformTranslate(
        target=_translateSheet,
        direction=[0.0, 1.0, 0.0],
        distance=(HorizWidth/2 - VertThick/2),
        makeCopy=False
    )

    # Save joint info for reference
    JointInfoAssy = model_1.createAssembly("Joint info")
    res = JointInfoAssy.createPart(name="Sheet 01 = {0}mm".format(HorizThick))
    res = JointInfoAssy.createPart(name="Sheet 02 = {0}mm".format(VertThick))
    res = JointInfoAssy.createPart(name="Width = {0}mm".format(HorizWidth))
    res = JointInfoAssy.createPart(name="Length = {0}mm".format(HorizLength))


    # Split regions for horizontal sheet
    _target = apex.EntityCollection()
    _target.append(Sheet01.getSolids()[0])
    listOfDist = [2.0, 3.0, 4.0, -2.0, -3.0, -4.0]
    for cutDist in listOfDist:
        _plane = apex.construct.Plane(
            apex.construct.Point3D(0.0, (
                        (HorizWidth / 2.0 + (cutDist / abs(cutDist)) * VertThick / 2.0) + cutDist * avgThick), 0.0),
            apex.construct.Vector3D(0.0, 1.0, 0.0)
        )
        result = apex.geometry.splitWithPlane(
            target=_target,
            plane=_plane,
            splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
        )

    # Split regions for vertical sheet
    _target = apex.EntityCollection()
    _target.append(Sheet02.getSolids()[0])
    listOfDist = [2.0, 3.0, 4.0]
    for cutDist in listOfDist:
        _plane = apex.construct.Plane(
            apex.construct.Point3D(0.0, 0.0, (HorizThick + cutDist * avgThick)),
            apex.construct.Vector3D(0.0, 0.0, 1.0)
        )
        result = apex.geometry.splitWithPlane(
            target=_target,
            plane=_plane,
            splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
        )



    ## - Perform meshing if requested
    if dict["MeshForMe"] == 'True':
        # - Meshing Sheet 01
        refPoint = apex.Coordinate(HorizLength / 2.0, HorizWidth / 2.0, 0.0)
        proxSearch = apex.utility.ProximitySearch()
        ans = proxSearch.insertList(list(Sheet01.getSolids()[0].getCells()))
        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=3)

        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            cellsToMesh.append(elem)

        _SweepFace = apex.EntityCollection()
        result = apex.mesh.createHexMesh(
            name="",
            target=cellsToMesh,
            meshSize=(min([VertThick, HorizThick]) / 2),
            surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
            mappedMeshDominanceLevel=2,
            elementOrder=apex.mesh.ElementOrder.Linear,
            refineMeshUsingCurvature=False,
            elementGeometryDeviationRatio=0.10,
            elementMinEdgeLengthRatio=0.20,
            createFeatureMeshOnWashers=False,
            createFeatureMeshOnArbitraryHoles=False,
            preserveWasherThroughMesh=True,
            sweepFace=_SweepFace,
            hexMeshMethod=apex.mesh.HexMeshMethod.Auto
        )

        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=7)
        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            if len(elem.getElements()) > 0:  # Check if it has a mesh already
                pass
            else:
                cellsToMesh.append(elem)
                seedEdge = apex.EntityCollection()
                for Edge in elem.getEdges():
                    if (Edge.getLength() == minThick) or (Edge.getLength() == maxThick):
                        seedEdge.append(Edge)
                result = apex.mesh.createEdgeSeedUniformByNumber(
                    target=seedEdge,
                    numberElementEdges=1
                )
        for Cell in cellsToMesh:
            vecFaces = Cell.getFaces()
            for Face in vecFaces:
                paramU = Face.evaluatePointOnFace(Face.getCentroid()).u
                paramV = Face.evaluatePointOnFace(Face.getCentroid()).v
                normalAtPoint = Face.evaluateNormal(paramU, paramV)
                if abs(normalAtPoint.z) == 1:   #-Extrusion direction for meshing
                    _SweepFace = apex.EntityCollection()
                    _SweepFace.append(Face)
                    meshCell = apex.EntityCollection()
                    meshCell.append(Cell)
                    result = apex.mesh.createHexMesh(
                        name="",
                        target=meshCell,
                        meshSize=maxThick,
                        surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
                        mappedMeshDominanceLevel=2,
                        elementOrder=apex.mesh.ElementOrder.Linear,
                        refineMeshUsingCurvature=False,
                        elementGeometryDeviationRatio=0.10,
                        elementMinEdgeLengthRatio=0.20,
                        createFeatureMeshOnWashers=False,
                        createFeatureMeshOnArbitraryHoles=False,
                        preserveWasherThroughMesh=True,
                        sweepFace=_SweepFace,
                        hexMeshMethod=apex.mesh.HexMeshMethod.Auto
                    )
                    break

        # - Meshing Sheet 02
        refPoint = apex.Coordinate(HorizLength / 2.0, HorizWidth / 2.0, 0.0)
        proxSearch = apex.utility.ProximitySearch()
        ans = proxSearch.insertList(list(Sheet02.getSolids()[0].getCells()))
        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=2)

        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            cellsToMesh.append(elem)

        _SweepFace = apex.EntityCollection()
        result = apex.mesh.createHexMesh(
            name="",
            target=cellsToMesh,
            meshSize=(min([VertThick, HorizThick]) / 2),
            surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
            mappedMeshDominanceLevel=2,
            elementOrder=apex.mesh.ElementOrder.Linear,
            refineMeshUsingCurvature=False,
            elementGeometryDeviationRatio=0.10,
            elementMinEdgeLengthRatio=0.20,
            createFeatureMeshOnWashers=False,
            createFeatureMeshOnArbitraryHoles=False,
            preserveWasherThroughMesh=True,
            sweepFace=_SweepFace,
            hexMeshMethod=apex.mesh.HexMeshMethod.Auto
        )

        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=4)
        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            if len(elem.getElements()) > 0:  # Check if it has a mesh already
                pass
            else:
                cellsToMesh.append(elem)
                seedEdge = apex.EntityCollection()
                for Edge in elem.getEdges():
                    if 0.9 * VertThick <= Edge.getLength() <= 1.1 * VertThick:
                        seedEdge.append(Edge)
                        print(Edge.getLength())
                result = apex.mesh.createEdgeSeedUniformByNumber(
                    target=seedEdge,
                    numberElementEdges=1
                )

        for Cell in cellsToMesh:
            vecFaces = Cell.getFaces()
            for Face in vecFaces:
                paramU = Face.evaluatePointOnFace(Face.getCentroid()).u
                paramV = Face.evaluatePointOnFace(Face.getCentroid()).v
                normalAtPoint = Face.evaluateNormal(paramU, paramV)
                if abs(normalAtPoint.y) == 1:   #-Extrusion direction for meshing
                    _SweepFace = apex.EntityCollection()
                    _SweepFace.append(Face)
                    meshCell = apex.EntityCollection()
                    meshCell.append(Cell)
                    result = apex.mesh.createHexMesh(
                        name="",
                        target=meshCell,
                        meshSize=maxThick,
                        surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
                        mappedMeshDominanceLevel=2,
                        elementOrder=apex.mesh.ElementOrder.Linear,
                        refineMeshUsingCurvature=False,
                        elementGeometryDeviationRatio=0.10,
                        elementMinEdgeLengthRatio=0.20,
                        createFeatureMeshOnWashers=False,
                        createFeatureMeshOnArbitraryHoles=False,
                        preserveWasherThroughMesh=True,
                        sweepFace=_SweepFace,
                        hexMeshMethod=apex.mesh.HexMeshMethod.Auto
                    )
                    break

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
def buildLapJoint(dict={}):
    # - Get the data from the dictionary
    HorizWidth = float(dict["HorizWidth"])
    HorizLength = float(dict["HorizLength"])
    HorizThick = float(dict["HorizThick"])
    VertHeight = float(dict["VertHeight"])
    VertLength = float(dict["VertLength"])
    VertThick = float(dict["VertThick"])

    ## Define max and min thickness
    if VertThick >= HorizThick:
        maxThick = VertThick
        minThick = HorizThick
    else:
        maxThick = HorizThick
        minThick = VertThick
    avgThick = (maxThick + minThick) / 2.0

    Sheet01 = apex.createPart()

    ParentAssy = model_1.createAssembly(name="LapJoint")

    # - Build the horizontal plate
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet01',
        description='',
        length=HorizLength,  # Length
        height=HorizWidth,  # Width
        depth=HorizThick,  # Thickness
        origin=apex.Coordinate(0.0, 0.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet01.setParent(ParentAssy)
    res = Sheet01.update(name='BottomSheet')

    # - Build the vertical plate
    Sheet02 = apex.createPart()
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet02',
        description='',
        length=VertLength,  # Length
        height=VertHeight,  # Width
        depth=VertThick,  # Thickness
        origin=apex.Coordinate(0.0, 0.0, HorizThick),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet02.setParent(ParentAssy)
    res = Sheet02.update(name='UpperSheet')

    # - Translate vertical plate to the middle of horizontal plate
    _translateSheet = apex.EntityCollection()
    _translateSheet.append(Sheet02.getSolids()[0])
    newEntities = apex.transformTranslate(
        target=_translateSheet,
        direction=[0.0, 1.0, 0.0],
        distance=(HorizWidth - 2.0 * HorizThick),
        makeCopy=False
    )

    # Save joint info for reference
    JointInfoAssy = model_1.createAssembly("Joint info")
    res = JointInfoAssy.createPart(name="Sheet 01 = {0}mm".format(HorizThick))
    res = JointInfoAssy.createPart(name="Sheet 02 = {0}mm".format(VertThick))
    res = JointInfoAssy.createPart(name="Width = {0}mm".format(HorizWidth))
    res = JointInfoAssy.createPart(name="Length = {0}mm".format(HorizLength))

    # Creating split regions
    ## Split sheet 01 (horizontal sheet)
    _target = apex.EntityCollection()
    _target.append(Sheet01.getSolids()[0])
    listOfDist = [-4.0, -5.0, -6.0]
    for cutDist in listOfDist:
        _plane = apex.construct.Plane(
            apex.construct.Point3D(0.0, (HorizWidth + cutDist * avgThick), 0.0),
            apex.construct.Vector3D(0.0, 1.0, 0.0)
        )
        result = apex.geometry.splitWithPlane(
            target=_target,
            plane=_plane,
            splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
        )


    ## Split sheet 02 (vertical sheet)
    _target = apex.EntityCollection()
    _target.append(Sheet02.getSolids()[0])
    listOfDist = [0.0, 2.0, 3.0]
    for cutDist in listOfDist:
        _plane = apex.construct.Plane(
            apex.construct.Point3D(0.0, (HorizWidth + cutDist * avgThick), 0.0),
            apex.construct.Vector3D(0.0, 1.0, 0.0)
        )
        result = apex.geometry.splitWithPlane(
            target=_target,
            plane=_plane,
            splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
        )

    ## - Perform meshing if requested
    if dict["MeshForMe"] == 'True':
        # - Meshing Sheet 01
        refPoint = apex.Coordinate(HorizLength / 2.0, HorizWidth - 2.0 * HorizThick, 0.0)
        proxSearch = apex.utility.ProximitySearch()
        ans = proxSearch.insertList(list(Sheet01.getSolids()[0].getCells()))
        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=2)

        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            cellsToMesh.append(elem)

        _SweepFace = apex.EntityCollection()
        result = apex.mesh.createHexMesh(
            name="",
            target=cellsToMesh,
            meshSize=(minThick / 2),
            surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
            mappedMeshDominanceLevel=2,
            elementOrder=apex.mesh.ElementOrder.Linear,
            refineMeshUsingCurvature=False,
            elementGeometryDeviationRatio=0.10,
            elementMinEdgeLengthRatio=0.20,
            createFeatureMeshOnWashers=False,
            createFeatureMeshOnArbitraryHoles=False,
            preserveWasherThroughMesh=True,
            sweepFace=_SweepFace,
            hexMeshMethod=apex.mesh.HexMeshMethod.Auto
        )

        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=4)
        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            if len(elem.getElements()) > 0:  # Check if it has a mesh already
                pass
            else:
                cellsToMesh.append(elem)
                seedEdge = apex.EntityCollection()
                for Edge in elem.getEdges():
                    if 0.9 * HorizThick <= Edge.getLength() <= 1.1 * HorizThick:
                        seedEdge.append(Edge)
                result = apex.mesh.createEdgeSeedUniformByNumber(
                    target=seedEdge,
                    numberElementEdges=1
                )
        for Cell in cellsToMesh:
            vecFaces = Cell.getFaces()
            for Face in vecFaces:
                paramU = Face.evaluatePointOnFace(Face.getCentroid()).u
                paramV = Face.evaluatePointOnFace(Face.getCentroid()).v
                normalAtPoint = Face.evaluateNormal(paramU, paramV)
                if abs(normalAtPoint.z) == 1:  # -Extrusion direction for meshing
                    _SweepFace = apex.EntityCollection()
                    _SweepFace.append(Face)
                    meshCell = apex.EntityCollection()
                    meshCell.append(Cell)
                    result = apex.mesh.createHexMesh(
                        name="",
                        target=meshCell,
                        meshSize=maxThick,
                        surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
                        mappedMeshDominanceLevel=2,
                        elementOrder=apex.mesh.ElementOrder.Linear,
                        refineMeshUsingCurvature=False,
                        elementGeometryDeviationRatio=0.10,
                        elementMinEdgeLengthRatio=0.20,
                        createFeatureMeshOnWashers=False,
                        createFeatureMeshOnArbitraryHoles=False,
                        preserveWasherThroughMesh=True,
                        sweepFace=_SweepFace,
                        hexMeshMethod=apex.mesh.HexMeshMethod.Auto
                    )
                    break

        # - Meshing Sheet 02
        refPoint = apex.Coordinate(HorizLength / 2.0, HorizWidth - 2.0 * HorizThick, 0.0)
        proxSearch = apex.utility.ProximitySearch()
        ans = proxSearch.insertList(list(Sheet02.getSolids()[0].getCells()))
        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=2)

        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            cellsToMesh.append(elem)

        _SweepFace = apex.EntityCollection()
        result = apex.mesh.createHexMesh(
            name="",
            target=cellsToMesh,
            meshSize=(minThick / 2),
            surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
            mappedMeshDominanceLevel=2,
            elementOrder=apex.mesh.ElementOrder.Linear,
            refineMeshUsingCurvature=False,
            elementGeometryDeviationRatio=0.10,
            elementMinEdgeLengthRatio=0.20,
            createFeatureMeshOnWashers=False,
            createFeatureMeshOnArbitraryHoles=False,
            preserveWasherThroughMesh=True,
            sweepFace=_SweepFace,
            hexMeshMethod=apex.mesh.HexMeshMethod.Auto
        )

        resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=4)
        cellsToMesh = apex.EntityCollection()
        for elem in resSearch.foundObjects():
            if len(elem.getElements()) > 0:  # Check if it has a mesh already
                pass
            else:
                cellsToMesh.append(elem)
                seedEdge = apex.EntityCollection()
                for Edge in elem.getEdges():
                    if 0.9 * VertThick <= Edge.getLength() <= 1.1 * VertThick:
                        seedEdge.append(Edge)
                        print(Edge.getLength())
                result = apex.mesh.createEdgeSeedUniformByNumber(
                    target=seedEdge,
                    numberElementEdges=1
                )

        for Cell in cellsToMesh:
            vecFaces = Cell.getFaces()
            for Face in vecFaces:
                paramU = Face.evaluatePointOnFace(Face.getCentroid()).u
                paramV = Face.evaluatePointOnFace(Face.getCentroid()).v
                normalAtPoint = Face.evaluateNormal(paramU, paramV)
                if abs(normalAtPoint.z) == 1:  # -Extrusion direction for meshing
                    _SweepFace = apex.EntityCollection()
                    _SweepFace.append(Face)
                    meshCell = apex.EntityCollection()
                    meshCell.append(Cell)
                    result = apex.mesh.createHexMesh(
                        name="",
                        target=meshCell,
                        meshSize=maxThick,
                        surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Pave,
                        mappedMeshDominanceLevel=2,
                        elementOrder=apex.mesh.ElementOrder.Linear,
                        refineMeshUsingCurvature=False,
                        elementGeometryDeviationRatio=0.10,
                        elementMinEdgeLengthRatio=0.20,
                        createFeatureMeshOnWashers=False,
                        createFeatureMeshOnArbitraryHoles=False,
                        preserveWasherThroughMesh=True,
                        sweepFace=_SweepFace,
                        hexMeshMethod=apex.mesh.HexMeshMethod.Auto
                    )
                    break


#############################################################################################################################
