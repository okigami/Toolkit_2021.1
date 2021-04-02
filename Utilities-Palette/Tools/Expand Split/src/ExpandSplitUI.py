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
    my_toolProperty.TitleText = "Expand & Split"
    my_toolProperty.WorkFlowInstructions = '''
    <p><strong><span style="color: #999999;">Expand &amp; Split<br /></span></strong></p>
    <p><span style="color: #999999;">Description: This tools takes existing geometries and creates expanded (offset) versions of the outer surfaces. No extra geometry will be created. It takes advantage of the existing built-in partitioning tool.<br /></span></p>
    <ul>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Distance (mm)</span>: Offset distance from the existing faces.<br /></span></li>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Split solids</span>: Check this option if you want to split solids within reach of the expanded faces.<br /></span></li>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Split surfaces</span>: Check this option if you want to split surfaces within reach of the expanded faces.</span><span style="color: #999999;"></span></li>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Suppress extra vertices</span>: Performs an extra step to cleanup vertices after performing the split (partitioning).<br /></span></li>
    </ul>
    <p><span style="color: #999999;">Workflow:</span></p>
    <ol>
    <li><span style="color: #999999;">Define offset distance<br /></span></li>
    <li><span style="color: #999999;">Select/skip split solids<br /></span></li>
    <li><span style="color: #999999;">Select/skip split surfaces<br /></span></li>
    <li><span style="color: #999999;">Select/skip suppression of extra vertices<br /></span></li>
    <li><span style="color: #999999;">Select an assembly containing all geometries used for splitting</span></li>
    <li><span style="color: #999999;">Click expand beads and split</span><span style="color: #999999;"></span></li>
    </ol>
    <p><span style="color: #999999;">For support: <span style="color: #ff0000;"><a href="mailto:support.americas@simufact.com">support.americas@simufact.com</a></span></span></p>
    <p><span style="color: #999999;"><span style="color: #ff0000;"></span></span></p>
    '''

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
    # pickChoices.Add(apex_sdk.PickFilterTypes.Face)
    pickChoices.Add(apex_sdk.PickFilterTypes.Assembly)

    # Return the pick filter list
    return pickChoices


# Define Layout and Components
def getCustomToolPropertyContent():
    # Create a Grid
    my_Grid = WPFControls.Grid()

    # Add 2 Rows and 1 Column
    my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
    my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())

    currRow = 0

    # Create input field
    currRow += 1
    lbl01 = WPFControls.TextBlock()
    lbl01.Text = "Distance (mm):"
    WPFControls.Grid.SetRow(lbl01, currRow)
    WPFControls.Grid.SetColumn(lbl01, 0)
    WPFControls.Grid.SetColumnSpan(lbl01, 1)

    global input01
    input01 = WPFControls.TextBox()
    WPFControls.Grid.SetRow(input01, currRow)
    WPFControls.Grid.SetColumn(input01, 1)

    # Create checkbox
    currRow += 1
    global chk01
    chk01 = WPFControls.CheckBox()
    chk01.Content = "Split solids"
    chk01.Height = 20
    WPFControls.Grid.SetRow(chk01, currRow)
    WPFControls.Grid.SetColumn(chk01, 0)
    WPFControls.Grid.SetColumnSpan(chk01, 1)

    # Create checkbox
    currRow += 1
    global chk02
    chk02 = WPFControls.CheckBox()
    chk02.Content = "Split surfaces"
    chk02.Height = 20
    WPFControls.Grid.SetRow(chk02, currRow)
    WPFControls.Grid.SetColumn(chk02, 0)
    WPFControls.Grid.SetColumnSpan(chk02, 1)
    chk02.IsChecked = System.Nullable[System.Boolean](True)

    # Create checkbox
    currRow += 1
    global chk03
    chk03 = WPFControls.CheckBox()
    chk03.Content = "Suppress extra vertices"
    chk03.Height = 20
    WPFControls.Grid.SetRow(chk03, currRow)
    WPFControls.Grid.SetColumn(chk03, 0)
    WPFControls.Grid.SetColumnSpan(chk03, 1)

    # Create a button
    currRow += 1
    actionButton = WPFControls.Button()
    actionButton.Content = "Expand beads and split"
    WPFControls.Grid.SetRow(actionButton, currRow)
    WPFControls.Grid.SetColumn(actionButton, 0)
    actionButton.Height = 30
    WPFControls.Grid.SetColumnSpan(actionButton, 2)
    actionButton.Click += HandleApplyButton         # Link a function to the Button "Click" event


    # Add the controls to the Grid
    my_Grid.Children.Add(lbl01)
    my_Grid.Children.Add(input01)
    my_Grid.Children.Add(chk01)
    my_Grid.Children.Add(chk02)
    my_Grid.Children.Add(chk03)

    my_Grid.Children.Add(actionButton)

    # Return the Grid
    return my_Grid


# Apply button handler (Green check mark)
# This function is called each time the Apply button is clicked
@apex_sdk.errorhandler
def HandleApplyButton(sender, args):
    # Create a Dictionary to store the user defined tool data
    dictionary = {}

    # Populate the Dictionary with the user defined tool data you need
    dictionary["distance"] = input01.Text
    dictionary["splitSolids"] = chk01.IsChecked
    dictionary["splitSurfaces"] = chk02.IsChecked
    dictionary["suppressVertices"] = chk03.IsChecked

    apex_sdk.runScriptFunction(os.path.join(current_file_path, r"ExpandSplit.py"), "ExpandSplit", dictionary)
