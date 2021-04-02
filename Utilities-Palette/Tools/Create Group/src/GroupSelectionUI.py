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
    my_toolProperty.TitleText = "Create group from selection"
    my_toolProperty.WorkFlowInstructions = '''
    <p><strong><span style="color: #999999;">Create group<br /></span></strong></p>
    <p><span style="color: #999999;">Description: This tools creates an assembly with selected solid bodies and/or surfaces.<br /></span></p>
    <ul>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Group name</span>: Assign an assembly name to the new group manually.<br /></span></li>
    <li><span style="color: #999999;"><span style="color: #00ccff;">Create under the same parent</span>: Takes the common uppermost parent of all selected bodies/surfaces as reference for creating the new assembly group.</span></li>
    </ul>
    <p><span style="color: #999999;">Workflow:</span></p>
    <ol>
    <li><span style="color: #999999;">Select the solid bodies and/or surfaces<br /></span></li>
    <li><span style="color: #999999;">Give the new group a name (optional)<br /></span></li>
    <li><span style="color: #999999;">Select whether it should be created under a common parent assembly<br /></span></li>
    <li><span style="color: #999999;">Click create assembly</span><span style="color: #999999;"></span></li>
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
    pickChoices.Add(apex_sdk.PickFilterTypes.Solid)
    pickChoices.Add(apex_sdk.PickFilterTypes.Surface)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Face)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Cell)
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

    # Create input field
    currRow += 1
    lbl01 = WPFControls.TextBlock()
    lbl01.Text = "Group name:"
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
    chkBox01.Content = "Create under the same parent"
    chkBox01.Height = 20
    WPFControls.Grid.SetRow(chkBox01, currRow)
    WPFControls.Grid.SetColumn(chkBox01, 1)

    # Create a button
    currRow += 1
    currRow += 1
    goButton = WPFControls.Button()
    goButton.Content = "Create assembly"
    WPFControls.Grid.SetRow(goButton, currRow)
    WPFControls.Grid.SetColumn(goButton, 0)
    goButton.Height = 30
    WPFControls.Grid.SetColumnSpan(goButton, 3)


    # Link a function to the Button "Click" event
    # This function will be called every time the Button is clicked
    goButton.Click += HandleApplyButton

    my_Grid.Children.Add(lbl01)
    my_Grid.Children.Add(input01)
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
    dictionary["useSolidName"] = chkBox01.IsChecked
    dictionary["assyName"] = input01.Text
    apex_sdk.runScriptFunction(os.path.join(current_file_path, r"GroupSelection.py"), "createAssy", dictionary)
