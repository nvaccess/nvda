# -*- coding: UTF-8 -*- 
#NVDAObjects/excel.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

# adding support for excel charts ticket 1987

import time
import ui
import eventHandler
import controlTypes
import excel 
from logHandler import log
from . import Window
import scriptHandler
import colors

from comtypes.client import *
import comtypes
from comtypes.automation import IDispatch
import ctypes
import comtypes.GUID

import math
from NVDAObjects import NVDAObject
import string
import weakref


#ChartEvents definition
class ChartEvents(IDispatch):
	_case_insensitive_ = True
	_iid_ = comtypes.GUID('{0002440F-0000-0000-C000-000000000046}')
	_idlflags_ = ['hidden']
	_methods_ = []
	_disp_methods_=[
		comtypes.DISPMETHOD([comtypes.dispid(235)], None, 'Select',
			( ['in'], ctypes.c_int, 'ElementID' ),
			( ['in'], ctypes.c_int, 'Arg1' ),
			( ['in'], ctypes.c_int, 'Arg2' )),
		]

# Chart types in Microsoft Excel.
xl3DArea = -4098
xl3DAreaStacked	= 78
xl3DAreaStacked100 = 79
xl3DBarClustered = 60
xl3DBarStacked = 61
xl3DBarStacked100 = 62
xl3DColumn = -4100
xl3DColumnClustered = 54
xl3DColumnStacked = 55
xl3DColumnStacked100 = 56
xl3DLine = -4101
xl3DPie = -4102
xl3DPieExploded = 70
xlArea = 1
xlAreaStacked = 76
xlAreaStacked100 = 77
xlBarClustered = 57
xlBarOfPie = 71
xlBarStacked = 58
xlBarStacked100 = 59
xlBubble = 15
xlBubble3DEffect = 87
xlColumnClustered = 51
xlColumnStacked = 52
xlColumnStacked100 = 53
xlConeBarClustered = 102
xlConeBarStacked = 103
xlConeBarStacked100 = 104
xlConeCol = 105
xlConeColClustered = 99
xlConeColStacked = 100
xlConeColStacked100 = 101
xlCylinderBarClustered = 95
xlCylinderBarStacked = 96
xlCylinderBarStacked100 = 97
xlCylinderCol = 98
xlCylinderColClustered = 92
xlCylinderColStacked = 93
xlCylinderColStacked100 = 94
xlDoughnut = -4120
xlDoughnutExploded = 80
xlLine = 4
xlLineMarkers = 65
xlLineMarkersStacked = 66
xlLineMarkersStacked100 = 67
xlLineStacked = 63
xlLineStacked100 = 64
xlPie = 5
xlPieExploded = 69
xlPieOfPie = 68
xlPyramidBarClustered = 109
xlPyramidBarStacked = 110
xlPyramidBarStacked100 = 111
xlPyramidCol = 112
xlPyramidColClustered = 106
xlPyramidColStacked = 107
xlPyramidColStacked100 = 108
xlRadar = -4151
xlRadarFilled = 82
xlRadarMarkers = 81
xlStockHLC = 88
xlStockOHLC = 89
xlStockVHLC = 90
xlStockVOHLC = 91
xlSurface = 83
xlSurfaceTopView = 85
xlSurfaceTopViewWireframe = 86
xlSurfaceWireframe = 84
xlXYScatter = -4169
xlXYScatterLines = 74
xlXYScatterLinesNoMarkers = 75
xlXYScatterSmooth = 72
xlXYScatterSmoothNoMarkers = 73

