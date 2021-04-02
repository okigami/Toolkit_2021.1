# coding: utf-8

import apex
from apex.construct import Point3D, Point2D
import os
import sys
from math import sin, cos, radians

apex.setScriptUnitSystem(unitSystemName=r'''mm-kg-s-N''')
apex.disableShowOutput()

# - Slicer function
#   1) Take solidBody -> Apex solid body (geometry)
#   2) Create cutting section at cutPos with cutAngleDeg -> cutPos is a 3-element list
#   3) Export trajectory
def Slicer(solidBody="", cutPos=[], cutAngleDeg="", maxPointSpacing=0.0, pathToSaveFile=""):
    workingSolid = solidBody

    # -Collect all vertices before partitioning, so I know which ones were created after the cut
    allEdgesIDBefore = []
    for elem in workingSolid.getEdges():
        allEdgesIDBefore.append(elem.getId())

    # -Create cutting plane location and orientation for partitioning (currently cutting on XY-plane)
    _plane = apex.construct.Plane(
        apex.construct.Point3D(float(cutPos[0]), float(cutPos[1]), float(cutPos[2])),
        apex.construct.Vector3D(cos(radians(cutAngleDeg)), sin(radians(cutAngleDeg)), 0.000000)
    )

    _target = apex.EntityCollection()
    _target.append(workingSolid)

    # -Create partition
    result = apex.geometry.splitWithPlane(
        target=_target,
        plane=_plane,
        splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
    )

    # -Collect all vertices after partitioning, IDs of old vertices will not change
    allEdgesIDAfter = []
    for elem in workingSolid.getEdges():
        allEdgesIDAfter.append(elem.getId())

    # -Check which vertices were created by the partitioning operation
    newEdgesID = (list(set(allEdgesIDAfter) - set(allEdgesIDBefore)))
    newEdgesHeight = []
    for EdgeID in newEdgesID:
        newEdgesHeight.append(workingSolid.getEdge(id=int(EdgeID)).getMidPoint().z)

    sortedByHeight = [int(x) for _,x in sorted(zip(newEdgesHeight, newEdgesID))]

    workingEdge = workingSolid.getEdge(id=sortedByHeight[-1])
    workingEdgeLength = workingEdge.getLength()

    
    # -Getting faces that are connected to this edge (at least three will come up)
    proxSearch = apex.utility.ProximitySearch()
    listOfConnectedFaces = workingEdge.getConnectedFaces()
    ans = proxSearch.insertCollection(listOfConnectedFaces)

    # -Find the face on which the edge is lying on top (should be only one)
    edgeMidpoint = workingEdge.getMidPoint()
    resSearch = proxSearch.findNearestObjects(location=edgeMidpoint, numObjects=1)
    selectedFace = ""
    for elem in resSearch.foundObjects():
        selectedFace = elem

    # -Define trajectory characteristics
    if maxPointSpacing > 0:
        trajStep = int(workingEdgeLength / maxPointSpacing)
        trajResolution = trajStep + 1 if trajStep > 2 else 3
    else:
        trajResolution = 4
    paramRange = workingEdge.getParametricRange()
    delta = abs(paramRange['uEnd'] - paramRange['uStart']) / trajResolution
    sampling = [(x * delta) + paramRange['uStart'] for x in range(0, trajResolution + 1)]

    # -Build trajectory information
    trajInfo = []
    for i in range(len(sampling)):
        pointCoord = [workingEdge.evaluateEdgeParametricCoordinate(sampling[i]).x / 1000,  # Converting to meters
                      workingEdge.evaluateEdgeParametricCoordinate(sampling[i]).y / 1000,  # Converting to meters
                      workingEdge.evaluateEdgeParametricCoordinate(sampling[i]).z / 1000]  # Converting to meters

        pointResolve = apex.Coordinate(pointCoord[0] * 1000,  # Converting to mm
                                       pointCoord[1] * 1000,  # Converting to mm
                                       pointCoord[2] * 1000)  # Converting to mm
        paramU = selectedFace.evaluatePointOnFace(pointResolve).u
        paramV = selectedFace.evaluatePointOnFace(pointResolve).v
        normalAtPoint = selectedFace.evaluateNormal(paramU, paramV)
        pointDir = [normalAtPoint.x, normalAtPoint.y, normalAtPoint.z]
        trajInfo.append(pointCoord + pointDir)

    # -Get the correct file header from a Simufact trajectory
    trajHeader = "# CSV file produced by the DED slicing code"
    trajHeader += "\n# Date of creation: xx xx xxxx xx:xx:xx"
    trajHeader += "\n# Length unit: Meter [m]"
    trajHeader += "\n#"
    trajHeader += "\n# Orientation: 0 - global vector ; 1 - local vector; 2 - local second point"
    trajHeader += "\n1"
    trajHeader += "\n#"
    trajHeader += "\n# order;activity;x-coordinate;y-coordinate;z-coordinate;x-second point;y-second point;z-second point"

    trajBuild = trajHeader
    
    for i in range(len(trajInfo)):
        lineBuild = "\n{0};true;{1};{2};{3};0.0;0.0;1.0".format(i + 1, trajInfo[i][0],
                                                                trajInfo[i][1], trajInfo[i][2])
        trajBuild += lineBuild

    # -Write the trajectory file
    if pathToSaveFile:
        with open(pathToSaveFile, 'w') as newTrajFile:
            newTrajFile.write(trajBuild)


