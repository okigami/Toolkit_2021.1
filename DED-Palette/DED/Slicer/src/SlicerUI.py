import sys
import os
import apex_sdk
import clr

# .NET references
import System
import System.Windows.Controls as WPFControls
from Microsoft.Win32 import OpenFileDialog

# Define current file path of example
current_file_path = os.path.dirname(os.path.realpath(__file__))


# Set pre-defined properties of ToolPropertyContainer
def getUIContent():
    my_toolProperty = apex_sdk.ToolPropertyContainer()

    # Provide an icon and a name for the tool property panel
    # my_toolProperty.TitleImageUriString = os.path.join(os.path.dirname(current_file_path), r"Icons\script.png")
    my_toolProperty.TitleText = "Slice body"
    my_toolProperty.WorkFlowInstructions = '''<p><strong><span style="color: #999999;">DED - Vertical slicing<br /></span></strong></p>
    <p><span style="color: #999999;">Description: This tool was designed to help with slicing geometries vertically.</span></p>
    <ul>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Layer height (mm)</span>: expected/desired layer height<br /></span></li>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Do not create multiple solids</span>: this option will create body partitions instead of splitting the body into multiple solids</span><span style="color: #999999;"><span style="color: #00ccff;"></span></span><span style="color: #999999;"><span style="color: #00ccff;"></span></span></li>
    </ul>
    <p><span style="color: #999999;">Workflow:</span></p>
    <ol>
    <li><span style="color: #999999;">Define the layer height</span></li>
    <li><span style="color: #999999;">Choose whether to create multiple solids or not</span></li>
    <li><span style="color: #999999;">Select the starting face of the splitting</span></li>
    <li><span style="color: #999999;">Click Slice geometry</span></li>
    </ol>
    <p><span style="color: #999999;">Selected starting face defines the body to be sliced (the body to which the surface belongs).</span></p>
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
    # pickChoices.Add(apex_sdk.PickFilterTypes.Part)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Solid)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Surface)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Cell)
    pickChoices.Add(apex_sdk.PickFilterTypes.Face)

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
    IDLbl.Text = "Slicing definition"
    WPFControls.Grid.SetRow(IDLbl, currRow)
    IDLbl.FontSize = 11

    # Create input field
    currRow += 1
    layerLbl = WPFControls.TextBlock()
    layerLbl.Text = "   Layer height (mm):"
    WPFControls.Grid.SetRow(layerLbl, currRow)
    WPFControls.Grid.SetColumn(layerLbl, 0)

    global layerHeight
    layerHeight = WPFControls.TextBox()
    WPFControls.Grid.SetRow(layerHeight, currRow)
    WPFControls.Grid.SetColumn(layerHeight, 1)

    # Create checkbox to ask for mesh
    currRow += 1
    global chkSplit
    chkSplit = WPFControls.CheckBox()
    chkSplit.Content = "Do not create multiple solids"
    chkSplit.Height = 20
    WPFControls.Grid.SetRow(chkSplit, currRow)
    WPFControls.Grid.SetColumn(chkSplit, 0)
    WPFControls.Grid.SetColumnSpan(chkSplit, 3)

    # Create a button
    currRow += 1
    goSlice = WPFControls.Button()
    goSlice.Content = "Slice geometry"
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
    my_Grid.Children.Add(layerHeight)

    my_Grid.Children.Add(chkSplit)
    my_Grid.Children.Add(goSlice)

    # Return the Grid
    return my_Grid


# Apply button handler (Green check mark)
# This function is called each time the Apply button is clicked
@apex_sdk.errorhandler
def HandleApplyButton(sender, args):
    # Create a Dictionary to store the user defined tool data
    dictionary = {}

    # Populate the Dictionary with the user defined tool data you need
    dictionary["layerHeight"] = layerHeight.Text
    dictionary["splitBody"] = chkSplit.IsChecked

    apex_sdk.runScriptFunction(os.path.join(current_file_path, r"SlicerCODE.py"), "verticalSlicing", dictionary)
