# coding: utf-8
import apex
apex.disableShowOutput()

def CreateSpots(dict={}):
    from apex.construct import Point3D, Point2D
    from math import sqrt, pow, degrees, acos, pi
    import os

    apex.setScriptUnitSystem(unitSystemName=r'''mm-kg-s-N''')
    absPath = os.path.dirname(os.path.realpath(__file__))

    ### Math functions needed when numpy is not available
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

    def CreateSpotGroup(CSVPath="Path", RefineDiam=8.0):
        model_1 = apex.currentModel()

        if "/" in CSVPath:
            TrajectoryName = CSVPath[CSVPath.rfind("/") + 1:-4]
        else:
            TrajectoryName = CSVPath[CSVPath.rfind("\\") + 1:-4]

        try:
            TrajAssy = model_1.getAssembly(pathName="Trajectories")
        except:
            TrajAssy = model_1.createAssembly(name="Trajectories")

        WeldPositions = []
        ScalingToMM = 1.0
        with open(CSVPath, 'r') as CSVFile:
            for line in CSVFile:
                if "Length unit:" in line:
                    unit = line.strip().split('[')[-1].replace("]", "")
                    if unit == "mm":
                        ScalingToMM = 1.0
                    elif unit == "m":
                        ScalingToMM = 1000.0
                    elif uni == "in":
                        ScalingToMM = 25.40

                if ('true' in line) or ('false' in line):
                    WeldPositions.append([ScalingToMM * float(x) for x in line.strip().split(';')[2:5]])

        for spotPoint in WeldPositions:
            result = apex.geometry.createSphereByLocationOrientation(
                name='',
                description='',
                radius=RefineDiam / 2.0,
                origin=apex.Coordinate(spotPoint[0], spotPoint[1], spotPoint[2]),
                orientation=apex.construct.createOrientation(alpha=0.0, beta=0.0, gamma=0.0)
            )

            model_1.getCurrentPart().update(name=TrajectoryName)
            ans = model_1.getCurrentPart().setParent(parent=TrajAssy)
        
        try:
            if model_1.getAssembly("Trajectories").getPart(name="RefDiam_{0}".format(RefineDiam)):
                pass
            else:
                SpecifiedDiameter = apex.createPart(name = "RefDiam_{0}".format(RefineDiam))
                SpecifiedDiameter.setParent(model_1.getAssembly("Trajectories"))
        except:
            print("Part creation failed!")

    
    vecFiles = dict["FileList"][0:-1].split(',')
    for file in vecFiles:
        CreateSpotGroup(CSVPath = file, RefineDiam = float(dict["RefineDiameter"]))

# 
# Macro recording stopped on Nov 26, 2018 at 17:52:26
#
