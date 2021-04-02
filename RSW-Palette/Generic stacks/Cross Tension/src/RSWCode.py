# coding: utf-8

import apex
from apex.construct import Point3D, Point2D
import os
apex.disableShowOutput()

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
model_1 = apex.currentModel()


#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
def buildLapShear(dict={}):
    # - Get the data from the dictionary
    HorizWidth = float(dict["HorizWidth"])
    HorizLength = float(dict["HorizLength"])
    LowerThick = float(dict["HorizThick"])
    VertHeight = float(dict["VertHeight"])
    VertLength = float(dict["VertLength"])
    UpperThick = float(dict["VertThick"])
    spotSize = float(dict["SpotSize"])
    OverlapLength = float(dict["OverlapLength"])
    
    
    ## Define max and min thickness
    if LowerThick >= UpperThick:
        maxThick = LowerThick
        minThick = UpperThick
    else:
        maxThick = UpperThick
        minThick = LowerThick
    avgThick = (maxThick + minThick) / 2.0

    model_1 = apex.currentModel()

    ParentAssy = model_1.createAssembly(name="LapShear")
    Sheet01 = apex.createPart()

    # - Build the bottom plate
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet01',
        description='',
        length=HorizLength,  # Length
        height=HorizWidth,  # Width
        depth=LowerThick,  # Thickness
        origin=apex.Coordinate(0.0, 0.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet01.setParent(ParentAssy)
    res = Sheet01.update(name='LowerSheet')

    # - Build the upper plate
    Sheet02 = apex.createPart()
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet02',
        description='',
        length=VertLength,  # Length
        height=VertHeight,  # Width
        depth=UpperThick,  # Thickness
        origin=apex.Coordinate(0.0, 0.0, LowerThick),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet02.setParent(ParentAssy)
    res = Sheet02.update(name='UpperSheet')

    # - Translate sheet
    _translateSheet = apex.EntityCollection()
    _translateSheet.append(Sheet02.getSolids()[0])
    newEntities = apex.transformTranslate(
        target=_translateSheet,
        direction=[-1.0, 0.0, 0.0],
        distance=(HorizLength - OverlapLength),
        makeCopy=False
    )

    # Save joint info for reference
    JointInfoAssy = model_1.createAssembly("Joint info")
    res = JointInfoAssy.createPart( name="Sheet 01 = {0}mm".format(LowerThick))
    res = JointInfoAssy.createPart( name="Sheet 02 = {0}mm".format(UpperThick))
    res = JointInfoAssy.createPart( name="Width = {0}mm".format(HorizWidth))
    res = JointInfoAssy.createPart( name="Length = {0}mm".format(HorizLength))

    
    # Creating split regions
    cylPart = model_1.createPart(name="Cylinder")
    result = apex.geometry.createCylinderByLocationOrientation(
        name='',
        description='',
        length=(maxThick + minThick),
        radius=spotSize,
        sweepangle=360.0,
        origin=apex.Coordinate(OverlapLength / 2.0, HorizWidth / 2.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )

    entities_1 = apex.EntityCollection()
    entities_1.append(result)
    entities_1.hide()

    result = apex.geometry.createCylinderByLocationOrientation(
        name='',
        description='',
        length=(maxThick + minThick),
        radius=1.5 * spotSize,
        sweepangle=360.0,
        origin=apex.Coordinate(OverlapLength / 2.0, HorizWidth / 2.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )

    entities_1 = apex.EntityCollection()
    entities_1.append(result)
    entities_1.hide()

    result = apex.geometry.createCylinderByLocationOrientation(
        name='',
        description='',
        length=(maxThick + minThick),
        radius=2.0 * spotSize,
        sweepangle=360.0,
        origin=apex.Coordinate(OverlapLength / 2.0, HorizWidth / 2.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )

    ## Split sheets
    _target = apex.EntityCollection()
    _target.append( Sheet01.getSolids()[0] )
    _target.append( Sheet02.getSolids()[0] )
    _splitter = apex.EntityCollection()
    for Solid in cylPart.getSolids():
        _splitter.extend(Solid.getFaces())
    result = apex.geometry.split(
        target = _target,
        splitter = _splitter,
        splitBehavior = apex.geometry.GeometrySplitBehavior.Partition
    )

    entities_1 = apex.EntityCollection()
    entities_1.append(cylPart)
    apex.deleteEntities(entities_1)

    _plane = apex.construct.Plane(
        apex.construct.Point3D(OverlapLength / 2.0, HorizWidth / 2.0, 0.0),
        apex.construct.Vector3D(1.0, 0.0, 0.0)
    )
    result = apex.geometry.splitWithPlane(
        target=_target,
        plane=_plane,
        splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
    )

    
    ## - Perform meshing if requested
    if dict["MeshForMe"] == 'True':
        # - Meshing Sheet 01 and Sheet 02
        refPoint = apex.Coordinate(OverlapLength / 2.0, HorizWidth / 2.0, 0.0)
        listOfSolids = [Sheet01.getSolids()[0], Sheet02.getSolids()[0]]
        for i in range(len(listOfSolids)):
            proxSearch = apex.utility.ProximitySearch()
            ans = proxSearch.insertList(list(listOfSolids[i].getCells()))
            resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=4)

            cellsToMesh = apex.EntityCollection()
            for elem in resSearch.foundObjects():
                cellsToMesh.append(elem)

            _SweepFace = apex.EntityCollection()
            result = apex.mesh.createHexMesh(
                name="",
                target=cellsToMesh,
                meshSize=(minThick / 4.0),
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

            resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=8)
            cellsToMesh = apex.EntityCollection()
            for elem in resSearch.foundObjects():
                if len(elem.getElements()) > 0:  # Check if it has a mesh already
                    pass
                else:
                    cellsToMesh.append(elem)
                    seedEdge = apex.EntityCollection()
                    for Edge in elem.getEdges():
                        if i == 0:
                            if 0.9 * LowerThick <= Edge.getLength() <= 1.1 * LowerThick:
                                seedEdge.append(Edge)
                        else:
                            if 0.9 * UpperThick <= Edge.getLength() <= 1.1 * UpperThick:
                                seedEdge.append(Edge)
                    result = apex.mesh.createEdgeSeedUniformByNumber(
                        target=seedEdge,
                        numberElementEdges=2
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
                            meshSize=maxThick/1.5,
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


    
def buildCrossTension(dict={}):
    # - Get the data from the dictionary
    HorizWidth = float(dict["HorizWidth"])
    HorizLength = float(dict["HorizLength"])
    LowerThick = float(dict["HorizThick"])
    VertHeight = float(dict["VertHeight"])
    VertLength = float(dict["VertLength"])
    UpperThick = float(dict["VertThick"])
    spotSize = float(dict["SpotSize"])

    ## Define max and min thickness
    if LowerThick >= UpperThick:
        maxThick = LowerThick
        minThick = UpperThick
    else:
        maxThick = UpperThick
        minThick = LowerThick
    avgThick = (maxThick + minThick) / 2.0

    model_1 = apex.currentModel()

    ParentAssy = model_1.createAssembly(name="CrossTension")
    Sheet01 = apex.createPart()

    # - Build the bottom plate
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet01',
        description='',
        length=HorizLength,  # Length
        height=HorizWidth,  # Width
        depth=LowerThick,  # Thickness
        origin=apex.Coordinate(0.0, 0.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet01.setParent(ParentAssy)
    res = Sheet01.update(name='LowerSheet')

    # - Build the upper plate
    Sheet02 = apex.createPart()
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet02',
        description='',
        length=VertHeight,  # Length
        height=VertLength,  # Width
        depth=UpperThick,  # Thickness
        origin=apex.Coordinate(0.0, 0.0, LowerThick),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet02.setParent(ParentAssy)
    res = Sheet02.update(name='UpperSheet')

    # - Translate sheet
    _translateSheet = apex.EntityCollection()
    _translateSheet.append(Sheet02.getSolids()[0])
    newEntities = apex.transformTranslate(
        target=_translateSheet,
        direction=[1.0, 0.0, 0.0],
        distance=(HorizLength / 2.0 - VertHeight / 2.0),
        makeCopy=False
    )
    _translateSheet = apex.EntityCollection()
    _translateSheet.append(Sheet02.getSolids()[0])
    newEntities = apex.transformTranslate(
        target=_translateSheet,
        direction=[0.0, -1.0, 0.0],
        distance=(HorizLength / 2.0 - HorizWidth / 2.0),
        makeCopy=False
    )

    # Save joint info for reference
    JointInfoAssy = model_1.createAssembly("Joint info")
    res = JointInfoAssy.createPart(name="Sheet 01 = {0}mm".format(LowerThick))
    res = JointInfoAssy.createPart(name="Sheet 02 = {0}mm".format(UpperThick))
    res = JointInfoAssy.createPart(name="Width = {0}mm".format(HorizWidth))
    res = JointInfoAssy.createPart(name="Length = {0}mm".format(HorizLength))


    # Creating split regions
    cylPart = model_1.createPart(name="Cylinder")
    result = apex.geometry.createCylinderByLocationOrientation(
        name='',
        description='',
        length=(maxThick + minThick),
        radius=spotSize,
        sweepangle=360.0,
        origin=apex.Coordinate(HorizLength / 2.0, HorizWidth / 2.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )

    entities_1 = apex.EntityCollection()
    entities_1.append(result)
    entities_1.hide()

    result = apex.geometry.createCylinderByLocationOrientation(
        name='',
        description='',
        length=(maxThick + minThick),
        radius=1.5 * spotSize,
        sweepangle=360.0,
        origin=apex.Coordinate(HorizLength / 2.0, HorizWidth / 2.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )

    entities_1 = apex.EntityCollection()
    entities_1.append(result)
    entities_1.hide()

    result = apex.geometry.createCylinderByLocationOrientation(
        name='',
        description='',
        length=(maxThick + minThick),
        radius=2.0 * spotSize,
        sweepangle=360.0,
        origin=apex.Coordinate(HorizLength / 2.0, HorizWidth / 2.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )


    ## Split sheets
    _target = apex.EntityCollection()
    _target.append(Sheet01.getSolids()[0])
    _target.append(Sheet02.getSolids()[0])
    _splitter = apex.EntityCollection()
    for Solid in cylPart.getSolids():
        _splitter.extend(Solid.getFaces())
    result = apex.geometry.split(
        target=_target,
        splitter=_splitter,
        splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
    )

    entities_1 = apex.EntityCollection()
    entities_1.append(cylPart)
    apex.deleteEntities(entities_1)

    _plane = apex.construct.Plane(
        apex.construct.Point3D(HorizLength / 2.0, HorizWidth / 2.0, 0.0),
        apex.construct.Vector3D(1.0, 0.0, 0.0)
    )
    result = apex.geometry.splitWithPlane(
        target=_target,
        plane=_plane,
        splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
    )

    ## - Perform meshing if requested
    if dict["MeshForMe"] == 'True':
        # - Meshing Sheet 01 and Sheet 02
        refPoint = apex.Coordinate(HorizLength / 2.0, HorizWidth / 2.0, 0.0)
        listOfSolids = [Sheet01.getSolids()[0], Sheet02.getSolids()[0]]
        for i in range(len(listOfSolids)):
            proxSearch = apex.utility.ProximitySearch()
            ans = proxSearch.insertList(list(listOfSolids[i].getCells()))
            resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=4)

            cellsToMesh = apex.EntityCollection()
            for elem in resSearch.foundObjects():
                cellsToMesh.append(elem)

            _SweepFace = apex.EntityCollection()
            result = apex.mesh.createHexMesh(
                name="",
                target=cellsToMesh,
                meshSize=(minThick / 4.0),
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

            resSearch = proxSearch.findNearestObjects(location=refPoint, numObjects=8)
            cellsToMesh = apex.EntityCollection()
            for elem in resSearch.foundObjects():
                if len(elem.getElements()) > 0:  # Check if it has a mesh already
                    pass
                else:
                    cellsToMesh.append(elem)
                    seedEdge = apex.EntityCollection()
                    for Edge in elem.getEdges():
                        if i == 0:
                            if 0.9 * LowerThick <= Edge.getLength() <= 1.1 * LowerThick:
                                seedEdge.append(Edge)
                        else:
                            if 0.9 * UpperThick <= Edge.getLength() <= 1.1 * UpperThick:
                                seedEdge.append(Edge)
                    result = apex.mesh.createEdgeSeedUniformByNumber(
                        target=seedEdge,
                        numberElementEdges=2
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
                            meshSize=maxThick / 1.5,
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