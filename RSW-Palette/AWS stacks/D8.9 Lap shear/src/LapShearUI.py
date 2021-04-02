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
   my_toolProperty.TitleText = "  AWS D8.9M lap shear coupon"
   my_toolProperty.WorkFlowInstructions = ''' Doc '''

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
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())

   currRow = 0


   # -- Horizontal sheet definition
   horizLabel = WPFControls.TextBlock()
   horizLabel.Text = "Shape definition"
   WPFControls.Grid.SetRow(horizLabel, currRow)
   horizLabel.FontSize = 11

   currRow += 1
   spotLbl = WPFControls.TextBlock()
   spotLbl.Text = "    Spot diam. (mm):"
   WPFControls.Grid.SetRow(spotLbl, currRow)
   WPFControls.Grid.SetColumn(spotLbl, 0)
   
   global spotSize
   spotSize =WPFControls.TextBox()
   WPFControls.Grid.SetRow(spotSize, currRow)
   WPFControls.Grid.SetColumn(spotSize, 1)
   
   currRow += 1
   horizThickLbl = WPFControls.TextBlock()
   horizThickLbl.Text = "    Sheet 01 thickn. (mm):"
   WPFControls.Grid.SetRow(horizThickLbl, currRow)
   WPFControls.Grid.SetColumn(horizThickLbl, 0)
   
   global horizThickInput
   horizThickInput =WPFControls.TextBox()
   WPFControls.Grid.SetRow(horizThickInput, currRow)
   WPFControls.Grid.SetColumn(horizThickInput, 1)


   # -- Parameters definition
   currRow += 1
   vertThickLbl = WPFControls.TextBlock()
   vertThickLbl.Text = "    Sheet 02 thickn. (mm):"
   WPFControls.Grid.SetRow(vertThickLbl, currRow)
   WPFControls.Grid.SetColumn(vertThickLbl, 0)
   
   global vertThickInput
   vertThickInput = WPFControls.TextBox()
   WPFControls.Grid.SetRow(vertThickInput, currRow)
   WPFControls.Grid.SetColumn(vertThickInput, 1)

   # -- Parameters definition
   currRow += 1
   gapLbl = WPFControls.TextBlock()
   gapLbl.Text = "    Gap between sheets (mm):"
   WPFControls.Grid.SetRow(gapLbl, currRow)
   WPFControls.Grid.SetColumn(gapLbl, 0)

   global gapInput
   gapInput = WPFControls.TextBox()
   WPFControls.Grid.SetRow(gapInput, currRow)
   WPFControls.Grid.SetColumn(gapInput, 1)

   # Create grippers?
   currRow += 1
   global chkCreateGrippers
   chkCreateGrippers = WPFControls.CheckBox()
   chkCreateGrippers.Content = "Create grippers"
   chkCreateGrippers.Height = 20
   WPFControls.Grid.SetRow(chkCreateGrippers, currRow)
   WPFControls.Grid.SetColumn(chkCreateGrippers, 0)
   #WPFControls.Grid.SetColumnSpan(chkCreateGrippers, 3)

   # Create a horizontal array of three radio buttons
   # Create a WrapPanel
   hWrapPanel = WPFControls.WrapPanel()
   hWrapPanel.Orientation = WPFControls.Orientation.Horizontal

   # Second Button Array
   # Create a label for the second radio button array
   currRow += 1
   lblMeshType = WPFControls.TextBlock()
   lblMeshType.Text = "Meshing"
   WPFControls.Grid.SetRow(lblMeshType, currRow)
   WPFControls.Grid.SetColumn(lblMeshType, 0)

   # Create a List to hold the radio buttons in the first array
   # We'll use this later to make it easier to find which button is checked
   global horizontal_radio_buttons
   horizontal_radio_buttons = []

   # Create a first radio button and add to the WrapPanel
   horizontal_radio_buttons.append(WPFControls.RadioButton())
   horizontal_radio_buttons[0].Content = "No mesh"

   # Set the first radio button to be checked
   # Note the horrible notation required to define a Nullable Boolean True
   horizontal_radio_buttons[0].IsChecked = System.Nullable[System.Boolean](True)
   hWrapPanel.Children.Add(horizontal_radio_buttons[0])

   # Create a second radio button and add to the WrapPanel
   horizontal_radio_buttons.append(WPFControls.RadioButton())
   horizontal_radio_buttons[1].Content = "For weld"
   hWrapPanel.Children.Add(horizontal_radio_buttons[1])

   # Create a third radio button and add to the WrapPanel
   horizontal_radio_buttons.append(WPFControls.RadioButton())
   horizontal_radio_buttons[2].Content = "Pull test"
   hWrapPanel.Children.Add(horizontal_radio_buttons[2])

   # Position the WrapPanel in the first row, column of the Grid
   currRow += 1
   WPFControls.Grid.SetRow(hWrapPanel, currRow)
   WPFControls.Grid.SetColumn(hWrapPanel, 0)
   WPFControls.Grid.SetColumnSpan(hWrapPanel, 3)

   #Create a button
   currRow += 2
   buildJoint = WPFControls.Button()
   buildJoint.Content="Build joint"
   WPFControls.Grid.SetRow(buildJoint, currRow)
   WPFControls.Grid.SetColumn(buildJoint, 0)
   buildJoint.Height = 30
   WPFControls.Grid.SetColumnSpan(buildJoint, 3)
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Button is clicked
   buildJoint.Click+=BuildJoint
   
   # Add the controls to the Grid
   my_Grid.Children.Add(spotLbl)
   my_Grid.Children.Add(spotSize)
   my_Grid.Children.Add(horizLabel)
   my_Grid.Children.Add(horizThickLbl)
   my_Grid.Children.Add(horizThickInput)
   my_Grid.Children.Add(vertThickLbl)
   my_Grid.Children.Add(vertThickInput)
   my_Grid.Children.Add(gapLbl)
   my_Grid.Children.Add(gapInput)

   my_Grid.Children.Add(chkCreateGrippers)

   my_Grid.Children.Add(lblMeshType)
   my_Grid.Children.Add(hWrapPanel)
   my_Grid.Children.Add(buildJoint)
      
   #Return the Grid
   return my_Grid
    
#user defined button clickHandlers
@apex_sdk.errorhandler
def BuildJoint(sender, args):
   horizontal_checked_content = [x for x in horizontal_radio_buttons if x.IsChecked == True][0].Content
   dictionary["Meshing"] = horizontal_checked_content

   dictionary["Thick01"]= horizThickInput.Text
   dictionary["Thick02"]= vertThickInput.Text
   dictionary["SpotSize"] = spotSize.Text
   dictionary["GapSize"] = gapInput.Text
   dictionary["CreateGrippers"] = chkCreateGrippers.IsChecked

   file_path = os.path.dirname(os.path.realpath(__file__))
   script_path= os.path.join(file_path, 'AWSRSWCode.py')
   apex_sdk.runScriptFunction(file=script_path, function="buildLapShear", args=dictionary)
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
 
