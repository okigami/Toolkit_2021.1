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
   my_toolProperty.TitleText = "  Heat source calculator (bead)"
   my_toolProperty.WorkFlowInstructions = '''<html><body>
   
   <p><strong><span style="color: #999999;">Heat source generator (bead)</span></strong></p>
<p><br /><span style="color: #999999;">This tool is used to estimate and generate heat source configurations for Simufact Welding. Please consider the estimated parameters as an initial guess.</span></p>
<p></p>
<ul>
<li><span style="color: #999999;"><span style="color: #00ccff;">Leg length (mm)</span>: expected/desired weld bead leg length<br /></span></li>
<li><span style="color: #999999;"><span style="color: #00ccff;">Travel speed (cm/min)</span>: this value represents the (average) velocity of the torch or whatever device is carrying the heat source.</span><span style="color: #999999;"><span style="color: #00ccff;"></span></span></li>
<li><span style="color: #999999;"><span style="color: #00ccff;">Efficiency</span>: parameter utilized for correlating the nominal values from the power source with the actual heat output at the tip of the torch/wire.</span></li>
</ul>
<p></p>
<p><span style="color: #999999;">This version of the heat source generator does a backward calculation based on desired bead leg. The input power required to produce the specified leg length combined with travel speed and efficiency is then estimated</span><span style="color: #999999;">. </span><span style="color: #999999;"></span><span style="color: #999999;">The output file can be used directly in a Simufact Welding simulation that uses the double ellipsoid model as heat source (arc welding).</span></p>
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
   
   
   currLine = 0
   
    #Create a text label for electrical current
   currLine += 1
   beadSizeText = WPFControls.TextBlock()
   beadSizeText.Text = "Leg length (mm):"
   WPFControls.Grid.SetRow(beadSizeText, currLine)
   WPFControls.Grid.SetColumn(beadSizeText, 0)
   
   #Create an empty input for electrical current
   global beadSizeInput
   beadSizeInput = WPFControls.TextBox()
   beadSizeInput.Text = "3.1"
   WPFControls.Grid.SetRow(beadSizeInput, currLine)
   WPFControls.Grid.SetColumn(beadSizeInput, 1)
   beadSizeInput.TextChanged += HandelTextChange  


   #Create a text label for travel speed
   currLine += 1
   travelSpeedText = WPFControls.TextBlock()
   travelSpeedText.Text = "Travel speed (cm/min):"
   WPFControls.Grid.SetRow(travelSpeedText, currLine)
   WPFControls.Grid.SetColumn(travelSpeedText, 0)
   
   #Create an empty input for travel speed
   global travelSpeedInput
   travelSpeedInput = WPFControls.TextBox()
   travelSpeedInput.Text = "45"
   WPFControls.Grid.SetRow(travelSpeedInput, currLine)
   WPFControls.Grid.SetColumn(travelSpeedInput, 1)
   travelSpeedInput.TextChanged += HandelTextChange
    
   
   #Create a text label for efficiency
   currLine += 1
   effParam = WPFControls.TextBlock()
   effParam.Text = "Efficiency:"
   WPFControls.Grid.SetRow(effParam, currLine)
   WPFControls.Grid.SetColumn(effParam, 0)
   
   #Create an empty input for efficiency
   global effParamInput
   effParamInput = WPFControls.TextBox()
   effParamInput.Text = "0.80"
   WPFControls.Grid.SetRow(effParamInput, currLine)
   WPFControls.Grid.SetColumn(effParamInput, 1)
   effParamInput.TextChanged += HandelTextChange
   
   #Create an empty separator
   currLine += 1
   Separator04 = WPFControls.TextBlock()
   Separator04.Text = ""
   #Separator04.HorizontalAlignment = 1
   WPFControls.Grid.SetRow(Separator04, currLine)
   WPFControls.Grid.SetColumn(Separator04, 0)
   WPFControls.Grid.SetColumnSpan(Separator04, 2)
   
   
   #Create a text separator
   currLine += 1
   Separator01 = WPFControls.TextBlock()
   Separator01.Text = "Configuration:"
   Separator01.FontSize = fontSize
   WPFControls.Grid.SetRow(Separator01, currLine)
   WPFControls.Grid.SetColumn(Separator01, 0)
   WPFControls.Grid.SetColumnSpan(Separator01, 2)
   
   
   #Create a text label for energy per length
   currLine += 1
   ReqPowerLbl = WPFControls.TextBlock()
   ReqPowerLbl.Text = "   Req. power input:"
   ReqPowerLbl.FontSize = fontSize
   WPFControls.Grid.SetRow(ReqPowerLbl, currLine)
   WPFControls.Grid.SetColumn(ReqPowerLbl, 0)

   #Create a text label for energy per length
   global ReqPowerText
   ReqPowerText = WPFControls.TextBlock()
   ReqPowerText.FontSize = fontSize
   ReqPowerText.Text = "-"
   WPFControls.Grid.SetRow(ReqPowerText, currLine)
   WPFControls.Grid.SetColumn(ReqPowerText, 1)



   #Create a text label for estimated bead leg
   currLine += 1
   EstThroatLbl = WPFControls.TextBlock()
   EstThroatLbl.Text = "   Estimated throat:"
   EstThroatLbl.FontSize = fontSize
   WPFControls.Grid.SetRow(EstThroatLbl, currLine)
   WPFControls.Grid.SetColumn(EstThroatLbl, 0)

   #Create a text label for estimated bead leg
   global EstThroatText
   EstThroatText = WPFControls.TextBlock()
   EstThroatText.Text = "-"
   EstThroatText.FontSize = fontSize
   WPFControls.Grid.SetRow(EstThroatText, currLine)
   WPFControls.Grid.SetColumn(EstThroatText, 1)

   
   
   #Create an empty separator
   currLine += 1
   Separator03 = WPFControls.TextBlock()
   Separator03.Text = ""
   WPFControls.Grid.SetRow(Separator03, currLine)
   WPFControls.Grid.SetColumn(Separator03, 0)
   WPFControls.Grid.SetColumnSpan(Separator03, 2)
   
   
   
   #Create a text separator
   currLine += 1
   Separator02 = WPFControls.TextBlock()
   Separator02.Text = "Heat source size information"
   Separator02.FontSize = 12
   #Separator02.HorizontalAlignment = 1
   WPFControls.Grid.SetRow(Separator02, currLine)
   WPFControls.Grid.SetColumn(Separator02, 0)
   WPFControls.Grid.SetColumnSpan(Separator02, 2)
   

   #Create a text label for front length heat source size
   currLine += 1
   FLLabel = WPFControls.TextBlock()
   FLLabel.Text = "   Front:"
   FLLabel.FontSize = fontSize
   WPFControls.Grid.SetRow(FLLabel, currLine)
   WPFControls.Grid.SetColumn(FLLabel, 0)

   #Create a text label for front length heat source size
   global FLEstimate
   FLEstimate = WPFControls.TextBlock()
   FLEstimate.Text = "-"
   FLEstimate.FontSize = fontSize
   WPFControls.Grid.SetRow(FLEstimate, currLine)
   WPFControls.Grid.SetColumn(FLEstimate, 1)
   
   
   #Create a text label for rear length heat source size
   currLine += 1
   RLLabel = WPFControls.TextBlock()
   RLLabel.Text = "   Rear:"
   RLLabel.FontSize = fontSize
   WPFControls.Grid.SetRow(RLLabel, currLine)
   WPFControls.Grid.SetColumn(RLLabel, 0)

   #Create a text label for rear length heat source size
   global RLEstimate
   RLEstimate = WPFControls.TextBlock()
   RLEstimate.Text = "-"
   RLEstimate.FontSize = fontSize
   WPFControls.Grid.SetRow(RLEstimate, currLine)
   WPFControls.Grid.SetColumn(RLEstimate, 1)   
   

   #Create a text label for width length heat source size
   currLine += 1
   WidthLabel = WPFControls.TextBlock()
   WidthLabel.Text = "   Width:"
   WidthLabel.FontSize = fontSize
   WPFControls.Grid.SetRow(WidthLabel, currLine)
   WPFControls.Grid.SetColumn(WidthLabel, 0)

   #Create a text label for width length heat source sizeer
   global WidthEstimate
   WidthEstimate = WPFControls.TextBlock()
   WidthEstimate.Text = "-"
   WidthEstimate.FontSize = fontSize
   WPFControls.Grid.SetRow(WidthEstimate, currLine)
   WPFControls.Grid.SetColumn(WidthEstimate, 1)   


   #Create a text label for depth length heat source size
   currLine += 1
   DepthLabel = WPFControls.TextBlock()
   DepthLabel.Text = "   Depth:"
   DepthLabel.FontSize = fontSize
   WPFControls.Grid.SetRow(DepthLabel, currLine)
   WPFControls.Grid.SetColumn(DepthLabel, 0)

   #Create a text label for the refinement diameter
   global DepthEstimate
   DepthEstimate = WPFControls.TextBlock()
   DepthEstimate.Text = "-"
   DepthEstimate.FontSize = fontSize
   WPFControls.Grid.SetRow(DepthEstimate, currLine)
   WPFControls.Grid.SetColumn(DepthEstimate, 1)      

   
   #Create an empty separator
   currLine += 1
   Separator05 = WPFControls.TextBlock()
   Separator05.Text = ""
   #Separator05.HorizontalAlignment = 1
   WPFControls.Grid.SetRow(Separator05, currLine)
   WPFControls.Grid.SetColumn(Separator05, 0)
   WPFControls.Grid.SetColumnSpan(Separator05, 2)
      
   
   #Create a button to export the heat source in Simufact format
   currLine += 1
   exportHeatSource = WPFControls.Button()
   exportHeatSource.Content="Export heat source"
   exportHeatSource.Height = 30
   WPFControls.Grid.SetRow(exportHeatSource, currLine)
   WPFControls.Grid.SetColumn(exportHeatSource, 0)
   WPFControls.Grid.SetColumnSpan(exportHeatSource, 2)
   #Link a function to the Button "Click" event 
   exportHeatSource.Click += HandleExportHeatSource
   
   
   # Add the controls to the Grid
   my_Grid.Children.Add(beadSizeText)
   my_Grid.Children.Add(beadSizeInput)
   my_Grid.Children.Add(travelSpeedText)
   my_Grid.Children.Add(travelSpeedInput)
   my_Grid.Children.Add(effParam)
   my_Grid.Children.Add(effParamInput)
   my_Grid.Children.Add(ReqPowerLbl)
   my_Grid.Children.Add(ReqPowerText)
   my_Grid.Children.Add(EstThroatLbl)
   my_Grid.Children.Add(EstThroatText)
   
   # Heat source
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
   my_Grid.Children.Add(exportHeatSource)

   #Return the Grid
   return my_Grid
   
#Function to handle the Import Button "Click" event
#This function gets called every time the Button is clicked
@apex_sdk.errorhandler
def HandelTextChange(sender,args):
    try:
        ans = float(effParamInput.Text)
        try: 
            ans = float(beadSizeInput.Text)
            try:
                ans = float(travelSpeedInput.Text)
                try:
                    BeadLeg = float(beadSizeInput.Text)
                    TravelSpeed = float(travelSpeedInput.Text)
                    Efficiency = float(effParamInput.Text)
                    ReqPower = int((BeadLeg/25.4)**2 * (TravelSpeed*500)/(Efficiency*2.54*0.06))
                    ReqPowerText.Text = str(ReqPower) + " kJ/cm"

                    Throat = round((BeadLeg ** 2)/sqrt(2*(BeadLeg ** 2)), 1)
                    EstThroatText.Text = str(Throat) + " mm"

                    FrontVal = round(0.6 * (1.5 + Throat), 1)
                    RearVal = round(FrontVal*3, 1)
                    WidthVal = round(1.2 * (Throat), 1)
                    DepthVal = round(1.2 * BeadLeg, 1)
                    
                    FLEstimate.Text = str(FrontVal) + " mm"
                    RLEstimate.Text = str(RearVal) + " mm"
                    WidthEstimate.Text = str(WidthVal) + " mm"
                    DepthEstimate.Text = str(DepthVal) + " mm"
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
   
    dialog.FileName = "{0}mm_{1}cm-min.xml".format(beadSizeInput.Text.replace('.', ','), travelSpeedInput.Text.replace('.', ','))
    dialog.Filter = "XML Files|*.xml"
    dialog.InitialDirectory = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments)
    
    if dialog.ShowDialog():
        NewFileLocation = dialog.FileName
        file_path = os.path.dirname(os.path.realpath(__file__))
        HeatSourceFile = os.path.join(file_path, 'Heat-source_Power.xml')

        RequiredPower,_ = ReqPowerText.Text.split(' kJ')
        FrontLength,_ = FLEstimate.Text.split(' mm')
        RearLength,_ = RLEstimate.Text.split(' mm')
        WidthLength,_ = WidthEstimate.Text.split(' mm')
        DepthLength,_ = DepthEstimate.Text.split(' mm')

        with open(NewFileLocation, 'w') as NewHeatSource:
            with open(HeatSourceFile, 'r') as Template:
                for line in Template:
                    if "<comment>" in line:
                        line = "<comment>{0}</comment>".format("Generated by MSC Apex welding toolkit")
                    if "<velocity dimension=" in line:
                        line = '<velocity dimension="7" unit="8">{0}</velocity>'.format(travelSpeedInput.Text)
                    if "<power dimension=" in line:
                        line = '<power dimension="12" unit="0">{0}</power>'.format(RequiredPower)
                    if "<efficiency>" in line:
                        line = '<efficiency>{0}</efficiency>'.format(effParamInput.Text)
                    if "<front_length" in line:
                        line = '<front_length dimension="5" unit="2" value="{0}"/>'.format(FrontLength)
                    if '<rear_length' in line:
                        line = '<rear_length dimension="5" unit="2" value="{0}"/>'.format(RearLength)
                    if '<width dimension'in line:
                        line = '<width dimension="5" unit="2" value="{0}"/>'.format(WidthLength)
                    if '<depth dimension' in line:
                        line = '<depth dimension="5" unit="2" value="{0}"/>'.format(DepthLength)
                    NewHeatSource.write(line)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    