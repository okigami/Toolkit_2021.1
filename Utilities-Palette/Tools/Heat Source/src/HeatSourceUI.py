import sys
import os
import apex_sdk
import clr

from math import sqrt


#.NET references
import System
from System import Environment
from System.Windows import MessageBox
import System.Windows.Controls as WPFControls
from System.Windows.Automation import AutomationProperties
from Microsoft.Win32 import OpenFileDialog
from Microsoft.Win32 import SaveFileDialog

dictionary = {}

#setting pre-defined properties of tool_propertyContainer
def getUIContent():

   my_toolProperty = apex_sdk.ToolPropertyContainer()
   my_toolProperty.ToolPropertyContent = getCustomToolPropertyContent()
   my_toolProperty.TitleText = "  Heat source calculator"
   my_toolProperty.WorkFlowInstructions = '''
   <html><body>
   
   <p><strong><span style="color: #999999;">Heat source generator (arc)</span></strong></p>
<p><br /><span style="color: #999999;">This tool is used to estimate and generate heat source configurations for Simufact Welding. Please consider the estimated parameters as an initial guess.</span></p>
<p></p>
<ul>
<li><span style="color: #999999;"><span style="color: #00ccff;">Travel speed (cm/min)</span>: this value represents the (average) velocity of the torch or whatever device is carrying the heat source.</span></li>
<li><span style="color: #999999;"><span style="color: #00ccff;">Current (amps)</span>: amount of electrical current imparted by the power source.</span></li>
<li><span style="color: #999999;"><span style="color: #00ccff;">Voltage (volts)</span>: amount of electrical voltage imparted by the power source.</span></li>
<li><span style="color: #999999;"><span style="color: #00ccff;">Efficiency</span>: parameter utilized for correlating the nominal values from the power source with the actual heat output at the tip of the torch/wire.</span></li>
</ul>
<p></p>
<p><span style="color: #999999;">Current and voltage values do not influence the resulting values independently. They are used by multiplying the travel speed to get the energy-per-length parameter. </span><span style="color: #999999;">Once input is correct and estimated bead size is matching the expected, click the export button to generate a separate file. </span><span style="color: #999999;"></span><span style="color: #999999;">This file can be used directly in a Simufact Welding simulation that uses the double ellipsoid model as heat source (arc welding).</span></p>
<p><span style="color: #999999;"></span></p>
<p><span style="color: #999999;">For support: <span style="color: #ff0000;"><a href="mailto:support.americas@simufact.com">support.americas@simufact.com</a></span></span></p>
<p><span style="color: #999999;"><span style="color: #ff0000;"></span></span></p>


   </body></html>'''
  
   return my_toolProperty

