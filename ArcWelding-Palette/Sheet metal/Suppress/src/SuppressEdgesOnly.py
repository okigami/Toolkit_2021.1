import apex
from apex.construct import Point3D, Point2D
apex.disableShowOutput()

def SuppressEdges(dict={}):
    #===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    model_1 = apex.currentModel()
    _target = apex.entityCollection()
    listOfVertices = []

    for part in model_1.getParts(True):
        if part.getVisibility():
            if 'Trajectories' not in part.getPath():
                for Solid in part.getSolids():
                    if Solid.getVisibility():
                        for Vertex in Solid.getVertices():
                            listOfEdges = []
                            listOfLengths = []
                            for Edge in Vertex.getConnectedEdges():
                                listOfEdges.append(Edge.getId())
                                listOfLengths.append(Edge.getLength())
                            if len(listOfEdges) > 2: # Suppress edges with more than 2 connections at the vertex
                                sortedByNumber = [int(x) for _, x in sorted(zip(listOfLengths, listOfEdges))]
                                _target.append(Solid.getEdge(id=sortedByNumber[0]))
                """
                for surface in part.getSurfaces():
                    if surface.getVisibility():
                        #_target.extend(surface.getEdges())
                        for Vertex in surface.getVertices():
                            listOfEdges = []
                            listOfLengths = []
                            for Edge in Vertex.getConnectedEdges():
                                listOfEdges.append(Edge.getId())
                                listOfLengths.append(Edge.getLength())
                            if len(listOfEdges) > 2:
                                sortedByHeight = [int(x) for _, x in sorted(zip(listOfLengths, listOfEdges))]
                                _target.append(surface.getEdge(id=sortedByHeight[0]))
                """

    result = apex.geometry.suppressOnly(
        target = _target,
        maxEdgeAngle = 1.745329251994330e-01,
        maxFaceAngle = 8.726646259971650e-02,
        keepVerticesAtCurvatureChange = False,
        cleanupTol = 1.000000000000000)
