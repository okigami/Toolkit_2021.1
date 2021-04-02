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
   my_toolProperty.TitleText = "  Create reference planes"
   my_toolProperty.WorkFlowInstructions = '''
   <p><strong><span style="color: #999999;">Create reference planes<br /></span></strong></p>
   <p><span style="color: #999999;">Description: This tools creates the three reference planes in the (0,0,0) location. A new part will be created at the model level to contain the three planes (small surfaces).<br /></span></p>
   <p><span style="color: #999999;">Workflow:</span></p>
   <ol>
   <li><span style="color: #999999;">Click create planes</span><span style="color: #999999;"></span></li>
   </ol>
   <p><span style="color: #999999;">For support: <span style="color: #ff0000;"><a href="mailto:support.americas@simufact.com">support.americas@simufact.com</a></span></span></p>
   <p><span style="color: #999999;"><span style="color: #ff0000;"></span></span></p>
   '''
  
   return my_toolProperty

#get tool property content
def getCustomToolPropertyContent():
   #Create a Grid
   my_Grid = WPFControls.Grid()
   
   #Add 2 Rows and 1 Column
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   
   
   #Create a button and set it's text to "Import"
   #Assign it to Row1, Column 0
   cleanBtn = WPFControls.Button()
   cleanBtn.Content="Create planes"
   WPFControls.Grid.SetRow(cleanBtn, 1)
   WPFControls.Grid.SetColumn(cleanBtn, 0)
   cleanBtn.Height = 30
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Button is clicked
   cleanBtn.Click+=HandlecleanBtn
   
   # Add the controls to the Grid
   my_Grid.Children.Add(cleanBtn)
   
   #Return the Grid
   return my_Grid
   
#Function to handle the Import Button "Click" event
#This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandlecleanBtn(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'CreateRefPlanes.py')
    apex_sdk.runScriptFunction(file=script_path, function="CreatePlanes", args=dictionary)
    

    #apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\Midsurface.py", "Midsurface", dictionary)    

   
   
   
   
   
   
   
   
   
   
   
   
 