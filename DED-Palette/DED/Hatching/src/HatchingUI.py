import sys
import os
import apex_sdk
import clr

# .NET references
import System
from System.Windows.Forms import FolderBrowserDialog
import System.Windows.Controls as WPFControls
#from Microsoft.Win32 import FolderBrowserDialog

# Define current file path of example
current_file_path = os.path.dirname(os.path.realpath(__file__))


# Set pre-defined properties of ToolPropertyContainer
def getUIContent():
    my_toolProperty = apex_sdk.ToolPropertyContainer()

    # Provide an icon and a name for the tool property panel
    # my_toolProperty.TitleImageUriString = os.path.join(os.path.dirname(current_file_path), r"Icons\script.png")
    my_toolProperty.TitleText = "Hatching layers"
    my_toolProperty.WorkFlowInstructions = '''<p><strong><span style="color: #999999;">DED - Hatching tool<br /></span></strong></p>
    <p><span style="color: #999999;">Description: This tool was designed to help with hatching layers of sliced geometry.<br /></span></p>
    <ul>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Trajec. spacing (mm)</span>: Distance between two trajectories calculated from the centerline.<br /></span></li>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Point spacing (mm)</span>: Distance between two points of a trajectory (sampling resolution)</span></li>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Angular cut</span>: Algorithm to vary the angular cut</span><span style="color: #999999;"></span>
    <ul>
    <li><span style="color: #999999;"><span style="color: #ff6600;">Single angle</span>: one single angle will be used for all layers</span></li>
    <li><span style="color: #999999;"><span style="color: #ff6600;">Incremental</span>: the angle will be multiplied by the layer number (1*angle, 2*angle, 3*angle, ...)</span></li>
    <li><span style="color: #999999;"><span style="color: #ff6600;">Cycle through</span>: inform the specific angles to be used separating them by comma (ex: 0, 30, 45)</span></li>
    </ul>
    </li>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Angle (deg)</span>: specify the cut angle for the hatching algorithm</span><span style="color: #999999;"></span></li>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Mesh the layers</span>: mesh the resulting hatched geometry with the 2.5D mesher (hexahedral elements)</span><span style="color: #999999;"></span></li>
    </ul>
    <p><span style="color: #999999;">Workflow:</span></p>
    <ol>
    <li><span style="color: #999999;">Define trajectory spacing (this depends on your process)</span></li>
    <li><span style="color: #999999;">Define point spacing</span></li>
    <li><span style="color: #999999;">Select hatching algorithm</span></li>
    <li><span style="color: #999999;">Define initial angle or angles</span></li>
    <li><span style="color: #999999;">Choose whether to perform meshing aftewards</span></li>
    <li><span style="color: #999999;">Select where to save the trajectories</span></li>
    <li><span style="color: #999999;">Click create hatching to start the process</span></li>
    </ol>
    <p><span style="color: #999999;">For support: <span style="color: #ff0000;"><a href="mailto:support.americas@simufact.com">support.americas@simufact.com</a></span></span></p>
    <p><span style="color: #999999;"><span style="color: #ff0000;"></span></span></p>'''

    # Define UI
    my_toolProperty.ToolPropertyContent = getCustomToolPropertyContent()

    # Handle apply button (green) click event
    my_toolProperty.AppliedCommand = apex_sdk.ActionCommand(System.Action(HandleApplyButton))

    # Define PickFilterList
    my_toolProperty.ShowPickChoice = True
    my_toolProperty.PickFilterList = setPickFilterList()

    return my_toolProperty


# Set PickFilters
def setPickFilterList():
    # Create an empty List of strings
    pickChoices = System.Collections.Generic.List[System.String]()

    # Exclusive picking and visibility picking
    pickChoices.Add(apex_sdk.PickFilterTypes.ExclusivePicking)
    pickChoices.Add(apex_sdk.PickFilterTypes.VisibilityPicking)

    # Add Types
    #pickChoices.Add(apex_sdk.PickFilterTypes.Part)
    pickChoices.Add(apex_sdk.PickFilterTypes.Solid)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Surface)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Face)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Cell)

    # Return the pick filter list
    return pickChoices


