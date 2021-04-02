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
   my_toolProperty.TitleText = "  Filter meshed components"
   my_toolProperty.WorkFlowInstructions = ""
  
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
   
   #Create a button and set it's text to "Import"
   #Assign it to Row1, Column 0
   ShowSurfMeshed = WPFControls.Button()
   ShowSurfMeshed.Content="With surface mesh only"
   WPFControls.Grid.SetRow(ShowSurfMeshed, 0)
   ShowSurfMeshed.Height = 30
   ShowSurfMeshed.Click+=HandleShowSurfMeshed

   ShowVolumeMeshed = WPFControls.Button()
   ShowVolumeMeshed.Content = "With volume mesh only"
   WPFControls.Grid.SetRow(ShowVolumeMeshed, 1)
   ShowVolumeMeshed.Height = 30
   #ShowSurfMeshed.Click += HandleShowVolumeMeshed

   ShowNotMeshed = WPFControls.Button()
   ShowNotMeshed.Content = "Without any mesh"
   WPFControls.Grid.SetRow(ShowNotMeshed, 2)
   ShowNotMeshed.Height = 30
   ShowNotMeshed.Click += HandleShowWithoutMesh

   ShowMeshed = WPFControls.Button()
   ShowMeshed.Content = "With any mesh"
   WPFControls.Grid.SetRow(ShowMeshed, 3)
   ShowMeshed.Height = 30
   ShowMeshed.Click += HandleShowWithMesh

   # Add the controls to the Grid
   my_Grid.Children.Add(ShowSurfMeshed)
   my_Grid.Children.Add(ShowVolumeMeshed)
   my_Grid.Children.Add(ShowNotMeshed)
   my_Grid.Children.Add(ShowMeshed)
   
   #Return the Grid
   return my_Grid
   
#Function to handle the Import Button "Click" event
#This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandleShowSurfMeshed(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'FilterMeshed.py')
    apex_sdk.runScriptFunction(file=script_path, function="ShowSurfMeshedOnly", args=dictionary)
"""
@apex_sdk.errorhandler
def HandleShowVolumeMeshed(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'FilterMeshed.py')
    apex_sdk.runScriptFunction(file=script_path, function="ShowVolMeshedOnly", args=dictionary)
"""
@apex_sdk.errorhandler
def HandleShowWithoutMesh(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'FilterMeshed.py')
    apex_sdk.runScriptFunction(file=script_path, function="ShowNoMeshed", args=dictionary)

@apex_sdk.errorhandler
def HandleShowWithMesh(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'FilterMeshed.py')
    apex_sdk.runScriptFunction(file=script_path, function="ShowAnyMeshed", args=dictionary)
