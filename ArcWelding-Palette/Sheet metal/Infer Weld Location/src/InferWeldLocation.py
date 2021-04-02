# coding: utf-8


import apex
from apex.construct import Point3D, Point2D
import sys
from math import sqrt, pow, degrees, acos, pi
import os

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
model_1 = apex.currentModel()
apex.disableShowOutput()
#
# Start of recorded operations
#

def createRefRegion(dict={}):
    model_1 = apex.currentModel()

    ### Math functions needed when numpy is not available
    def multip3D(v1, k):  # Addition of two ponts in 3D
        return [x * k for x in v1]

    def add3D(v1, v2):  # Addition of two ponts in 3D
        return [x + y for x, y in zip(v1, v2)]

    def subtract3D(v1, v2):  # Subtraction of two ponts in 3D
        return [x - y for x, y in zip(v1, v2)]

    def distance3D(v1, v2):  # Distance between two points in 3D
        return sqrt(abs(sum((a - b) for a, b in zip(v1, v2))))

    def dotproduct(v1, v2):  # Dot product of two vectors (list), cosine of the angle
        return sum((a * b) for a, b in zip(v1, v2))

    def length(v):  # Length of a vector (list)
        return sqrt(dotproduct(v, v))

    def angle(v1, v2):  # Angle between two vectors in degrees (lists)
        return degrees(acos(dotproduct(v1, v2) / (length(v1) * length(v2))))  # Return the angle in degrees

    def cross(a, b):  # Cross-product (orthogonal vector) of two vectors (list)
        c = [a[1] * b[2] - a[2] * b[1],
             a[2] * b[0] - a[0] * b[2],
             a[0] * b[1] - a[1] * b[0]]
        return c  # List of three components (x,y,z) of the orthogonal vector

    def doCircle(diam=8.0):
        part_1 = model_1.getCurrentPart()
        if part_1 is None:
            part_1 = model_1.createPart()
        sketch_1 = part_1.createSketchOnGlobalPlane(
            name='',
            plane=apex.construct.GlobalPlane.YZ,
            alignSketchViewWithViewport=True
        )

        circle_1 = sketch_1.createCircleCenterPoint(
            name="",
            centerPoint=Point2D(0, 0),
            pointOnCircle=Point2D(0, diam / 2)
        )
        return sketch_1.completeSketch(fillSketches=True)

    try:
        refDiameter = float(dict["refDiam"])
    except:
        apex.enableShowOutput()
        print("\nInvalid diameter value!")
        raise

    try:
        TrajAssy = model_1.getAssembly(pathName="Refinement regions")
    except:
        TrajAssy = model_1.createAssembly(name="Refinement regions")

    try:
        if TrajAssy.getPart(name=f"RefDiam_{refDiameter}"):
            pass
        else:
            SpecifiedDiameter = TrajAssy.createPart(name=f"RefDiam_{refDiameter}")
    except:
        apex.enableShowOutput()
        print("Part creation with refinement diameter info failed!")

    allLongEdges = apex.EntityCollection()
    for selElement in apex.selection.getCurrentSelection():
        # If selection is is a Part, go check what is inside
        if selElement.getVisibility():
            if selElement.entityType == apex.EntityType.Part:
                for Solid in selElement.getSolids():
                    if Solid.getVisibility():
                        maxEdgeLength = 0.0
                        selectedEdge = apex.EntityType.Edge
                        for Edge in Solid.getEdges():
                            if Edge.getLength() > maxEdgeLength:
                                selectedEdge = Edge
                                maxEdgeLength = Edge.getLength()
                        allLongEdges.append(selectedEdge)
                for Surface in selElement.getSurfaces():
                    if Surface.getVisibility():
                        maxEdgeLength = 0.0
                        selectedEdge = apex.EntityType.Edge
                        for Edge in Surface.getEdges():
                            if Edge.getLength() > maxEdgeLength:
                                selectedEdge = Edge
                                maxEdgeLength = Edge.getLength()
                        allLongEdges.append(selectedEdge)

        # If selection is an Assembly, get the Parts and check what is inside
        if selElement.entityType == apex.EntityType.Assembly:
            if selElement.getVisibility():
                for Part in selElement.getParts(True):
                    if Part.getVisibility():
                        for Solid in Part.getSolids():
                            if Solid.getVisibility():
                                maxEdgeLength = 0.0
                                selectedEdge = apex.EntityType.Edge
                                for Edge in Solid.getEdges():
                                    if Edge.getLength() > maxEdgeLength:
                                        selectedEdge = Edge
                                        maxEdgeLength = Edge.getLength()
                                allLongEdges.append(selectedEdge)
                        for Surface in Part.getSurfaces():
                            if Surface.getVisibility():
                                maxEdgeLength = 0.0
                                selectedEdge = apex.EntityType.Edge
                                for Edge in Surface.getEdges():
                                    if Edge.getLength() > maxEdgeLength:
                                        selectedEdge = Edge
                                        maxEdgeLength = Edge.getLength()
                                allLongEdges.append(selectedEdge)

    for selEdge in allLongEdges:
        CurrPart = TrajAssy.createPart(name="Edge_{0}_{1}mm".format(selEdge.getId(), refDiameter))

        maxPointSpacing = 2 #mm

        if maxPointSpacing > 0:
            trajStep = int(selEdge.getLength() / maxPointSpacing)
            trajResolution = trajStep + 1 if trajStep > 2 else 3
        else:
            trajResolution = 4
        paramRange = selEdge.getParametricRange()
        delta = abs(paramRange['uEnd'] - paramRange['uStart']) / trajResolution
        sampling = [(x * delta) + paramRange['uStart'] for x in range(0, trajResolution + 1)]

        _PointCollection = apex.IPhysicalCollection()
        PathPoints = []
        for i in range(len(sampling)):
            pointCoord = apex.Coordinate(selEdge.evaluateEdgeParametricCoordinate(sampling[i]).x ,
                                         selEdge.evaluateEdgeParametricCoordinate(sampling[i]).y ,
                                         selEdge.evaluateEdgeParametricCoordinate(sampling[i]).z)
            _PointCollection.append(pointCoord)

            PathPoints.append([selEdge.evaluateEdgeParametricCoordinate(sampling[i]).x ,
                               selEdge.evaluateEdgeParametricCoordinate(sampling[i]).y ,
                               selEdge.evaluateEdgeParametricCoordinate(sampling[i]).z])

        newSpline = apex.geometry.createCurve(
            target=_PointCollection,
            behavior=apex.geometry.CurveBehavior.Spline
        )

        CircleDone = doCircle(diam=refDiameter)

        ## Move circle to a new point location
        _target = apex.EntityCollection()
        _target.append(CurrPart.getSurfaces()[0])
        PathLength = sqrt(pow(PathPoints[0][0], 2) + pow(PathPoints[0][1], 2) + pow(PathPoints[0][2], 2))
        apex.transformTranslate(target=_target,
                                direction=[PathPoints[0][0], PathPoints[0][1], PathPoints[0][2]],
                                distance=PathLength,
                                makeCopy=False)
        ## Rotate the circle
        TurnAngle = angle([1, 0, 0], [a - b for a, b in zip(PathPoints[1], PathPoints[0])])
        if TurnAngle == 180:
            TurnAngle = 0
        apex.transformRotate(target=_target,
                             axisDirection=cross([1, 0, 0], [a - b for a, b in zip(PathPoints[1], PathPoints[0])]),
                             axisPoint=Point3D(PathPoints[0][0], PathPoints[0][1], PathPoints[0][2]),
                             angle=TurnAngle,
                             makeCopy=False)

        ## Do the sweep
        _target = apex.EntityCollection()
        _target.append(CurrPart.getSurfaces()[0])
        _path = apex.EntityCollection()
        _path.append(CurrPart.getCurves()[0])
        _lockDirection = apex.construct.Vector3D(0.0, 0.0, 0.0)

        try:
            result = apex.geometry.createGeometrySweepPath(
                target=_target,
                path=_path,
                scale=0.0,
                twist=0.0,
                profileSweepAlignmentMethod=apex.geometry.SweepProfileAlignmentMethod.Normal,
                islocked=False,
                lockDirection=_lockDirection,
                profileClamp=apex.geometry.SweepProfileClampingMethod.Smooth
            )

            CurrPart.getSolids()[0].update(enableTransparency=True, transparencyLevel=50)

            DelEntities = apex.EntityCollection()
            for Surface in CurrPart.getSurfaces():
                DelEntities.append(Surface)
            apex.deleteEntities(DelEntities)

            if dict["extendRegion"] == "True":
                for Face in CurrPart.getSolids()[0].getFaces():
                    XSectionArea = 3.14159 * (refDiameter / 2) ** 2
                    if (0.9 * XSectionArea) < Face.getArea() < (1.1 * XSectionArea):
                        _target = apex.EntityCollection()
                        _target.append(Face)
                        result = apex.geometry.pushPull(
                            target=_target,
                            method=apex.geometry.PushPullMethod.Normal,
                            behavior=apex.geometry.PushPullBehavior.FollowShape,
                            removeInnerLoops=False,
                            createBooleanUnion=False,
                            distance=refDiameter,
                            direction=[1.0, 1.0, 1.0]
                        )


        except:
            print("\nSweep failed!")
            NewPartName = apex.getPart(selEdge.getBody().getPath()).getName() + "_(failed)"
            ans = apex.getPart(selEdge.getBody().getPath()).update(name = NewPartName)

