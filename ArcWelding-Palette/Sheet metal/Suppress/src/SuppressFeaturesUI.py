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
   my_toolProperty.TitleText = "  Suppress features"
   my_toolProperty.WorkFlowInstructions = '''
   <p><span style="color: #a9a9a9;">Operation: Click the </span><span style="color: #00ffff;">Suppress vertices </span><span style="color: #a9a9a9;">button to suppress all visible vertices of surfaces.</span></p>
   <p><span style="color: #a9a9a9;">Operation: Click the </span><span style="color: #00ffff;">Suppress edges </span><span style="color: #a9a9a9;">button to suppress all visible edges of surfaces.</span></p>
   <p><span style="color: #a9a9a9;">Operation: Click the </span><span style="color: #00ffff;">Suppress all </span><span style="color: #a9a9a9;">button to suppress all visible vertices and edges of surfaces.</span></p>
   <ul>
   <li><span style="color: #a9a9a9;">This tool is used to simplify the geometrical representation by suppressing edges and vertices.</span></li>
   <li><span style="color: #a9a9a9;">Sometimes, this simplification is needed to avoid big discrepancies between small and big faces.</span></li>
   <li><span style="color: #a9a9a9;">It will not perform any defeaturing on the part/surface. For that use the </span><span style="color: #add8e6;">Apex Defeature</span><span style="color: #a9a9a9;">&nbsp; tool instead under the </span><span style="color: #ee82ee;">Geometry Edit Tools</span><span style="color: #a9a9a9;">&nbsp; palette.</span></li>
   </ul>
   <p><span style="color: #999999;">For support: <span style="color: #ff0000;"><a href="mailto:support.americas@simufact.com">support.americas@simufact.com</a></span></span></p>
   
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
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
   
   
   #Create a button to suppress all vertices only
   cleanVertices = WPFControls.Button()
   cleanVertices.Content="Suppress vertices"
   WPFControls.Grid.SetRow(cleanVertices, 0)
   WPFControls.Grid.SetColumn(cleanVertices, 0)
   cleanVertices.Height = 30
   cleanVertices.Click+=HandleCleanVertices
   
   
   #Create a button to suppress all edges only
   cleanEdges = WPFControls.Button()
   cleanEdges.Content="Suppress edges"
   WPFControls.Grid.SetRow(cleanEdges, 0)
   WPFControls.Grid.SetColumn(cleanEdges, 1)
   cleanEdges.Height = 30
   cleanEdges.Click+=HandleCleanEdges
   
   
   
   #Create a button to suppress all vertices and edges
   cleanAll = WPFControls.Button()
   cleanAll.Content="Suppress all"
   WPFControls.Grid.SetRow(cleanAll, 1)
   WPFControls.Grid.SetColumn(cleanAll, 0)
   cleanAll.Click+=HandleCleanAll
   cleanAll.Height = 30
   WPFControls.Grid.SetColumnSpan(cleanAll, 2)
   
   
   # Add the controls to the Grid
   my_Grid.Children.Add(cleanAll)
   my_Grid.Children.Add(cleanEdges)
   my_Grid.Children.Add(cleanVertices)
   
   #Return the Grid
   return my_Grid
   

@apex_sdk.errorhandler
def HandleCleanAll(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'SuppressFeatures.py')
    apex_sdk.runScriptFunction(file=script_path, function="SuppressFeatures", args=dictionary)
    #apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\SuppressFeatures.py", "SuppressFeatures", dictionary)

@apex_sdk.errorhandler
def HandleCleanVertices(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'SuppressVerticesOnly.py')
    apex_sdk.runScriptFunction(file=script_path, function="SuppressVertices", args=dictionary)
    #apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\SuppressVerticesOnly.py", "SuppressVertices", dictionary)   
   
@apex_sdk.errorhandler
def HandleCleanEdges(sender,args):
    file_path = os.path.dirname(os.path.realpath(__file__))
    script_path= os.path.join(file_path, 'SuppressEdgesOnly.py')
    apex_sdk.runScriptFunction(file=script_path, function="SuppressEdges", args=dictionary)
    #apex_sdk.runScriptFunction(r"D:\Personal\00-Okigami\04.2-ApexAutoARC\00-Modularized-IL\SuppressEdgesOnly.py", "SuppressEdges", dictionary)   
   
   
   
   
   
   
   
   
   
 