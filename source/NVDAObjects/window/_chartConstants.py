#NVDAObjects/window/_chartConstants.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2014-2015 James Teh, Michael Curren, NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

#This file contains chart constants common to Chart Object in MS Word and MS Excel.

# Chart types in Microsoft Excel.
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

#XlTrendlineType Enumeration for Charts in Word
xlExponential=5
xlLinear=-4132
xlLogarithmic=-4133
xlMovingAvg=6
xlPolynomial=3
xlPower=4
