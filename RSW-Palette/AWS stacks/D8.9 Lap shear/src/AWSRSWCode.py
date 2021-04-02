# coding: utf-8

import apex
from apex.construct import Point3D, Point2D
import os
apex.disableShowOutput()

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
model_1 = apex.currentModel()


def buildLapShear(dict={}):
    # - Get the data from the dictionary
    try:
        Thick01 = float(dict["Thick01"])
        Thick02 = float(dict["Thick02"])
        GapSize = float(dict["GapSize"])
        spotSize = float(dict["SpotSize"])
    except:
        apex.enableShowOutput()
        print("Please use only numbers as input in the fields.")


    ## Define max and min thickness
    if Thick01 >= Thick02:
        maxThick = Thick01
        minThick = Thick02
    else:
        maxThick = Thick02
        minThick = Thick01
    avgThick = (maxThick + minThick) / 2.0

    if maxThick < 1.30:
        CouponLength = 105
        CouponWidth = 45
        CouponOverlap = 35
        SampleLength = 175
        GrippedLength = 40
        UnclampedLength = 95
    else:
        CouponLength = 138
        CouponWidth = 60
        CouponOverlap = 45
        SampleLength = 230
        GrippedLength = 62.5
        UnclampedLength = 105


    model_1 = apex.currentModel()

    ParentAssy = model_1.createAssembly(name="AWS-RSW-LapShear")

    # -- Build Upper sheet
    Sheet01 = apex.createPart()
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet01',
        description='',
        length=CouponLength,  # Length
        height=CouponWidth,  # Width
        depth=Thick02,  # Thickness
        origin=apex.Coordinate(0.0, 0.0, Thick01),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet01.setParent(ParentAssy)
    res = Sheet01.update(name=f'UpperSheet-{Thick02}mm')

    # -- Build lower sheet
    Sheet02 = apex.createPart()
    result = apex.geometry.createBoxByLocationOrientation(
        name='Sheet02',
        description='',
        length=CouponLength,  # Length
        height=CouponWidth,  # Width
        depth=Thick01,  # Thickness
        origin=apex.Coordinate(0.0, 0.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )
    res = Sheet02.setParent(ParentAssy)
    res = Sheet02.update(name=f'LowerSheet-{Thick01}mm')


    # -- Translate sheet to the correct overlap length
    _translateSheet = apex.EntityCollection()
    _translateSheet.append(Sheet02.getSolids()[0])
    newEntities = apex.transformTranslate(
        target=_translateSheet,
        direction=[-1.0, 0.0, 0.0],
        distance=(CouponLength - CouponOverlap),
        makeCopy=False
    )
    
    # -- Creating split regions
    cylPart = model_1.createPart(name="Cylinder")
    result = apex.geometry.createCylinderByLocationOrientation(
        name='',
        description='',
        length=(maxThick + minThick),
        radius=spotSize,
        sweepangle=360.0,
        origin=apex.Coordinate(CouponOverlap / 2.0, CouponWidth / 2.0, 0.0),
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
        origin=apex.Coordinate(CouponOverlap / 2.0, CouponWidth / 2.0, 0.0),
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
        origin=apex.Coordinate(CouponOverlap / 2.0, CouponWidth / 2.0, 0.0),
        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
    )

    # -- Split sheets
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
    #apex.deleteEntities(entities_1)

    _plane = apex.construct.Plane(
        apex.construct.Point3D(CouponOverlap / 2.0, CouponWidth / 2.0, 0.0),
        apex.construct.Vector3D(1.0, 0.0, 0.0)
    )
    result = apex.geometry.splitWithPlane(
        target=_target,
        plane=_plane,
        splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
    )
    # -- Translate
    _translateSheet = apex.EntityCollection()
    _translateSheet.append(Sheet01.getSolids()[0])
    newPosition = apex.transformTranslate(
        target=_translateSheet,
        direction=[0.0, 0.0, 1.0],
        distance=GapSize,
        makeCopy=False
    )

    # -- Create grippers
    if dict["CreateGrippers"] == 'True':
        # -- Build Upper gripper
        UpperGripper = apex.createPart()
        result = apex.geometry.createBoxByLocationOrientation(
            name='UpperGripper',
            description='',
            length=1.2 * GrippedLength,  # Length
            height=CouponWidth,  # Width
            depth=3 * Thick02,  # Thickness
            origin=apex.Coordinate(0.0, 0.0, Thick01),
            orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
        )
        res = UpperGripper.setParent(ParentAssy)
        res = UpperGripper.update(name=f'UpperGripper')

        # -- Translate
        _translateSheet = apex.EntityCollection()
        _translateSheet.append(UpperGripper.getSolids()[0])
        newPosition = apex.transformTranslate(
            target=_translateSheet,
            direction=[1.0, 0.0, 0.0],
            distance=(CouponLength - GrippedLength),
            makeCopy=False
        )
        newPosition = apex.transformTranslate(
            target=_translateSheet,
            direction=[0.0, 0.0, -1.0],
            distance=(Thick02 + GapSize),
            makeCopy=False
        )
        _target = apex.EntityCollection()
        _target.append(UpperGripper.getSolids()[0])
        _subtractingEntities = apex.EntityCollection()
        _subtractingEntities.append(Sheet01.getSolids()[0])
        result = apex.geometry.subtractBoolean(
            target=_target,
            subtractingEntity=_subtractingEntities,
            retainOriginalBodies=True
        )

        # -- Build Lower gripper
        LowerGripper = apex.createPart()
        result = apex.geometry.createBoxByLocationOrientation(
            name='LowerGripper',
            description='',
            length=1.2 * GrippedLength,  # Length
            height=CouponWidth,  # Width
            depth=3 * Thick01,  # Thickness
            origin=apex.Coordinate(0.0, 0.0, Thick01),
            orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
        )
        res = LowerGripper.setParent(ParentAssy)
        res = LowerGripper.update(name=f'LowerGripper')

        # -- Translate
        _translateSheet = apex.EntityCollection()
        _translateSheet.append(LowerGripper.getSolids()[0])
        newPosition = apex.transformTranslate(
            target=_translateSheet,
            direction=[-1.0, 0.0, 0.0],
            distance=(CouponLength - CouponOverlap + 0.2 * GrippedLength),
            makeCopy=False
        )
        newPosition = apex.transformTranslate(
            target=_translateSheet,
            direction=[0.0, 0.0, -1.0],
            distance=(Thick01 + Thick02),
            makeCopy=False
        )
        _target = apex.EntityCollection()
        _target.append(LowerGripper.getSolids()[0])
        _subtractingEntities = apex.EntityCollection()
        _subtractingEntities.append(Sheet02.getSolids()[0])
        result = apex.geometry.subtractBoolean(
            target=_target,
            subtractingEntity=_subtractingEntities,
            retainOriginalBodies=True
        )

        _target = apex.EntityCollection()
        for Edge in UpperGripper.getSolids()[0].getEdges():
            _target.append(Edge)
        for Edge in LowerGripper.getSolids()[0].getEdges():
            _target.append(Edge)

        try:
            result = apex.geometry.pushPull(
                target=_target,
                method=apex.geometry.PushPullMethod.Fillet,
                behavior=apex.geometry.PushPullBehavior.FollowShape,
                removeInnerLoops=False,
                createBooleanUnion=False,
                distance=0.05,
                direction=[7.071067811865475e-01, 7.071067811865475e-01, 0.0]
            )
        except:
            pass

    
    # -- Perform meshing if requested
    if dict["Meshing"] != 'No mesh':

        if dict["Meshing"] == "For weld":
            refLevel = 4.0 # Ref level for weld only
        else:
            refLevel = 8.0 # Ref level for pull test

        # - Meshing Sheet 01 and Sheet 02
        refPoint = apex.Coordinate(CouponOverlap / 2.0, CouponWidth / 2.0, 0.0)
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
                meshSize=(minThick / refLevel),
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
                            if 0.9 * Thick02 <= Edge.getLength() <= 1.1 * Thick02:
                                seedEdge.append(Edge)
                        else:
                            if 0.9 * Thick01 <= Edge.getLength() <= 1.1 * Thick01:
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

        _target = apex.EntityCollection()
        _target.append(LowerGripper.getSolids()[0])
        _target.append(UpperGripper.getSolids()[0])
        featuremeshtypes_2 = apex.mesh.FeatureMeshTypeVector()
        result = apex.mesh.createSurfaceMesh(
            name="",
            target=_target,
            meshSize=minThick,
            meshType=apex.mesh.SurfaceMeshElementShape.Quadrilateral,
            meshMethod=apex.mesh.SurfaceMeshMethod.Auto,
            mappedMeshDominanceLevel=2,
            elementOrder=apex.mesh.ElementOrder.Linear,
            refineMeshUsingCurvature=False,
            elementGeometryDeviationRatio=0.10,
            elementMinEdgeLengthRatio=0.20,
            growFaceMeshSize=False,
            faceMeshGrowthRatio=1.2,
            createFeatureMeshes=False,
            featureMeshTypes=featuremeshtypes_2,
            projectMidsideNodesToGeometry=True,
            useMeshFlowOptimization=True,
            meshFlow=apex.mesh.MeshFlow.Grid
        )
