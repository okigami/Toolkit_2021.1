# coding: utf-8

import apex
from apex.construct import Point3D, Point2D

apex.setScriptUnitSystem(unitSystemName=r'''mm-kg-s-N''')
apex.disableShowOutput()


def ExpandSplit(dict={}):
    try:
        distance = float(dict["distance"])
    except ValueError:
        apex.enableShowOutput()
        print("Non-numeric input for distance, must be a number!")
        raise

    model_1 = apex.currentModel()
    SelectedAssyName = ""
    _splitter = apex.EntityCollection()
    for Assembly in apex.selection.getCurrentSelection():
        SelectedAssyName = Assembly.getName()
        for Part in Assembly.getParts(True):
            for Solid in Part.getSolids():
                for Face in Solid.getFaces():
                    _splitter.append(Face)

    if dict["splitSolids"] == 'True':
        includeSolid = True
    else:
        includeSolid = False
    if dict["splitSurfaces"] == 'True':
        includeSurface = True
    else:
        includeSurface = False

    _target = apex.EntityCollection()
    for Part in model_1.getParts(True):
        if SelectedAssyName not in Part.getPathName():
            if Part.getVisibility():
                if includeSolid:
                    for Solid in Part.getSolids():
                        if Solid.getVisibility():
                            _target.append(Solid)
                if includeSurface:
                    for Surface in Part.getSurfaces():
                        if Surface.getVisibility():
                            _target.append(Surface)


    try:
        result = apex.geometry.splitEntityWithOffsetFaces(
            target=_target,
            splitter=_splitter,
            offset= (-1.0 * distance), # Negative value to make it expand outwards, it does inwards otherwise
            splitBehavior=apex.geometry.GeometrySplitBehavior.Partition
        )
    except:
        print("Split failed, ty using the Apex builtin tool instead. It is under partitioning, using offset.")
        apex.enableShowOutput()

    if dict["suppressVertices"] == 'True':
        _target = apex.EntityCollection()
        for Part in model_1.getParts(True):
            if SelectedAssyName not in Part.getPathName():
                for Surface in Part.getSurfaces():
                    if Surface.getVisibility():
                        _target.append(Surface.getVertices())
        try:
            result = apex.geometry.suppressOnly(
                target=_target,
                maxEdgeAngle=1.000000000000000e+01,
                maxFaceAngle=5.000000000000000,
                keepVerticesAtCurvatureChange=False,
                cleanupTol=1.000000000000000,
                forceSuppress=False
            )
        except:
            apex.enableShowOutput()
            raise
