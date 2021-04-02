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
    my_toolProperty.TitleText = "Find bodies within distance"
    my_toolProperty.WorkFlowInstructions = '''
    <p><strong><span style="color: #999999;">Find fixture<br /></span></strong></p>
    <p><span style="color: #999999;">Description: This tools uses the distance search algorithm to find bodies in contact with the selected assembly.<br /></span></p>
    <ul>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Distance (mm)</span>: Search distance.<br /></span></li>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Separate in new assembly</span>: Check this option if you want to separate the bodies found within the specified distance. This is usually the expected behavior.</span><span style="color: #999999;"><br /></span></li>
    </ul>
    <p><span style="color: #999999;">Workflow:</span></p>
    <ol>
    <li><span style="color: #999999;">Define the search distance<br /></span></li>
    <li><span style="color: #999999;">Select/skip separate in new assembly<br /></span></li>
    <li><span style="color: #999999;">Select an assembly containing the reference geometries</span></li>
    <li><span style="color: #999999;">Click find close parts<br /></span></li>
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
    pickChoices.Add(apex_sdk.PickFilterTypes.Part)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Solid)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Surface)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Face)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Cell)
    pickChoices.Add(apex_sdk.PickFilterTypes.Assembly)

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
    IDLbl.Text = "Separate by distance"
    WPFControls.Grid.SetRow(IDLbl, currRow)
    IDLbl.FontSize = 11

    # Create input field
    currRow += 1
    lbl01 = WPFControls.TextBlock()
    lbl01.Text = "Distance (mm):"
    WPFControls.Grid.SetRow(lbl01, currRow)
    WPFControls.Grid.SetColumn(lbl01, 0)

    global input01
    input01 = WPFControls.TextBox()
    WPFControls.Grid.SetRow(input01, currRow)
    WPFControls.Grid.SetColumn(input01, 1)
    input01.Text = "2.0"
    
    # Create checkbox to ask for mesh
    currRow += 1
    global check01
    check01 = WPFControls.CheckBox()
    check01.Content = "Separate in new assembly"
    check01.Height = 30
    WPFControls.Grid.SetRow(check01, currRow)
    WPFControls.Grid.SetColumn(check01, 0)
    WPFControls.Grid.SetColumnSpan(check01, 3)
    check01.IsChecked = System.Nullable[System.Boolean](True)

    # Create a button
    currRow += 1
    goButton = WPFControls.Button()
    goButton.Content = "Find close parts"
    WPFControls.Grid.SetRow(goButton, currRow)
    WPFControls.Grid.SetColumn(goButton, 0)
    goButton.Height = 30
    WPFControls.Grid.SetColumnSpan(goButton, 3)


    # Link a function to the Button "Click" event
    # This function will be called every time the Button is clicked
    goButton.Click += HandleApplyButton

    # Add the controls to the Grid
    #my_Grid.Children.Add(IDLbl)
    my_Grid.Children.Add(lbl01)
    my_Grid.Children.Add(input01)
 
    my_Grid.Children.Add(check01)
    my_Grid.Children.Add(goButton)


    # Return the Grid
    return my_Grid


# Apply button handler (Green check mark)
# This function is called each time the Apply button is clicked
@apex_sdk.errorhandler
def HandleApplyButton(sender, args):
    # Create a Dictionary to store the user defined tool data
    dictionary = {}

    # Populate the Dictionary with the user defined tool data you need
    dictionary["newAssy"] = check01.IsChecked
    dictionary["searchDistance"] = input01.Text

    apex_sdk.runScriptFunction(os.path.join(current_file_path, r"FilterTouching.py"), "filterFixture", dictionary)
