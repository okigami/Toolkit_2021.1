import sys
import os
import apex_sdk
import clr


#.NET references
import System
import System.Windows.Controls as WPFControls
from System.Windows.Automation import AutomationProperties
from Microsoft.Win32 import OpenFileDialog

dictionary = {}

#setting pre-defined properties of tool_propertyContainer
def getUIContent():

   my_toolProperty = apex_sdk.ToolPropertyContainer()
   my_toolProperty.ToolPropertyContent = getCustomToolPropertyContent()
   my_toolProperty.TitleText = "  Mesh coarser regions"
   my_toolProperty.WorkFlowInstructions = '<html><body><p><span style="color:#A9A9A9;">Instructions:</span></p><ol>	<li><span style="color:#A9A9A9;">Define the </span><span style="color:#00FFFF;">mesh size </span><span style="color:#A9A9A9;">in millimeter.</span></li>	<li><span style="color:#A9A9A9;">Click the </span><span style="color:#00FFFF;">Mesh outside region </span><span style="color:#A9A9A9;">button.</span></li></ol><ul>	<li><span style="color:#A9A9A9;">Information from the created trajectories combined with partitions will be used to create a coarser mesh outside of those specific locations.</span></li>	<li><span style="color:#A9A9A9;">Make sure you select and appropriate mesh size to capture the welding effects (structural response).</span></li>	<li><span style="color:#A9A9A9;">Do not use more than a 4x growth ratio between two adjacent regions (e.g.: finer mesh of 2mm and coarser mesh of max 8mm)</span></li>	<li><span style="color:#A9A9A9;">If your structure/component is very big, consider splitting it into multiple locations to control mesh transition.</span></li></ul></body></html>'
  
   return my_toolProperty

#get tool property content
def getCustomToolPropertyContent():
   #Create a Grid
   my_Grid = WPFControls.Grid()
   
   #Add 2 Rows and 1 Column
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
   
   #Row 0
   #Create a label (TextBlock)
   #Set it's Text value
   #Assign it to Row 0, Column 0
   refineTextBlock = WPFControls.TextBlock()
   refineTextBlock.Text = "Mesh size (mm):"
   WPFControls.Grid.SetRow(refineTextBlock, 0)
   WPFControls.Grid.SetColumn(refineTextBlock, 0)
   global refineSizeTextBox

   #Create an empty input TextBox assign it to Row 0, Column 1
   refineSizeTextBox =WPFControls.TextBox()
   WPFControls.Grid.SetRow(refineSizeTextBox, 0)
   WPFControls.Grid.SetColumn(refineSizeTextBox, 1)
   
   
   #Create a button and set it's text to "Import"
   #Assign it to Row1, Column 0
   meshCoarse = WPFControls.Button()
   meshCoarse.Content="Mesh outside region"
   WPFControls.Grid.SetRow(meshCoarse, 1)
   WPFControls.Grid.SetColumn(meshCoarse, 0)
   meshCoarse.Height = 30
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Button is clicked
   meshCoarse.Click+=MeshPartitions
   
   # Add the controls to the Grid
   my_Grid.Children.Add(meshCoarse)
   my_Grid.Children.Add(refineTextBlock)
   my_Grid.Children.Add(refineSizeTextBox)
   
   #Return the Grid
   return my_Grid
    
#user defined button clickHandlers
@apex_sdk.errorhandler
def MeshPartitions(sender, args):
   dictionary["MeshSize"]= refineSizeTextBox.Text
   
   file_path = os.path.dirname(os.path.realpath(__file__))
   script_path= os.path.join(file_path, 'MeshNONPartitions.py')
   apex_sdk.runScriptFunction(file=script_path, function="CreateMeshNONPartitions", args=dictionary)

   
   #apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\MeshNONPartitions.py", "CreateMeshNONPartitions", dictionary)
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
 