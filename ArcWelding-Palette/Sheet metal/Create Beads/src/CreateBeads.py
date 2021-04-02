# coding: utf-8

def BeadBySweep(dict={}):
    import apex
    apex.disableShowOutput()
    from apex.construct import Point3D, Point2D
    from math import sqrt, pow, degrees, acos, pi
    import os
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')

    ### Math functions needed when numpy is not available
    def multip3D(v1, k): # Addition of two ponts in 3D
        return [x*k for x in v1]
    def add3D(v1, v2): # Addition of two ponts in 3D
        return [x + y for x, y in zip(v1, v2)]
    def subtract3D(v1, v2): # Subtraction of two ponts in 3D
        return [x - y for x, y in zip(v1, v2)]
    def distance3D(v1, v2): # Distance between two points in 3D
        return sqrt(abs(sum((a-b) for a, b in zip(v1, v2))))
    def dotproduct(v1, v2): # Dot product of two vectors (list), cosine of the angle
        return sum((a*b) for a, b in zip(v1, v2))
    def length(v): # Length of a vector (list)
        return sqrt(dotproduct(v, v))
    def angle(v1, v2): # Angle between two vectors in degrees (lists)
        return degrees(acos(dotproduct(v1, v2) / (length(v1) * length(v2)))) # Return the angle in degrees
    def cross(a, b): # Cross-product (orthogonal vector) of two vectors (list)
        c = [a[1]*b[2] - a[2]*b[1],
             a[2]*b[0] - a[0]*b[2],
             a[0]*b[1] - a[1]*b[0]]
        return c # List of three components (x,y,z) of the orthogonal vector
               
    def CreateWeldBead(CSVPath = "NoPath", RefineDiam = 4.0, UnitType = "None"):
        model_1 = apex.currentModel()
        if "/" in CSVPath:
            TrajectoryName = CSVPath[CSVPath.rfind("/")+1:-4]
        else:
            TrajectoryName = CSVPath[CSVPath.rfind("\\")+1:-4]
        
        try: 
            TrajAssy = model_1.getAssembly(pathName="Refinement regions")
        except:
            TrajAssy = model_1.createAssembly(name="Refinement regions")
        
        CurrPart = apex.createPart(name = TrajectoryName)
        CurrPart.setParent(model_1.getAssembly("Refinement regions"))
        
        vecLine = []
        with open(CSVPath, 'r') as CSVContent:
            if UnitType == 'Millimeters':
                convRatio = 1.0
            elif UnitType == 'Meters':
                convRatio = 1000.0
            elif UnitType == 'Inches':
                convRatio = 2.54
            for line in CSVContent:
                if ('true' in line) or ('false' in line):
                    vecLine.append([convRatio * float(X) for X in line.strip().split(';')[2:5]])

        
        ## Creating points at the location in the CSV file, these will guide the spline creation
        _iphysicalCollection = apex.IPhysicalCollection() 
        for i in range(len(vecLine)):
            _iphysicalCollection.append(apex.Coordinate(vecLine[i][0], vecLine[i][1], vecLine[i][2]))
        
        
        ## Create spline based on the list of points given by the CSV file
        result = apex.geometry.createCurve(
            target = _iphysicalCollection,
            behavior = apex.geometry.CurveBehavior.Spline
        )
        


        def doCircle(diam = 8.0):
            part_1 = model_1.getCurrentPart()
            if part_1 is None:
                part_1 = model_1.createPart()
            sketch_1 = part_1.createSketchOnGlobalPlane(
                name = 'Sketch 1',
                plane = apex.construct.GlobalPlane.YZ,
                alignSketchViewWithViewport = True
            )

            circle_1 = sketch_1.createCircleCenterPoint(
                name = "Circle 1",
                centerPoint = Point2D(0, 0),
                pointOnCircle = Point2D(0, diam/2)
            )
            return sketch_1.completeSketch( fillSketches = True )

        CircleDone = doCircle(diam = RefineDiam)
        

        ## Move circle to a new point location
        part_2 = model_1.getCurrentPart()
        for Surf in part_2.getSurfaces():
            CurrPath = Surf.getPathName()
        CurrPath = CurrPath[CurrPath.find('/')+1:]
        _entities = model_1.getEntities( pathNames = [ CurrPath ] )
        PathLength = sqrt(pow(vecLine[0][0],2)+pow(vecLine[0][1],2)+pow(vecLine[0][2],2))
        apex.transformTranslate( target = _entities,
                        direction = vecLine[0],
                        distance = PathLength,
                        makeCopy = False)

                        
        ## Rotate the circle
        _entities = model_1.getEntities( pathNames = [ CurrPath ] )
        TurnAngle = angle([1, 0, 0], [a-b for a,b in zip(vecLine[1],vecLine[0])])
        if TurnAngle == 180:
            TurnAngle = 0
        apex.transformRotate( target = _entities,
                        axisDirection = cross([1,0,0], [a - b for a, b in zip(vecLine[1], vecLine[0])]),
                        axisPoint = Point3D( vecLine[0][0], vecLine[0][1], vecLine[0][2]),
                        angle = TurnAngle,
                        makeCopy = False)

        _target = apex.EntityCollection()
        _target.append( model_1.getCurrentPart().getSurfaces()[0] )
        _path = apex.EntityCollection()
        _path.append( model_1.getCurrentPart().getCurves()[0] )
        _lockDirection = apex.construct.Vector3D( 0.0, 0.0, 0.0 )

        try:
            result = apex.geometry.createGeometrySweepPath(
                target = _target,
                path = _path,
                scale = 0.0,
                twist = 0.0,
                profileSweepAlignmentMethod = apex.geometry.SweepProfileAlignmentMethod.Normal,
                islocked = False,
                lockDirection = _lockDirection,
                profileClamp = apex.geometry.SweepProfileClampingMethod.Smooth
            )
            GotBead = True
        except:
            print("Sweep failed...")
            GotBead = False


        ## Clean up the supporting geometries (points, curves, surfaces, etc.)
        DelEntities = apex.EntityCollection()
        
        ## Do NOT delete curves, they are used to get weld bead length
        """
        DelCurves = model_1.getCurrentPart().getCurves()
        for Curve in DelCurves:
            DelEntities.append(Curve)
            
        DelPoints = model_1.getCurrentPart().getPoints()
        for Point in DelPoints:
            DelEntities.append(Point)
        """

        if GotBead:
            DelSurfaces = model_1.getCurrentPart().getSurfaces()
            for Surface in DelSurfaces:
                DelEntities.append(Surface)
            apex.deleteEntities(DelEntities)

        ## Rename part and solid
        if GotBead:
            updateSolidName = model_1.getCurrentPart().getSolids()[0].update(name = TrajectoryName)
            if dict["ExtendBead"] == "True": #Push-pull the extremities by the diameter amount
                try:
                    for Face in model_1.getCurrentPart().getSolids()[0].getFaces():
                        XSectionArea = 3.14159 * (RefineDiam / 2) ** 2
                        if (0.9 * XSectionArea) < Face.getArea() < (1.1 * XSectionArea):
                            _target = apex.EntityCollection()
                            _target.append(Face)
                            result = apex.geometry.pushPull(
                                target=_target,
                                method=apex.geometry.PushPullMethod.Normal,
                                behavior=apex.geometry.PushPullBehavior.FollowShape,
                                removeInnerLoops=False,
                                createBooleanUnion=False,
                                distance=RefineDiam,
                                direction=[1.0, 1.0, 1.0]
                            )
                except:
                    updatePartName = model_1.getCurrentPart().update(name=TrajectoryName + "_ExtendFailed")
        else:
            updatePartName = model_1.getCurrentPart().update(name=TrajectoryName + "_SweepFailed")
        
        try:
            if model_1.getAssembly("Refinement regions").getPart(name="RefDiam_{0}".format(RefineDiam)):
                pass
            else:
                SpecifiedDiameter = apex.createPart(name = "RefDiam_{0}".format(RefineDiam))
                SpecifiedDiameter.setParent(model_1.getAssembly("Refinement regions"))
        except:
            print("Part creation failed!")

    #print(len(dict["FileList"]))
    vecFiles = dict["FileList"][0:-1].split(',')
    for file in vecFiles:
        CreateWeldBead(CSVPath = file, RefineDiam = float(dict["BeadLeg"])*2, UnitType = dict["unitType"])
