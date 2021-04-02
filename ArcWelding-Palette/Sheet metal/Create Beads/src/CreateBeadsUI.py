import sys
import os
import apex_sdk
import clr

# .NET references
import System
import System.Windows.Controls as WPFControls
from System.Windows.Automation import AutomationProperties
from Microsoft.Win32 import OpenFileDialog

dictionary = {}


# setting pre-defined properties of tool_propertyContainer
def getUIContent():
    my_toolProperty = apex_sdk.ToolPropertyContainer()
    my_toolProperty.ToolPropertyContent = getCustomToolPropertyContent()
    my_toolProperty.TitleText = "  Create trajectories"
    my_toolProperty.WorkFlowInstructions = '<html><body><p><span style="color:#A9A9A9;">Instructions:</span></p><ol>	<li><span style="color:#A9A9A9;">Define the </span><span style="color:#00FFFF;">refinement diameter </span><span style="color:#A9A9A9;">(usually 4x the plate thickness)</span></li>	<li><span style="color:#A9A9A9;">Click </span><span style="color:#00FFFF;">Import CSV files </span><span style="color:#A9A9A9;">button (trajectories from </span><span style="color:#FF0000;">Simufact Welding</span><span style="color:#A9A9A9;">)</span></li>	<li><span style="color:#A9A9A9;">Check if the number of trajectories is what you have selected</span></li>	<li><span style="color:#A9A9A9;">Click </span><span style="color:#00FFFF;">Create trajectories </span><span style="color:#A9A9A9;">button</span></li></ol><ul>	<li><span style="color:#A9A9A9;">Use this tool to create curved cylindrical shapes at the same location of weld trajectories.</span></li>	<li><span style="color:#A9A9A9;">These locations will be used to split the surface/bodies to create defined zones for refined meshing.</span></li>	<li><span style="color:#A9A9A9;">Trajectory information has to come in </span><span style="color:#FF0000;">Simufact Welding </span><span style="color:#A9A9A9;">format.</span></li></ul></body></html>'

    return my_toolProperty


