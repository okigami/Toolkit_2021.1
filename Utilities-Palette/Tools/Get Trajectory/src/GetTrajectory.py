# coding: utf-8


import apex
from apex.construct import Point3D, Point2D
import sys
from math import sqrt, pow, degrees, acos, pi
import os

apex.setScriptUnitSystem(unitSystemName=r'''mm-kg-s-N''')
model_1 = apex.currentModel()
apex.disableShowOutput()


#
# Start of recorded operations
#

def extractTrajectory(dictionary={}):
    model_1 = apex.currentModel()
    dirToSave = dictionary["saveToDir"]

    for selEdge in apex.selection.getCurrentSelection():
        maxPointSpacing = 2  # mm
        workingEdge = selEdge
        workingEdgeLength = workingEdge.getLength()
        if selEdge.entityType != apex.EntityType.Edge:
            dictionary["getNormalDirection"] = "False"
            trajName = f"Trajectory_{selEdge.getName()}.csv"
        else:
            trajName = f"Trajectory_{selEdge.getId()}.csv"

        pathToSaveFile = os.path.join(dirToSave, trajName)


        if dictionary["getNormalDirection"] == 'True':
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
                pointCoord = [workingEdge.evaluateEdgeParametricCoordinate(sampling[i]).x / 1000,
                              # Converting to meters
                              workingEdge.evaluateEdgeParametricCoordinate(sampling[i]).y / 1000,
                              # Converting to meters
                              workingEdge.evaluateEdgeParametricCoordinate(
                                  sampling[i]).z / 1000]  # Converting to meters

                pointResolve = apex.Coordinate(pointCoord[0] * 1000,  # Converting to mm
                                               pointCoord[1] * 1000,  # Converting to mm
                                               pointCoord[2] * 1000)  # Converting to mm
                paramU = selectedFace.evaluatePointOnFace(pointResolve).u
                paramV = selectedFace.evaluatePointOnFace(pointResolve).v
                normalAtPoint = selectedFace.evaluateNormal(paramU, paramV)
                pointDir = [normalAtPoint.x, normalAtPoint.y, normalAtPoint.z]
                trajInfo.append(pointCoord + pointDir)

            # -Get the correct file header from a Simufact trajectory
            trajHeader = "# CSV file produced by the Welding Toolkit on MSC Apex"
            trajHeader += "\n# Date of creation: xx xx xxxx xx:xx:xx"
            trajHeader += "\n# Length unit: Meter [m]"
            trajHeader += "\n#"
            trajHeader += "\n# Orientation: 0 - global vector ; 1 - local vector; 2 - local second point"
            trajHeader += "\n1"
            trajHeader += "\n#"
            trajHeader += "\n# order;activity;x-coordinate;y-coordinate;z-coordinate;x-second point;y-second point;z-second point"

            trajBuild = trajHeader

            for i in range(len(trajInfo)):
                lineBuild = f"\n{i + 1};true;{trajInfo[i][0]};{trajInfo[i][1]};{trajInfo[i][2]};{trajInfo[i][3]};{trajInfo[i][4]};{trajInfo[i][5]}"
                trajBuild += lineBuild

            # -Write the trajectory file
            if pathToSaveFile:
                with open(pathToSaveFile, 'w') as newTrajFile:
                    newTrajFile.write(trajBuild)


        else:
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
                pointCoord = [workingEdge.evaluateEdgeParametricCoordinate(sampling[i]).x / 1000,
                              # Converting to meters
                              workingEdge.evaluateEdgeParametricCoordinate(sampling[i]).y / 1000,
                              # Converting to meters
                              workingEdge.evaluateEdgeParametricCoordinate(
                                  sampling[i]).z / 1000]  # Converting to meters
                trajInfo.append(pointCoord)

            # -Get the correct file header from a Simufact trajectory
            trajHeader = "# CSV file produced by the Apex Welding toolkit"
            trajHeader += "\n# Date of creation: xx xx xxxx xx:xx:xx"
            trajHeader += "\n# Length unit: Meter [m]"
            trajHeader += "\n#"
            trajHeader += "\n# Orientation: 0 - global vector ; 1 - local vector; 2 - local second point"
            trajHeader += "\n1"
            trajHeader += "\n#"
            trajHeader += "\n# order;activity;x-coordinate;y-coordinate;z-coordinate;x-second point;y-second point;z-second point"

            trajBuild = trajHeader

            for i in range(len(trajInfo)):
                lineBuild = f"\n{i + 1};true;{trajInfo[i][0]};{trajInfo[i][1]};{trajInfo[i][2]};0.0;0.0;1.0"
                trajBuild += lineBuild

            # -Write the trajectory file
            if pathToSaveFile:
                with open(pathToSaveFile, 'w') as newTrajFile:
                    newTrajFile.write(trajBuild)
