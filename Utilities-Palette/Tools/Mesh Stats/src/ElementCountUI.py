# MSC Apex - User Defined Tools using Python Scripts
# Data Grid UI Example
# 
import sys
import os
import apex_sdk
import clr

# .NET references
import System
import System.Windows.Controls as WPFControls
import System.Data as WPFData
from Microsoft.Win32 import OpenFileDialog

# Define current file path of example
current_file_path = os.path.dirname(os.path.realpath(__file__))


# Set pre-defined properties of ToolPropertyContainer
def getUIContent():
   my_toolProperty = apex_sdk.ToolPropertyContainer()
   
   # Provide an icon and a name for the tool property panel
   my_toolProperty.TitleText = "Mesh statistics"
   my_toolProperty.WorkFlowInstructions = '''
    <p><strong><span style="color: #999999;">Mesh statistics<br /></span></strong></p>
    <p><span style="color: #999999;">Description: This tool calculates the element count and get mesh type for all visible parts.</span></p>
    <ul></ul>
    <p><span style="color: #999999;">For support: <span style="color: #ff0000;"><a href="mailto:support.americas@simufact.com">support.americas@simufact.com</a></span></span></p>
    <p><span style="color: #999999;"><span style="color: #ff0000;"></span></span></p>
   '''

   # Define UI
   my_toolProperty.ToolPropertyContent = getCustomToolPropertyContent()
   
   # Update Grid
   UpdateDataGridData()

   # Define PickFilterList
   my_toolProperty.ShowPickChoice = True
   my_toolProperty.PickFilterList = setPickFilterList()
   
   return my_toolProperty


# Set PickFilters
def setPickFilterList():
    # Create an empty List of strings
    pickChoices = System.Collections.Generic.List[System.String]()

    # Exclusive picking and visibility picking
    pickChoices.Add(apex_sdk.PickFilterTypes.ExclusivePicking)
    pickChoices.Add(apex_sdk.PickFilterTypes.VisibilityPicking)

    # Add Types
    pickChoices.Add(apex_sdk.PickFilterTypes.Part)
    pickChoices.Add(apex_sdk.PickFilterTypes.Assembly)
    pickChoices.Add(apex_sdk.PickFilterTypes.SurfaceMesh)
    pickChoices.Add(apex_sdk.PickFilterTypes.SolidMesh)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Solid)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Surface)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Cell)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Face)


    # Return the pick filter list
    return pickChoices


# Define Layout and Components
def getCustomToolPropertyContent():
   currRow = 0
   # Create a Grid
   my_Grid = WPFControls.Grid()

   # Add 1 Row and One Column
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())

   # Create a DataGrid
   global myDataGrid
   myDataGrid = WPFControls.DataGrid()

   # Create a button
   currRow += 20
   actionButton = WPFControls.Button()
   actionButton.Content = "Calculate selected"
   WPFControls.Grid.SetRow(actionButton, currRow)
   WPFControls.Grid.SetColumn(actionButton, 0)
   actionButton.Height = 30
   WPFControls.Grid.SetColumnSpan(actionButton, 2)
   actionButton.Click += GetSelectionInfo  # Link a function to the Button "Click" event

   # Add the DataGrid to the Grid
   my_Grid.Children.Add(myDataGrid)
   my_Grid.Children.Add(actionButton)

   # Return the Grid   
   return my_Grid

# Function to handle the Datagrid "Loaded" event
@apex_sdk.errorhandler
def ResizeColumns(sender,args):
   # Get the current width of the DataGrid
   width = myDataGrid.ActualWidth

   # Get the number of columns
   num_cols = myDataGrid.Columns.Count
   
   # Calculate the columns width
   col_width = myDataGrid.ActualWidth/myDataGrid.Columns.Count
    
   # Set the width of each columns
   for column in myDataGrid.Columns:
       column.Width = WPFControls.DataGridLength(col_width)   
    

@apex_sdk.errorhandler
def UpdateDataGridData():
   apex_sdk.runScriptFunction(os.path.join(current_file_path, r"ElementCount.py"),
                              "prepare_data_grid",
                              callback=UpdateDataGridView)

@apex_sdk.errorhandler
def GetSelectionInfo(*args, **kwargs):
   apex_sdk.runScriptFunction(os.path.join(current_file_path, r"ElementCount.py"),
                              "calcSelected",
                              callback=UpdateDataGridView)


#This function receives data from the Script API function and updates the Tool UI 
@apex_sdk.errorhandler
def UpdateDataGridView():

   # Retrieve grid results
   grid = apex_sdk.getScriptFunctionReturnData()

   # Create parts table
   data_table = WPFData.DataTable("Meshes")
   data_table.Columns.Add("Name")
   data_table.Columns.Add("Parent")
   data_table.Columns.Add("Type")
   data_table.Columns.Add("Elements")


   # Add data to the table for each part
   parts = grid['meshes']
   for part in parts:      
      data_table.Rows.Add(part['mesh_name'], part['parent_name'], part['mesh_type'], part['elements_count'])
   
   # Set the IetmsSource for the data grid to the DataTable 
   myDataGrid.ItemsSource = data_table.DefaultView 
   
   # Position the DataGrid in the first row, column of the Grid
   WPFControls.Grid.SetRow(myDataGrid, 0)
   WPFControls.Grid.SetColumn(myDataGrid, 0)

