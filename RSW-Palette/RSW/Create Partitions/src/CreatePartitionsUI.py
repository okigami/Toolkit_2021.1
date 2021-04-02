import sys
import os
import apex_sdk
import clr


#.NET references
import System
import System.Windows.Controls as WPFControls
from System.Windows.Automation import AutomationProperties

dictionary = {}

#setting pre-defined properties of tool_propertyContainer
def getUIContent():

   my_toolProperty = apex_sdk.ToolPropertyContainer()
   my_toolProperty.ToolPropertyContent = getCustomToolPropertyContent()
   my_toolProperty.TitleText = "  Define refinement regions"
   my_toolProperty.WorkFlowInstructions = '<html><body><p><span style="color:#A9A9A9;">Instructions:</span></p><ol>	<li><span style="color:#A9A9A9;">Click the </span><span style="color:#00FFFF;">Split at weld trajectories </span><span style="color:#A9A9A9;">button.</span></li></ol><ul>	<li><span style="color:#A9A9A9;">If you have created the expanded trajectories, this tool will use them to split the visible surfaces in order to create refinement zones (partitions).</span></li>	<li><span style="color:#A9A9A9;">These partitions can then receive a finer mesh to capture the welding effects properly.</span></li></ul></body></html>'
  
   return my_toolProperty

#get tool property content
def getCustomToolPropertyContent():
   #Create a Grid
   my_Grid = WPFControls.Grid()
   
   #Add 2 Rows and 1 Column
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   
   
   #Create a button and set it's text to "Import"
   #Assign it to Row1, Column 0
   splitBeads = WPFControls.Button()
   splitBeads.Content="Split at spot location"
   WPFControls.Grid.SetRow(splitBeads, 1)
   WPFControls.Grid.SetColumn(splitBeads, 0)
   splitBeads.Height = 30
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Button is clicked
   splitBeads.Click+=HandlecleanBtn
   
   # Add the controls to the Grid
   my_Grid.Children.Add(splitBeads)
   
   #Return the Grid
   return my_Grid
   
#Function to handle the Import Button "Click" event
#This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandlecleanBtn(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'CreatePartitions.py')
    apex_sdk.runScriptFunction(file=script_path, function="SplitByTrajectories", args=dictionary)

    #apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\SplitByTrajectories.py", "SplitByTrajectories", dictionary)    

   
   
   
   
   
   
   
   
   
   
   
   
 