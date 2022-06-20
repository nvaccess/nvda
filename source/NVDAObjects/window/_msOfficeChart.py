# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2014-2021 NV Access Limited, NVDA India, dineshkaushal
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import eventHandler
import ui
from . import Window
import ctypes
import math
import controlTypes
import colors
import inputCore
import re
from logHandler import log
import browseMode
from scriptHandler import script


#This file contains chart constants common to Chart Object for Microsoft Office.

#definitions 
xlListSeparator = 5

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

# Chart types in Microsoft Office.
xl3DArea = -4098
xl3DAreaStacked    = 78
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
    # Translators: A type of chart in Microsoft Office. 
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DArea : _( "3D Area" ),
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DAreaStacked : _( "3D Stacked Area" ),
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DAreaStacked100 : _( "100 percent Stacked Area" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DBarClustered : _( "3D Clustered Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DBarStacked : _( "3D Stacked Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DBarStacked100 : _( "3D 100 percent Stacked Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DColumn : _( "3D Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DColumnClustered : _( "3D Clustered Column" ),
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DColumnStacked : _( "3D Stacked Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DColumnStacked100 : _( "3D 100 percent Stacked Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DLine : _( "3D Line" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DPie : _( "3D Pie" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xl3DPieExploded : _( "Exploded 3D Pie" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlArea : _( "Area" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlAreaStacked : _( "Stacked Area" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlAreaStacked100 : _( "100 percent Stacked Area" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlBarClustered : _( "Clustered Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlBarOfPie : _( "Bar of Pie" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlBarStacked : _( "Stacked Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlBarStacked100 : _( "100 percent Stacked Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlBubble : _( "Bubble" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlBubble3DEffect : _( "Bubble with 3D effects" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlColumnClustered : _( "Clustered Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlColumnStacked : _( "Stacked Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlColumnStacked100 : _( "100 percent Stacked Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlConeBarClustered : _( "Clustered Cone Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlConeBarStacked : _( "Stacked Cone Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlConeBarStacked100 : _( "100 percent Stacked Cone Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlConeCol : _( "3D Cone Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlConeColClustered : _( "Clustered Cone Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlConeColStacked : _( "Stacked Cone Column" ),
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlConeColStacked100 : _( "100 percent Stacked Cone Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlCylinderBarClustered : _( "Clustered Cylinder Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlCylinderBarStacked : _( "Stacked Cylinder Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlCylinderBarStacked100 : _( "100 percent Stacked Cylinder Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlCylinderCol : _( "3D Cylinder Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlCylinderColClustered : _( "Clustered Cone Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlCylinderColStacked : _( "Stacked Cone Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlCylinderColStacked100 : _( "100 percent Stacked Cylinder Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlDoughnut : _( "Doughnut" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlDoughnutExploded : _( "Exploded Doughnut" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlLine : _( "Line" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlLineMarkers : _( "Line with Markers" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlLineMarkersStacked : _( "Stacked Line with Markers" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlLineMarkersStacked100 : _( "100 percent Stacked Line with Markers" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlLineStacked : _( "Stacked Line" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlLineStacked100 : _( "100 percent Stacked Line" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlPie : _( "Pie" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlPieExploded : _( "Exploded Pie" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlPieOfPie : _( "Pie of Pie" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlPyramidBarClustered : _( "Clustered Pyramid Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlPyramidBarStacked : _( "Stacked Pyramid Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlPyramidBarStacked100 : _( "100 percent Stacked Pyramid Bar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlPyramidCol : _( "3D Pyramid Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlPyramidColClustered : _( "Clustered Pyramid Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlPyramidColStacked : _( "Stacked Pyramid Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-b22a8bb9-a673-4d7f-b481-aa747c48eb3d
    xlPyramidColStacked100 : _( "100 percent Stacked Pyramid Column" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlRadar : _( "Radar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlRadarFilled : _( "Filled Radar" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlRadarMarkers : _( "Radar with Data Markers" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlStockHLC : _( "High-Low-Close" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlStockOHLC : _( "Open-High-Low-Close" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlStockVHLC : _( "Volume-High-Low-Close" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlStockVOHLC : _( "Volume-Open-High-Low-Close" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlSurface : _( "3D Surface" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlSurfaceTopView : _( "Surface (Top View)" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlSurfaceTopViewWireframe : _( "Surface (Top View wireframe)" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlSurfaceWireframe : _( "3D Surface (wireframe)" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlXYScatter : _( "Scatter" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlXYScatterLines : _( "Scatter with Lines" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlXYScatterLinesNoMarkers : _( "Scatter with Lines and No Data Markers" ) ,
    # Translators: A type of chart in Microsoft Office.
    # See https://support.office.com/en-in/article/Available-chart-types-a019c053-ba7f-4c46-a09a-82e17f3ee5be
    xlXYScatterSmooth : _( "Scatter with Smoothed Lines" ) ,
    # Translators: A type of chart in Microsoft Office.
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

#XlTrendlineType Enumeration for Charts in Word
xlExponential=5
xlLinear=-4132
xlLogarithmic=-4133
xlMovingAvg=6
xlPolynomial=3
xlPower=4

class OfficeChartElementBase(Window):

	#used for deciding whether to report extra information for chart or plot areas
	reportExtraInfo = False

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		self.officeChartObject = officeChartObject
		self.elementID = elementID 
		self.arg1 = arg1
		self.arg2 = arg2
		super(OfficeChartElementBase ,self).__init__(windowHandle=windowHandle)

	def GetChartSegment(self):
		chartType = self.officeChartObject.ChartType
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
		return controlTypes.Role.UNKNOWN

	def _get_name(self):
		return self._getChartElementText(self.elementID , self.arg1 , self.arg2 , self.reportExtraInfo )

	def select(self):
		"""used to activate specific element in the office application"""
		raise NotImplementedError
		
	def script_reportCurrentChartElementWithExtraInfo(self,gesture):
		ui.message( self._getChartElementText(self.elementID , self.arg1 , self.arg2 , True ) )

	def script_reportCurrentChartElementColor(self,gesture):
		if self.elementID == xlSeries:
			if self.arg2 == -1:
				ui.message ( _( "Series color: {colorName} ").format(colorName=colors.RGB.fromCOLORREF(int( self.officeChartObject.SeriesCollection( self.arg1 ).Interior.Color ) ).name  ) )

	ELEMENT_IDS = {
		# Translators: A type of element in a Microsoft Office chart.
		xlDisplayUnitLabel:  _("Display Unit Label"),
		# Translators: A type of element in a Microsoft Office chart.
		xlMajorGridlines:  _("Major Gridlines"),
		# Translators: A type of element in a Microsoft Office chart.
		xlMinorGridlines: _("Minor Gridlines"),
		# Translators: A type of element in a Microsoft Office chart.
		xlPivotChartDropZone: _("Pivot Chart Drop Zone"),
		# Translators: A type of element in a Microsoft Office chart.
		xlPivotChartFieldButton: _("Pivot Chart Field Button"),
		# Translators: A type of element in a Microsoft Office chart.
		xlDownBars: _("Down Bars"),
		# Translators: A type of element in a Microsoft Office chart.
		xlDropLines: _("Drop Lines"),
		# Translators: A type of element in a Microsoft Office chart.
		xlHiLoLines:  _("Hi Lo Lines"),
		# Translators: A type of element in a Microsoft Office chart.
		xlRadarAxisLabels: _("Radar Axis Labels"),
		# Translators: A type of element in a Microsoft Office chart.
		xlSeriesLines: _("Series Lines"),
		# Translators: A type of element in a Microsoft Office chart.
		xlUpBars: _("Up Bars"),
		# Translators: A type of element in a Microsoft Office chart.
		xlCorners: _("Corners"),
		# Translators: A type of element in a Microsoft Office chart.
		xlDataTable: _("Data Table"),
		# Translators: A type of element in a Microsoft Office chart.
		xlFloor:  _("Floor"),
		# Translators: A type of element in a Microsoft Office chart.
		xlNothing: _("Nothing"),
		# Translators: A type of element in a Microsoft Office chart.
		xlWalls: _("Walls"),
		# Translators: A type of element in a Microsoft Office chart.
		xlDataLabel: _("Data Label"),
		# Translators: A type of element in a Microsoft Office chart.
		xlErrorBars: _("Error Bars"),
		# Translators: A type of element in a Microsoft Office chart.
		xlXErrorBars: _("X Error Bars"),
		# Translators: A type of element in a Microsoft Office chart.
		xlYErrorBars: _("Y Error Bars"),
		# Translators: A type of element in a Microsoft Office chart.
		xlShape: _("Shape"),
	}
	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		return self.ELEMENT_IDS[ElementID]

	__gestures = {
		"kb:NVDA+d" : "reportCurrentChartElementWithExtraInfo",
		"kb:NVDA+f" : "reportCurrentChartElementColor",
	}

class OfficeChartElementList(Window):

	def __init__(self, windowHandle , officeChartObject , elementID=None  , arg1=None , arg2=None ):
		self.officeChartObject = officeChartObject
		self.elementList = []
		self.activeElement = None	
		super(OfficeChartElementList,self).__init__(windowHandle=windowHandle )

	def addElement(self , element , parent):
		element.parent = parent
		self.elementList.append(element)
		elementCount = len(self.elementList)

		if( elementCount > 1):
			self.elementList[ elementCount - 2 ].next= self.elementList[ elementCount -1]    
			self.elementList[ elementCount  -1].previous= self.elementList[ elementCount - 2 ]

		self.elementList[0].previous = self.elementList[ elementCount -1]    
		self.elementList[ elementCount -1].next = self.elementList[0]

	def navigateToElement(self, direction):
		if len(self.elementList) == 0: 
			ui.message(self.name)
		else:
			if self.activeElement == None: self.activeElement = self.elementList[0]
			else: 
				if direction=="previous": self.activeElement = self.activeElement.previous
				elif direction=="next": self.activeElement = self.activeElement.next
			self.activeElement.select() 
			eventHandler.queueEvent("gainFocus", self.activeElement)
							
	def script_previousElement(self,gesture):
		self.navigateToElement("previous")
	script_previousElement.canPropagate=True
	
	def script_nextElement(self,gesture):
		self.navigateToElement("next")
	script_nextElement.canPropagate=True

	__gestures = {
				"kb(laptop):leftArrow":"previousElement",
				"kb(desktop):leftArrow":"previousElement",
				"kb(laptop):rightArrow":"nextElement",
				"kb(desktop):rightArrow":"nextElement",
	}

class OfficeChart(OfficeChartElementList):

	role=controlTypes.Role.CHART

	def __init__(self,windowHandle, officeApplicationObject, officeChartObject, initialDocument , keyIndex=0):
		super(OfficeChart,self).__init__(windowHandle=windowHandle  , officeChartObject = officeChartObject )
		self.initialDocument = initialDocument 
		self.parent=initialDocument
		self.officeApplicationObject=officeApplicationObject
		try:
			seriesCount=self.officeChartObject.SeriesCollection().Count
		except:
			seriesCount=None
		if seriesCount:
			for i in range(seriesCount):
				self.addElement( OfficeChartElementSeries(windowHandle=self.windowHandle, officeChartObject = self.officeChartObject , elementID = xlSeries , arg1 = i +1 ) , self) 

		self.addElement( OfficeChartElementCollection(windowHandle=self.windowHandle, officeChartObject = self.officeChartObject ) , self )
		try:
			self.officeChartObject.Select()
		except:
			pass		
		
	def _get_name(self):
		if self.officeChartObject.HasTitle:
			name=self.officeChartObject.ChartTitle.Text
		else:
			name=self.officeChartObject.Name
		#find the type of the chart
		chartType = self.officeChartObject.ChartType
		chartTypeText = chartTypeDict.get(chartType,
                # Translators: Reported when the type of a chart is not known.
                                _("unknown"))
		# Translators: Message reporting the title and type of a chart.
		text=_("Chart title: {chartTitle}, type: {chartType}").format(chartTitle=name, chartType=chartTypeText)
		return text

	def _get_description(self):
		count = self.officeChartObject.SeriesCollection().count
		text=""
		if count>0:
			if count == 1:
				# Translators: Indicates that there is 1 series in a chart.
				seriesValueString = _( "There is 1 series in this chart" )
			else:
				# Translators: Indicates the number of series in a chart where there are multiple series.
				seriesValueString = _( "There are total %d series in this chart" ) %(count)
				for i in range(1, count+1):
					# Translators: Specifies the number and name of a series when listing series in a chart.
					seriesValueString += ", " + _("series {number} {name}").format(number=i, name=self.officeChartObject.SeriesCollection(i).Name)
				text += seriesValueString
		else:
			# Translators: Indicates that there are no series in a chart.
			text +=_("No Series defined.")
		return text

	@script(
		description=_(
			# Translators: Input help mode message for toggle focus and browse mode command
			# in web browsing and other situations.
			"Toggles between browse mode and focus mode."
			" When in focus mode, keys will pass straight through to the application, "
			"allowing you to interact directly with a control. "
			"When in browse mode, you can navigate the document with the cursor, quick navigation keys, etc."
		),
		category=inputCore.SCRCAT_BROWSEMODE,
		gestures=("kb:enter", "kb(desktop):numpadEnter", "kb:space")
	)
	def script_activatePosition(self, gesture):
		# Toggle browse mode pass-through.
		self.passThrough = True
		self.ignoreTreeInterceptorPassThrough=False
		browseMode.reportPassThrough(self)

	def script_disablePassThrough(self, gesture):
		log.debugWarning("script_disablePassThrough")
		self.initialDocument.focusOnActiveDocument(self.officeChartObject) 
	script_disablePassThrough.canPropagate=True

	__gestures = {
				"kb:upArrow":"previousElement",
				"kb:downArrow":"nextElement",
				"kb:escape": "disablePassThrough",
	}

class OfficeChartElementCollection(OfficeChartElementList):

	role=controlTypes.Role.CHARTELEMENT
	description=None

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( OfficeChartElementCollection ,self).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )
		if officeChartObject.HasTitle:
			self.addElement(OfficeChartElementChartTitle(windowHandle = windowHandle, officeChartObject = officeChartObject ) , self )

		axisAndAxisTitles = OfficeChartElementAxis.getAvailableAxisAndAxisTitle(windowHandle, officeChartObject )
		for item in axisAndAxisTitles:
			self.addElement( item , self)

		chartAreaObject = OfficeChartElementChartArea(windowHandle=self.windowHandle,  officeChartObject = officeChartObject ) 
		chartAreaObject.reportExtraInfo = True
		self.addElement( chartAreaObject , self )
		plotAreaObject = OfficeChartElementPlotArea(windowHandle=self.windowHandle,  officeChartObject = officeChartObject ) 
		plotAreaObject.reportExtraInfo = True
		self.addElement( plotAreaObject , self )

		if officeChartObject.HasLegend:
			self.addElement(OfficeChartElementLegend(windowHandle=self.windowHandle,  officeChartObject = officeChartObject ) , self )

			self.legendEntryCount = self.officeChartObject.Legend.LegendEntries().Count
			for legendEntryIndex in range( 1 , self.legendEntryCount  + 1 ) :
				legendEntry = OfficeChartElementLegendEntry(windowHandle=self.windowHandle,  officeChartObject = self.officeChartObject ,  elementID= xlLegendEntry ,  arg1 = legendEntryIndex , arg2 = self.legendEntryCount ) 
				legendEntry.eventDriven = False
				self.addElement ( legendEntry , self )

		if officeChartObject.HasDataTable:
			self.addElement(OfficeChartElementDataTable(windowHandle=self.windowHandle,  officeChartObject = officeChartObject ) , self )

	def _get_name(self):
		#Translators: Speak text chart elements when virtual row of chart elements is reached while navigation
		return _("Chart Elements")

	def select(self):
		pass

class OfficeChartElementSeries(OfficeChartElementList):

	description=None
	role=controlTypes.Role.CHARTELEMENT

	def __init__(self,windowHandle, officeChartObject , elementID , arg1 = None , arg2= None   ):
		super(OfficeChartElementSeries,self).__init__( windowHandle=windowHandle , officeChartObject = officeChartObject ) 
		self.elementID=elementID 
		self.seriesIndex=arg1
		self.currentPointIndex=arg2
		self.seriesCount=self.officeChartObject.SeriesCollection().Count
		self.pointsCollection=self.officeChartObject.SeriesCollection(self.seriesIndex).Points()
		self.pointsCount=self.pointsCollection.Count

		for pointIndex in range(1,self.pointsCount +1) :
			self.addElement ( OfficeChartElementPoint(windowHandle=self.windowHandle,  officeChartObject = self.officeChartObject ,  elementID= xlSeries, arg1 =self.seriesIndex, arg2 =pointIndex) , self )

		self.trendlinesCount = self.officeChartObject.SeriesCollection(self.seriesIndex).Trendlines().Count
		for trendlineIndex in range( 1 , self.trendlinesCount + 1 ) :
			self.addElement ( OfficeChartElementTrendline(windowHandle=self.windowHandle,  officeChartObject = self.officeChartObject ,  elementID= xlTrendline ,  arg1 = self.seriesIndex , arg2 = trendlineIndex ) , self )
	
	def _get_name(self):
		currentSeries=self.officeChartObject.SeriesCollection(self.seriesIndex)
		# Translators: Details about a series in a chart. For example, this might report "foo series 1 of 2"
		seriesText=_("{seriesName} series {seriesIndex} of {seriesCount}").format( seriesName = self.officeChartObject.SeriesCollection(self.seriesIndex).Name , seriesIndex = self.seriesIndex , seriesCount = self.seriesCount )
		return seriesText

	def select(self):
		self.officeChartObject.SeriesCollection(self.seriesIndex).Select()

	def script_reportColor(self, gesture):
		if self.officeChartObject.ChartType in (xlPie, xlPieExploded, xlPieOfPie):
			#Translators: Message to be spoken to report Slice Color in Pie Chart
			ui.message ( _( "Slice color: {colorName} ").format(colorName=colors.RGB.fromCOLORREF(int( self.officeChartObject.SeriesCollection( self.seriesIndex ).Points(self.currentPointIndex).Format.Fill.ForeColor.RGB) ).name  ) )
		else:
			#Translators: Message to be spoken to report Series Color
			ui.message ( _( "Series color: {colorName} ").format(colorName=colors.RGB.fromCOLORREF(int( self.officeChartObject.SeriesCollection( self.seriesIndex ).Interior.Color ) ).name  ) )

	__gestures = {
				"kb:NVDA+5": "reportColor",
	}

class OfficeChartElementPoint(OfficeChartElementBase):

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super(OfficeChartElementPoint ,self).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlSeries:
			if arg2 == -1:
				# Translators: Details about a series in a chart.
				# For example, this might report "foo series 1 of 2"
				return _( "{seriesName} series {seriesIndex} of {seriesCount}").format( seriesName = self.officeChartObject.SeriesCollection(arg1).Name , seriesIndex = arg1 , seriesCount = self.officeChartObject.SeriesCollection().Count )
			else:
				if self.officeChartObject.Application.name == "Microsoft Excel": 
					# get the formula string and split it on comma separator to obtain range.
	# the formula should be in the form SERIES(name_ref, categories, values, plot_order
					listSeparator = self.officeChartObject.Application.International(xlListSeparator) 
					formulas = self.officeChartObject.SeriesCollection(arg1).Formula.split(listSeparator ) 
					if len(formulas) == 4:
						chartSeriesXValue = self.officeChartObject.Application.Range(formulas[1]).Rows[arg2].Text
					else:
						chartSeriesXValue = self.officeChartObject.SeriesCollection(arg1).XValues[arg2 - 1] 
				else:
					chartSeriesXValue = self.officeChartObject.SeriesCollection(arg1).XValues[arg2 - 1] 

				output=""
				if self.officeChartObject.ChartType in (xlLine, xlLineMarkers , xlLineMarkersStacked, xlLineMarkersStacked100, xlLineStacked, xlLineStacked100):
					if arg2 > 1:

						if self.officeChartObject.SeriesCollection(arg1).Values[arg2 - 1] == self.officeChartObject.SeriesCollection(arg1).Values[arg2 - 2]: 
							# Translators: For line charts, indicates no change from the previous data point on the left
							output += _( "no change from point {previousIndex}, ").format( previousIndex = arg2 - 1 )
						elif self.officeChartObject.SeriesCollection(arg1).Values[arg2 - 1] > self.officeChartObject.SeriesCollection(arg1).Values[arg2 - 2]: 
							# Translators: For line charts, indicates an increase from the previous data point on the left
							output += _( "Increased by {incrementValue} from point {previousIndex}, ").format( incrementValue = self.officeChartObject.SeriesCollection(arg1).Values[arg2 - 1] - self.officeChartObject.SeriesCollection(arg1).Values[arg2 - 2] , previousIndex = arg2 - 1 ) 
						else:
							# Translators: For line charts, indicates a decrease from the previous data point on the left
							output += _( "decreased by {decrementValue} from point {previousIndex}, ").format( decrementValue = self.officeChartObject.SeriesCollection(arg1).Values[arg2 - 2] - self.officeChartObject.SeriesCollection(arg1).Values[arg2 - 1] , previousIndex = arg2 - 1 ) 

				if self.officeChartObject.HasAxis(xlCategory) and self.officeChartObject.Axes(xlCategory).HasTitle:
					# Translators: Specifies the category of a data point.
					# {categoryAxisTitle} will be replaced with the title of the category axis; e.g. "Month".
					# {categoryAxisData} will be replaced with the category itself; e.g. "January".
					output += _( "{categoryAxisTitle} {categoryAxisData}: ").format( categoryAxisTitle = self.officeChartObject.Axes(xlCategory).AxisTitle.Text , categoryAxisData = chartSeriesXValue ) 
				else:
					# Translators: Specifies the category of a data point.
					# {categoryAxisData} will be replaced with the category itself; e.g. "January".
					output += _( "Category {categoryAxisData}: ").format( categoryAxisData = chartSeriesXValue ) 

				if self.officeChartObject.HasAxis(xlValue) and self.officeChartObject.Axes(xlValue).HasTitle:
					# Translators: Specifies the value of a data point.
					# {valueAxisTitle} will be replaced with the title of the value axis; e.g. "Amount".
					# {valueAxisData} will be replaced with the value itself; e.g. "1000".
					output +=  _( "{valueAxisTitle} {valueAxisData}").format( valueAxisTitle = self.officeChartObject.Axes(xlValue).AxisTitle.Text , valueAxisData = self.officeChartObject.SeriesCollection(arg1).Values[arg2-1]) 
				else:
					# Translators: Specifies the value of a data point.
					# {valueAxisData} will be replaced with the value itself; e.g. "1000".
					output +=  _( "value {valueAxisData}").format( valueAxisData = self.officeChartObject.SeriesCollection(arg1).Values[arg2-1]) 

				if self.officeChartObject.ChartType in (xlPie, xlPieExploded, xlPieOfPie):
					total = math.fsum( self.officeChartObject.SeriesCollection(arg1).Values ) 
					# Translators: Details about a slice of a pie chart.
					# For example, this might report "fraction 25.25 percent slice 1 of 5"
					output += _( " fraction {fractionValue:.2f} Percent slice {pointIndex} of {pointCount}").format( fractionValue = self.officeChartObject.SeriesCollection(arg1).Values[arg2-1] / total *100.00 , pointIndex = arg2 , pointCount = len( self.officeChartObject.SeriesCollection(arg1).Values ) )
				else:
					# Translators: Details about a segment of a chart.
					# For example, this might report "column 1 of 5"
					output += _( " {segmentType} {pointIndex} of {pointCount}").format( segmentType = self.GetChartSegment() ,  pointIndex = arg2 , pointCount = len( self.officeChartObject.SeriesCollection(arg1).Values ) )

				return  output 

	def select(self):
		if self.arg2 != -1:
			self.officeChartObject.SeriesCollection(self.arg1).Points(self.arg2).Select()

class OfficeChartElementAxis(OfficeChartElementBase):

	_axisMap={
				xlCategory: {
													# Translators: Indicates Primary Category Axis
													xlPrimary: _("Primary Category Axis"),
													# Translators: Indicates Secondary Category Axis
													xlSecondary: _("Secondary Category Axis")},
				xlValue: {
													# Translators: Indicates Primary Value Axis
													xlPrimary: _("Primary Value Axis"),
													# Translators: Indicates Secondary Value Axis
													xlSecondary: _("Secondary Value Axis")},
				xlSeriesAxis: {
													# Translators: Indicates Primary Series Axis
													xlPrimary: _("Primary Series Axis"),
													# Translators: Indicates Secondary Series Axis
													xlSecondary: _("Secondary Series Axis")}
	}

	@classmethod
	def getAvailableAxisAndAxisTitle( cls , windowHandle , tempChartObject ):
		listOfChartAxis = []
		for axisType in [xlCategory, xlValue, xlSeriesAxis]:
			for axisGroup in [xlPrimary, xlSecondary]:
				if tempChartObject.HasAxis(axisType, axisGroup): 
					listOfChartAxis.append(OfficeChartElementAxis(windowHandle = windowHandle , officeChartObject = tempChartObject , elementID = xlAxis , arg1 = axisType , arg2 = axisGroup))
					if(tempChartObject.Axes(axisType, axisGroup).HasTitle):
						listOfChartAxis.append(OfficeChartElementAxisTitle(windowHandle = windowHandle , officeChartObject = tempChartObject , elementID = xlAxisTitle , arg1 = axisType , arg2 = axisGroup))
		return listOfChartAxis

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		self.axisGroup = arg1
		self.axisType = arg2
		super( OfficeChartElementAxis , self ).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		return self._axisMap[self.axisType][self.axisGroup]

	def select(self):
		self.officeChartObject.Axes( self.axisType , self.axisGroup ).Select()

class OfficeChartElementAxisTitle( OfficeChartElementAxis ):

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( OfficeChartElementAxisTitle , self ).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		# Translators: Indicates a chart axis title in Microsoft Office.
		axisTitle = super(OfficeChartElementAxisTitle , self)._getChartElementText(ElementID , arg1 , arg2 )
		if self.officeChartObject.HasAxis( arg2 , arg1 ) and self.officeChartObject.Axes( arg2 , arg1 ).HasTitle:
			# Translators: the title of a chart axis 
			axisTitle += _(" title: {axisTitle}").format( axisTitle = self.officeChartObject.Axes(self.axisType, self.axisGroup).AxisTitle.Text)
		return  axisTitle 

	def select(self):
		self.officeChartObject.Axes( self.axisType , self.axisGroup ).AxisTitle.Select()

class OfficeChartElementTrendline( OfficeChartElementBase):

	_trendlineTypeMap = {
								# Translators: Indicates that trendline type is Exponential
								xlExponential: _("Exponential"),
								# Translators: Indicates that trendline type is Linear
								xlLinear: _("Linear"),
								# Translators: Indicates that trendline type is Logarithmic
								xlLogarithmic: _("Logarithmic"),
								# Translators: Indicates that trendline type is Moving Average
								xlMovingAvg: _("Moving Average"),
								# Translators: Indicates that trendline type is Polynomial
								xlPolynomial: _("Polynomial"),
								# Translators: Indicates that trendline type is Power
								xlPower: _("Power") 
	}

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		self.seriesIndex = arg1
		self.trendlineIndex = arg2
		self.currentTrendline = officeChartObject.SeriesCollection(self.seriesIndex).Trendlines(self.trendlineIndex)
		super( OfficeChartElementTrendline , self ).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if self.currentTrendline.DisplayEquation or self.currentTrendline.DisplayRSquared:
			label=self.currentTrendline.DataLabel.Text
			#Translators: Substitute superscript two by square for R square value
			label=label.replace(u"²", _( " square " ))
			label=re.sub(r'([a-zA-Z]+)([2])',r'\1 square', label)
			label=re.sub(r'([a-zA-Z]+)([3])',r'\1 cube', label)
			label=re.sub(r'([a-zA-Z]+)([-]*[04-9][0-9]*)',r'\1 to the power \2', label)
			#Translators: Substitute - by minus in trendline equations.
			label=label.replace(u"-",_(" minus "))
			# Translators: This message gives trendline type and name for selected series
			output=_("{seriesName} trendline type: {trendlineType}, name: {trendlineName}, label: {trendlineLabel} ").format(seriesName=self.officeChartObject.SeriesCollection(self.seriesIndex).Name, trendlineType=self._trendlineTypeMap[self.currentTrendline.Type], trendlineName=self.currentTrendline.Name, trendlineLabel=label)
		else:
			# Translators: This message gives trendline type and name for selected series
			output=_("{seriesName} trendline type: {trendlineType}, name: {trendlineName} ").format(seriesName=self.officeChartObject.SeriesCollection(self.seriesIndex).Name, trendlineType=self._trendlineTypeMap[self.currentTrendline.Type], trendlineName=self.currentTrendline.Name)
		return output

	def select(self):
		self.currentTrendline.Select() 

class OfficeChartElementChartTitle( OfficeChartElementBase):

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( OfficeChartElementChartTitle , self ).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if self.officeChartObject.HasTitle:
			# Translators: Details about a chart title in Microsoft Office.
			return _( "Chart title: {chartTitle}").format ( chartTitle = self.officeChartObject.ChartTitle.Text )
		else:
				# Translators: Indicates an untitled chart in Microsoft Office.
			return _( "Untitled chart" )

	def select(self):
		self.officeChartObject.ChartTitle.Select()

class OfficeChartElementChartArea( OfficeChartElementBase):

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( OfficeChartElementChartArea , self ).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if reportExtraInfo:
			# Translators: Details about the chart area in a Microsoft Office chart.
			return _( "Chart area, height: {chartAreaHeight}, width: {chartAreaWidth}, top: {chartAreaTop}, left: {chartAreaLeft}").format ( chartAreaHeight = self.officeChartObject.ChartArea.Height , chartAreaWidth = self.officeChartObject.ChartArea.Width , chartAreaTop = self.officeChartObject.ChartArea.Top , chartAreaLeft = self.officeChartObject.ChartArea.Left)
		else:
			# Translators: Indicates the chart area of a Microsoft Office chart.
			return _( "Chart area ")

	def select(self):
		self.officeChartObject.ChartArea.Select()

class OfficeChartElementPlotArea( OfficeChartElementBase):

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( OfficeChartElementPlotArea , self ).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if reportExtraInfo:
			# useing {:.0f} to remove fractions
			# Translators: Details about the plot area of a Microsoft Office chart.
			return _( "Plot area, inside height: {plotAreaInsideHeight:.0f}, inside width: {plotAreaInsideWidth:.0f}, inside top: {plotAreaInsideTop:.0f}, inside left: {plotAreaInsideLeft:.0f}").format ( plotAreaInsideHeight = self.officeChartObject.PlotArea.InsideHeight , plotAreaInsideWidth = self.officeChartObject.PlotArea.InsideWidth , plotAreaInsideTop = self.officeChartObject.PlotArea.InsideTop , plotAreaInsideLeft = self.officeChartObject.PlotArea.InsideLeft )
		else:
			# Translators: Indicates the plot area of a Microsoft Office chart.
			return _( "Plot area " )

	def select(self):
		self.officeChartObject.PlotArea.Select()

class OfficeChartElementLegend( OfficeChartElementBase):

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		self.chartLegend = officeChartObject.Legend
		super( OfficeChartElementLegend , self ).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		return self.chartLegend.Name

	def select(self):
		self.chartLegend.Select() 

class OfficeChartElementLegendEntry( OfficeChartElementBase):

	eventDriven = True

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		if self.eventDriven:
			self.legendEntry = officeChartObject.Legend.LegendEntries(arg1)
		super( OfficeChartElementLegendEntry , self ).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		# Translators: Details about a legend entry for a series in a Microsoft Office chart.
		# For example, this might report "Legend entry for series Temperature 1 of 2"
		if self.eventDriven:
			# Translators: a message for the legend entry of a chart in MS Office
			return _( "Legend entry for series {seriesName} {seriesIndex} of {seriesCount}").format( seriesName = self.officeChartObject.SeriesCollection(arg1).Name , seriesIndex = arg1 , seriesCount = self.officeChartObject.SeriesCollection().Count ) 
		else:
			# Translators: the legend entry for a chart in Microsoft Office
			return _( "Legend entry {legendEntryIndex} of {legendEntryCount}").format( legendEntryIndex = arg1 , legendEntryCount = arg2 ) 

	def select(self):
		if self.eventDriven:
			self.legendEntry.Select() 

class OfficeChartElementLegendKey( OfficeChartElementBase):

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super( OfficeChartElementLegendKey , self ).__init__( windowHandle=windowHandle , officeChartObject=officeChartObject , elementID=elementID , arg1=arg1 , arg2=arg2 )

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		if ElementID == xlLegendKey:
			# Translators: Details about a legend key for a series in a Microsoft office chart.
			# For example, this might report "Legend key for series Temperature 1 of 2"
			# See https://support.office.com/en-us/article/Excel-Glossary-53b6ce43-1a9f-4ac2-a33c-d6f64ea2d1fc?CorrelationId=44f003e6-453a-4b14-a9a6-3fb5287109c7&ui=en-US&rs=en-US&ad=US
			return _( "Legend key for Series {seriesName} {seriesIndex} of {seriesCount}").format( seriesName = self.officeChartObject.SeriesCollection(arg1).Name , seriesIndex = arg1 , seriesCount = self.officeChartObject.SeriesCollection().Count )


class OfficeChartElementDataTable( OfficeChartElementBase):

	def __init__(self, windowHandle=None , officeChartObject=None   , elementID=None  , arg1=None , arg2=None ):
		super().__init__(
			windowHandle=windowHandle,
			officeChartObject=officeChartObject,
			elementID=elementID,
			arg1=arg1,
			arg2=arg2
		)

	def _getChartElementText(self, ElementID ,arg1,arg2 , reportExtraInfo=False ):
		#Translators: Data Table will be spoken when chart element Data Table is selected
		return _("Data Table")

	def select(self):
		self.officeChartObject.DataTable.Select()