#get tool property content
def getCustomToolPropertyContent():
   #Create a Grid
   my_Grid = WPFControls.Grid()
   
   fontSize = 11
   
   #Add Rows and Columns
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
   my_Grid.RowDefinitions.Add(WPFControls.RowDefinition())
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
   my_Grid.ColumnDefinitions.Add(WPFControls.ColumnDefinition())
   
   
   
   #Create a text label for travel speed
   travelSpeedText = WPFControls.TextBlock()
   travelSpeedText.Text = "Travel speed (cm/min):"
   WPFControls.Grid.SetRow(travelSpeedText, 1)
   WPFControls.Grid.SetColumn(travelSpeedText, 0)
   
   #Create an empty input for travel speed
   global travelSpeedInput
   travelSpeedInput = WPFControls.TextBox()
   travelSpeedInput.Text = "45"
   WPFControls.Grid.SetRow(travelSpeedInput, 1)
   WPFControls.Grid.SetColumn(travelSpeedInput, 1)
   travelSpeedInput.TextChanged += HandelTextChange
   
   
   
   
   
   #Create a text label for electrical current
   elecCurrentText = WPFControls.TextBlock()
   elecCurrentText.Text = "Current (A):"
   WPFControls.Grid.SetRow(elecCurrentText, 2)
   WPFControls.Grid.SetColumn(elecCurrentText, 0)
   
   #Create an empty input for electrical current
   global elecCurrentInput
   elecCurrentInput = WPFControls.TextBox()
   elecCurrentInput.Text = "150"
   WPFControls.Grid.SetRow(elecCurrentInput, 2)
   WPFControls.Grid.SetColumn(elecCurrentInput, 1)
   elecCurrentInput.TextChanged += HandelTextChange
   
   
   
   #Create a text label for voltage
   elecVoltageText = WPFControls.TextBlock()
   elecVoltageText.Text = "Voltage (V):"
   WPFControls.Grid.SetRow(elecVoltageText, 3)
   WPFControls.Grid.SetColumn(elecVoltageText, 0)
   
   #Create an empty input for voltage
   global elecVoltageInput
   elecVoltageInput = WPFControls.TextBox()
   elecVoltageInput.Text = "17"
   WPFControls.Grid.SetRow(elecVoltageInput, 3)
   WPFControls.Grid.SetColumn(elecVoltageInput, 1)
   elecVoltageInput.TextChanged += HandelTextChange
   
   
   
   #Create a text label for efficiency
   effParam = WPFControls.TextBlock()
   effParam.Text = "Efficiency:"
   WPFControls.Grid.SetRow(effParam, 4)
   WPFControls.Grid.SetColumn(effParam, 0)
   
   #Create an empty input for efficiency
   global effParamInput
   effParamInput = WPFControls.TextBox()
   effParamInput.Text = "0.85"
   WPFControls.Grid.SetRow(effParamInput, 4)
   WPFControls.Grid.SetColumn(effParamInput, 1)
   effParamInput.TextChanged += HandelTextChange

   
   
   #Create an empty separator
   Separator04 = WPFControls.TextBlock()
   Separator04.Text = ""
   #Separator04.HorizontalAlignment = 1
   WPFControls.Grid.SetRow(Separator04, 5)
   WPFControls.Grid.SetColumn(Separator04, 0)
   WPFControls.Grid.SetColumnSpan(Separator04, 2)
   
   
   
   #Create a text separator
   Separator01 = WPFControls.TextBlock()
   Separator01.Text = "Weld bead information"
   Separator01.FontSize = fontSize
   WPFControls.Grid.SetRow(Separator01, 6)
   WPFControls.Grid.SetColumn(Separator01, 0)
   WPFControls.Grid.SetColumnSpan(Separator01, 2)
   
   
   
    

   #Create a text label for energy per length
   EPLLabel = WPFControls.TextBlock()
   EPLLabel.Text = "   Energy per length:"
   EPLLabel.FontSize = fontSize
   WPFControls.Grid.SetRow(EPLLabel, 7)
   WPFControls.Grid.SetColumn(EPLLabel, 0)

   #Create a text label for energy per length
   global EPLEstimate
   EPLEstimate = WPFControls.TextBlock()
   EPLEstimate.FontSize = fontSize
   EPLEstimate.Text = "-"
   WPFControls.Grid.SetRow(EPLEstimate, 7)
   WPFControls.Grid.SetColumn(EPLEstimate, 1)



   #Create a text label for estimated bead leg
   BeadLegLabel = WPFControls.TextBlock()
   BeadLegLabel.Text = "   Estimated bead leg:"
   BeadLegLabel.FontSize = fontSize
   WPFControls.Grid.SetRow(BeadLegLabel, 8)
   WPFControls.Grid.SetColumn(BeadLegLabel, 0)

   #Create a text label for estimated bead leg
   global BeadLegEstimate
   BeadLegEstimate = WPFControls.TextBlock()
   BeadLegEstimate.Text = "-"
   BeadLegEstimate.FontSize = fontSize
   WPFControls.Grid.SetRow(BeadLegEstimate, 8)
   WPFControls.Grid.SetColumn(BeadLegEstimate, 1)

   
   
   #Create an empty separator
   Separator03 = WPFControls.TextBlock()
   Separator03.Text = ""
   WPFControls.Grid.SetRow(Separator03, 9)
   WPFControls.Grid.SetColumn(Separator03, 0)
   WPFControls.Grid.SetColumnSpan(Separator03, 2)
   
   
   
   #Create a text separator
   Separator02 = WPFControls.TextBlock()
   Separator02.Text = "Heat source size information"
   Separator02.FontSize = 12
   #Separator02.HorizontalAlignment = 1
   WPFControls.Grid.SetRow(Separator02, 10)
   WPFControls.Grid.SetColumn(Separator02, 0)
   WPFControls.Grid.SetColumnSpan(Separator02, 2)
   
  
  
  

   #Create a text label for front length heat source size
   FLLabel = WPFControls.TextBlock()
   FLLabel.Text = "   Front (mm):"
   FLLabel.FontSize = fontSize
   WPFControls.Grid.SetRow(FLLabel, 11)
   WPFControls.Grid.SetColumn(FLLabel, 0)

   #Create a text label for front length heat source size
   global FLEstimate
   FLEstimate = WPFControls.TextBlock()
   FLEstimate.Text = "-"
   FLEstimate.FontSize = fontSize
   WPFControls.Grid.SetRow(FLEstimate, 11)
   WPFControls.Grid.SetColumn(FLEstimate, 1)
   
   
   #Create a text label for rear length heat source size
   RLLabel = WPFControls.TextBlock()
   RLLabel.Text = "   Rear (mm):"
   RLLabel.FontSize = fontSize
   WPFControls.Grid.SetRow(RLLabel, 12)
   WPFControls.Grid.SetColumn(RLLabel, 0)

   #Create a text label for rear length heat source size
   global RLEstimate
   RLEstimate = WPFControls.TextBlock()
   RLEstimate.Text = "-"
   RLEstimate.FontSize = fontSize
   WPFControls.Grid.SetRow(RLEstimate, 12)
   WPFControls.Grid.SetColumn(RLEstimate, 1)   
   

   #Create a text label for width length heat source size
   WidthLabel = WPFControls.TextBlock()
   WidthLabel.Text = "   Width (mm):"
   WidthLabel.FontSize = fontSize
   WPFControls.Grid.SetRow(WidthLabel, 13)
   WPFControls.Grid.SetColumn(WidthLabel, 0)

   #Create a text label for width length heat source sizeer
   global WidthEstimate
   WidthEstimate = WPFControls.TextBlock()
   WidthEstimate.Text = "-"
   WidthEstimate.FontSize = fontSize
   WPFControls.Grid.SetRow(WidthEstimate, 13)
   WPFControls.Grid.SetColumn(WidthEstimate, 1)   


   #Create a text label for depth length heat source size
   DepthLabel = WPFControls.TextBlock()
   DepthLabel.Text = "   Depth (mm):"
   DepthLabel.FontSize = fontSize
   WPFControls.Grid.SetRow(DepthLabel, 14)
   WPFControls.Grid.SetColumn(DepthLabel, 0)

   #Create a text label for the refinement diameter
   global DepthEstimate
   DepthEstimate = WPFControls.TextBlock()
   DepthEstimate.Text = "-"
   DepthEstimate.FontSize = fontSize
   WPFControls.Grid.SetRow(DepthEstimate, 14)
   WPFControls.Grid.SetColumn(DepthEstimate, 1)      

   
   #Create an empty separator
   Separator05 = WPFControls.TextBlock()
   Separator05.Text = ""
   #Separator05.HorizontalAlignment = 1
   WPFControls.Grid.SetRow(Separator05, 15)
   WPFControls.Grid.SetColumn(Separator05, 0)
   WPFControls.Grid.SetColumnSpan(Separator05, 2)
      
   
   

   #Create a button to export the heat source in Simufact format
   exportHeatSource = WPFControls.Button()
   exportHeatSource.Content="Export heat source"
   exportHeatSource.Height = 30
   WPFControls.Grid.SetRow(exportHeatSource, 16)
   WPFControls.Grid.SetColumn(exportHeatSource, 0)
   WPFControls.Grid.SetColumnSpan(exportHeatSource, 2)
   #Link a function to the Button "Click" event 
   exportHeatSource.Click += HandleExportHeatSource
   
   
   # Add the controls to the Grid
   my_Grid.Children.Add(exportHeatSource)
   my_Grid.Children.Add(elecVoltageText)
   my_Grid.Children.Add(elecVoltageInput)
   my_Grid.Children.Add(travelSpeedText)
   my_Grid.Children.Add(travelSpeedInput)
   my_Grid.Children.Add(elecCurrentText)
   my_Grid.Children.Add(elecCurrentInput)
   my_Grid.Children.Add(effParam)
   my_Grid.Children.Add(effParamInput)
   my_Grid.Children.Add(EPLLabel)
   my_Grid.Children.Add(EPLEstimate)
   my_Grid.Children.Add(BeadLegLabel)
   my_Grid.Children.Add(BeadLegEstimate)
   my_Grid.Children.Add(FLLabel)
   my_Grid.Children.Add(FLEstimate)
   my_Grid.Children.Add(RLLabel)
   my_Grid.Children.Add(RLEstimate)
   my_Grid.Children.Add(WidthLabel)
   my_Grid.Children.Add(WidthEstimate)
   my_Grid.Children.Add(DepthLabel)
   my_Grid.Children.Add(DepthEstimate)
   my_Grid.Children.Add(Separator01)
   my_Grid.Children.Add(Separator02)
   my_Grid.Children.Add(Separator03)
   my_Grid.Children.Add(Separator04)
   my_Grid.Children.Add(Separator05)

   #Return the Grid
   return my_Grid
   
