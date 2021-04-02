import sys
import os
import apex_sdk
import clr


# .NET references
import System
import System.Windows.Controls as WPFControls
from System.Windows.Automation import AutomationProperties
from Microsoft.Win32 import OpenFileDialog
from System.Windows.Forms import FolderBrowserDialog

dictionary = {}

#setting pre-defined properties of tool_propertyContainer
def getUIContent():

   my_toolProperty = apex_sdk.ToolPropertyContainer()
   my_toolProperty.ToolPropertyContent = getCustomToolPropertyContent()
   my_toolProperty.TitleText = "  Export BDF files from part"
   my_toolProperty.WorkFlowInstructions = '''
   <html><body>
<p><span style="color: #999999;">This tool is used to export each part as a single BDF file to be used in Simufact Welding.<br /></span></p>
<p><span style="color: #999999;"></span></p>
<p><span style="color: #999999;">It will ask you to point to the directory in which the BDF files shall be saved.</span></p>
<p><span style="color: #999999;"></span></p>
<p><span style="color: #999999;">Remember that solid meshes can be directly imported in Simufact and shell meshes have to be expanded back to a solid mesh.</span></p>
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
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())

   
   #Create a button and set it's text to "Import"
   #Assign it to Row1, Column 0
   exportBtn = WPFControls.Button()
   exportBtn.Content="Export BDF from part"
   WPFControls.Grid.SetRow(exportBtn, 1)
   WPFControls.Grid.SetColumn(exportBtn, 0)
   exportBtn.Height = 30
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Button is clicked
   exportBtn.Click+=ExportBDFData
   
   # Add the controls to the Grid
   my_Grid.Children.Add(exportBtn)
   
   #Return the Grid
   return my_Grid
   
   
#Function to handle the Import Button "Click" event
#This function gets called every time the Button is clicked
# Function to handle the Import Button "Click" event
# This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def ExportBDFData(sender, args):
    # Create a File open dialog
    dialog = FolderBrowserDialog()
    dialog.Title = "Select directory to save the BDF files"

    # Display the dialog
    # If it returns anything
    #   get the file name
    global projectPath
    if dialog.ShowDialog():
        projectPath = dialog.SelectedPath
        file_path = os.path.dirname(os.path.realpath(__file__))
        dictionary["DirPath"]= projectPath
        script_path= os.path.join(file_path, 'ExportBDF.py')
        apex_sdk.runScriptFunction(file=script_path, function="ExportBDF", args=dictionary)

