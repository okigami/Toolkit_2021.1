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
   my_toolProperty.TitleText = "  Create edge joint"
   my_toolProperty.WorkFlowInstructions = '''
<html>
<body>

<p><span style="color: #999999;">Instructions:</span></p>
<p></p>
<p><span style="color: #999999;">Use this tool to create an EDGE JOINT based on:</span></p>
<ul>
<li><span style="color: #00ccff;">Joint width</span></li>
<li><span style="color: #00ccff;">Joint length</span></li>
<li><span style="color: #00ccff;">Thickness of sheet 01</span></li>
<li><span style="color: #00ccff;">Thickness of sheet 02</span></li>
</ul>
<p><span style="color: #999999;">By checking <span style="color: #00ccff;">Mesh the joint for me</span>, Apex will also split the geometry and mesh it with recommended mesh size based on the provided thickness information.</span></p>
<p></p>
<p><span style="color: #999999;">Click the <span style="color: #00ccff;">Build joint</span> button to create the model.</span></p>
<p></p>
<p><span style="color: #999999;">The initial purpose of this tool is to provide a fast way to create simplified versions of real models' joints to perform thermal calibration on Simufact Welding. This way, one can calibrate the heat source faster and more accurately.</span></p>
<p></p>
<p><span style="color: #999999;">For support: <a href="mailto:support.americas@simufact.com" style="color: #999999;"><span style="color: #ff0000;">support.americas@simufact.com</span></a></span></p>
<p></p>

</body>
</html>

            '''
  
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

   generalLbl = WPFControls.TextBlock()
   generalLbl.Text = "Shape definition"
   WPFControls.Grid.SetRow(generalLbl, currRow)
   generalLbl.FontSize = 11
   
   
   # -- Sheet 01 definition
   currRow += 1
   globalWidthLbl = WPFControls.TextBlock()
   globalWidthLbl.Text = "    Width (mm):"
   WPFControls.Grid.SetRow(globalWidthLbl, currRow)
   WPFControls.Grid.SetColumn(globalWidthLbl, 0)
   
   global globalWidthInput
   globalWidthInput =WPFControls.TextBox()
   WPFControls.Grid.SetRow(globalWidthInput, currRow)
   WPFControls.Grid.SetColumn(globalWidthInput, 1)

   currRow += 1
   globalLengthLbl = WPFControls.TextBlock()
   globalLengthLbl.Text = "    Length (mm):"
   WPFControls.Grid.SetRow(globalLengthLbl, currRow)
   WPFControls.Grid.SetColumn(globalLengthLbl, 0)
   
   global globalLengthInput
   globalLengthInput =WPFControls.TextBox()
   WPFControls.Grid.SetRow(globalLengthInput, currRow)
   WPFControls.Grid.SetColumn(globalLengthInput, 1)
   
   currRow += 1
   thick01Lbl = WPFControls.TextBlock()
   thick01Lbl.Text = "    Thickness 01 (mm):"
   WPFControls.Grid.SetRow(thick01Lbl, currRow)
   WPFControls.Grid.SetColumn(thick01Lbl, 0)
   
   global thick01Input
   thick01Input =WPFControls.TextBox()
   WPFControls.Grid.SetRow(thick01Input, currRow)
   WPFControls.Grid.SetColumn(thick01Input, 1)


   
   # -- Vertical sheet definition
   currRow += 1
   thick02Lbl = WPFControls.TextBlock()
   thick02Lbl.Text = "    Thickness 02 (mm):"
   WPFControls.Grid.SetRow(thick02Lbl, currRow)
   WPFControls.Grid.SetColumn(thick02Lbl, 0)
   
   global thick02Input
   thick02Input = WPFControls.TextBox()
   WPFControls.Grid.SetRow(thick02Input, currRow)
   WPFControls.Grid.SetColumn(thick02Input, 1)


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
   my_Grid.Children.Add(generalLbl)
   my_Grid.Children.Add(globalWidthLbl)
   my_Grid.Children.Add(globalWidthInput)
   my_Grid.Children.Add(globalLengthLbl)
   my_Grid.Children.Add(globalLengthInput)
   
   my_Grid.Children.Add(thick01Lbl)
   my_Grid.Children.Add(thick01Input)

   my_Grid.Children.Add(thick02Lbl)
   my_Grid.Children.Add(thick02Input)

   my_Grid.Children.Add(chkMesh)
   my_Grid.Children.Add(buildJoint)
      
   #Return the Grid
   return my_Grid
    
#user defined button clickHandlers
@apex_sdk.errorhandler
def BuildJoint(sender, args):
   dictionary["JointWidth"]= globalWidthInput.Text
   dictionary["JointLength"]= globalLengthInput.Text
   dictionary["Thick01"]= thick01Input.Text
   dictionary["Thick02"]= thick02Input.Text
   dictionary["MeshForMe"] = chkMesh.IsChecked
   file_path = os.path.dirname(os.path.realpath(__file__))
   script_path= os.path.join(file_path, 'JointCreator_Code.py')
   apex_sdk.runScriptFunction(file=script_path, function="buildEdgeJoint", args=dictionary)
   
   
   
   
   