#Function to handle the Import Button "Click" event
#This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandelTextChange(sender,args):
    try:
        ans = float(effParamInput.Text)
        try: 
            ans = float(elecCurrentInput.Text)
            try:
                ans = float(elecVoltageInput.Text)
                try:
                    ans = float(travelSpeedInput.Text)
                    try:
                        EPLEstimate.Text = " {0} kJ/cm".format(round(0.06*float(effParamInput.Text)*float(elecCurrentInput.Text)*float(elecVoltageInput.Text)/float(travelSpeedInput.Text), 2))
                        BeadLeg = round(sqrt(0.06* float(effParamInput.Text) * float(elecVoltageInput.Text) * float(elecCurrentInput.Text)/( float(travelSpeedInput.Text)/2.54)/500)*25.4, 2)
                        BeadLegEstimate.Text = " {0} mm".format(BeadLeg)
                        Throat = round((BeadLeg ** 2)/sqrt(2*(BeadLeg ** 2)), 1)
                        FrontVal = round(0.6 * (1.5 + Throat), 1)
                        RearVal = round(FrontVal*3, 1)
                        WidthVal = round(1.2 * (Throat), 1)
                        DepthVal = round(1.2 * BeadLeg, 1)
                        
                        FLEstimate.Text = str(FrontVal)
                        RLEstimate.Text = str(RearVal)
                        WidthEstimate.Text = str(WidthVal)
                        DepthEstimate.Text = str(DepthVal)
                        
                    except:
                        pass
                except:
                    pass
            except:
                pass
        except:
            pass                
    except:
        pass

        
