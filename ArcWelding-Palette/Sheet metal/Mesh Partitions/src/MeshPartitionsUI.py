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
   my_toolProperty.TitleText = "  Mesh refinement regions"
   my_toolProperty.WorkFlowInstructions = '<html><body><p><span style="color:#A9A9A9;">Instructions:</span></p><ol>	<li><span style="color:#A9A9A9;">Define the </span><span style="color:#00FFFF;">mesh size </span><span style="color:#A9A9A9;">in millimeters.</span></li>	<li><span style="color:#A9A9A9;">Click the </span><span style="color:#00FFFF;">Mesh partitions </span><span style="color:#A9A9A9;">button.</span></li></ol><ul>	<li><span style="color:#A9A9A9;">Information from the created trajectories combined with partitions will be used to create a finer mesh on those specific locations.</span></li>	<li><span style="color:#A9A9A9;">Make sure you select and appropriate mesh size to capture the welding effects.</span></li>	<li><span style="color:#A9A9A9;">Some general rules:</span>	<ul>		<li><span style="color:#ADD8E6;">Arc Welding: </span><span style="color:#A9A9A9;">check the size of your heat source first and make sure you have at least four elements along the welding direction, two elements accross the width and two elements in the depth.</span></li>		<li><span style="color:#AFEEEE;">Laser Welding: </span><span style="color:#A9A9A9;">check the size of your heat source first and make sure you have at least two elements in the diameter and five elements in the depth.</span></li>		<li><span style="color:#AFEEEE;">RSW: </span><span style="color:#A9A9A9;">check the size of your electrode first and make sure you have at least eight elements in the diamater.</span></li>	</ul>	</li>	<li><span style="color:#A9A9A9;">Refer to the infosheets in </span><span style="color:#FF0000;">Simufact Welding </span><span style="color:#A9A9A9;">for a more detailed explanation.</span></li></ul></body></html>'
  
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
   importBtn = WPFControls.Button()
   importBtn.Content="Mesh partitions"
   WPFControls.Grid.SetRow(importBtn, 1)
   WPFControls.Grid.SetColumn(importBtn, 0)
   WPFControls.Grid.SetColumnSpan(importBtn, 2)
   importBtn.Height = 30
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Button is clicked
   importBtn.Click+=MeshPartitions
   
   # Add the controls to the Grid
   my_Grid.Children.Add(importBtn)
   my_Grid.Children.Add(refineTextBlock)
   my_Grid.Children.Add(refineSizeTextBox)
   
   #Return the Grid
   return my_Grid
    
#user defined button clickHandlers
@apex_sdk.errorhandler
def MeshPartitions(sender, args):
   dictionary["MeshSize"]= refineSizeTextBox.Text
   file_path = os.path.dirname(os.path.realpath(__file__))
   script_path= os.path.join(file_path, 'MeshPartitions.py')
   apex_sdk.runScriptFunction(file=script_path, function="CreateMeshPartitions", args=dictionary)

   #apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\MeshPartitions.py", "CreateMeshPartitions", dictionary)
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
 