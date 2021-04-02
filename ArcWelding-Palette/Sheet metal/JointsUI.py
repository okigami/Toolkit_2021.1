# MSC Apex - User Defined Tools using Python Scripts
# Radio Button UI Example
#
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
    my_toolProperty.TitleImageUriString = os.path.join(os.path.dirname(current_file_path), r"Icons\script.png")

    my_toolProperty.TitleText = "Create simple joints"

    # Define UI
    my_toolProperty.ToolPropertyContent = getCustomToolPropertyContent()

    # Handle apply button (green) click event
    my_toolProperty.AppliedCommand = apex_sdk.ActionCommand(System.Action(HandleApplyButton))

    return my_toolProperty


# Define Layout and Components
def getCustomToolPropertyContent():
    # Create a Grid
    my_Grid = WPFControls.Grid()

    # Add 6 Rows and One Column
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
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
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())

    currRow = 0

    # Create a label for the first radio button array
    meshTextBlock = WPFControls.TextBlock()
    meshTextBlock.Text = "Vertical Array"
    WPFControls.Grid.SetRow(meshTextBlock, currRow)
    WPFControls.Grid.SetColumn(meshTextBlock, 0)

    currRow += 1
    # Create a label for the second radio button array
    meshTextBlock2 = WPFControls.TextBlock()
    meshTextBlock2.Text = "Joint type"
    meshTextBlock2.FontSize = 11
    WPFControls.Grid.SetRow(meshTextBlock2, currRow)
    WPFControls.Grid.SetColumn(meshTextBlock2, 0)


    # Create a horizontal array of three radio buttons
    # Create a WrapPanel
    hWrapPanel = WPFControls.WrapPanel()
    hWrapPanel.Orientation = WPFControls.Orientation.Horizontal

    # Create a List to hold the radio buttons in the first array
    # We'll use this later to make it easier to find which button is checked
    currRow += 1
    global horizontal_radio_buttons
    horizontal_radio_buttons = []

    # Create a first radio button and add to the WrapPanel
    horizontal_radio_buttons.append(WPFControls.RadioButton())
    horizontal_radio_buttons[0].Content = "Lap joint"

    # Set the first radio button to be checked
    # Note the horrible notation required to define a Nullable Boolean True
    horizontal_radio_buttons[0].IsChecked = System.Nullable[System.Boolean](True)
    hWrapPanel.Children.Add(horizontal_radio_buttons[0])

    # Create a second radio button and add to the WrapPanel
    horizontal_radio_buttons.append(WPFControls.RadioButton())
    horizontal_radio_buttons[1].Content = "T-joint"
    hWrapPanel.Children.Add(horizontal_radio_buttons[1])

    # Create a third radio button and add to the WrapPanel
    horizontal_radio_buttons.append(WPFControls.RadioButton())
    horizontal_radio_buttons[2].Content = "Flush corner"
    hWrapPanel.Children.Add(horizontal_radio_buttons[2])

    # Position the WrapPanel in the first row, column of the Grid
    WPFControls.Grid.SetRow(hWrapPanel, 3)
    WPFControls.Grid.SetColumn(hWrapPanel, 0)
    WPFControls.Grid.SetColumnSpan(hWrapPanel, 2)

    # -- Horizontal sheet definition
    currRow += 1
    currRow += 1
    currRow += 1
    horizLabel = WPFControls.TextBlock()
    horizLabel.Text = "Shape definition"
    WPFControls.Grid.SetRow(horizLabel, currRow)
    horizLabel.FontSize = 11

    currRow += 1
    horizWidthLbl = WPFControls.TextBlock()
    horizWidthLbl.Text = "    Width (mm):"
    WPFControls.Grid.SetRow(horizWidthLbl, currRow)
    WPFControls.Grid.SetColumn(horizWidthLbl, 0)

    global horizWidthInput
    horizWidthInput = WPFControls.TextBox()
    WPFControls.Grid.SetRow(horizWidthInput, currRow)
    WPFControls.Grid.SetColumn(horizWidthInput, 1)
    WPFControls.Grid.SetColumnSpan(horizWidthInput, 2)

    currRow += 1
    horizLengthLbl = WPFControls.TextBlock()
    horizLengthLbl.Text = "    Length (mm):"
    WPFControls.Grid.SetRow(horizLengthLbl, currRow)
    WPFControls.Grid.SetColumn(horizLengthLbl, 0)

    global horizLengthInput
    horizLengthInput = WPFControls.TextBox()
    WPFControls.Grid.SetRow(horizLengthInput, currRow)
    WPFControls.Grid.SetColumn(horizLengthInput, 1)
    WPFControls.Grid.SetColumnSpan(horizLengthInput, 2)

    currRow += 1
    horizThickLbl = WPFControls.TextBlock()
    horizThickLbl.Text = "    Thickness 01 (mm):"
    WPFControls.Grid.SetRow(horizThickLbl, currRow)
    WPFControls.Grid.SetColumn(horizThickLbl, 0)

    global horizThickInput
    horizThickInput = WPFControls.TextBox()
    WPFControls.Grid.SetRow(horizThickInput, currRow)
    WPFControls.Grid.SetColumn(horizThickInput, 1)
    WPFControls.Grid.SetColumnSpan(horizThickInput, 2)

    currRow += 1
    vertThickLbl = WPFControls.TextBlock()
    vertThickLbl.Text = "    Thickness 02 (mm):"
    WPFControls.Grid.SetRow(vertThickLbl, currRow)
    WPFControls.Grid.SetColumn(vertThickLbl, 0)

    global vertThickInput
    vertThickInput = WPFControls.TextBox()
    WPFControls.Grid.SetRow(vertThickInput, currRow)
    WPFControls.Grid.SetColumn(vertThickInput, 1)
    WPFControls.Grid.SetColumnSpan(vertThickInput, 2)

    # Create checkbox to ask for mesh
    currRow += 1
    global chkMesh
    chkMesh = WPFControls.CheckBox()
    chkMesh.Content = "Mesh the joint"
    chkMesh.Height = 20
    WPFControls.Grid.SetRow(chkMesh, currRow)
    WPFControls.Grid.SetColumn(chkMesh, 0)
    WPFControls.Grid.SetColumnSpan(chkMesh, 3)

    # Create a button
    currRow += 1
    buildJoint = WPFControls.Button()
    buildJoint.Content = "Build joint"
    WPFControls.Grid.SetRow(buildJoint, currRow)
    WPFControls.Grid.SetColumn(buildJoint, 0)
    buildJoint.Height = 30
    WPFControls.Grid.SetColumnSpan(buildJoint, 3)

    # Link a function to the Button "Click" event
    # This function will be called every time the Button is clicked
    #buildJoint.Click += BuildJoint


    # Add the WrapPanel to the Grid
    my_Grid.Children.Add(meshTextBlock2)
    my_Grid.Children.Add(hWrapPanel)

    # Add the controls to the Grid
    my_Grid.Children.Add(horizLabel)
    my_Grid.Children.Add(horizWidthLbl)
    my_Grid.Children.Add(horizWidthInput)
    my_Grid.Children.Add(horizLengthLbl)
    my_Grid.Children.Add(horizLengthInput)
    my_Grid.Children.Add(horizThickLbl)
    my_Grid.Children.Add(horizThickInput)

    my_Grid.Children.Add(vertThickLbl)
    my_Grid.Children.Add(vertThickInput)

    my_Grid.Children.Add(chkMesh)
    my_Grid.Children.Add(buildJoint)



    # Return the Grid
    return my_Grid


# Apply button handler (Green check mark)
# This function is called each time the Apply button is clicked
@apex_sdk.errorhandler
def HandleApplyButton():
    # Create a Dictionary to store the user defined tool data
    dictionary = {}

    # Find the checked button in radio_button_vertical
    # And store it in the dictionary
    # Note that this is somewhat safe since only one radio button can be checked
    vertical_checked_content = [x for x in vertical_radio_buttons if x.IsChecked == True][0].Content
    dictionary["vertical_checked"] = vertical_checked_content

    # Find the checked button in radio_button_horizontal
    # And store it in the dictionary
    horizontal_checked_content = [x for x in horizontal_radio_buttons if x.IsChecked == True][0].Content
    dictionary["horizontal_checked"] = horizontal_checked_content

    # Call the Apex API script using apex_sdk.runScriptFunction()
    # argument 1 = the fully qualified path name of your API script
    # argument 2 = the name of the function in your API script that will receive the Dictionary
    # argument 3 = the Dictionary containing the UI data
    apex_sdk.runScriptFunction(os.path.join(current_file_path, r"radio_button.py"),
                               "radio_button",
                               dictionary)
