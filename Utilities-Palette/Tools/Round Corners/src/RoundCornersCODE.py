# coding: utf-8


import apex
from apex.construct import Point3D, Point2D

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
model_1 = apex.currentModel()
apex.disableShowOutput()
#
# Start of recorded operations
#

def roundSelection(dict={}):
    model_1 = apex.currentModel()

    try:
        roundRadius = float(dict["roundRadius"])
    except:
        apex.enableShowOutput()
        print("Invalid radius value!")

    _target = apex.EntityCollection()
    for selFace in apex.selection.getCurrentSelection():
        for Edge in selFace.getEdges():
            _target.append(Edge)

        try:
            result = apex.geometry.pushPull(
                target = _target,
                method = apex.geometry.PushPullMethod.Fillet,
                behavior = apex.geometry.PushPullBehavior.FollowShape,
                removeInnerLoops = False,
                createBooleanUnion = False,
                distance = roundRadius,
                direction = [ 7.071067811865475e-01, 7.071067811865475e-01, 0.0 ]
            )
        except:
            apex.enableShowOutput()
            print("Rounding failed for \n", selFace.getBody().getPathName() )
