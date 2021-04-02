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
   my_toolProperty.TitleText = "  Create spot locations"
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
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
   
   #Row 0
   #Create a label (TextBlock)
   #Set it's Text value
   #Assign it to Row 0, Column 0
   refineTextBlock = WPFControls.TextBlock()
   refineTextBlock.Text = "Refinement diameter (mm):"
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
   importBtn.Content="Import CSV files"
   WPFControls.Grid.SetRow(importBtn, 1)
   WPFControls.Grid.SetColumn(importBtn, 0)
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Button is clicked
   importBtn.Click+=HandleimportBtn
   
   #Create an empty input TextBox
   global fileNameTextBox
   fileNameTextBox =WPFControls.TextBox()
   WPFControls.Grid.SetRow(fileNameTextBox, 2)
   WPFControls.Grid.SetColumn(fileNameTextBox, 1)
   
   selectedFilesText = WPFControls.TextBlock()
   selectedFilesText.Text = "File(s) selected:"
   WPFControls.Grid.SetRow(selectedFilesText, 2)
   WPFControls.Grid.SetColumn(selectedFilesText, 0)
   
   
   #Create a button
   #Assign it to Row1, Column 0
   goSpots = WPFControls.Button()
   goSpots.Content="Create spot locations"
   WPFControls.Grid.SetRow(goSpots, 3)
   WPFControls.Grid.SetColumn(goSpots, 0)
   WPFControls.Grid.SetColumnSpan(goSpots, 2)
   goSpots.Height = 30
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Butto is clicked
   goSpots.Click+=HandleCreateSpots
   
   
   # Add the controls to the Grid
   my_Grid.Children.Add(importBtn)
   my_Grid.Children.Add(goSpots)
   my_Grid.Children.Add(refineTextBlock)
   my_Grid.Children.Add(refineSizeTextBox)
   my_Grid.Children.Add(fileNameTextBox)
   my_Grid.Children.Add(selectedFilesText)
   
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
   
   #Display the dialog
   #If it returns anything
   #   get the file name
   global selectedFiles
   if dialog.ShowDialog():
    selectedFiles = dialog.FileNames
    fileNameTextBox.Text = str(len(selectedFiles))
    
#user defined button clickHandlers
@apex_sdk.errorhandler
def HandleCreateSpots(sender, args):
   dictionary["RefineDiameter"]= refineSizeTextBox.Text
   
   dictionary["FileList"] = ""
   for elem in selectedFiles:
    dictionary["FileList"] += elem
    dictionary["FileList"] += ','
   
   file_path = os.path.dirname(os.path.realpath(__file__))
   script_path= os.path.join(file_path, 'SpotWeld.py')
   apex_sdk.runScriptFunction(script_path, "CreateSpots", dictionary)
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
 