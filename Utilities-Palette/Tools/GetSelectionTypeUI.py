import sys
import os
import apex_sdk
import clr

# .NET references
import System
import System.Windows.Controls as WPFControls
from System.Windows.Automation import AutomationProperties

dictionary = {}


# setting pre-defined properties of tool_propertyContainer
def getUIContent():
    my_toolProperty = apex_sdk.ToolPropertyContainer()
    my_toolProperty.ToolPropertyContent = getCustomToolPropertyContent()
    my_toolProperty.TitleText = "  Extract and map midsurface"
    my_toolProperty.WorkFlowInstructions = '<html><body><p><span style="color:#A9A9A9;">Operation: Click the </span><span style="color:#40E0D0;">Extract and annotate thickness </span><span style="color:#A9A9A9;"> button</span></p><ul><li><span style="color:#A9A9A9;">This tool is used to extract the midsurface of single-thickness parts.</span></li><li><span style="color:#A9A9A9;">By extracting the midsurface, the user has more flexibility to control the mesh in a 2D format.</span></li><li><span style="color:#A9A9A9;">The midsurface is a surface object that is created under the same locaton as the originating solid.</span></li><li><span style="color:#A9A9A9;">The thickness value will be annotated in the part name to be later referred to in </span><span style="color:#FF0000;">Simufact Welding</span><span style="color:#A9A9A9;">.</span></li></ul><p><span style="color:#A9A9A9;">2D meshes of components will be converted back to a 3D mesh when importing the file in </span><span style="color:#FF0000;">Simufact Welding </span><span style="color:#A9A9A9;"> by assigning a thickness and number of layers to it.</span></p></body></html>'

    # Define PickFilterList
    my_toolProperty.ShowPickChoice = True
    my_toolProperty.PickFilterList = setPickFilterList()

    return my_toolProperty


# Set PickFilters
def setPickFilterList():
    # Create an empty List of strings
    pickChoices = System.Collections.Generic.List[System.String]()

    # Exclusive picking and visibility picking
    #pickChoices.Add(apex_sdk.PickFilterTypes.ExclusivePicking)
    pickChoices.Add(apex_sdk.PickFilterTypes.VisibilityPicking)

    # Add Types
    pickChoices.Add(apex_sdk.PickFilterTypes.Assembly)
    pickChoices.Add(apex_sdk.PickFilterTypes.Part)
    pickChoices.Add(apex_sdk.PickFilterTypes.Solid)
    pickChoices.Add(apex_sdk.PickFilterTypes.Surface)
    pickChoices.Add(apex_sdk.PickFilterTypes.Cell)
    pickChoices.Add(apex_sdk.PickFilterTypes.Face)
    pickChoices.Add(apex_sdk.PickFilterTypes.Curve)
    pickChoices.Add(apex_sdk.PickFilterTypes.Edge)
    pickChoices.Add(apex_sdk.PickFilterTypes.Point)
    pickChoices.Add(apex_sdk.PickFilterTypes.Vertex)
    pickChoices.Add(apex_sdk.PickFilterTypes.CellMesh)
    pickChoices.Add(apex_sdk.PickFilterTypes.CurveMesh)
    pickChoices.Add(apex_sdk.PickFilterTypes.EdgeMesh)
    pickChoices.Add(apex_sdk.PickFilterTypes.Element1D)
    pickChoices.Add(apex_sdk.PickFilterTypes.Element2D)
    pickChoices.Add(apex_sdk.PickFilterTypes.Element3D)
    pickChoices.Add(apex_sdk.PickFilterTypes.ElementEdge)
    pickChoices.Add(apex_sdk.PickFilterTypes.ElementFace)
    pickChoices.Add(apex_sdk.PickFilterTypes.FaceMesh)
    pickChoices.Add(apex_sdk.PickFilterTypes.MeshSeed)
    pickChoices.Add(apex_sdk.PickFilterTypes.Node)
    pickChoices.Add(apex_sdk.PickFilterTypes.SeedPoint)
    pickChoices.Add(apex_sdk.PickFilterTypes.SolidMesh)
    pickChoices.Add(apex_sdk.PickFilterTypes.SurfaceMesh)
    pickChoices.Add(apex_sdk.PickFilterTypes.VertexMesh)

    # Return the pick filter list
    return pickChoices


# get tool property content
def getCustomToolPropertyContent():
    # Create a Grid
    my_Grid = WPFControls.Grid()

    # Add 2 Rows and 1 Column
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())

    # Create a button and set it's text to "Import"
    # Assign it to Row1, Column 0
    cleanBtn = WPFControls.Button()
    cleanBtn.Content = "Show me type and path"
    WPFControls.Grid.SetRow(cleanBtn, 1)
    WPFControls.Grid.SetColumn(cleanBtn, 0)

    # Link a function to the Button "Click" event
    # This function will be called every time the Button is clicked
    cleanBtn.Click += HandlecleanBtn

    # Add the controls to the Grid
    my_Grid.Children.Add(cleanBtn)

    # Return the Grid
    return my_Grid


# Function to handle the Import Button "Click" event
# This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandlecleanBtn(sender, args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(file_path, 'GetSelectionType.py')
    apex_sdk.runScriptFunction(file=script_path, function="ShowType")
