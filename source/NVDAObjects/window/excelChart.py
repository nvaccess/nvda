# -*- coding: UTF-8 -*- 
#NVDAObjects/excel.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014-2015 Dinesh Kaushal, NV Access Limited
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
import api


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
	# Translators: A type of chart in Microsoft Excel. 
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DArea : _( "3D Area" ),
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DAreaStacked : _( "3D Stacked Area" ),
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DAreaStacked100 : _( "100 percent Stacked Area" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DBarClustered : _( "3D Clustered Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DBarStacked : _( "3D Stacked Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DBarStacked100 : _( "3D 100 percent Stacked Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DColumn : _( "3D Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DColumnClustered : _( "3D Clustered Column" ),
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DColumnStacked : _( "3D Stacked Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DColumnStacked100 : _( "3D 100 percent Stacked Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DLine : _( "3D Line" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DPie : _( "3D Pie" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xl3DPieExploded : _( "Exploded 3D Pie" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlArea : _( "Area" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlAreaStacked : _( "Stacked Area" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlAreaStacked100 : _( "100 percent Stacked Area" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlBarClustered : _( "Clustered Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlBarOfPie : _( "Bar of Pie" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlBarStacked : _( "Stacked Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlBarStacked100 : _( "100 percent Stacked Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlBubble : _( "Bubble" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlBubble3DEffect : _( "Bubble with 3D effects" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlColumnClustered : _( "Clustered Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlColumnStacked : _( "Stacked Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlColumnStacked100 : _( "100 percent Stacked Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlConeBarClustered : _( "Clustered Cone Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlConeBarStacked : _( "Stacked Cone Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlConeBarStacked100 : _( "100 percent Stacked Cone Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlConeCol : _( "3D Cone Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlConeColClustered : _( "Clustered Cone Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlConeColStacked : _( "Stacked Cone Column" ),
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlConeColStacked100 : _( "100 percent Stacked Cone Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlCylinderBarClustered : _( "Clustered Cylinder Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlCylinderBarStacked : _( "Stacked Cylinder Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlCylinderBarStacked100 : _( "100 percent Stacked Cylinder Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlCylinderCol : _( "3D Cylinder Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlCylinderColClustered : _( "Clustered Cone Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlCylinderColStacked : _( "Stacked Cone Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlCylinderColStacked100 : _( "100 percent Stacked Cylinder Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlDoughnut : _( "Doughnut" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlDoughnutExploded : _( "Exploded Doughnut" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlLine : _( "Line" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlLineMarkers : _( "Line with Markers" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlLineMarkersStacked : _( "Stacked Line with Markers" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlLineMarkersStacked100 : _( "100 percent Stacked Line with Markers" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlLineStacked : _( "Stacked Line" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlLineStacked100 : _( "100 percent Stacked Line" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlPie : _( "Pie" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlPieExploded : _( "Exploded Pie" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlPieOfPie : _( "Pie of Pie" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlPyramidBarClustered : _( "Clustered Pyramid Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlPyramidBarStacked : _( "Stacked Pyramid Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlPyramidBarStacked100 : _( "100 percent Stacked Pyramid Bar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlPyramidCol : _( "3D Pyramid Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlPyramidColClustered : _( "Clustered Pyramid Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlPyramidColStacked : _( "Stacked Pyramid Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
	xlPyramidColStacked100 : _( "100 percent Stacked Pyramid Column" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlRadar : _( "Radar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlRadarFilled : _( "Filled Radar" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlRadarMarkers : _( "Radar with Data Markers" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlStockHLC : _( "High-Low-Close" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlStockOHLC : _( "Open-High-Low-Close" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlStockVHLC : _( "Volume-High-Low-Close" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlStockVOHLC : _( "Volume-Open-High-Low-Close" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlSurface : _( "3D Surface" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlSurfaceTopView : _( "Surface (Top View)" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlSurfaceTopViewWireframe : _( "Surface (Top View wireframe)" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlSurfaceWireframe : _( "3D Surface (wireframe)" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlXYScatter : _( "Scatter" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlXYScatterLines : _( "Scatter with Lines" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlXYScatterLinesNoMarkers : _( "Scatter with Lines and No Data Markers" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
	xlXYScatterSmooth : _( "Scatter with Smoothed Lines" ) ,
	# Translators: A type of chart in Microsoft Excel.
	# See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
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
		chartTypeText = chartTypeDict.get(chartType,
			# Translators: Reported when the type of a chart is not known.
			_("unknown"))
		# Translators: Message reporting the title and type of a chart.
		return _("Chart title: {chartTitle}, type: {chartType}").format(chartTitle=name, chartType=chartTypeText)

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
		ui.message(self.name)
		self.reportSeriesSummary()

	def script_reportTitle(self,gesture):
		ui.message (self._get_name())
	script_reportTitle.canPropagate=True

	def reportAxisTitle(self, axisType):
		axis=None
		if self.excelChartObject.HasAxis(axisType, xlPrimary):
			axis = self.excelChartObject.Axes(axisType, xlPrimary)
		# Translators: Reported when there is no title for an axis in a chart.
		axisTitle = axis.AxisTitle.Text if axis and axis.HasTitle else _("Not defined")
		axisName = (
			# Translators: A type of axis in a chart.
			_( "Category" ) if axisType==xlCategory
			# Translators: A type of axis in a chart.
			else _( "Value" ) if axisType==xlValue
			# Translators: A type of axis in a chart.
			else _( "Series" ))
		# Translators: Message reporting the type and title of an axis in a chart.
		# For example, this might report "Category axis is month"
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
				# Translators: Indicates that there is 1 series in a chart.
				seriesValueString = _( "There is 1 series in this chart" )
			else:
				# Translators: Indicates the number of series in a chart where there are multiple series.
				seriesValueString = _( "There are total %d series in this chart" ) %(count)

			for i in xrange(1, count+1):
				# Translators: Specifies the number and name of a series when listing series in a chart.
				seriesValueString += ", " + _("series {number} {name}").format(number=i, name=self.excelChartObject.SeriesCollection(i).Name)
			text = seriesValueString	
		else:
			# Translators: Indicates that there are no series in a chart.
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
			text=pgettext('chart','column')
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

	ELEMENT_IDS = {
		# Translators: A type of element in a Microsoft Excel chart.
		xlDisplayUnitLabel:  _("Display Unit Label"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlMajorGridlines:  _("Major Gridlines"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlMinorGridlines: _("Minor Gridlines"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlPivotChartDropZone: _("Pivot Chart Drop Zone"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlPivotChartFieldButton: _("Pivot Chart Field Button"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlDownBars: _("Down Bars"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlDropLines: _("Drop Lines"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlHiLoLines:  _("Hi Lo Lines"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlRadarAxisLabels: _("Radar Axis Labels"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlSeriesLines: _("Series Lines"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlUpBars: _("Up Bars"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlCorners: _("Corners"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlDataTable: _("Data Table"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlFloor:  _("Floor"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlNothing: _("Nothing"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlWalls: _("Walls"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlDataLabel: _("Data Label"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlErrorBars: _("Error Bars"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlXErrorBars: _("X Error Bars"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlYErrorBars: _("Y Error Bars"),
		# Translators: A type of element in a Microsoft Excel chart.
		xlShape: _("Shape"),
	}
	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		return self.ELEMENT_IDS[ElementID]

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
				return _( "{seriesName} series {seriesIndex} of {seriesCount}").format( seriesName = self.excelChartObject.SeriesCollection(arg1).Name , seriesIndex = arg1 , seriesCount = self.excelChartObject.SeriesCollection().Count )
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
				# Translators: The primary axis group in a Microsoft Excel chart.
				axisGroup = _("Primary")
			elif arg1 == xlSecondary :
				# Translators: The secondary axis group in a Microsoft Excel chart.
				axisGroup = _("Secondary")

			if arg2 == xlCategory: 
				# Translators: The category axis in a Microsoft Excel chart.
				# See https://support.office.com/en-us/article/Excel-Glossary-53b6ce43-1a9f-4ac2-a33c-d6f64ea2d1fc?CorrelationId=44f003e6-453a-4b14-a9a6-3fb5287109c7&ui=en-US&rs=en-US&ad=US
				axisType= _("Category")
			elif arg2 == xlValue:
				# Translators: The value axis in a Microsoft Excel chart.
				# See https://support.office.com/en-us/article/Excel-Glossary-53b6ce43-1a9f-4ac2-a33c-d6f64ea2d1fc?CorrelationId=44f003e6-453a-4b14-a9a6-3fb5287109c7&ui=en-US&rs=en-US&ad=US
				axisType= _("Value")
			elif arg2 == xlSeriesAxis: 
				# Translators: The series axis in a Microsoft Excel chart.
				# See https://support.office.com/en-us/article/Excel-Glossary-53b6ce43-1a9f-4ac2-a33c-d6f64ea2d1fc?CorrelationId=44f003e6-453a-4b14-a9a6-3fb5287109c7&ui=en-US&rs=en-US&ad=US
				axisType= _("Series")

			axisDescription =""
			if self.excelChartObject.HasAxis( arg2 ) and self.excelChartObject.Axes( arg2 ).HasTitle:
				# Translators: Details about an axis in a chart.
				axisDescription += _("Chart axis, type: {axisType}, group: {axisGroup}, title: {axisTitle}").format( axisType = axisType , axisGroup = axisGroup , axisTitle = self.excelChartObject.Axes( arg2 , arg1 ).AxisTitle.Text )
			else:
				# Translators: Details about an untitled axis in a chart.
				axisDescription += _("Chart axis, type: {axisType}, group: {axisGroup}").format( axisType = axisType , axisGroup = axisGroup)

			return  axisDescription 

class ExcelChartElementAxisTitle(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementAxisTitle , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlAxisTitle:  
			# Translators: Indicates a chart axis title in Microsoft Excel.
			axisTitle=_("Chart axis title")
			if self.excelChartObject.HasAxis( arg2 ) and self.excelChartObject.Axes( arg2 ).HasTitle:
				axisTitle += ": " + self.excelChartObject.Axes( arg2 , arg1 ).AxisTitle.Text 

			return  axisTitle 

class ExcelChartElementTrendline(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementTrendline , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlTrendline:
			# Translators: Indicates a trendline in a Microsoft Excel chart.
			# See https://support.office.com/en-us/article/Excel-Glossary-53b6ce43-1a9f-4ac2-a33c-d6f64ea2d1fc?CorrelationId=44f003e6-453a-4b14-a9a6-3fb5287109c7&ui=en-US&rs=en-US&ad=US
			text = _("trendline")
			if self.excelChartObject.SeriesCollection(arg1).Trendlines(arg2).DisplayEquation    or self.excelChartObject.SeriesCollection(arg1).Trendlines(arg2).DisplayRSquared:
				# Translators: Describes the squared symbol used in the label for a trendline in a Microsoft Excel chart.
				text += " " + self.excelChartObject.SeriesCollection(arg1).Trendlines(arg2).DataLabel.Text.replace(u"²", _( " squared " ) )
			return text

class ExcelChartElementChartTitle(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementChartTitle , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlChartTitle:
			if self.excelChartObject.HasTitle:
				# Translators: Details about a chart title in Microsoft Excel.
				return _( "Chart title: {chartTitle}").format ( chartTitle = self.excelChartObject.ChartTitle.Text )
			else:
				# Translators: Indicates an untitled chart in Microsoft Excel.
				return _( "Untitled chart" )

class ExcelChartElementChartArea(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementChartArea , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlChartArea:
			if reportExtraInfo:
				# Translators: Details about the chart area in a Microsoft Excel chart.
				return _( "Chart area, height: {chartAreaHeight}, width: {chartAreaWidth}, top: {chartAreaTop}, left: {chartAreaLeft}").format ( chartAreaHeight = self.excelChartObject.ChartArea.Height , chartAreaWidth = self.excelChartObject.ChartArea.Width , chartAreaTop = self.excelChartObject.ChartArea.Top , chartAreaLeft = self.excelChartObject.ChartArea.Left)
			else:
				# Translators: Indicates the chart area of a Microsoft Excel chart.
				return _( "Chart area ")

class ExcelChartElementPlotArea(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementPlotArea , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlPlotArea:
			if reportExtraInfo:
				# useing {:.0f} to remove fractions
				# Translators: Details about the plot area of a Microsoft Excel chart.
				return _( "Plot area, inside height: {plotAreaInsideHeight:.0f}, inside width: {plotAreaInsideWidth:.0f}, inside top: {plotAreaInsideTop:.0f}, inside left: {plotAreaInsideLeft:.0f}").format ( plotAreaInsideHeight = self.excelChartObject.PlotArea.InsideHeight , plotAreaInsideWidth = self.excelChartObject.PlotArea.InsideWidth , plotAreaInsideTop = self.excelChartObject.PlotArea.InsideTop , plotAreaInsideLeft = self.excelChartObject.PlotArea.InsideLeft )
			else:
				# Translators: Indicates the plot area of a Microsoft Excel chart.
				return _( "Plot area " )

class ExcelChartElementLegend(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementLegend , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlLegend:
			if self.excelChartObject.HasLegend:
				# Translators: Indicates the legend in a Microsoft Excel chart.
				# See https://support.office.com/en-us/article/Excel-Glossary-53b6ce43-1a9f-4ac2-a33c-d6f64ea2d1fc?CorrelationId=44f003e6-453a-4b14-a9a6-3fb5287109c7&ui=en-US&rs=en-US&ad=US
				return _( "Legend" ) 
			else:
				# Translators: Indicates that there is no legend in a Microsoft Excel chart.
				return _( "No legend" )

class ExcelChartElementLegendEntry(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementLegendEntry , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlLegendEntry:
			# Translators: Details about a legend entry for a series in a Microsoft Excel chart.
			# For example, this might report "Legend entry for series Temperature 1 of 2"
			return _( "Legend entry for series {seriesName} {seriesIndex} of {seriesCount}").format( seriesName = self.excelChartObject.SeriesCollection(arg1).Name , seriesIndex = arg1 , seriesCount = self.excelChartObject.SeriesCollection().Count ) 

class ExcelChartElementLegendKey(ExcelChartElementBase):

	def __init__(self, windowHandle=None , excelChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( ExcelChartElementLegendKey , self ).__init__( windowHandle=windowHandle , excelChartObject=excelChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlLegendKey:
			# Translators: Details about a legend key for a series in a Microsoft Excel chart.
			# For example, this might report "Legend key for series Temperature 1 of 2"
			# See https://support.office.com/en-us/article/Excel-Glossary-53b6ce43-1a9f-4ac2-a33c-d6f64ea2d1fc?CorrelationId=44f003e6-453a-4b14-a9a6-3fb5287109c7&ui=en-US&rs=en-US&ad=US
			return _( "Legend key for Series {seriesName} {seriesIndex} of {seriesCount}").format( seriesName = self.excelChartObject.SeriesCollection(arg1).Name , seriesIndex = arg1 , seriesCount = self.excelChartObject.SeriesCollection().Count )
