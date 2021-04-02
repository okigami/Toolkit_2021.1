# coding: utf-8


import apex
from apex.construct import Point3D, Point2D

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
model_1 = apex.currentModel()

# 
# Start of recorded operations
# 

def filterFixture(dict={}):
    #apex.disableShowOutput()
    model_1 = apex.currentModel()

    try:
        distTolerance = float(dict["searchDistance"])
    except:
        raise

    for selElem in apex.selection.getCurrentSelection():
        listOfRefSolid = []
        listOfRefSolidPaths = []

        if dict["newAssy"] == 'True':
            ntAssy = model_1.createAssembly(name="Coincident with {0}".format(selElem.getName()))
        else:
            ntAssy = None

        if selElem.entityType == apex.EntityType.Assembly:
            if ntAssy:
                ntAssy.setParent(selElem)

            for Part in selElem.getParts(True):
                Part.update(color=[0, 0, 255])
                Part.show()
                for Solid in Part.getSolids():
                    listOfRefSolidPaths.append(Solid.getPathName())
                    listOfRefSolid.append(Solid)

        elif selElem.entityType == apex.EntityType.Part:
            if ntAssy:
                ntAssy.setParent(selElem.getParent())

            selElem.update(color=[0, 0, 255])
            selElem.show()
            for Solid in selElem.getSolids():
                listOfRefSolidPaths.append(Solid.getPathName())
                listOfRefSolid.append(Solid)

        listOfTargetSolids = apex.EntityCollection()
        for Part in model_1.getParts(True):
            if Part.getVisibility():
                for Solid in Part.getSolids():
                    if Solid.getPathName() not in listOfRefSolidPaths:
                        listOfTargetSolids.append(Solid)
        listOfTargetSolids.hide()

        for refSolid in listOfRefSolid:
            textDisplay = apex.display.displayText(text=refSolid.getName(),
                                     textLocation=refSolid.getCentroid(),
                                     graphicsFont="Calibri",
                                     graphicsFontColor=apex.ColorRGB(255, 191, 0),
                                     graphicsFontSize=12,
                                     graphicsFontStyle=apex.display.GraphicsFontStyle.Normal,
                                     graphicsFontUnderlineStyle=apex.display.GraphicsFontUnderlineStyle.NoUnderline
                                     )
            distance_ = apex.measureDistance(source=refSolid,
                                             target=listOfTargetSolids)
            newList = apex.EntityCollection()
            for k in range(len(distance_)):
                if distance_[k] <= distTolerance:
                    listOfTargetSolids[k].getParent().show()
                    if ntAssy:
                        res = listOfTargetSolids[k].getParent().setParent(parent=ntAssy)
                else:
                    newList.append(listOfTargetSolids[k])
            listOfTargetSolids = newList

            apex.display.clearAllGraphicsText()

