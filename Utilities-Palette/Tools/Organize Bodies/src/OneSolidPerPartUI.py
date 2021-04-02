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
   my_toolProperty.TitleText = "  Organize part structure"
   my_toolProperty.WorkFlowInstructions = '''
   <html><body>
   <p><span style="color: #999999;">This tool is used to organize bodies in the model structure.</span></p>
<p></p>
<p><span style="color: #999999;">For welding simulations, it is recommended to have one body per part in the model structure so a part has only one mesh assigned to it.</span></p>
<p></p>
<p><span style="color: #999999;">This is necessary to export bodies/meshes in separate files, so when creating a model in Simufact Welding each mesh will be a separate component.</span></p>
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
   
   # Create checkbox to extend the weld bead
   global useSolidName
   useSolidName = WPFControls.CheckBox()
   useSolidName.Content = "Use solid body name for part"
   useSolidName.Height = 20
   WPFControls.Grid.SetRow(useSolidName, 1)
   WPFControls.Grid.SetColumn(useSolidName, 1)
   useSolidName.IsChecked = System.Nullable[System.Boolean](True)
   #WPFControls.Grid.SetColumnSpan(useSolidName, 2)
   
   #Create a button and set it's text to "Import"
   #Assign it to Row1, Column 0
   doOrganize = WPFControls.Button()
   doOrganize.Content="One solid per part"
   WPFControls.Grid.SetRow(doOrganize, 2)
   WPFControls.Grid.SetColumn(doOrganize, 0)
   doOrganize.Height = 30
   
   #Link a function to the Button "Click" event 
   #This function will be called every time the Button is clicked
   doOrganize.Click+=HandlecleanBtn
   
   # Add the controls to the Grid
   my_Grid.Children.Add(useSolidName)
   my_Grid.Children.Add(doOrganize)
   
   #Return the Grid
   return my_Grid
   
   
#Function to handle the Import Button "Click" event
#This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandlecleanBtn(sender,args):
   if useSolidName.IsChecked == True:
      dictionary["useSolidName"] = True
   else:
      dictionary["useSolidName"] = False
   file_path = os.path.dirname(os.path.realpath(__file__))
   script_path= os.path.join(file_path, 'OneSolidPerPart.py')
   apex_sdk.runScriptFunction(file=script_path, function="OrganizeSolids", args=dictionary)
    

            
            
            
            
            
            
            
            
            
            
            
            
            
            