# get tool property content
def getCustomToolPropertyContent():
    # Create a Grid
    my_Grid = WPFControls.Grid()

    # Add 2 Rows and 1 Column
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
    my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
    my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())

    # Row 0
    currRow = 0
    # Create a label (TextBlock)
    # Set it's Text value
    # Assign it to Row 0, Column 0
    refineTextBlock = WPFControls.TextBlock()
    refineTextBlock.Text = "Bead leg (mm):"
    WPFControls.Grid.SetRow(refineTextBlock, currRow)
    WPFControls.Grid.SetColumn(refineTextBlock, 0)
    global refineSizeTextBox
    

    # Create an empty input TextBox assign it to Row 0, Column 1
    refineSizeTextBox = WPFControls.TextBox()
    WPFControls.Grid.SetRow(refineSizeTextBox, currRow)
    WPFControls.Grid.SetColumn(refineSizeTextBox, 1)

    
    # Create a button and set it's text to "Import"
    # Assign it to Row1, Column 0
    currRow += 1
    importBtn = WPFControls.Button()
    importBtn.Content = "Import CSV files"
    WPFControls.Grid.SetRow(importBtn, currRow)
    WPFControls.Grid.SetColumn(importBtn, 0)
    WPFControls.Grid.SetColumnSpan(importBtn, 2)
    importBtn.Height = 30

    # Link a function to the Button "Click" event
    # This function will be called every time the Button is clicked
    importBtn.Click += HandleimportBtn


    # Create an empty input TextBox
    currRow += 1
    global fileNameTextBox
    fileNameTextBox = WPFControls.TextBlock()
    WPFControls.Grid.SetRow(fileNameTextBox, currRow)
    WPFControls.Grid.SetColumn(fileNameTextBox, 1)
    fileNameTextBox.Text = "None"

    selectedFilesText = WPFControls.TextBlock()
    selectedFilesText.Text = "File(s) selected:"
    WPFControls.Grid.SetRow(selectedFilesText, currRow)
    WPFControls.Grid.SetColumn(selectedFilesText, 0)

    # Create a Combo box
    currRow += 1
    UnitNameLbl = WPFControls.TextBlock()
    UnitNameLbl.Text = "Length unit in file(s):"
    WPFControls.Grid.SetRow(UnitNameLbl, currRow)
    WPFControls.Grid.SetColumn(UnitNameLbl, 0)
    global unitType
    unitType = WPFControls.ComboBox()

    item1 = WPFControls.ComboBoxItem()
    item1.Content = "Millimeters"
    unitType.Items.Add(item1)

    item2 = WPFControls.ComboBoxItem()
    item2.Content = "Meters"
    unitType.Items.Add(item2)

    item3 = WPFControls.ComboBoxItem()
    item3.Content = "Inches"
    unitType.Items.Add(item3)

    unitType.SelectedIndex = "0"
    WPFControls.Grid.SetRow(unitType, currRow)
    WPFControls.Grid.SetColumn(unitType, 1)

    # Create checkbox to extend the weld bead
    currRow += 1
    extendLbl = WPFControls.TextBlock()
    WPFControls.Grid.SetRow(extendLbl, currRow)
    WPFControls.Grid.SetColumn(extendLbl, 0)
    extendLbl.Text = "Extend by diameter:"
    global extendBead
    extendBead = WPFControls.CheckBox()
    extendBead.Content = "Extend"
    extendBead.Height = 20
    WPFControls.Grid.SetRow(extendBead, currRow)
    WPFControls.Grid.SetColumn(extendBead, 1)
    # WPFControls.Grid.SetColumnSpan(extendBead, 2)


    # Create a button and set it's text to "Create beads"
    # Assign it to Row1, Column 0
    currRow += 1
    createBeads = WPFControls.Button()
    createBeads.Content = "Create trajectories"
    WPFControls.Grid.SetRow(createBeads, currRow)
    WPFControls.Grid.SetColumn(createBeads, 0)
    WPFControls.Grid.SetColumnSpan(createBeads, 2)
    createBeads.Height = 30

    # Link a function to the Button "Click" event
    # This function will be called every time the Butto is clicked
    createBeads.Click += CreateBeads

    # Add the controls to the Grid
    my_Grid.Children.Add(refineSizeTextBox)
    my_Grid.Children.Add(extendLbl)
    my_Grid.Children.Add(extendBead)
    my_Grid.Children.Add(importBtn)
    my_Grid.Children.Add(refineTextBlock)
    my_Grid.Children.Add(selectedFilesText)
    my_Grid.Children.Add(fileNameTextBox)
    my_Grid.Children.Add(UnitNameLbl)
    my_Grid.Children.Add(unitType)
    my_Grid.Children.Add(createBeads)

    # Return the Grid
    return my_Grid


# Function to handle the Import Button "Click" event
# This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandleimportBtn(sender, args):
    # Create a File open dialog
    dialog = OpenFileDialog()
    dialog.Title = "Select CSV file(s)"

    # Configure for single file selection
    dialog.Multiselect = True

    # Set up the file types you want to support
    dialog.Filter = "CSV Files|*.csv|All Files|*.*"

    # Display the dialog
    # If it returns anything
    #   get the file name
    global selectedFiles
    if dialog.ShowDialog():
        selectedFiles = dialog.FileNames
        fileNameTextBox.Text = str(len(selectedFiles))


# user defined button clickHandlers
@apex_sdk.errorhandler
def CreateBeads(sender, args):
    dictionary["BeadLeg"] = refineSizeTextBox.Text
    dictionary["unitType"] = unitType.Text
    if extendBead.IsChecked == True:
        dictionary["ExtendBead"] = True
    else:
        dictionary["ExtendBead"] = False
    dictionary["FileList"] = ""
    for elem in selectedFiles:
        dictionary["FileList"] += elem
        dictionary["FileList"] += ','
    
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'CreateBeads.py')
    apex_sdk.runScriptFunction(file=script_path, function="BeadBySweep", args=dictionary)

    
    #apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\BeadBySweep.py","BeadBySweep", dictionary)