# Dictionary for the Description of chart types.
chartTypeDict = {
	# Translators: Chart type
	xl3DArea : _( "3D Area" ),
	# Translators: Chart type
	xl3DAreaStacked : _( "3D Stacked Area" ),
	# Translators: Chart type
	xl3DAreaStacked100 : _( "100 percent Stacked Area" ) ,
	# Translators: Chart type
	xl3DBarClustered : _( "3D Clustered Bar" ) ,
	# Translators: Chart type
	xl3DBarStacked : _( "3D Stacked Bar" ) ,
	# Translators: Chart type
	xl3DBarStacked100 : _( "3D 100 percent Stacked Bar" ) ,
	# Translators: Chart type
	xl3DColumn : _( "3D Column" ) ,
	# Translators: Chart type
	xl3DColumnClustered : _( "3D Clustered Column" ),
	# Translators: Chart type
	xl3DColumnStacked : _( "3D Stacked Column" ) ,
	# Translators: Chart type
	xl3DColumnStacked100 : _( "3D 100 percent Stacked Column" ) ,
	# Translators: Chart type
	xl3DLine : _( "3D Line" ) ,
	# Translators: Chart type
	xl3DPie : _( "3D Pie" ) ,
	# Translators: Chart type
	xl3DPieExploded : _( "Exploded 3D Pie" ) ,
	# Translators: Chart type
	xlArea : _( "Area" ) ,
	# Translators: Chart type
	xlAreaStacked : _( "Stacked Area" ) ,
	# Translators: Chart type
	xlAreaStacked100 : _( "100 percent Stacked Area" ) ,
	# Translators: Chart type
	xlBarClustered : _( "Clustered Bar" ) ,
	# Translators: Chart type
	xlBarOfPie : _( "Bar of Pie" ) ,
	# Translators: Chart type
	xlBarStacked : _( "Stacked Bar" ) ,
	# Translators: Chart type
	xlBarStacked100 : _( "100 percent Stacked Bar" ) ,
	# Translators: Chart type
	xlBubble : _( "Bubble" ) ,
	# Translators: Chart type
	xlBubble3DEffect : _( "Bubble with 3D effects" ) ,
	# Translators: Chart type
	xlColumnClustered : _( "Clustered Column" ) ,
	# Translators: Chart type
	xlColumnStacked : _( "Stacked Column" ) ,
	# Translators: Chart type
	xlColumnStacked100 : _( "100 percent Stacked Column" ) ,
	# Translators: Chart type
	xlConeBarClustered : _( "Clustered Cone Bar" ) ,
	# Translators: Chart type
	xlConeBarStacked : _( "Stacked Cone Bar" ) ,
	# Translators: Chart type
	xlConeBarStacked100 : _( "100 percent Stacked Cone Bar" ) ,
	# Translators: Chart type
	xlConeCol : _( "3D Cone Column" ) ,
	# Translators: Chart type
	xlConeColClustered : _( "Clustered Cone Column" ) ,
	# Translators: Chart type
	xlConeColStacked : _( "Stacked Cone Column" ),
	# Translators: Chart type
	xlConeColStacked100 : _( "100 percent Stacked Cone Column" ) ,
	# Translators: Chart type
	xlCylinderBarClustered : _( "Clustered Cylinder Bar" ) ,
	# Translators: Chart type
	xlCylinderBarStacked : _( "Stacked Cylinder Bar" ) ,
	# Translators: Chart type
	xlCylinderBarStacked100 : _( "100 percent Stacked Cylinder Bar" ) ,
	# Translators: Chart type
	xlCylinderCol : _( "3D Cylinder Column" ) ,
	# Translators: Chart type
	xlCylinderColClustered : _( "Clustered Cone Column" ) ,
	# Translators: Chart type
	xlCylinderColStacked : _( "Stacked Cone Column" ) ,
	# Translators: Chart type
	xlCylinderColStacked100 : _( "100 percent Stacked Cylinder Column" ) ,
	# Translators: Chart type
	xlDoughnut : _( "Doughnut" ) ,
	# Translators: Chart type
	xlDoughnutExploded : _( "Exploded Doughnut" ) ,
	# Translators: Chart type
	xlLine : _( "Line" ) ,
	# Translators: Chart type
	xlLineMarkers : _( "Line with Markers" ) ,
	# Translators: Chart type
	xlLineMarkersStacked : _( "Stacked Line with Markers" ) ,
	# Translators: Chart type
	xlLineMarkersStacked100 : _( "100 percent Stacked Line with Markers" ) ,
	# Translators: Chart type
	xlLineStacked : _( "Stacked Line" ) ,
	# Translators: Chart type
	xlLineStacked100 : _( "100 percent Stacked Line" ) ,
	# Translators: Chart type
	xlPie : _( "Pie" ) ,
	# Translators: Chart type
	xlPieExploded : _( "Exploded Pie" ) ,
	# Translators: Chart type
	xlPieOfPie : _( "Pie of Pie" ) ,
	# Translators: Chart type
	xlPyramidBarClustered : _( "Clustered Pyramid Bar" ) ,
	# Translators: Chart type
	xlPyramidBarStacked : _( "Stacked Pyramid Bar" ) ,
	# Translators: Chart type
	xlPyramidBarStacked100 : _( "100 percent Stacked Pyramid Bar" ) ,
	# Translators: Chart type
	xlPyramidCol : _( "3D Pyramid Column" ) ,
	# Translators: Chart type
	xlPyramidColClustered : _( "Clustered Pyramid Column" ) ,
	# Translators: Chart type
	xlPyramidColStacked : _( "Stacked Pyramid Column" ) ,
	# Translators: Chart type
	xlPyramidColStacked100 : _( "100 percent Stacked Pyramid Column" ) ,
	# Translators: Chart type
	xlRadar : _( "Radar" ) ,
	# Translators: Chart type
	xlRadarFilled : _( "Filled Radar" ) ,
	# Translators: Chart type
	xlRadarMarkers : _( "Radar with Data Markers" ) ,
	# Translators: Chart type
	xlStockHLC : _( "High-Low-Close" ) ,
	# Translators: Chart type
	xlStockOHLC : _( "Open-High-Low-Close" ) ,
	# Translators: Chart type
	xlStockVHLC : _( "Volume-High-Low-Close" ) ,
	# Translators: Chart type
	xlStockVOHLC : _( "Volume-Open-High-Low-Close" ) ,
	# Translators: Chart type
	xlSurface : _( "3D Surface" ) ,
	# Translators: Chart type
	xlSurfaceTopView : _( "Surface (Top View)" ) ,
	# Translators: Chart type
	xlSurfaceTopViewWireframe : _( "Surface (Top View wireframe)" ) ,
	# Translators: Chart type
	xlSurfaceWireframe : _( "3D Surface (wireframe)" ) ,
	# Translators: Chart type
	xlXYScatter : _( "Scatter" ) ,
	# Translators: Chart type
	xlXYScatterLines : _( "Scatter with Lines" ) ,
	# Translators: Chart type
	xlXYScatterLinesNoMarkers : _( "Scatter with Lines and No Data Markers" ) ,
	# Translators: Chart type
	xlXYScatterSmooth : _( "Scatter with Smoothed Lines" ) ,
	# Translators: Chart type
	xlXYScatterSmoothNoMarkers : _( "Scatter with Smoothed Lines and No Data Markers")
}

