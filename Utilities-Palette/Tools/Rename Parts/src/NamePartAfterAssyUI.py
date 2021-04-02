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
   my_toolProperty.TitleText = "  Rename part after assembly"
   my_toolProperty.WorkFlowInstructions = "Rename all single parts in an assembly with the assembly name. This helps identifying the mesh after exporting."
  
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
   doOrganize.Content="Rename single parts"
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
    script_path= os.path.join(file_path, 'NamePartAfterAssy.py')
    apex_sdk.runScriptFunction(file=script_path, function="NameAfterAssy", args=dictionary)
    

            
            
            
            
            
            
            
            
            
            
            
            
            
            