# Define Layout and Components
def getCustomToolPropertyContent():
    # Create a Grid
    my_Grid = WPFControls.Grid()

    # Add 2 Rows and 1 Column
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())

    currRow = 0

    # -- Horizontal sheet definition
    IDLbl = WPFControls.TextBlock()
    IDLbl.Text = "Hatching definition"
    WPFControls.Grid.SetRow(IDLbl, currRow)
    IDLbl.FontSize = 11

    # Create label and input field
    currRow += 1
    layerLbl = WPFControls.TextBlock()
    layerLbl.Text = "   Trajec. spacing (mm): "
    WPFControls.Grid.SetRow(layerLbl, currRow)
    WPFControls.Grid.SetColumn(layerLbl, 0)

    global distanceLine
    distanceLine = WPFControls.TextBox()
    WPFControls.Grid.SetRow(distanceLine, currRow)
    WPFControls.Grid.SetColumn(distanceLine, 1)

    # Create label and input field
    currRow += 1
    pointSpacing = WPFControls.TextBlock()
    pointSpacing.Text = "   Point spacing (mm):"
    WPFControls.Grid.SetRow(pointSpacing, currRow)
    WPFControls.Grid.SetColumn(pointSpacing, 0)

    global pointSpacingValue
    pointSpacingValue = WPFControls.TextBox()
    WPFControls.Grid.SetRow(pointSpacingValue, currRow)
    WPFControls.Grid.SetColumn(pointSpacingValue, 1)

    # Type of angular cut
    currRow += 1
    angleCutType = WPFControls.TextBlock()
    angleCutType.Text = "   Angular cut:"
    WPFControls.Grid.SetRow(angleCutType, currRow)
    WPFControls.Grid.SetColumn(angleCutType, 0)


    # Create a Combo box
    global angleTypeSelection
    angleTypeSelection = WPFControls.ComboBox()

    item1 = WPFControls.ComboBoxItem()
    item1.Content = "Single angle"
    angleTypeSelection.Items.Add(item1)

    item2 = WPFControls.ComboBoxItem()
    item2.Content = "Incremental"
    angleTypeSelection.Items.Add(item2)

    item3 = WPFControls.ComboBoxItem()
    item3.Content = "Cycle through"
    angleTypeSelection.Items.Add(item3)

    angleTypeSelection.SelectedIndex = "0"
    WPFControls.Grid.SetRow(angleTypeSelection, currRow)
    WPFControls.Grid.SetColumn(angleTypeSelection, 1)
    #angleTypeSelection.SelectionChanged += HandleAngleSelection



    # Create label and input field
    currRow += 1
    global angleLbl
    angleLbl = WPFControls.TextBlock()
    angleLbl.Text = "   Angle (deg):"
    WPFControls.Grid.SetRow(angleLbl, currRow)
    WPFControls.Grid.SetColumn(angleLbl, 0)

    global angleValue
    angleValue = WPFControls.TextBox()
    WPFControls.Grid.SetRow(angleValue, currRow)
    WPFControls.Grid.SetColumn(angleValue, 1)


    # Create checkbox to ask for mesh
    currRow += 1
    global meshCheck
    meshCheck = WPFControls.CheckBox()
    meshCheck.Content = "Mesh the layers for me"
    meshCheck.Height = 25
    WPFControls.Grid.SetRow(meshCheck, currRow)
    WPFControls.Grid.SetColumn(meshCheck, 0)
    WPFControls.Grid.SetColumnSpan(meshCheck, 3)


    # Create a button
    currRow += 1
    getDirectory = WPFControls.Button()
    getDirectory.Content = "Select directory to save"
    WPFControls.Grid.SetRow(getDirectory, currRow)
    WPFControls.Grid.SetColumn(getDirectory, 0)
    getDirectory.Height = 30
    WPFControls.Grid.SetColumnSpan(getDirectory, 3)
    getDirectory.Click += HandleGetDir

    global dialog
    dialog = FolderBrowserDialog()
    dialog.Description = "Choose where to save trajectories"
    dialog.ShowNewFolderButton = True


    # Create a button
    currRow += 1
    goSlice = WPFControls.Button()
    goSlice.Content = "Create hatching"
    WPFControls.Grid.SetRow(goSlice, currRow)
    WPFControls.Grid.SetColumn(goSlice, 0)
    goSlice.Height = 30
    WPFControls.Grid.SetColumnSpan(goSlice, 3)



    # Link a function to the Button "Click" event
    # This function will be called every time the Button is clicked
    goSlice.Click += HandleApplyButton

    # Add the controls to the Grid
    my_Grid.Children.Add(IDLbl)
    my_Grid.Children.Add(layerLbl)
    my_Grid.Children.Add(distanceLine)
    my_Grid.Children.Add(pointSpacing)
    my_Grid.Children.Add(pointSpacingValue)

    my_Grid.Children.Add(angleCutType)
    my_Grid.Children.Add(angleTypeSelection)
    my_Grid.Children.Add(angleLbl)
    my_Grid.Children.Add(angleValue)

    my_Grid.Children.Add(getDirectory)

    my_Grid.Children.Add(meshCheck)
    my_Grid.Children.Add(goSlice)


    # Return the Grid
    return my_Grid



@apex_sdk.errorhandler
def HandleGetDir(sender,args):
    if dialog.ShowDialog():
        selectedDirPath = str(dialog.SelectedPath)
    else:
        selectedDirPath = ""

# Apply button handler (Green check mark)
# This function is called each time the Apply button is clicked
@apex_sdk.errorhandler
def HandleApplyButton(sender, args):
    # Create a Dictionary to store the user defined tool data
    dictionary = {}

    # Populate the Dictionary with the user defined tool data you need
    dictionary["distanceLine"] = distanceLine.Text
    dictionary["angleType"] = angleTypeSelection.Text
    dictionary["angleValue"] = angleValue.Text
    dictionary["pointSpacing"] = pointSpacingValue.Text
    dictionary["meshIt"] = meshCheck.IsChecked
    if str(dialog.SelectedPath):
        dictionary["saveToDir"] = str(dialog.SelectedPath)
    else:
        dictionary["saveToDir"] = ""

    apex_sdk.runScriptFunction(os.path.join(current_file_path, r"SlicerCODE.py"), "hatchingLayers", dictionary)
