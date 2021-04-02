import apex
apex.enableShowOutput()

def CountVisibleElements(dict={}):
    apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
    model_1 = apex.currentModel()

    numOfElements = 0
    listOfParts = model_1.getParts(True)
    for Part in listOfParts:
        if Part.getVisibility():
            for Mesh in Part.getMeshes():
                numOfElements += len(Mesh.getElements())
                
    print('Elements in all visible meshes: ', numOfElements)
