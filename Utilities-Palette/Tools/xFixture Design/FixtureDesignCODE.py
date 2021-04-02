import apex
from apex.construct import Point3D, Point2D
import datetime

apex.setScriptUnitSystem(unitSystemName = r'''mm-kg-s-N''')
model_1 = apex.currentModel()

#
# Start of recorded operations
#

def StiffnessOptimizer(dict={}):
    #apex.disableShowOutput()
    model_1 = apex.currentModel()

    try:
        maxNumPts = int(dict["MaxNumOfPoints"])
    except:
        apex.enableShowOutput()
        print("Need a number for the maximum number of points. Please have the correct input.")
        raise

    dummyMaterial = apex.catalog.createMaterial(name="Steel", description="", color=[64, 254, 250])
    dummyMaterial.update(elasticModulus=210.e+9, poissonRatio=0.3, density=7.8e-6)

    newAssyName = datetime.datetime.now().strftime("Test_%Y.%m.%d_%Hh%Mm%Ss")
    currAssy = model_1.createAssembly(name = newAssyName)

    for selPart in apex.selection.getCurrentSelection():
        _target = apex.EntityCollection()
        _target.append(selPart)
        apex.attribute.assignMaterial(material=dummyMaterial, target=_target)

        selPart.setParent(currAssy)

    context_ = currAssy
    study = apex.getPrimaryStudy()
    study.createScenarioByModelRep(context=context_, simulationType=apex.studies.SimulationType.NormalModes)

    study = apex.getPrimaryStudy()
    currScenario = study.getScenario(name = "Mode Scenario " + currAssy.getName())

    """
    simSetting1 = currScenario.simulationSettings
    simSetting1.partReduction = False
    simSetting1.freqRangeLower = 1000.
    simSetting1.freqRangeUpper = float('NaN')
    simSetting1.stopCalculation = True
    simSetting1.maxModes = 10
    currScenario.simulationSettings = simSetting1
    """

    model_1.save()
    currScenario.execute()
    executedscenario_1 = scenario1.getLastExecutedScenario()
