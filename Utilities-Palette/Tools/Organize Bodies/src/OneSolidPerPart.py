import apex
from apex.construct import Point3D, Point2D
apex.disableShowOutput()

def OrganizeSolids(dict={}):
    #===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    try:
        numOfSolidsChanged = 0
        for Part in apex.currentModel().getParts(recursive = True):
            if len(Part.getSolids()) > 1:
                for Solid in Part.getSolids()[1:]:
                    if Solid.getVisibility():
                        if dict["useSolidName"] == 'True':
                            newPart = apex.createPart(name = Solid.getName())
                            Solid.setParent(newPart)
                            numOfSolidsChanged += 1
                            if Part.getParent():
                                newPart.setParent(Part.getParent())
                        else:
                            newPart = apex.createPart(name = Part.getName())
                            Solid.setParent(newPart)
                            numOfSolidsChanged += 1
                            if Part.getParent():
                                newPart.setParent(Part.getParent())
        print("Reorganized {0} solids.".format(numOfSolidsChanged))
    except:
        print("Operation failed or not performed.")
                
