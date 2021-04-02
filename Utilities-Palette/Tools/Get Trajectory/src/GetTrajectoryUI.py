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
    my_toolProperty.TitleText = "Get trajectory from edge"
    my_toolProperty.WorkFlowInstructions = '''
        <p><strong><span style="color: #999999;">Get trajectory tool<br /></span></strong></p>
        <p><span style="color: #999999;">Description: This tool was designed to help extracting trajectory information to be used in Simufact Welding.<br /></span></p>
        <ul>
        <li><span style="color: #999999;"><span style="color: #00ccff;">Calculate normal direction</span>: Using this option the user also gets the normal direction at the points of the trajectory.</span><span style="color: #999999;"></span><span style="color: #999999;"></span></li>
        <li><span style="color: #999999;"><span style="color: #00ccff;">Get trajectory from edge</span>: Extract trajectories from selected edges.<br /></span></li>
        </ul>
        <p><span style="color: #999999;">Workflow:</span></p>
        <ol>
        <li><span style="color: #999999;">Select the edges you want to create trajectories from (one or multiple)<br /></span></li>
        <li><span style="color: #999999;">Define whether you need the normal direction by marking the checkbox<br /></span></li>
        <li><span style="color: #999999;">Click get trajectory from edge<br /></span></li>
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
    #pickChoices.Add(apex_sdk.PickFilterTypes.Part)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Solid)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Surface)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Face)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Cell)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Assembly)
    pickChoices.Add(apex_sdk.PickFilterTypes.Edge)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Curve)

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
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    #my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())

    currRow = 0

    # Create input field
    currRow += 1
    lbl01 = WPFControls.TextBlock()
    lbl01.Text = "Region diam. (mm):"
    WPFControls.Grid.SetRow(lbl01, currRow)
    WPFControls.Grid.SetColumn(lbl01, 0)

    global input01
    input01 = WPFControls.TextBox()
    WPFControls.Grid.SetRow(input01, currRow)
    WPFControls.Grid.SetColumn(input01, 1)

    # Create checkbox to extend the weld bead
    currRow += 1
    global chkBox01
    chkBox01 = WPFControls.CheckBox()
    chkBox01.Content = "Calculate normal directions"
    chkBox01.Height = 20
    WPFControls.Grid.SetRow(chkBox01, currRow)
    WPFControls.Grid.SetColumn(chkBox01, 0)
    chkBox01.IsChecked = System.Nullable[System.Boolean](True)
    #WPFControls.Grid.SetColumnSpan(chkBox01, 2)

    # Create a button
    currRow += 2
    goButton = WPFControls.Button()
    goButton.Content = "Get trajectory from selected edge"
    WPFControls.Grid.SetRow(goButton, currRow)
    WPFControls.Grid.SetColumn(goButton, 0)
    goButton.Height = 30
    WPFControls.Grid.SetColumnSpan(goButton, 2)

    # Link a function to the Button "Click" event
    # This function will be called every time the Button is clicked
    goButton.Click += HandleApplyButton

    global dialog
    dialog = FolderBrowserDialog()
    dialog.Description = "Directory where to save trajectories"
    dialog.ShowNewFolderButton = True

    #my_Grid.Children.Add(lbl01)
    #my_Grid.Children.Add(input01)
    my_Grid.Children.Add(chkBox01)

    my_Grid.Children.Add(goButton)


    # Return the Grid
    return my_Grid


# Apply button handler (Green check mark)
# This function is called each time the Apply button is clicked
@apex_sdk.errorhandler
def HandleApplyButton(sender, args):
    # Create a Dictionary to store the user defined tool data
    dictionary = {}
    #dictionary["refDiam"] = input01.Text
    if dialog.ShowDialog():
        dictionary["saveToDir"] = str(dialog.SelectedPath)
    else:
        dictionary["saveToDir"] = ""

    dictionary["getNormalDirection"] = chkBox01.IsChecked
    apex_sdk.runScriptFunction(os.path.join(current_file_path, r"GetTrajectory.py"), "extractTrajectory", dictionary)