# Axis types in chart
xlCategory = 1
xlValue = 2
xlSeriesAxis = 3 # Valid only for 3-D charts

# Axis Groups in chart
xlPrimary = 1
xlSecondary = 2



# values for enumeration 'XlChartItem'
xlDataLabel = 0
xlChartArea = 2
xlSeries = 3
xlChartTitle = 4
xlWalls = 5
xlCorners = 6
xlDataTable = 7
xlTrendline = 8
xlErrorBars = 9
xlXErrorBars = 10
xlYErrorBars = 11
xlLegendEntry = 12
xlLegendKey = 13
xlShape = 14
xlMajorGridlines = 15
xlMinorGridlines = 16
xlAxisTitle = 17
xlUpBars = 18
xlPlotArea = 19
xlDownBars = 20
xlAxis = 21
xlSeriesLines = 22
xlFloor = 23
xlLegend = 24
xlHiLoLines = 25
xlDropLines = 26
xlRadarAxisLabels = 27
xlNothing = 28
xlLeaderLines = 29
xlDisplayUnitLabel = 30
xlPivotChartFieldButton = 31
xlPivotChartDropZone = 32
XlChartItem = ctypes.c_int # enum



class ExcelChart(excel.ExcelBase):
	def __init__(self,windowHandle=None,excelWindowObject=None,excelChartObject=None):
		self.windowHandle = windowHandle
		self.excelWindowObject = excelWindowObject
		self.excelChartObject = excelChartObject
		self.excelChartEventHandlerObject = ExcelChartEventHandler( self  )
		self.excelChartEventConnection = GetEvents( self.excelChartObject , self.excelChartEventHandlerObject , ChartEvents)
		log.debugWarning("ExcelChart init")
		super(ExcelChart,self).__init__(windowHandle=windowHandle)
		for gesture in self.__changeSelectionGestures:
			self.bindGesture(gesture, "changeSelection")

	def _isEqual(self, other):
		if not super(ExcelChart, self)._isEqual(other):
			return False
		return self.excelChartObject.Parent.Index == other.excelChartObject.Parent.Index

	def _get_name(self):
		if self.excelChartObject.HasTitle:
			name=self.excelChartObject.ChartTitle.Text
		else:
			name=self.excelChartObject.Name
