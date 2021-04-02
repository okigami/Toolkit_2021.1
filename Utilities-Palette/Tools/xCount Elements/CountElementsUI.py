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
   my_toolProperty.TitleText = "  Count mesh elements"
   my_toolProperty.WorkFlowInstructions = '''
   <html><body>

   <p><span style="color: #999999;">This tool is used to count the elements of all visible meshes.</span></p>
<p></p>
<p><span style="color: #999999;">For support: <span style="color: #ff0000;">support.americas@simufact.com</span></span></p>
<p><span style="color: #999999;"></span></p>

   </body></html>'''
  
   return my_toolProperty

#get tool property content
def getCustomToolPropertyContent():
   #Create a Grid
   my_Grid = WPFControls.Grid()
   
   #Add 2 Rows and 1 Column
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   
   
   #Create a button and set it's text to "Import"
   #Assign it to Row1, Column 0
   CountMeshElementsButton = WPFControls.Button()
   CountMeshElementsButton.Content="Count visible mesh elements"
   WPFControls.Grid.SetRow(CountMeshElementsButton, 1)
   CountMeshElementsButton.Height = 30
   
   CountMeshElementsButton.Click+=HandleCountElements
   
   
   # Add the controls to the Grid
   my_Grid.Children.Add(CountMeshElementsButton)
   
   #Return the Grid
   return my_Grid
   
#Function to handle the Import Button "Click" event
#This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandleCountElements(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'CountElements.py')
    apex_sdk.runScriptFunction(file=script_path, function="CountVisibleElements", args=dictionary)

#    apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\CountElements.py", "CountVisibleElements", dictionary)    

   
   
   
   
   
   
   
   
   
   
   
   
 