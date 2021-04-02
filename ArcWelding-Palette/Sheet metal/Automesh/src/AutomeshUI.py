import sys
import os
import apex_sdk
import clr


#.NET references
import System
from System.Windows import MessageBox
import System.Windows.Controls as WPFControls
from System.Windows.Automation import AutomationProperties
from Microsoft.Win32 import OpenFileDialog

dictionary = {}

#setting pre-defined properties of tool_propertyContainer
def getUIContent():

   my_toolProperty = apex_sdk.ToolPropertyContainer()
   my_toolProperty.ToolPropertyContent = getCustomToolPropertyContent()
   my_toolProperty.TitleText = "  Arc welding automesh"
   my_toolProperty.WorkFlowInstructions = '<html><body><p><span style="color:#A9A9A9;">Instructions:</span></p><ol>	<li><span style="color:#A9A9A9;">Define the </span><span style="color:#00FFFF;">finer mesh size </span><span style="color:#A9A9A9;">in millimeters.</span></li>	<li><span style="color:#A9A9A9;">Define the </span><span style="color:#00FFFF;">coarser mesh size </span><span style="color:#A9A9A9;">in millimeters.</span></li>	<li><span style="color:#A9A9A9;">Define the </span><span style="color:#00FFFF;">refinement diameter </span><span style="color:#A9A9A9;">in millmeters.</span></li>	<li><span style="color:#A9A9A9;">Click the </span><span style="color:#00FFFF;">Mesh outside region </span><span style="color:#A9A9A9;">button.</span></li>	<li><span style="color:#A9A9A9;">Click the </span><span style="color:#00FFFF;">Automesh for arc welding </span><span style="color:#A9A9A9;">button.</span></li></ol><ul>	<li><span style="color:#A9A9A9;">By making calls to the individual meshing tools, this operation will perform all commands in sequence.</span></li>	<li><span style="color:#A9A9A9;">Make sure you have defined the proper mesh sizes and refinement areas.</span></li>	<li><span style="color:#A9A9A9;">You can perform individual operations again once the automesh finishes to adjust other parameters.</span></li></ul></body></html>'

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
    pickChoices.Add(apex_sdk.PickFilterTypes.Assembly)
    #pickChoices.Add(apex_sdk.PickFilterTypes.Edge)

    # Return the pick filter list
    return pickChoices

