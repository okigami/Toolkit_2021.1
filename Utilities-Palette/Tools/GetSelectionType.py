# coding: utf-8

import apex
from apex.construct import Point3D, Point2D

apex.setScriptUnitSystem(unitSystemName=r'''mm-kg-s-N''')
#apex.disableShowOutput()


def ShowType(dict={}):
    model_1 = apex.currentModel()
    _splitter = apex.EntityCollection()
    for Elem in apex.selection.getCurrentSelection():
        print(type(Elem))
        print(Elem.getBody().getPathName())