#find the type of the chart
		chartType = self.excelChartObject.ChartType
		if chartType in chartTypeDict.keys():
			chartTypeText = "%s" %(chartTypeDict[chartType])
		else:
			# Translators: chart type to be reported when the type is not available
			chartTypeText=_("unknown")
		# Translators: prompt for chart title and chart type to be reported 
		return _("Chart title equals {chartTitle} type equals {chartType}").format(chartTitle=name, chartType=chartTypeText)

	def _get_title(self):
		try:
			title=self.excelChartObject.ChartTitle	
		except COMError:
			title=None
		return title
	
	def _get_role(self):
		return controlTypes.ROLE_CHART 
	
	def script_switchToCell(self,gesture):
		cell=self.excelWindowObject.ActiveCell
		cell.Activate()
		cellObj=self._getSelection()
		eventHandler.queueEvent("gainFocus",cellObj)
	script_switchToCell.canPropagate=True

	def event_gainFocus(self):
		if self.excelChartObject.HasTitle:
			name=self.excelChartObject.ChartTitle.Text
		else:
			name=self.excelChartObject.Name
#find the type of the chart
		chartType = self.excelChartObject.ChartType
		if chartType in chartTypeDict.keys():
			chartTypeText=_("%s" %(chartTypeDict[chartType]))
		else:
			# Translators: chart type to be reported when the type is not available
			chartTypeText=_("unknown")
		# Translators: prompt for chart title and chart type to be reported 
		ui.message( _("Chart title equals {chartTitle} type equals {chartType}").format(chartTitle=name, chartType=chartTypeText)) 
		self.reportSeriesSummary()

	def script_reportTitle(self,gesture):
		ui.message (self._get_name())
	script_reportTitle.canPropagate=True

	def reportAxisTitle(self, axisType):
		axis=None
		if self.excelChartObject.HasAxis(axisType, xlPrimary):
			axis = self.excelChartObject.Axes(axisType, xlPrimary)
		else:
			pass
		# Translators: Axis title to be reported when the title is not available
		axisTitle = axis.AxisTitle.Text if axis and axis.HasTitle else _("Not defined")
		# Translators: Chart Axis types  
		axisName = _( "Category" ) if axisType==xlCategory else _( "Value" ) if axisType==xlValue else _( "Series" )
		# Translators: Prompt for axis title and axis type to be reported 
		text=_("{axisName} Axis is {axisTitle}").format(axisName=axisName, axisTitle=axisTitle)
		ui.message(text)

	def script_reportCategoryAxis(self, gesture):
		self.reportAxisTitle(xlCategory)
	script_reportCategoryAxis.canPropagate=True

	def script_reportValueAxis(self, gesture):
		self.reportAxisTitle(xlValue)
	script_reportValueAxis.canPropagate=True

	def script_reportSeriesAxis(self, gesture):
		self.reportAxisTitle(xlSeriesAxis)
	script_reportSeriesAxis.canPropagate=True

	def reportSeriesSummary(self ):
		count = self.excelChartObject.SeriesCollection().count
		if count>0:
			if count == 1:
				# Translators: Number of series when there is only one series  
				seriesValueString = _( "There is %d series in this chart" ) %(count)
			else:
				# Translators: Number of series when there are multiple series 
				seriesValueString = _( "There are total %d series in this chart" ) %(count)

			for i in xrange(1, count+1):
				# Translators: prompt for series number and name to be reported 
				seriesValueString += ", Series %d %s" %(i, self.excelChartObject.SeriesCollection(i).Name)
			text = seriesValueString	
		else:
			# Translators: prompt to be reported when there is no series
			text=_("No Series defined.")
		ui.message(text)

	def script_reportSeriesSummary(self, gesture):
		self.reportSeriesSummary()
	script_reportSeriesSummary.canPropagate=True

	__gestures = {
		"kb:escape": "switchToCell",
		"kb:NVDA+t" : "reportTitle",
		"kb:NVDA+shift+1" : "reportCategoryAxis",
		"kb:NVDA+shift+2" : "reportValueAxis",
		"kb:NVDA+shift+3" : "reportSeriesAxis",
		"kb:NVDA+shift+4" : "reportSeriesSummary",
	}

	def script_changeSelection(self,gesture):
		oldSelection=self._getSelection()
		gesture.send()
		newSelection=None
		curTime=startTime=time.time()
		while (curTime-startTime)<=0.15:
			if scriptHandler.isScriptWaiting():
				# Prevent lag if keys are pressed rapidly
				return
			if eventHandler.isPendingEvents('gainFocus'):
				return
			newSelection=self._getSelection()
			if newSelection and newSelection!=oldSelection:
				break
			api.processPendingEvents(processEventQueue=False)
			time.sleep(0.015)
			curTime=time.time()
		if newSelection:
			eventHandler.executeEvent('gainFocus',newSelection)
	script_changeSelection.canPropagate=True
			
	__changeSelectionGestures = {
		"kb:control+pageUp",
		"kb:control+pageDown",
		"kb:tab",
		"kb:shift+tab",
	}

	def elementChanged( self , ElementID ,arg1,arg2):
		selectedChartElement = None
		if ElementID == xlAxis:
			selectedChartElement = ExcelChartElementAxis( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlAxisTitle:  
			selectedChartElement = ExcelChartElementAxisTitle( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlSeries:
			selectedChartElement = ExcelChartElementSeries( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlTrendline:
			selectedChartElement = ExcelChartElementTrendline( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlChartTitle:
			selectedChartElement = ExcelChartElementChartTitle( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlChartArea:
			selectedChartElement = ExcelChartElementChartArea( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlPlotArea:
			selectedChartElement = ExcelChartElementPlotArea( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlLegend:
			selectedChartElement = ExcelChartElementLegend( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlLegendEntry:
			selectedChartElement = ExcelChartElementLegendEntry( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlLegendKey:
			selectedChartElement = ExcelChartElementLegendKey( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		else:
			selectedChartElement = ExcelChartElementBase( windowHandle= self.windowHandle , excelChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )

		if selectedChartElement :
			selectedChartElement.parent = self
			selectedChartElement.previous = None
			selectedChartElement.next = None
			eventHandler.queueEvent("gainFocus", selectedChartElement )

class ExcelChartEventHandler(comtypes.COMObject):
	_com_interfaces_=[ChartEvents,IDispatch]

	def __init__(self, owner ):
		self.owner = weakref.proxy( owner )
		super(ExcelChartEventHandler ,self).__init__()

	def ChartEvents_Select(self, this, ElementID ,arg1,arg2):
		self.owner.elementChanged( ElementID ,arg1,arg2)

class ExcelChartElementBase(Window):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		self.excelChartObject = excelChartObject
		self.elementID = elementID 
		self.arg1 = arg1
		self.arg2 = arg2
		super(ExcelChartElementBase ,self).__init__(windowHandle=windowHandle)

	def GetChartSegment(self):
		chartType = self.excelChartObject.ChartType
		if chartType in (xl3DPie, xl3DPieExploded, xlPie, xlPieExploded, xlPieOfPie):
			# Translators: A slice in a pie chart.
			text=_("slice")
		elif chartType in (xl3DColumn, xl3DColumnClustered, xl3DColumnStacked, xl3DColumnStacked100, xlColumnClustered, xlColumnStacked100, xlColumnStacked):
			# Translators: A column in a column chart.
			text=_("column")
		elif chartType in (xl3DLine, xlLine, xlLineMarkers, xlLineMarkersStacked, xlLineMarkersStacked100, xlLineStacked, xlLineStacked100):
			# Translators: A data point in a line chart.
			text=_("data point")
		else:
			# Translators: A segment of a chart for charts which don't have a specific name for segments.
			text=_("item")
		return text

	def _get_role(self):
			return controlTypes.ROLE_UNKNOWN

	def _get_name(self):
		return self._getChartElementText(self.elementID , self.arg1 , self.arg2)

	def script_reportCurrentChartElementWithExtraInfo(self,gesture):
		ui.message( self._getChartElementText(self.elementID , self.arg1 , self.arg2 , True ) )

	def script_reportCurrentChartElementColor(self,gesture):
		if self.elementID == xlSeries:
			if self.arg2 == -1:
				ui.message ( _( "Series color: {colorName} ").format(colorName=colors.RGB.fromCOLORREF(int( self.excelChartObject.SeriesCollection( self.arg1 ).Interior.Color ) ).name  ) )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlDisplayUnitLabel:  
			# Translators: prompt for xlDisplayUnitLabel
			return  _( "Display Unit Label") 

		elif ElementID == xlMajorGridlines:  
			# Translators: prompt for xlMajorGridlines
			return  _( "Major Gridlines" ) 

		elif ElementID == xlMinorGridlines:  
			# Translators: prompt for xlMinorGridlines
			return _( "Minor Gridlines" ) 

		elif ElementID == xlPivotChartDropZone:  
			# Translators: prompt for xlPivotChartDropZone
			return _( "Pivot Chart Drop Zone" ) 

		elif ElementID == xlPivotChartFieldButton:
			# Translators: prompt for xlPivotChartFieldButton
			return _( "Pivot Chart Field Button" ) 

		elif ElementID == xlDownBars:
			# Translators: prompt for xlDownBars
			return _( "Down Bars" ) 

		elif ElementID == xlDropLines:
			# Translators: prompt for xlDropLines
			return _( "Drop Lines" )

		elif ElementID == xlHiLoLines:
			# Translators: prompt for xlHiLoLines
			return  _( "Hi Lo Lines" )

		elif ElementID == xlRadarAxisLabels:
			# Translators: prompt for xlRadarAxisLabels
			return _( "Radar Axis Labels" )

		elif ElementID == xlSeriesLines:
			# Translators: prompt for xlSeriesLines
			return _( "Series Lines" )

		elif ElementID == xlUpBars:
			# Translators: prompt for xlUpBars
			return _( "Up Bars" )

		elif ElementID == xlCorners:
			# Translators: prompt for xlCorners
			return _( "Corners" )

		elif ElementID == xlDataTable:
			# Translators: prompt for xlDataTable
			return _( "Data Table" )

		elif ElementID == xlFloor:
			# Translators: prompt for xlFloor
			return  _( "Floor" )

		elif ElementID == xlNothing:
			# Translators: prompt for xlNothing
			return _( "xlNothing" )

		elif ElementID == xlWalls:
			# Translators: prompt for xlWalls
			return _( "Walls" )

		elif ElementID == xlDataLabel:
			# Translators: prompt for xlDataLabel
			return _( "Data Label" )

		elif ElementID == xlErrorBars:
			# Translators: prompt for xlErrorBars
			return _( "Error Bars" )

		elif ElementID == xlXErrorBars:
			# Translators: prompt for xlXErrorBars
			return _( "X Error Bars" )

		elif ElementID == xlYErrorBars:
			# Translators: prompt for xlYErrorBars
			return _( "Y Error Bars" )

		elif ElementID == xlShape:
			# Translators: prompt for xlShape
			return _( "Shape" )

	#end def _Select

	__gestures = {
		"kb:NVDA+d" : "reportCurrentChartElementWithExtraInfo",
		"kb:NVDA+f" : "reportCurrentChartElementColor",
	}




# end class ExcelChartEventHandler

class ExcelChartElementSeries(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super(ExcelChartElementSeries,self).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlSeries:
			if arg2 == -1:
				# Translators: Details about a series in a chart.
				# For example, this might report "foo series 1 of 2"
				return _( "{seriesName} Series {seriesIndex} of {seriesCount}").format( seriesName = self.excelChartObject.SeriesCollection(arg1).Name , seriesIndex = arg1 , seriesCount = self.excelChartObject.SeriesCollection().Count )
			else:
# if XValue is a float, change it to int, else dates are shown with points. hope this does not introduce another bug
				if isinstance( self.excelChartObject.SeriesCollection(arg1).XValues[arg2 - 1] , float): 
					excelSeriesXValue = int(self.excelChartObject.SeriesCollection(arg1).XValues[arg2 - 1] )
				else:
					excelSeriesXValue = self.excelChartObject.SeriesCollection(arg1).XValues[arg2 - 1] 

				output=""
				if self.excelChartObject.ChartType in (xlLine, xlLineMarkers , xlLineMarkersStacked, xlLineMarkersStacked100, xlLineStacked, xlLineStacked100):
					if arg2 > 1:

						if self.excelChartObject.SeriesCollection(arg1).Values[arg2 - 1] == self.excelChartObject.SeriesCollection(arg1).Values[arg2 - 2]: 
							# Translators: For line charts, indicates no change from the previous data point on the left
							output += _( "no change from point {previousIndex}, ").format( previousIndex = arg2 - 1 )
						elif self.excelChartObject.SeriesCollection(arg1).Values[arg2 - 1] > self.excelChartObject.SeriesCollection(arg1).Values[arg2 - 2]: 
							# Translators: For line charts, indicates an increase from the previous data point on the left
							output += _( "Increased by {incrementValue} from point {previousIndex}, ").format( incrementValue = self.excelChartObject.SeriesCollection(arg1).Values[arg2 - 1] - self.excelChartObject.SeriesCollection(arg1).Values[arg2 - 2] , previousIndex = arg2 - 1 ) 
						else:
							# Translators: For line charts, indicates a decrease from the previous data point on the left
							output += _( "decreased by {decrementValue} from point {previousIndex}, ").format( decrementValue = self.excelChartObject.SeriesCollection(arg1).Values[arg2 - 2] - self.excelChartObject.SeriesCollection(arg1).Values[arg2 - 1] , previousIndex = arg2 - 1 ) 

				if self.excelChartObject.HasAxis(xlCategory) and self.excelChartObject.Axes(xlCategory).HasTitle:
					# Translators: Specifies the category of a data point.
					# {categoryAxisTitle} will be replaced with the title of the category axis; e.g. "Month".
					# {categoryAxisData} will be replaced with the category itself; e.g. "January".
					output += _( "{categoryAxisTitle} {categoryAxisData}: ").format( categoryAxisTitle = self.excelChartObject.Axes(xlCategory).AxisTitle.Text , categoryAxisData = excelSeriesXValue ) 
				else:
					# Translators: Specifies the category of a data point.
					# {categoryAxisData} will be replaced with the category itself; e.g. "January".
					output += _( "Category {categoryAxisData}: ").format( categoryAxisData = excelSeriesXValue ) 

				if self.excelChartObject.HasAxis(xlValue) and self.excelChartObject.Axes(xlValue).HasTitle:
					# Translators: Specifies the value of a data point.
					# {valueAxisTitle} will be replaced with the title of the value axis; e.g. "Amount".
					# {valueAxisData} will be replaced with the value itself; e.g. "1000".
					output +=  _( "{valueAxisTitle} {valueAxisData}").format( valueAxisTitle = self.excelChartObject.Axes(xlValue).AxisTitle.Text , valueAxisData = self.excelChartObject.SeriesCollection(arg1).Values[arg2-1]) 
				else:
					# Translators: Specifies the value of a data point.
					# {valueAxisData} will be replaced with the value itself; e.g. "1000".
					output +=  _( "value {valueAxisData}").format( valueAxisData = self.excelChartObject.SeriesCollection(arg1).Values[arg2-1]) 

				if self.excelChartObject.ChartType in (xlPie, xlPieExploded, xlPieOfPie):
					total = math.fsum( self.excelChartObject.SeriesCollection(arg1).Values ) 
					# Translators: Details about a slice of a pie chart.
					# For example, this might report "fraction 25.25 percent slice 1 of 5"
					output += _( " fraction {fractionValue:.2f} Percent slice {pointIndex} of {pointCount}").format( fractionValue = self.excelChartObject.SeriesCollection(arg1).Values[arg2-1] / total *100.00 , pointIndex = arg2 , pointCount = len( self.excelChartObject.SeriesCollection(arg1).Values ) )
				else:
					# Translators: Details about a segment of a chart.
					# For example, this might report "column 1 of 5"
					output += _( " {segmentType} {pointIndex} of {pointCount}").format( segmentType = self.GetChartSegment() ,  pointIndex = arg2 , pointCount = len( self.excelChartObject.SeriesCollection(arg1).Values ) )

				return  output 

class ExcelChartElementAxis(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementAxis , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlAxis:
			if arg1 == xlPrimary: 
				# Translators: axis group
				axisGroup = _("Primary")
			elif arg1 == xlSecondary :
				# Translators: axis group
				axisGroup = _("Secondary")

			if arg2 == xlCategory: 
				# Translators: axis type 
				axisType= _("Category")
			elif arg2 == xlValue:
				# Translators: axis type 
				axisType= _("Value")
			elif arg2 == xlSeriesAxis: 
				# Translators: axis type 
				axisType= _("Series")

			axisDescription =""
			if self.excelChartObject.HasAxis( arg2 ) and self.excelChartObject.Axes( arg2 ).HasTitle:
				# Translators: Prompt for axis details such as: type, group, and title 
				axisDescription += _("Chart Axis, type equals {axisType}, group equals {axisGroup}, Title equals {axisTitle}").format( axisType = axisType , axisGroup = axisGroup , axisTitle = self.excelChartObject.Axes( arg2 , arg1 ).AxisTitle.Text ) 
			elif self.excelChartObject.HasAxis( arg2 ) and not self.excelChartObject.Axes( arg2 ).HasTitle:
				# Translators: Prompt for axis details such as: type, group, and title when there is no title
				axisDescription += _("Chart Axis, type equals {axisType}, group equals {axisGroup}, Title equals {axisTitle}").format( axisType = axisType , axisGroup = axisGroup , axisTitle = _("none")  ) 

			return  axisDescription 

class ExcelChartElementAxisTitle(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementAxisTitle , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlAxisTitle:  
			axisTitle=""
			if self.excelChartObject.HasAxis( arg2 ) and self.excelChartObject.Axes( arg2 ).HasTitle:
				# Translators: Prompt for axis title if axis has title
				axisTitle += _("Chart Axis Title equals {axisTitle} ").format( axisTitle = self.excelChartObject.Axes( arg2 , arg1 ).AxisTitle.Text  ) 
			elif self.excelChartObject.HasAxis( arg2 ) and not self.excelChartObject.Axes( arg2 ).HasTitle:
				# Translators: Prompt for axis title without title
				axisTitle += _("Chart Axis Title equals {axisTitle} ").format( axisTitle = _("none") ) 

			return  axisTitle 

class ExcelChartElementTrendline(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementTrendline , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlTrendline:
			if self.excelChartObject.SeriesCollection(arg1).Trendlines(arg2).DisplayEquation    or self.excelChartObject.SeriesCollection(arg1).Trendlines(arg2).DisplayRSquared:
				# Translators: description for the word square
				trendlineText = unicode( self.excelChartObject.SeriesCollection(arg1).Trendlines(arg2).DataLabel.Text ).encode("utf-8").replace("\xc2\xb2" , _( " square " ) )
				# Translators: Prompt for trendline with equation or r square
				return  _( " trendline {dataLabel} ").format( dataLabel = trendlineText ) 
			else:
				# Translators: Prompt for trendline without equation or r square
				return _( "Trendline" ) 

class ExcelChartElementChartTitle(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementChartTitle , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlChartTitle:
			if self.excelChartObject.HasTitle:
				# Translators: Prompt for chart title
				return _( "Chart Title equals {chartTitle}").format ( chartTitle = self.excelChartObject.ChartTitle.Text )
			else:
				# Translators: Prompt for chart title when the title is not available
				return _( "Untitled chart" )

class ExcelChartElementChartArea(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementChartArea , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlChartArea:
			if reportExtraInfo:
				# Translators: Prompt for chart area with dimentions
				return _( "Chart area height equals {chartAreaHeight}, width equals {chartAreaWidth}, top equals {chartAreaTop}, left equals {chartAreaLeft}").format ( chartAreaHeight = self.excelChartObject.ChartArea.Height , chartAreaWidth = self.excelChartObject.ChartArea.Width , chartAreaTop = self.excelChartObject.ChartArea.Top , chartAreaLeft = self.excelChartObject.ChartArea.Left)
			else:
				# Translators: Prompt for chart area 
				return _( "Chart area ")

class ExcelChartElementPlotArea(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementPlotArea , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlPlotArea:
			if reportExtraInfo:
			# useing {:.0f} to remove fractions
				# Translators: Prompt for plot area with inner dimentions
				return _( "Plot Area inside height equals {plotAreaInsideHeight:.0f}, inside width equals {plotAreaInsideWidth:.0f}, inside top equals {plotAreaInsideTop:.0f}, inside left equals {plotAreaInsideLeft:.0f}").format ( plotAreaInsideHeight = self.excelChartObject.PlotArea.InsideHeight , plotAreaInsideWidth = self.excelChartObject.PlotArea.InsideWidth , plotAreaInsideTop = self.excelChartObject.PlotArea.InsideTop , plotAreaInsideLeft = self.excelChartObject.PlotArea.InsideLeft )
			else:
				# Translators: Prompt for plot area 
				return _( "Plot Area " )

class ExcelChartElementLegend(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementLegend , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlLegend:
			if self.excelChartObject.HasLegend:
			# Translators: Prompt for Legend
				return _( "Legend" ) 
			else:
			# Translators: Prompt for Legend when no legend is present
				return _( "No legend" )

class ExcelChartElementLegendEntry(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementLegendEntry , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlLegendEntry:
			# Translators: Prompt for Legend entry for series name index of count
			return _( "Legend entry for Series {seriesName}, {seriesIndex} of {seriesCount}").format( seriesName = self.excelChartObject.SeriesCollection(arg1).Name , seriesIndex = arg1 , seriesCount = self.excelChartObject.SeriesCollection().Count ) 

class ExcelChartElementLegendKey(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementLegendKey , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlLegendKey:
			# Translators: Prompt for Legend key for series name index of count
			return _( "Legend key for Series {seriesName} {seriesIndex} of {seriesCount}").format( seriesName = self.excelChartObject.SeriesCollection(arg1).Name , seriesIndex = arg1 , seriesCount = self.excelChartObject.SeriesCollection().Count )