@apex_sdk.errorhandler
def HandleExportHeatSource(sender, args):
    NewFileLocation = r"C:\Users"
    
    dialog = SaveFileDialog()
    dialog.Title = "Export heat source"
   
    dialog.FileName = "{0}cm-min_{1}A_{2}V.xml".format(travelSpeedInput.Text, elecCurrentInput.Text, elecVoltageInput.Text)
    dialog.Filter = "XML Files|*.xml"
    dialog.InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
    
    if dialog.ShowDialog():
        NewFileLocation = dialog.FileName
        file_path = os.path.dirname(os.path.realpath(__file__))
        HeatSourceFile = os.path.join(file_path, 'Heat-source.xml')
        with open(NewFileLocation, 'w') as NewHeatSource:
            with open(HeatSourceFile, 'r') as Template:
                for line in Template:
                    if "<comment>" in line:
                        line = "<comment>{0}</comment>".format("Generated by MSC Apex welding toolkit")
                    if "<velocity dimension=" in line:
                        line = '<velocity dimension="7" unit="8">{0}</velocity>'.format(travelSpeedInput.Text)
                    if "<voltage dimension=" in line:
                        line = '<voltage dimension="20" unit="0">{0}</voltage>'.format(elecVoltageInput.Text)
                    if "<current dimension=" in line:
                        line = '<current dimension="2" unit="0">{0}</current>'.format(elecCurrentInput.Text)
                    if "<efficiency>" in line:
                        line = '<efficiency>{0}</efficiency>'.format(effParamInput.Text)
                    if "<front_length" in line:
                        line = '<front_length dimension="5" unit="2" value="{0}"/>'.format(FLEstimate.Text)
                    if '<rear_length' in line:
                        line = '<rear_length dimension="5" unit="2" value="{0}"/>'.format(RLEstimate.Text)
                    if '<width dimension'in line:
                        line = '<width dimension="5" unit="2" value="{0}"/>'.format(WidthEstimate.Text)
                    if '<depth dimension' in line:
                        line = '<depth dimension="5" unit="2" value="{0}"/>'.format(DepthEstimate.Text)
                    NewHeatSource.write(line)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    