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
   my_toolProperty.TitleText = "  Create flush corner joint"
   my_toolProperty.WorkFlowInstructions = '''
   <html><body>
   
   <p><span style="color: #999999;">Instructions:</span></p>
<p></p>
<p><span style="color: #999999;">Use this tool to create an FLUSH CORNER based on:</span></p>
<ul>
<li><span style="color: #00ccff;">Joint width</span></li>
<li><span style="color: #00ccff;">Joint length</span></li>
<li><span style="color: #00ccff;">Base plate thickness</span></li>
<li><span style="color: #00ccff;">Web plate thickness<br /></span></li>
</ul>
<p><span style="color: #999999;">By checking <span style="color: #00ccff;">Mesh the joint for me</span>, Apex will also split the geometry and mesh it with recommended mesh size based on the provided thickness information.</span></p>
<p></p>
<p><span style="color: #999999;">Click the <span style="color: #00ccff;">Build joint</span> button to create the model.</span></p>
<p></p>
<p><span style="color: #999999;">The initial purpose of this tool is to provide a fast way to create simplified versions of real models' joints to perform thermal calibration on Simufact Welding. This way, one can calibrate the heat source faster and more accurately.</span></p>
<p></p>
<p><span style="color: #999999;">For support: <a href="mailto:support.americas@simufact.com" style="color: #999999;"><span style="color: #ff0000;">support.americas@simufact.com</span></a></span></p>
<p></p>

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
   horizWidthLbl = WPFControls.TextBlock()
   horizWidthLbl.Text = "    Width (mm):"
   WPFControls.Grid.SetRow(horizWidthLbl, currRow)
   WPFControls.Grid.SetColumn(horizWidthLbl, 0)
   
   global horizWidthInput
   horizWidthInput =WPFControls.TextBox()
   WPFControls.Grid.SetRow(horizWidthInput, currRow)
   WPFControls.Grid.SetColumn(horizWidthInput, 1)

   currRow += 1
   horizLengthLbl = WPFControls.TextBlock()
   horizLengthLbl.Text = "    Length (mm):"
   WPFControls.Grid.SetRow(horizLengthLbl, currRow)
   WPFControls.Grid.SetColumn(horizLengthLbl, 0)
   
   global horizLengthInput
   horizLengthInput =WPFControls.TextBox()
   WPFControls.Grid.SetRow(horizLengthInput, currRow)
   WPFControls.Grid.SetColumn(horizLengthInput, 1)
   
   currRow += 1
   horizThickLbl = WPFControls.TextBlock()
   horizThickLbl.Text = "    Base thickness (mm):"
   WPFControls.Grid.SetRow(horizThickLbl, currRow)
   WPFControls.Grid.SetColumn(horizThickLbl, 0)
   
   global horizThickInput
   horizThickInput =WPFControls.TextBox()
   WPFControls.Grid.SetRow(horizThickInput, currRow)
   WPFControls.Grid.SetColumn(horizThickInput, 1)


   
   # -- Vertical sheet definition
   currRow += 1
   vertLabel = WPFControls.TextBlock()
   vertLabel.Text = "Vertical sheet definition"
   WPFControls.Grid.SetRow(vertLabel, currRow)
   vertLabel.FontSize = 11
   
   currRow += 1
   vertHeightLbl = WPFControls.TextBlock()
   vertHeightLbl.Text = "    Height (mm):"
   WPFControls.Grid.SetRow(vertHeightLbl, currRow)
   WPFControls.Grid.SetColumn(vertHeightLbl, 0)
   
   global vertHeightInput
   vertHeightInput =WPFControls.TextBox()
   WPFControls.Grid.SetRow(vertHeightInput, currRow)
   WPFControls.Grid.SetColumn(vertHeightInput, 1)

   currRow += 1
   vertLengthLbl = WPFControls.TextBlock()
   vertLengthLbl.Text = "    Length (mm):"
   WPFControls.Grid.SetRow(vertLengthLbl, currRow)
   WPFControls.Grid.SetColumn(vertLengthLbl, 0)
   
   global vertLengthInput
   vertLengthInput = WPFControls.TextBox()
   WPFControls.Grid.SetRow(vertLengthInput, currRow)
   WPFControls.Grid.SetColumn(vertLengthInput, 1)
   
   currRow += 1
   vertThickLbl = WPFControls.TextBlock()
   vertThickLbl.Text = "    Web thickness (mm):"
   WPFControls.Grid.SetRow(vertThickLbl, currRow)
   WPFControls.Grid.SetColumn(vertThickLbl, 0)
   
   global vertThickInput
   vertThickInput = WPFControls.TextBox()
   WPFControls.Grid.SetRow(vertThickInput, currRow)
   WPFControls.Grid.SetColumn(vertThickInput, 1)


   # Create checkbox to ask for mesh
   currRow += 1
   global chkMesh
   chkMesh = WPFControls.CheckBox()
   chkMesh.Content = "Mesh the joint for me"
   chkMesh.Height = 20
   WPFControls.Grid.SetRow(chkMesh, currRow)
   WPFControls.Grid.SetColumn(chkMesh, 0)
   WPFControls.Grid.SetColumnSpan(chkMesh, 3)

   #Create a button
   currRow += 1
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
   my_Grid.Children.Add(horizLabel)
   my_Grid.Children.Add(horizWidthLbl)
   my_Grid.Children.Add(horizWidthInput)
   my_Grid.Children.Add(horizLengthLbl)
   my_Grid.Children.Add(horizLengthInput)
   my_Grid.Children.Add(horizThickLbl)
   my_Grid.Children.Add(horizThickInput)

   #my_Grid.Children.Add(vertLabel)
   #my_Grid.Children.Add(vertHeightLbl)
   #my_Grid.Children.Add(vertHeightInput)
   #my_Grid.Children.Add(vertLengthLbl)
   #my_Grid.Children.Add(vertLengthInput)
   my_Grid.Children.Add(vertThickLbl)
   my_Grid.Children.Add(vertThickInput)

   my_Grid.Children.Add(chkMesh)
   my_Grid.Children.Add(buildJoint)
      
   #Return the Grid
   return my_Grid
    
#user defined button clickHandlers
@apex_sdk.errorhandler
def BuildJoint(sender, args):
   dictionary["HorizWidth"]= horizWidthInput.Text
   dictionary["HorizLength"]= horizLengthInput.Text
   dictionary["HorizThick"]= horizThickInput.Text
   dictionary["VertHeight"]= horizWidthInput.Text
   dictionary["VertLength"]= horizLengthInput.Text
   dictionary["VertThick"]= vertThickInput.Text
   dictionary["MeshForMe"] = chkMesh.IsChecked
   file_path = os.path.dirname(os.path.realpath(__file__))
   script_path= os.path.join(file_path, 'JointCreator_Code.py')
   apex_sdk.runScriptFunction(file=script_path, function="buildFlushCorner", args=dictionary)
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
 
