import apex
from apex.construct import Point3D, Point2D

def Midsurface(dict={}):
    #===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    model_1 = apex.currentModel()

    # ===================================================================
    ## Extract midsurface for all parts
    numOfInvisible = 0
    numOfFailed = 0
    numOfMultiple = 0
    numOfCreated = 0
    numOfParts = len(model_1.getParts(recursive = True))
    for Part in model_1.getParts(recursive = True):
        if 'Trajectories' not in Part.getPathName():
            _target = apex.entityCollection()
            if Part.getVisibility():
                try:
                    listOfSolids = Part.getSolids()  # Get a list of all solids for a given part
                    for Solid in listOfSolids:  # Append this list of solids to the _target variable
                        _target = apex.entityCollection()
                        _target.append(Solid)
                        
                        A_old = apex.catalog.getSectionDictionary()
                        result = apex.geometry.assignConstantThicknessMidSurface(
                            target=_target,
                            autoAssignThickness=True,
                            autoAssignTolerance=5.0e-02
                        )
                        A_new = apex.catalog.getSectionDictionary()
                        new_thickness = { k : A_new[k] for k in set(A_new) - set(A_old) }
                        for key,value in new_thickness.items():
                            nthickness = value.thickness
                        
                        if len(Part.getSurfaces()) > 1:
                            Part.update(name = "{0}_CHECK(multiple)".format(Part.getName()))
                            numOfMultiple += 1
                        
                        else:
                            for entity in result: #'result' comes from the resulting collection of the midsurface extraction
                                if entity.entityType is apex.EntityType.Surface:
                                    CurrPartPath = apex.getPart(entity.getPath())
                                    CurrPartPath.update(name="{0}_{1}mm".format(CurrPartPath.getName(), str(round(float(nthickness),2)).replace(".",",")))
                                    numOfCreated += 1
                except:
                    Part.update(name = "{0}_CHECK(failed)".format(Part.getName()))
                    numOfFailed += 1
            else:
                numOfInvisible += 1