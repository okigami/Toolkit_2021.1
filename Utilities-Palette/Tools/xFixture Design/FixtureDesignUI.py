import sys
import os
import apex_sdk
import clr

# .NET references
import System
from System.Windows.Forms import FolderBrowserDialog
import System.Windows.Controls as WPFControls

# from Microsoft.Win32 import FolderBrowserDialog

# Define current file path of example
current_file_path = os.path.dirname(os.path.realpath(__file__))


# Set pre-defined properties of ToolPropertyContainer
def getUIContent():
    my_toolProperty = apex_sdk.ToolPropertyContainer()

    # Provide an icon and a name for the tool property panel
    # my_toolProperty.TitleImageUriString = os.path.join(os.path.dirname(current_file_path), r"Icons\script.png")
    my_toolProperty.TitleText = "Design fixture by stiffness"

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
    # pickChoices.Add(apex_sdk.PickFilterTypes.Solid)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Surface)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Face)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Cell)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Assembly)

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

    # --
    IDLbl = WPFControls.TextBlock()
    IDLbl.Text = "Separate by distance"
    WPFControls.Grid.SetRow(IDLbl, currRow)
    IDLbl.FontSize = 11

    # Create input field
    currRow += 1
    lbl01 = WPFControls.TextBlock()
    lbl01.Text = "Max number of points:"
    WPFControls.Grid.SetRow(lbl01, currRow)
    WPFControls.Grid.SetColumn(lbl01, 0)

    global input01
    input01 = WPFControls.TextBox()
    WPFControls.Grid.SetRow(input01, currRow)
    WPFControls.Grid.SetColumn(input01, 1)
    input01.Text = "4"

    # Create a button
    currRow += 1
    goButton = WPFControls.Button()
    goButton.Content = "Run fixture designer"
    WPFControls.Grid.SetRow(goButton, currRow)
    WPFControls.Grid.SetColumn(goButton, 0)
    goButton.Height = 30
    WPFControls.Grid.SetColumnSpan(goButton, 3)

    # Link a function to the Button "Click" event
    # This function will be called every time the Button is clicked
    goButton.Click += HandleApplyButton

    # Add the controls to the Grid
    # my_Grid.Children.Add(IDLbl)
    my_Grid.Children.Add(lbl01)
    my_Grid.Children.Add(input01)

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
    dictionary["MaxNumOfPoints"] = input01.Text

    apex_sdk.runScriptFunction(os.path.join(current_file_path, r"FixtureDesignCODE.py"), "StiffnessOptimizer", dictionary)