def FullSlicing(bodyToSlice="", cutStartPos=[], cutStepping=0.0, cutAngleDeg=0.0, maxPointSpacing=0.0,
                dirToSaveFiles="", trajName=""):
    if dirToSaveFiles:
        if not os.path.exists(dirToSaveFiles):
            os.makedirs(dirToSaveFiles)

    sinNum = sin(radians(cutAngleDeg))
    cosNum = cos(radians(cutAngleDeg))

    currTrajNum = 0
    currCutNum = 0
    while (True):  # Do the cutting to the left of the start point
        try:
            if trajName:
                newFile = str(trajName) + "_" + str(currTrajNum) + ".csv"
            else:
                newFile = "Trajectory_" + str(currTrajNum) + ".csv"

            if dirToSaveFiles:
                pathToSave = os.path.join(dirToSaveFiles, newFile)
            else:
                pathToSave = ""

            currCutPos = [float(cutStartPos[0]) + currCutNum * (cutStepping * cosNum),
                          float(cutStartPos[1]) + currCutNum * (cutStepping * sinNum),
                          float(cutStartPos[2])]

            Slicer(solidBody=bodyToSlice,
                   cutPos=currCutPos,
                   cutAngleDeg=cutAngleDeg,
                   maxPointSpacing=maxPointSpacing,
                   pathToSaveFile=pathToSave)
            currTrajNum += 1
            currCutNum += 1
        except:
            break


    currCutNum = 1
    while (True):  # Do the cutting to the right of the start point
        try:
            if trajName:
                newFile = str(trajName) + "_" + str(currTrajNum) + ".csv"
            else:
                newFile = "Trajectory_" + str(currTrajNum) + ".csv"

            if dirToSaveFiles:
                pathToSave = os.path.join(dirToSaveFiles, newFile)
            else:
                pathToSave = ""

            currCutPos = [float(cutStartPos[0]) - currCutNum * (cutStepping * cosNum),
                          float(cutStartPos[1]) - currCutNum * (cutStepping * sinNum),
                          float(cutStartPos[2])]

            Slicer(solidBody=bodyToSlice,
                   cutPos=currCutPos,
                   cutAngleDeg=cutAngleDeg,
                   maxPointSpacing=maxPointSpacing,
                   pathToSaveFile=pathToSave)
            currTrajNum += 1
            currCutNum += 1
        except:
            break


