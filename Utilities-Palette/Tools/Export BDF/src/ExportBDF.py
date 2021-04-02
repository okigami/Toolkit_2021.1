import apex
from apex.construct import Point3D, Point2D
import os

apex.disableShowOutput()


def ExportBDF(dict={}):
    # ===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName=r'''mm-kg-s-N''')
    # Export mesh to BDF
    model_1 = apex.currentModel()
    pathToSave = dict["DirPath"]
    for Part in model_1.getParts(True):
        if "=" not in Part.getName():
            if Part.getVisibility():
                try:
                    Part.exportFEModel(
                        filename=os.path.join(pathToSave, Part.getName().replace(",",".") + ".bdf"),
                        unitSystem="m-kg-s-N-K",
                        exportWideFormat=False,
                        exportHierarchicalFiles=False,
                        resultOutputType=apex.attribute.NastranResultOutputType.Hdf5,
                        renumberMethod=apex.attribute.ExportRenumberMethod.Internal,
                        apexEngineeringAbstractions=False,
                    )
                except:
                    pass
    for f in os.listdir(pathToSave):
        if '.bdf' in f:
            BDFPath = os.path.join(pathToSave, f)
            newContent = ""
            print(f)
            with open(BDFPath, 'r') as oldBDF:
                for line in oldBDF:
                    line = line.strip()
                    spaceVec = "        "
                    if 'CQUAD' in line:
                        line = ' '.join(line.split())
                        vecStr = line.split()
                        vecStr[2] = '1'
                        finString = ""
                        for elem in vecStr:
                            finString += elem + spaceVec[0:8 - len(elem)]
                        newContent += finString + '\n'
                    elif 'CTRIA' in line:
                        line = ' '.join(line.split())
                        vecStr = line.split()
                        vecStr[2] = '1'
                        finString = ""
                        for elem in vecStr:
                            finString += elem + spaceVec[0:8 - len(elem)]
                        newContent += finString + '\n'
                    #elif 'PSHELL' in line:
                    #    pass
                    else:
                        newContent += line + '\n'
            with open(BDFPath, 'w') as newBDF:
                newBDF.write(newContent)