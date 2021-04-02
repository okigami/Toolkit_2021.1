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
        print("Part creation failed!")

    CurrPart = apex.createPart(name=f"FromEdge_{refDiameter}mm")
    CurrPart.setParent(TrajAssy)

    # - Merge contiguous edges into curves
    _edgeCollection = apex.geometry.EdgeCollection()
    _curveCollection = apex.geometry.CurveCollection()
    for selElem in apex.selection.getCurrentSelection():
        if selElem.entityType == apex.EntityType.Edge:
            _edgeCollection.append(selElem)
        elif selElem.entityType == apex.EntityType.Curve:
            _curveCollection.append(selElem)
    result_ = apex.geometry.createCurvesFromEdges(edges=_edgeCollection)
    result_.extend(_curveCollection)

    for k in range(len(result_)):
        thisCurve = result_[k]
        CurrPart = apex.createPart(name=f"FromEdge_L={int(thisCurve.getLength())}mm_D={refDiameter}mm")
        CurrPart.setParent(TrajAssy)
        thisCurve.setParent(CurrPart)

        CircleDone = doCircle(diam=refDiameter)

        StartPoint = thisCurve.getExteriorVertices()[0]

        ## Move circle to a new point location
        _target = apex.EntityCollection()
        _target.append(CurrPart.getSurfaces()[0])
        PathLength = sqrt(pow(StartPoint.getX(), 2) + pow(StartPoint.getY(), 2) + pow(StartPoint.getZ(), 2))
        apex.transformTranslate(target=_target,
                                direction=[StartPoint.getX(), StartPoint.getY(), StartPoint.getZ()],
                                distance=PathLength,
                                makeCopy=False)

        ## Rotate the circle
        tangVec = thisCurve.evaluateTangent(StartPoint)
        TurnAngle = angle([1, 0, 0], [tangVec.getX(), tangVec.getY(), tangVec.getZ()])
        axisDir = cross([1, 0, 0], [tangVec.getX(), tangVec.getY(), tangVec.getZ()])
        if TurnAngle == 180:
            TurnAngle = 0
        apex.transformRotate(target=_target,
                             axisDirection=axisDir,
                             axisPoint=StartPoint,
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


            DelEntities = apex.EntityCollection()
            for Surface in CurrPart.getSurfaces():
                DelEntities.append(Surface)
            apex.deleteEntities(DelEntities)

            if dict["extendRegion"] == "True":
                for pointLocation in thisCurve.getExteriorVertices():
                    result = apex.geometry.createSphereByLocationOrientation(
                        name='Sphere',
                        description='',
                        radius=refDiameter/2.0,
                        origin=pointLocation,
                        orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
                    )

                _target = apex.EntityCollection()
                _target.extend(CurrPart.getSolids())
                result = apex.geometry.mergeBoolean(
                    target=_target,
                    retainOriginalBodies=False,
                    mergeSolidsAsCells=False
                )

            CurrPart.getSolids()[0].update(enableTransparency=True, transparencyLevel=50)

        except:
            print("\nSweep failed!")
            raise