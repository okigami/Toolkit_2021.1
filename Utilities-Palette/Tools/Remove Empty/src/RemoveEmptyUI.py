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
   my_toolProperty.TitleText = "  Remove empty containers"
   my_toolProperty.WorkFlowInstructions = '''
   <html><body>

   <p><span style="color: #999999;">This tool is used to remove (delete) empty containers from the model tree. It will delete parts that contain nothing in it and assemblies that contain no part or assembly in it in this order.</span></p>
<p></p>
<p><span style="color: #999999;">It is recommended to run this tool once you have deleted components directly from the view to keep the model tree organized and clean.</span></p>
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
   doOrganize = WPFControls.Button()
   doOrganize.Content="Remove empty containers"
   WPFControls.Grid.SetRow(doOrganize, 1)
   WPFControls.Grid.SetColumn(doOrganize, 0)
   doOrganize.Height = 30
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Button is clicked
   doOrganize.Click+=HandlecleanBtn
   
   # Add the controls to the Grid
   my_Grid.Children.Add(doOrganize)
   
   #Return the Grid
   return my_Grid
   
   
#Function to handle the Import Button "Click" event
#This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandlecleanBtn(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'RemoveEmpty.py')
    apex_sdk.runScriptFunction(file=script_path, function="RemoveEmpty", args=dictionary)
    

            
            
            
            
            
            
            
            
            
            
            
            
            
            