#get tool property content
def getCustomToolPropertyContent():
   #Create a Grid
   my_Grid = WPFControls.Grid()
   
   #Add Rows and Columns
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
   
   
   #Create a text label for the mesh refinement
   meshRefinementText = WPFControls.TextBlock()
   meshRefinementText.Text = "Finer mesh size (mm):"
   WPFControls.Grid.SetRow(meshRefinementText, 1)
   WPFControls.Grid.SetColumn(meshRefinementText, 0)
   
   #Create an empty input TextBox to input the mesh refinement
   global meshRefinementInput
   meshRefinementInput = WPFControls.TextBox()
   WPFControls.Grid.SetRow(meshRefinementInput, 1)
   WPFControls.Grid.SetColumn(meshRefinementInput, 1)
   
   
   
   #Create a text label for the coarse mesh
   meshCoarseText = WPFControls.TextBlock()
   meshCoarseText.Text = "Coarse mesh size (mm):"
   WPFControls.Grid.SetRow(meshCoarseText, 2)
   WPFControls.Grid.SetColumn(meshCoarseText, 0)
   
   #Create an empty input TextBox to input the coarse mesh
   global meshCoarseInput
   meshCoarseInput = WPFControls.TextBox()
   WPFControls.Grid.SetRow(meshCoarseInput, 2)
   WPFControls.Grid.SetColumn(meshCoarseInput, 1)
   
   
   
   #Create a text label for the refinement diameter
   refineDiamText = WPFControls.TextBlock()
   refineDiamText.Text = "Refinement diameter (mm):"
   WPFControls.Grid.SetRow(refineDiamText, 3)
   WPFControls.Grid.SetColumn(refineDiamText, 0)
   
   #Create an empty input TextBox to input the refinement diameter
   global refineDiamInput
   refineDiamInput = WPFControls.TextBox()
   WPFControls.Grid.SetRow(refineDiamInput, 3)
   WPFControls.Grid.SetColumn(refineDiamInput, 1)

   
   #Create a text label for the CSV trajectory import
   importCSVFiles = WPFControls.Button()
   importCSVFiles.Content="Import trajectories"
   WPFControls.Grid.SetRow(importCSVFiles, 4)
   WPFControls.Grid.SetColumn(importCSVFiles, 0)
   importCSVFiles.Height = 30
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Button is clicked
   importCSVFiles.Click+=HandleimportBtn
   
   #Create an empty input TextBox
   #Create a text label for the refinement diameter
   global numOfTrajectories
   numOfTrajectories = WPFControls.TextBlock()
   numOfTrajectories.Text = "  0 file(s)"
   WPFControls.Grid.SetRow(numOfTrajectories, 4)
   WPFControls.Grid.SetColumn(numOfTrajectories, 1)

   
   
   #Create a button to perform the Automesh
   goAutomesh = WPFControls.Button()
   goAutomesh.Content="Automesh for arc welding"
   WPFControls.Grid.SetRow(goAutomesh, 7)
   WPFControls.Grid.SetColumn(goAutomesh, 0)
   WPFControls.Grid.SetColumnSpan(goAutomesh, 2)
   goAutomesh.Height = 30
    #Link a function to the Button "Click" event 
   goAutomesh.Click+=GoAutoMesh
   
   
   # Add the controls to the Grid
   my_Grid.Children.Add(meshRefinementInput)
   my_Grid.Children.Add(meshCoarseInput)
   my_Grid.Children.Add(refineDiamInput)
   my_Grid.Children.Add(importCSVFiles)
   my_Grid.Children.Add(goAutomesh)

   my_Grid.Children.Add(numOfTrajectories)
   my_Grid.Children.Add(meshRefinementText)
   my_Grid.Children.Add(meshCoarseText)
   my_Grid.Children.Add(refineDiamText)

   
   #Return the Grid
   return my_Grid
   
#Function to handle the Import Button "Click" event
#This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandleimportBtn(sender,args):

   #Create a File open dialog
   dialog = OpenFileDialog()
   dialog.Title = "Select CSV file(s)"
   
   #Configure for single file selection
   dialog.Multiselect = True
   
   #Set up the file types you want to support
   dialog.Filter = "CSV Files|*.csv|All Files|*.*"
   
   global selectedFiles
   if dialog.ShowDialog():
    selectedFiles = dialog.FileNames
    numOfTrajectories.Text = "  {0} file(s)".format(len(selectedFiles))
    
#user defined button clickHandlers
@apex_sdk.errorhandler
def GoAutoMesh(sender, args):
    file_path = os.path.dirname(os.path.realpath(__file__))

    dictionary["RefineDiameter"] = refineDiamInput.Text
    dictionary["FineMeshSize"] = meshRefinementInput.Text
    dictionary["CoarseMeshSize"] = meshCoarseInput.Text
    dictionary["FileList"] = ""
    dictionary["ExtendBead"] = True
    
    if not selectedFiles:
        ans = MessageBox.Show("Please import trajectories first", "Error")
        
    elif refineDiamInput.Text=="":
        ans = MessageBox.Show("Please specify the refinement diameter first", "Error")
    
    elif meshRefinementInput.Text=="":
        ans = MessageBox.Show("Please specify the refinement mesh size first", "Error")
        
    elif meshCoarseInput.Text=="":
        ans = MessageBox.Show("Please specify the coarse mesh size first", "Error")
    
    else:
        for elem in selectedFiles:
            dictionary["FileList"] += elem
            dictionary["FileList"] += ','

        apex_sdk.runScriptFunction(file=os.path.join(file_path, 'Automesh.py'), function="ArcWeldAutomesh", args=dictionary)


    #apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\ArcWeldAutomesh.py", "ArcWeldAutomesh", dictionary)
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
 