def verticalSlicing(dict={}):
    layerHeight = float(dict['layerHeight']) if dict['layerHeight'] else -1
    model_1 = apex.currentModel()

    for selectedFace in apex.selection.getCurrentSelection():
        currCut = layerHeight

        fCentr = [selectedFace.getCentroid().x, selectedFace.getCentroid().y, selectedFace.getCentroid().z]
        print(fCentr)
        paramU = selectedFace.evaluatePointOnFace(selectedFace.getCentroid()).u
        paramV = selectedFace.evaluatePointOnFace(selectedFace.getCentroid()).v
        normalAtPoint = selectedFace.evaluateNormal(paramU, paramV)
        normInvDir = [-1*normalAtPoint.x, -1*normalAtPoint.y, -1*normalAtPoint.z]
        print(paramU, paramV)
        
        _target = apex.EntityCollection()
        _target.append(selectedFace.getBody())
        while (True):  # Loop to split vertically
            try:
                vecDir = apex.construct.Vector3D(currCut * normInvDir[0], currCut * normInvDir[1], currCut * normInvDir[2])
                point3D = apex.construct.Point3D(   (currCut*normInvDir[0]) + fCentr[0],
                                                    (currCut*normInvDir[1]) + fCentr[1],
                                                    (currCut*normInvDir[2]) + fCentr[2])
                
                _plane = apex.construct.Plane(
                    point3D,
                    vecDir
                )
                if dict["splitBody"] == 'True':
                    result = apex.geometry.splitWithPlane(
                        target=_target,
                        plane=_plane,
                        splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
                    )
                else:
                    result = apex.geometry.splitWithPlane(
                        target=_target,
                        plane=_plane,
                        splitBehavior=apex.geometry.GeometrySplitBehavior.Split
                    )

                currCut += layerHeight
            except:
                e = sys.exc_info()[0]
                print(e)
                break



        listOfNames = []
        listOfCenterHeight = []
        for solid in model_1.getCurrentPart().getSolids():
            solid.update(enableTransparency=True, transparencyLevel=50)
            listOfNames.append(solid.getPathName())
            listOfCenterHeight.append(solid.getCentroid().z)

        sortedByHeight = [x for _, x in sorted(zip(listOfCenterHeight, listOfNames))]
        newPath = []
        for layerNum in range(len(sortedByHeight)):
            newPath.append(apex.getSolid(pathName=sortedByHeight[layerNum]).getPath() + "/Layer_{0}".format(layerNum))
            res = apex.getSolid(pathName=sortedByHeight[layerNum]).update(name="Layer_{0}".format(layerNum))

def hatchingLayers(dict={}):
    listOfNames = []
    listOfCenterHeight = []

    distLine = float(dict["distanceLine"])
    angleType = dict["angleType"]
    angleValue = dict["angleValue"]
    pointSpace = float(dict["pointSpacing"])
    meshIt = dict["meshIt"]
    saveToDir = dict["saveToDir"]

    if angleType == 'Cycle through':
        from itertools import cycle
        angleList = angleValue.strip().replace(' ', '').split(',')
        angleList = [float(x) for x in angleList]
        anglesCycle = cycle(angleList)

        def nextAngle():
            return next(anglesCycle)

    #for selObj in apex.selection.getCurrentSelection():
    model_1 = apex.currentModel()
    for Solid in apex.selection.getCurrentSelection():
        listOfNames.append(Solid.getPathName())
        listOfCenterHeight.append(Solid.getCentroid().z)
        entities_1 = apex.EntityCollection()
        entities_1.append(Solid)
        entities_1.hide()

    sortedByHeight = [x for _, x in sorted(zip(listOfCenterHeight, listOfNames))]

    currLayer = 1
    for solidPath in sortedByHeight:
        solidToSlice = apex.getSolid(pathName=solidPath)
        solidName = solidToSlice.getName()
        xCenter = solidToSlice.getCentroid().x
        yCenter = solidToSlice.getCentroid().y
        zCenter = solidToSlice.getCentroid().z
        startPos = [xCenter, yCenter, zCenter]

        entities_1 = apex.EntityCollection()
        entities_1.append(solidToSlice)
        entities_1.show()

        if angleType == 'Single angle':
            angle = float(angleValue)
        elif angleType == 'Incremental':
            angle = float(angleValue) * currLayer
        elif angleType == 'Cycle through':
            angle = nextAngle()

        FullSlicing(bodyToSlice=solidToSlice,
                    cutStartPos=startPos,
                    cutStepping=distLine,
                    cutAngleDeg=angle,
                    maxPointSpacing=pointSpace,
                    dirToSaveFiles=saveToDir,
                    trajName=solidName)
        currLayer += 1

    if meshIt == 'True':
        for solidPath in sortedByHeight:
            solidToMesh = apex.getSolid(pathName=solidPath)

            _target = apex.EntityCollection()
            _target.append(solidToMesh)
            _SweepFace = apex.EntityCollection()

            result = apex.mesh.createHexMesh(
                name="",
                target=_target,
                meshSize=distLine / 3,
                surfaceMeshMethod=apex.mesh.SurfaceMeshMethod.Mapped,
                mappedMeshDominanceLevel=3,
                elementOrder=apex.mesh.ElementOrder.Linear,
                refineMeshUsingCurvature=False,
                elementGeometryDeviationRatio=0.10,
                elementMinEdgeLengthRatio=0.50,
                createFeatureMeshOnWashers=False,
                createFeatureMeshOnArbitraryHoles=False,
                preserveWasherThroughMesh=False,
                sweepFace=_SweepFace,
                hexMeshMethod=apex.mesh.HexMeshMethod.Auto
            )
