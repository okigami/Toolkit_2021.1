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
   my_toolProperty.TitleText = "  Extract and map midsurface"
   my_toolProperty.WorkFlowInstructions = '''
   <p><span style="color: #a9a9a9;">Operation: Click the </span><span style="color: #40e0d0;">Extract and annotate thickness </span><span style="color: #a9a9a9;"> button</span></p>
   <ul>
   <li><span style="color: #a9a9a9;">This tool is used to extract the midsurface of single-thickness parts.</span></li>
   <li><span style="color: #a9a9a9;">By extracting the midsurface, the user has more flexibility to control the mesh in a 2D format.</span></li>
   <li><span style="color: #a9a9a9;">The midsurface is a surface object that is created under the same locaton as the originating solid.</span></li>
   <li><span style="color: #a9a9a9;">The thickness value will be annotated in the part name to be later referred to in </span><span style="color: #ff0000;">Simufact Welding</span><span style="color: #a9a9a9;">.</span></li>
   </ul>
   <p><span style="color: #a9a9a9;">2D meshes of components will be converted back to a 3D mesh when importing the file in </span><span style="color: #ff0000;">Simufact Welding </span><span style="color: #a9a9a9;"> by assigning a thickness and number of layers to it.</span></p>
   <p><span style="color: #a9a9a9;"></span></p>
   <p><span style="color: #999999;">For support: <span style="color: #ff0000;"><a href="mailto:support.americas@simufact.com">support.americas@simufact.com</a></span></span></p>
   
   '''


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
    # pickChoices.Add(apex_sdk.PickFilterTypes.Part)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Solid)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Surface)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Cell)
    # pickChoices.Add(apex_sdk.PickFilterTypes.Face)
    pickChoices.Add(apex_sdk.PickFilterTypes.Assembly)

    # Return the pick filter list
    return pickChoices




#get tool property content
def getCustomToolPropertyContent():
   #Create a Grid
   my_Grid = WPFControls.Grid()
   
   #Add 2 Rows and 1 Column
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   
   
   #Create a button and set it's text to "Import"
   #Assign it to Row1, Column 0
   cleanBtn = WPFControls.Button()
   cleanBtn.Content="Extract and annotate thickness"
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
    script_path= os.path.join(file_path, 'Midsurface.py')
    apex_sdk.runScriptFunction(file=script_path, function="Midsurface", args=dictionary)
    

    #apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\Midsurface.py", "Midsurface", dictionary)    

   
   
   
   
   
   
   
   
   
   
   
   
 