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
from _msOfficeChartConstants import *

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
			selectedChartElement = OfficeChartElementAxis( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlAxisTitle:  
			selectedChartElement = OfficeChartElementAxisTitle( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlSeries:
			selectedChartElement = OfficeChartElementSeries( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlTrendline:
			selectedChartElement = OfficeChartElementTrendline( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlChartTitle:
			selectedChartElement = OfficeChartElementChartTitle( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlChartArea:
			selectedChartElement = OfficeChartElementChartArea( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlPlotArea:
			selectedChartElement = OfficeChartElementPlotArea( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlLegend:
			selectedChartElement = OfficeChartElementLegend( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlLegendEntry:
			selectedChartElement = OfficeChartElementLegendEntry( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		elif ElementID == xlLegendKey:
			selectedChartElement = OfficeChartElementLegendKey( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )
		else:
			selectedChartElement = OfficeChartElementBase( windowHandle= self.windowHandle , officeChartObject= self.excelChartObject  , elementID=ElementID  , arg1=arg1 , arg2=arg2 )

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

		# end class ExcelChartEventHandler
		