import apex
from apex.construct import Point3D, Point2D
import os, time


# apex.disableShowOutput()

def GenerateStudies(dict={}):
    # ===================================================================
    ## Initializing Apex code
    apex.setScriptUnitSystem(unitSystemName=r'''mm-kg-s-N''')
    model_1 = apex.currentModel()

    # Check existing material and create generic steel if needed
    if "SteelGeneric" not in apex.catalog.getMaterialDictionary().keys():
        apex.setScriptUnitSystem(unitSystemName=r'''m-kg-s-N''')
        SteelMaterial = apex.catalog.createMaterial(name="SteelGeneric", description="", color=[64, 254, 250])
        SteelMaterial.update(elasticModulus=210.e+9, poissonRatio=0.3, density=7.8e-6)
        apex.setScriptUnitSystem(unitSystemName=r'''mm-kg-s-N''')
        #print("Material data for generic steel created")
    else:
        #print("Material already exists, skipping...")
        pass

    # Assign generic steel material to all Parts
    GenericMaterial = apex.catalog.getMaterial(name="SteelGeneric")
    _target = apex.EntityCollection()
    _target.extend(model_1.getParts(True))
    apex.attribute.assignMaterial(material=GenericMaterial, target=_target)

    # Run body selection
    for selAssy in apex.selection.getCurrentSelection():
        listOfRefSolid = []
        listOfRefSolidPaths = []
        for Part in selAssy.getParts(True):
            Part.update(color=[255, 0, 0])
            Part.show()
            for Solid in Part.getSolids():
                listOfRefSolidPaths.append(Solid.getPathName())
                listOfRefSolid.append(Solid)

        listOfTargetSolids = apex.EntityCollection()
        for Part in model_1.getParts(True):
            for Solid in Part.getSolids():
                if Solid.getPathName() not in listOfRefSolidPaths:
                    listOfTargetSolids.append(Solid)
                    Solid.update(color=[0, 0, 255])
                    Part.addUserAttribute(
                        userAttributeName=Part.getPathName(),
                        stringValue='Self')

        for refSolid in listOfRefSolid:
            textDisplay = apex.display.displayText(text=refSolid.getName(),
                                     textLocation=refSolid.getCentroid(),
                                     graphicsFont="Calibri",
                                     graphicsFontColor=apex.ColorRGB(255, 191, 0),
                                     graphicsFontSize=16,
                                     graphicsFontStyle=apex.display.GraphicsFontStyle.Normal,
                                     graphicsFontUnderlineStyle=apex.display.GraphicsFontUnderlineStyle.NoUnderline
                                     )
            distance_ = apex.measureDistance(source=refSolid, target=listOfTargetSolids)

            listOfTouchedBodies = apex.EntityCollection()

            try:
                _ans = refSolid.getParent().removeUserAttributes(userAttributeNames = [])
            except:
                pass

            refSolid.getParent().addUserAttribute(userAttributeName=refSolid.getParent().getPathName(),
                                                  stringValue='Self')
            for k in range(len(distance_)):
                if distance_[k] <= 0.0:
                    listOfTouchedBodies.append(listOfTargetSolids[k])
                    refSolid.getParent().addUserAttribute(
                        userAttributeName=listOfTargetSolids[k].getParent().getPathName(),
                        stringValue='Touched')
            apex.display.clearAllGraphicsText()

        # Organizing Parts and getting ready for modal analysis
        for refSolid in listOfRefSolid:
            StudyAssy = model_1.createAssembly(name="StudyAssy")
            dictInfo = {"Self": "", "Touched": []}
            solidParent = refSolid.getParent()

            # Moving Parts to the StudyAssy
            for Attribute in solidParent.getUserAttributes():
                if Attribute.getStringValue() == 'Self':
                    dictInfo[Attribute.getStringValue()] = Attribute.getAttributeName()
                else:
                    dictInfo[Attribute.getStringValue()].append(Attribute.getAttributeName())
                    ans_ = apex.getPart(Attribute.getAttributeName()).setParent(parent=StudyAssy)
            refSolid.getParent().setParent(parent=StudyAssy)


            # Creating ties based on touching bodies
            listOfTies = apex.EntityCollection()
            BeadPath = StudyAssy.getPart(dictInfo["Self"][dictInfo["Self"].rfind("/")+1:]).getPathName()
            for elem in dictInfo["Touched"]:
                compPath = StudyAssy.getPart(elem[elem.rfind("/")+1:]).getPathName()
                _entities = apex.getEntities(pathNames=[BeadPath, compPath])
                newTies = apex.attribute.createMeshIndependentTieAutomatic(
                    target=_entities,
                    tiePairTolerance=5.,
                    patchToleranceCalculationMethod=apex.AutoManual.Automatic
                )
                listOfTies.extend(newTies)


            # --- Running the modal thing
            scenaryName = "Scenario for " + solidParent.getName()
            context_ = StudyAssy
            study = apex.getPrimaryStudy()
            study.createScenario(
                name=scenaryName,
                description="Generated by the Optimization Toolbox - FO",
                scenarioConfiguration=apex.studies.ScenarioConfiguration.NormalModes
            )

            study = apex.getPrimaryStudy()
            scenario1 = study.getScenario(name=scenaryName)
            scenario1.associateModelRep(context_)

            
            # study = apex.getPrimaryStudy()
            # scenario1 = study.getScenario(name=scenaryName)
            # simSetting1 = scenario1.simulationSettings
            # simSetting1.partReduction = False
            # simSetting1.freqRangeLower = 1000.
            # simSetting1.freqRangeUpper = float('NaN')
            # simSetting1.stopCalculation = True
            # simSetting1.maxModes = 3
            # scenario1.simulationSettings = simSetting1
            
            #model_1.save()

            scenario1.execute() # Kick it

            # --- Done with execution


            # Deleting ties
            apex.deleteEntities(listOfTies)

            # Reset the model tree
            for Part in StudyAssy.getParts(True):
                for Attribute in Part.getUserAttributes():
                    if Attribute.getStringValue() == 'Self':
                        index = Attribute.getAttributeName().rfind("/")
                        ParentAssy = Attribute.getAttributeName()[0:index]
                        Part.setParent(parent=apex.getAssembly(ParentAssy))

            # Delete the Assembly used to build the study
            toDelete = apex.EntityCollection()
            toDelete.append(StudyAssy)
            apex.deleteEntities(toDelete)

            # --- Do postprocessing
            result = apex.session.displayMeshCracks(False)
            result = apex.session.display2DSpans(False)
            result = apex.session.display3DSpans(False)
            apex.display.hideRotationCenter()
            result = apex.session.displayMeshCracks(False)
            result = apex.session.displayInteractionMarkers(True)
            result = apex.session.displayConnectionMarkers(True)
            result = apex.session.display2DSpans(False)
            result = apex.session.display3DSpans(True)
            result = apex.session.displayLoadsAndBCMarkers(True)
            result = apex.session.displaySensorMarkers(True)

            study = apex.getPrimaryStudy()
            scenario1 = study.getScenario(name=scenaryName)
            executedscenario_1 = scenario1.getLastExecutedScenario()
            event1 = executedscenario_1.getEvent(pathName="/Study/{0}<< -1>>/Event 1".format(scenaryName))
            stateplot_1 = apex.post.createStatePlot(
                event=event1,
                resultDataSetIndex=[7]
            )

            visualizationTarget1 = apex.entityCollection()
            study = apex.getPrimaryStudy()
            scenario1 = study.getScenario(name=scenaryName)
            executedscenario_1 = scenario1.getLastExecutedScenario()
            visualizationTarget1.append(
                executedscenario_1.getAssembly(pathName=apex.currentModel().name + "/ar:StudyAssy_Default Rep"))
            deformvisualization_1 = stateplot_1.createDeformVisualization(
                target=visualizationTarget1,
                deformScalingMethod=apex.post.DeformScalingMethod.Relative,
                relativeScalingFactor=2.,
                displayUnit="mm"
            )

            result = apex.session.displaySensorMarkers(False)

            colormap_1 = apex.post.createColorMap(
                name="FringeSpectrum",
                colorMapSegmentMethod=apex.post.ColorMapSegmentMethod.Linear,
                start=0.0,
                end=0.0,
                isLocked=False,
                useOutOfRangeColors=False,
                displayContinuousColors=False
            )

            visualizationTarget1 = apex.entityCollection()
            study = apex.getPrimaryStudy()
            scenario1 = study.getScenario(name=scenaryName)
            executedscenario_1 = scenario1.getLastExecutedScenario()
            visualizationTarget1.append(
                executedscenario_1.getAssembly(pathName=apex.currentModel().name + "/ar:StudyAssy_Default Rep"))
            contourvisualization_1 = stateplot_1.createContourVisualization(
                contourStyle=apex.post.ContourStyle.Fringe,
                target=visualizationTarget1,
                resultQuantity=apex.post.ResultQuantity.DisplacementTranslational,
                resultDerivation=apex.post.ResultDerivation.Magnitude,
                layerIdentificationMethod=apex.post.LayerIdentificationMethod.Position,
                layers=["NONE"],
                layerEnvelopingMethod=apex.post.LayerEnvelopingMethod.Unknown,
                elementNodalProcessing=apex.post.ElementNodalProcessing.Averaged,
                coordinateSystemMethod=apex.post.CoordinateSystemMethod.Global,
                colorMap=colormap_1,
                displayUnit="mm"
            )

            contourvisualization_1.update()
            result = apex.session.display3DSpans(False)
            result = apex.session.displaySensorMarkers(True)
            result = apex.session.display2DSpans(False)
            result = apex.session.display3DSpans(False)
            result = apex.session.displaySensorMarkers(True)

            for i in range(4):
                stateplot_1.update(
                    resultDataSetIndex=[7+i]
                )
                time.sleep(3)
                capturedImage = apex.display.captureImage(path=r"D:\00-Projects\01-SequenceOptimization\ApexFiles\Images",
                                                          imageNamePrefix=scenaryName,
                                                          imageCaptureRegion=apex.display.CaptureRegionType.Viewport,
                                                          imageFormat=apex.display.ImageType.jpg
                                                          )

            apex.post.exitPostProcess()

            # --- Done with postprocessing

