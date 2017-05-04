#NVDAObjects/excel.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2016 NV Access Limited, Dinesh Kaushal, Siddhartha Gupta
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import comtypes.automation
import wx
import time
import winsound
import re
import uuid
import collections
import oleacc
import ui
import speech
from tableUtils import HeaderCellInfo, HeaderCellTracker
import config
import textInfos
import colors
import eventHandler
import api
from logHandler import log
import gui
import winUser
from displayModel import DisplayModelTextInfo
import controlTypes
from . import Window
from .. import NVDAObjectTextInfo
import scriptHandler
import browseMode
import inputCore
import ctypes

xlNone=-4142
xlSimple=-4154
xlExtended=3
xlCenter=-4108
xlJustify=-4130
xlLeft=-4131
xlRight=-4152
xlDistributed=-4117
xlBottom=-4107
xlTop=-4160
xlDown=-4121
xlToLeft=-4159
xlToRight=-4161
xlUp=-4162
xlCellWidthUnitToPixels = 7.5919335705812574139976275207592
xlSheetVisible=-1
alignmentLabels={
	xlCenter:"center",
	xlJustify:"justify",
	xlLeft:"left",
	xlRight:"right",
	xlDistributed:"distributed",
	xlBottom:"botom",
	xlTop:"top",
	1:"default",
}

xlA1 = 1
xlRC = 2
xlUnderlineStyleNone=-4142

#Excel cell types
xlCellTypeAllFormatConditions =-4172      # from enum XlCellType
xlCellTypeAllValidation       =-4174      # from enum XlCellType
xlCellTypeBlanks              =4          # from enum XlCellType
xlCellTypeComments            =-4144      # from enum XlCellType
xlCellTypeConstants           =2          # from enum XlCellType
xlCellTypeFormulas            =-4123      # from enum XlCellType
xlCellTypeLastCell            =11         # from enum XlCellType
xlCellTypeSameFormatConditions=-4173      # from enum XlCellType
xlCellTypeSameValidation      =-4175      # from enum XlCellType
xlCellTypeVisible             =12         # from enum XlCellType
#MsoShapeType Enumeration
msoFormControl=8
msoTextBox=17
#XlFormControl Enumeration
xlButtonControl=0
xlCheckBox=1
xlDropDown=2
xlEditBox=3
xlGroupBox=4
xlLabel=5
xlListBox=6
xlOptionButton=7
xlScrollBar=8
xlSpinner=9
#MsoTriState Enumeration
msoTrue=-1    #True
msoFalse=0    #False
#CheckBox and RadioButton States
checked=1
unchecked=-4146
mixed=2
#LogPixels
LOGPIXELSX=88
LOGPIXELSY=90

#Excel Cell Patterns (from enum XlPattern)
xlPatternAutomatic = -4105
xlPatternChecker = 9
xlPatternCrissCross = 16
xlPatternDown = -4121
xlPatternGray16 = 17
xlPatternGray25 = -4124
xlPatternGray50 = -4125
xlPatternGray75 = -4126
xlPatternGray8 = 18
xlPatternGrid = 15
xlPatternHorizontal = -4128
xlPatternLightDown = 13
xlPatternLightHorizontal = 11
xlPatternLightUp = 14
xlPatternLightVertical = 12
xlPatternNone = -4142
xlPatternSemiGray75 = 10
xlPatternSolid = 1
xlPatternUp = -4162
xlPatternVertical = -4166
xlPatternLinearGradient = 4000
xlPatternRectangularGradient = 4001

backgroundPatternLabels={
		# See https://msdn.microsoft.com/en-us/library/microsoft.office.interop.excel.xlpattern.aspx
		# Translators: A type of background pattern in Microsoft Excel. 
		# Excel controls the pattern.
		xlPatternAutomatic:_("automatic"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Checkerboard
		xlPatternChecker:_("diagonal crosshatch"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Criss-cross lines
		xlPatternCrissCross:_("thin diagonal crosshatch"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Dark diagonal lines running from the upper left to the lower right
		xlPatternDown:_("reverse diagonal stripe"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# 12.5% gray
		# xgettext:no-python-format
		xlPatternGray16:_("12.5% gray"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# 25% gray
		# xgettext:no-python-format
		xlPatternGray25:_("25% gray"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# xgettext:no-python-format
		# 50% gray
		xlPatternGray50:_("50% gray"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# 75% gray
		# xgettext:no-python-format
		xlPatternGray75:_("75% gray"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# 6.25% gray
		# xgettext:no-python-format
		xlPatternGray8:_("6.25% gray"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Grid
		xlPatternGrid:_("thin horizontal crosshatch"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Dark horizontal lines
		xlPatternHorizontal:_("horizontal stripe"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Light diagonal lines running from the upper left to the lower right
		xlPatternLightDown:_("thin reverse diagonal stripe"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Light horizontal lines
		xlPatternLightHorizontal:_("thin horizontal stripe"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Light diagonal lines running from the lower left to the upper right
		xlPatternLightUp:_("thin diagonal stripe"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Light vertical bars
		xlPatternLightVertical:_("thin vertical stripe"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# No pattern
		xlPatternNone:_("none"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# 75% dark moire
		xlPatternSemiGray75:_("thick diagonal crosshatch"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Solid color
		xlPatternSolid:_("solid"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Dark diagonal lines running from the lower left to the upper right
		xlPatternUp:_("diagonal stripe"),
		# Translators: A type of background pattern in Microsoft Excel. 
		# Dark vertical bars
		xlPatternVertical:_("vertical stripe"),
		# Translators: A type of background pattern in Microsoft Excel.
		xlPatternLinearGradient:_("linear gradient"),
		# Translators: A type of background pattern in Microsoft Excel.
		xlPatternRectangularGradient:_("rectangular gradient"),
	}

from excelCellBorder import getCellBorderStyleDescription

re_RC=re.compile(r'R(?:\[(\d+)\])?C(?:\[(\d+)\])?')
re_absRC=re.compile(r'^R(\d+)C(\d+)(?::R(\d+)C(\d+))?$')

class ExcelQuickNavItem(browseMode.QuickNavItem):

	def __init__( self , nodeType , document , itemObject , itemCollection ):
		self.excelItemObject = itemObject
		self.excelItemCollection = itemCollection 
		super( ExcelQuickNavItem ,self).__init__( nodeType , document )

	def activate(self):
		pass

	def isChild(self,parent):
		return False

	def report(self,readUnit=None):
		pass

class ExcelChartQuickNavItem(ExcelQuickNavItem):

	def __init__( self , nodeType , document , chartObject , chartCollection ):
		self.chartIndex = chartObject.Index
		if chartObject.Chart.HasTitle:

			self.label = chartObject.Chart.ChartTitle.Text + " " + chartObject.TopLeftCell.address(False,False,1,False) + "-" + chartObject.BottomRightCell.address(False,False,1,False) 

		else:

			self.label = chartObject.Name + " " + chartObject.TopLeftCell.address(False,False,1,False) + "-" + chartObject.BottomRightCell.address(False,False,1,False) 

		super( ExcelChartQuickNavItem ,self).__init__( nodeType , document , chartObject , chartCollection )

	def __lt__(self,other):
		return self.chartIndex < other.chartIndex

	def moveTo(self):
		try:
			self.excelItemObject.Activate()

			# After activate(), though the chart object is selected, 

			# pressing arrow keys moves the object, rather than 

			# let use go inside for sub-objects. Somehow 
		# calling an COM function on a different object fixes that !

			log.debugWarning( self.excelItemCollection.Count )

		except(COMError):

			pass
		focus=api.getDesktopObject().objectWithFocus()
		if not focus or not isinstance(focus,ExcelBase):
			return
		# Charts are not yet automatically detected with objectFromFocus, so therefore use selection
		sel=focus._getSelection()
		if not sel:
			return
		eventHandler.queueEvent("gainFocus",sel)


	@property
	def isAfterSelection(self):
		activeCell = self.document.Application.ActiveCell
		#log.debugWarning("active row: {} active column: {} current row: {} current column: {}".format ( activeCell.row , activeCell.column , self.excelCommentObject.row , self.excelCommentObject.column   ) )

		if self.excelItemObject.TopLeftCell.row == activeCell.row:
			if self.excelItemObject.TopLeftCell.column > activeCell.column:
				return False
		elif self.excelItemObject.TopLeftCell.row > activeCell.row:
			return False
		return True

class ExcelRangeBasedQuickNavItem(ExcelQuickNavItem):

	def __lt__(self,other):
		if self.excelItemObject.row == other.excelItemObject.row:
			return self.excelItemObject.column < other.excelItemObject.column
		else:
			return self.excelItemObject.row < other.excelItemObject.row

	def moveTo(self):
		self.excelItemObject.Activate()
		eventHandler.queueEvent("gainFocus",api.getDesktopObject().objectWithFocus())

	@property
	def isAfterSelection(self):
		activeCell = self.document.Application.ActiveCell
		log.debugWarning("active row: {} active column: {} current row: {} current column: {}".format ( activeCell.row , activeCell.column , self.excelItemObject.row , self.excelItemObject.column   ) )

		if self.excelItemObject.row == activeCell.row:
			if self.excelItemObject.column > activeCell.column:
				return False
		elif self.excelItemObject.row > activeCell.row:
			return False
		return True

class ExcelCommentQuickNavItem(ExcelRangeBasedQuickNavItem):

	def __init__( self , nodeType , document , commentObject , commentCollection ):
		self.comment=commentObject.comment
		self.label = commentObject.address(False,False,1,False) + " " + (self.comment.Text() if self.comment else "")
		super( ExcelCommentQuickNavItem , self).__init__( nodeType , document , commentObject , commentCollection )

class ExcelFormulaQuickNavItem(ExcelRangeBasedQuickNavItem):

	def __init__( self , nodeType , document , formulaObject , formulaCollection ):
		self.label = formulaObject.address(False,False,1,False) + " " + formulaObject.Formula
		super( ExcelFormulaQuickNavItem , self).__init__( nodeType , document , formulaObject , formulaCollection )

class ExcelQuicknavIterator(object):
	"""
	Allows iterating over an MS excel collection (e.g. Comments, Formulas or charts) emitting L{QuickNavItem} objects.
	"""

	def __init__(self, itemType , document , direction , includeCurrent):
		"""
		See L{QuickNavItemIterator} for itemType, document and direction definitions.
		@ param includeCurrent: if true then any item at the initial position will be also emitted rather than just further ones. 
		"""
		self.document=document
		self.itemType=itemType
		self.direction=direction if direction else "next"
		self.includeCurrent=includeCurrent

	def collectionFromWorksheet(self,worksheetObject):
		"""
		Fetches a Microsoft Excel collection object from a Microsoft excel worksheet object. E.g. charts, comments, or formula.
		@param worksheetObject: a Microsoft excel worksheet object.
		@return: a Microsoft excel collection object.
		"""
		raise NotImplementedError

	def filter(self,item):
		"""
		Only allows certain items fom a collection to be emitted. E.g. a chart .
		@param item: an item from a Microsoft excel collection (e.g. chart object).
		@return True if this item should be allowd, false otherwise.
		@rtype: bool
		"""
		return True

	def iterate(self):
		"""
		returns a generator that emits L{QuickNavItem} objects for this collection.
		"""
		items=self.collectionFromWorksheet(self.document)
		if not items:
			return
		if self.direction=="previous":
			items=reversed(items)
		for collectionItem in items:
			item=self.quickNavItemClass(self.itemType,self.document,collectionItem , items )
			if not self.filter(collectionItem):
				continue
			yield item

class ChartExcelCollectionQuicknavIterator(ExcelQuicknavIterator):
	quickNavItemClass=ExcelChartQuickNavItem#: the QuickNavItem class that should be instanciated and emitted. 
	def collectionFromWorksheet( self , worksheetObject ):
		return worksheetObject.ChartObjects() 

class CommentExcelCollectionQuicknavIterator(ExcelQuicknavIterator):
	quickNavItemClass=ExcelCommentQuickNavItem#: the QuickNavItem class that should be instanciated and emitted. 
	def collectionFromWorksheet( self , worksheetObject ):
		try:
			return  worksheetObject.cells.SpecialCells( xlCellTypeComments )
		except(COMError):
			return None

	def filter(self,item):
		return item is not None and item.comment is not None

class FormulaExcelCollectionQuicknavIterator(ExcelQuicknavIterator):
	quickNavItemClass=ExcelFormulaQuickNavItem#: the QuickNavItem class that should be instanciated and emitted. 
	def collectionFromWorksheet( self , worksheetObject ):
		try:
			return  worksheetObject.cells.SpecialCells( xlCellTypeFormulas )
		except(COMError):

			return None

class ExcelSheetQuickNavItem(ExcelQuickNavItem):

	def __init__( self , nodeType , document , sheetObject , sheetCollection ):
		self.label = sheetObject.Name
		self.sheetIndex = sheetObject.Index
		self.sheetObject = sheetObject
		super( ExcelSheetQuickNavItem , self).__init__( nodeType , document , sheetObject , sheetCollection )

	def __lt__(self,other):
		return self.sheetIndex < other.sheetIndex

	def moveTo(self):
		self.sheetObject.Activate()
		eventHandler.queueEvent("gainFocus",api.getDesktopObject().objectWithFocus())

	def rename(self,newName):
		if newName and newName!=self.label:
			self.sheetObject.Name=newName
			self.label=newName

	@property
	def isRenameAllowed(self):
		return True

	@property
	def isAfterSelection(self):
		activeSheet = self.document.Application.ActiveSheet
		if self.sheetObject.Index <= activeSheet.Index:
			return False
		else:
			return True

class SheetsExcelCollectionQuicknavIterator(ExcelQuicknavIterator):
	"""
	Allows iterating over an MS excel Sheets collection emitting L{QuickNavItem} object.
	"""
	quickNavItemClass=ExcelSheetQuickNavItem#: the QuickNavItem class that should be instantiated and emitted. 
	def collectionFromWorksheet( self , worksheetObject ):
		try:
			return worksheetObject.Application.ActiveWorkbook.sheets
		except(COMError):
			return None

	def filter(self,sheet):
		if sheet.Visible==xlSheetVisible:
			return True

class ExcelBrowseModeTreeInterceptor(browseMode.BrowseModeTreeInterceptor):

	# This treeInterceptor starts in focus mode, thus escape should not switch back to browse mode
	disableAutoPassThrough=True

	def __init__(self,rootNVDAObject):
		super(ExcelBrowseModeTreeInterceptor,self).__init__(rootNVDAObject)
		self.passThrough=True
		browseMode.reportPassThrough.last=True

	def _get_currentNVDAObject(self):
		obj=api.getFocusObject()
		return obj if obj.treeInterceptor is self else None

	def _get_isAlive(self):
		if not winUser.isWindow(self.rootNVDAObject.windowHandle):
			return False
		try:
			return self.rootNVDAObject.excelWorksheetObject.name==self.rootNVDAObject.excelApplicationObject.activeSheet.name
		except (COMError,AttributeError,NameError):
			log.debugWarning("could not compare sheet names",exc_info=True)
			return False

	def navigationHelper(self,direction):
		excelWindowObject=self.rootNVDAObject.excelWindowObject
		cellPosition = excelWindowObject.activeCell
		try:
			if   direction == "left":
				cellPosition = cellPosition.Offset(0,-1)
			elif direction == "right":
				cellPosition = cellPosition.Offset(0,1)
			elif direction == "up":
				cellPosition = cellPosition.Offset(-1,0)
			elif direction == "down":
				cellPosition = cellPosition.Offset(1,0)
			#Start-of-Column
			elif direction == "startcol":
				cellPosition = cellPosition.end(xlUp)
			#Start-of-Row
			elif direction == "startrow":
				cellPosition = cellPosition.end(xlToLeft)
			#End-of-Row
			elif direction == "endrow":
				cellPosition = cellPosition.end(xlToRight)
			#End-of-Column
			elif direction == "endcol":
				cellPosition = cellPosition.end(xlDown)
			else:
				return
		except COMError:
			pass

		try:
			isMerged=cellPosition.mergeCells
		except (COMError,NameError):
			isMerged=False
		if isMerged:
			cellPosition=cellPosition.MergeArea(1)
			obj=ExcelMergedCell(windowHandle=self.rootNVDAObject.windowHandle,excelWindowObject=excelWindowObject,excelCellObject=cellPosition)
		else:
			obj=ExcelCell(windowHandle=self.rootNVDAObject.windowHandle,excelWindowObject=excelWindowObject,excelCellObject=cellPosition)
		cellPosition.Select()
		cellPosition.Activate()
		eventHandler.executeEvent('gainFocus',obj)

	def script_moveLeft(self,gesture):
		self.navigationHelper("left")

	def script_moveRight(self,gesture):
		self.navigationHelper("right")

	def script_moveUp(self,gesture):
		self.navigationHelper("up")

	def script_moveDown(self,gesture):
		self.navigationHelper("down")

	def script_startOfColumn(self,gesture):
		self.navigationHelper("startcol")

	def script_startOfRow(self,gesture):
		self.navigationHelper("startrow")

	def script_endOfRow(self,gesture):
		self.navigationHelper("endrow")

	def script_endOfColumn(self,gesture):
		self.navigationHelper("endcol")

	def __contains__(self,obj):
		return winUser.isDescendantWindow(self.rootNVDAObject.windowHandle,obj.windowHandle)

	def _get_selection(self):
		return self.rootNVDAObject._getSelection()

	def _set_selection(self,info):
		super(ExcelBrowseModeTreeInterceptor,self)._set_selection(info)
		#review.handleCaretMove(info)

	def _get_ElementsListDialog(self):
		return ElementsListDialog

	def _iterNodesByType(self,nodeType,direction="next",pos=None):
		if nodeType=="chart":
			return ChartExcelCollectionQuicknavIterator( nodeType , self.rootNVDAObject.excelWorksheetObject , direction , None ).iterate()
		elif nodeType=="comment":
			return CommentExcelCollectionQuicknavIterator( nodeType , self.rootNVDAObject.excelWorksheetObject , direction , None ).iterate()
		elif nodeType=="formula":
			return FormulaExcelCollectionQuicknavIterator( nodeType , self.rootNVDAObject.excelWorksheetObject , direction , None ).iterate()
		elif nodeType=="sheet":
			return SheetsExcelCollectionQuicknavIterator( nodeType , self.rootNVDAObject.excelWorksheetObject , direction , None ).iterate()
		elif nodeType=="formField":
			return ExcelFormControlQuicknavIterator( nodeType , self.rootNVDAObject.excelWorksheetObject , direction , None,self ).iterate(pos)
		else:
			raise NotImplementedError

	def script_elementsList(self,gesture):
		super(ExcelBrowseModeTreeInterceptor,self).script_elementsList(gesture)
	# Translators: the description for the elements list command in Microsoft Excel.
	script_elementsList.__doc__ = _("Lists various types of elements in this spreadsheet")
	script_elementsList.ignoreTreeInterceptorPassThrough=True

	__gestures = {
		"kb:upArrow": "moveUp",
		"kb:downArrow":"moveDown",
		"kb:leftArrow":"moveLeft",
		"kb:rightArrow":"moveRight",
		"kb:control+upArrow":"startOfColumn",
		"kb:control+downArrow":"endOfColumn",
		"kb:control+leftArrow":"startOfRow",
		"kb:control+rightArrow":"endOfRow",
	}

class ElementsListDialog(browseMode.ElementsListDialog):

	ELEMENT_TYPES=(
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("chart", _("&Charts")),
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("comment", _("C&omments")),
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("formula", _("Fo&rmulas")),
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("formField", _("&Form fields")),
		# Translators: The label of a radio button to select the type of element
		# in the browse mode Elements List dialog.
		("sheet", _("&Sheets")),
	)

class ExcelBase(Window):
	"""A base that all Excel NVDAObjects inherit from, which contains some useful methods."""

	@staticmethod
	def excelWindowObjectFromWindow(windowHandle):
		try:
			pDispatch=oleacc.AccessibleObjectFromWindow(windowHandle,winUser.OBJID_NATIVEOM,interface=comtypes.automation.IDispatch)
		except (COMError,WindowsError):
			return None
		return comtypes.client.dynamic.Dispatch(pDispatch)

	@staticmethod
	def getCellAddress(cell, external=False,format=xlA1):
		text=cell.Address(False, False, format, external)
		textList=text.split(':')
		if len(textList)==2:
			# Translators: Used to express an address range in excel.
			text=_("{start} through {end}").format(start=textList[0], end=textList[1])
		return text

	def _getDropdown(self):
		w=winUser.getAncestor(self.windowHandle,winUser.GA_ROOT)
		if not w:
			log.debugWarning("Could not get ancestor window (GA_ROOT)")
			return
		obj=Window(windowHandle=w,chooseBestAPI=False)
		if not obj:
			log.debugWarning("Could not instnaciate NVDAObject for ancestor window")
			return
		threadID=obj.windowThreadID
		while not eventHandler.isPendingEvents("gainFocus"):
			obj=obj.previous
			if not obj or not isinstance(obj,Window) or obj.windowThreadID!=threadID:
				log.debugWarning("Could not locate dropdown list in previous objects")
				return
			if obj.windowClassName=='EXCEL:':
				break
		return obj

	def _getSelection(self):
		selection=self.excelWindowObject.Selection
		try:
			isMerged=selection.mergeCells
		except (COMError,NameError):
			isMerged=False

		try:
			numCells=selection.count
		except (COMError,NameError):
			numCells=0

		isChartActive = True if self.excelWindowObject.ActiveChart else False
		obj=None
		if isMerged:
			obj=ExcelMergedCell(windowHandle=self.windowHandle,excelWindowObject=self.excelWindowObject,excelCellObject=selection.item(1))
		elif numCells>1:
			obj=ExcelSelection(windowHandle=self.windowHandle,excelWindowObject=self.excelWindowObject,excelRangeObject=selection)
		elif numCells==1:
			obj=ExcelCell(windowHandle=self.windowHandle,excelWindowObject=self.excelWindowObject,excelCellObject=selection)
		elif isChartActive:
			selection = self.excelWindowObject.ActiveChart
			import excelChart
			obj=excelChart.ExcelChart(windowHandle=self.windowHandle,excelWindowObject=self.excelWindowObject,excelChartObject=selection)
		return obj


class Excel7Window(ExcelBase):
	"""An overlay class for Window for the EXCEL7 window class, which simply bounces focus to the active excel cell."""

	def _get_excelWindowObject(self):
		return self.excelWindowObjectFromWindow(self.windowHandle)

	def event_gainFocus(self):
		selection=self._getSelection()
		dropdown=self._getDropdown()
		if dropdown:
			if selection:
				dropdown.parent=selection
			eventHandler.executeEvent('gainFocus',dropdown)
			return
		if selection:
			eventHandler.executeEvent('gainFocus',selection)

class ExcelWorksheet(ExcelBase):


	treeInterceptorClass=ExcelBrowseModeTreeInterceptor

	role=controlTypes.ROLE_TABLE

	def _get_excelApplicationObject(self):
		self.excelApplicationObject=self.excelWorksheetObject.application
		return self.excelApplicationObject

	re_definedName=re.compile(
		# Starts with an optional sheet name followed by an exclamation mark (!).
		# If a sheet name contains spaces then it is surrounded by single quotes (')
		# Examples:
		# Sheet1!
		# ''Sheet2 (4)'!
		# 'profit and loss'!
		u'^((?P<sheet>(\'[^\']+\'|[^!]+))!)?'
		# followed by a unique name (not containing spaces). Example:
		# rowtitle_ab12-cd34-de45
		u'(?P<name>\w+)'
		# Optionally followed by minimum and maximum addresses, starting with a period (.). Example:
		# .a1.c3
		# .ab34
		u'(\.(?P<minAddress>[a-zA-Z]+[0-9]+)?(\.(?P<maxAddress>[a-zA-Z]+[0-9]+)?'
		# Optionally followed by a period (.) and extra random data (sometimes produced by other screen readers)
		u'(\..*)*)?)?$'
	)

	def populateHeaderCellTrackerFromNames(self,headerCellTracker):
		sheetName=self.excelWorksheetObject.name
		for x in self.excelWorksheetObject.parent.names:
			fullName=x.name
			nameMatch=self.re_definedName.match(fullName)
			if not nameMatch:
				continue
			sheet=nameMatch.group('sheet')
			if sheet and sheet[0]=="'" and sheet[-1]=="'":
				sheet=sheet[1:-1]
			if sheet and sheet!=sheetName:
				continue
			name=nameMatch.group('name').lower()
			isColumnHeader=isRowHeader=False
			if name.startswith('title'):
				isColumnHeader=isRowHeader=True
			elif name.startswith('columntitle'):
				isColumnHeader=True
			elif name.startswith('rowtitle'):
				isRowHeader=True
			else:
				continue
			try:
				headerCell=x.refersToRange
			except COMError:
				continue
			if headerCell.parent.name!=sheetName:
				continue
			minColumnNumber=maxColumnNumber=minRowNumber=maxRowNumber=None
			minAddress=nameMatch.group('minAddress')
			if minAddress:
				try:
					minCell=self.excelWorksheetObject.range(minAddress)
				except COMError:
					minCell=None
				if minCell:
					minRowNumber=minCell.row
					minColumnNumber=minCell.column
			maxAddress=nameMatch.group('maxAddress')
			if maxAddress:
				try:
					maxCell=self.excelWorksheetObject.range(maxAddress)
				except COMError:
					maxCell=None
				if maxCell:
					maxRowNumber=maxCell.row
					maxColumnNumber=maxCell.column
			if maxColumnNumber is None:
				maxColumnNumber=self._getMaxColumnNumberForHeaderCell(headerCell)
			headerCellTracker.addHeaderCellInfo(rowNumber=headerCell.row,columnNumber=headerCell.column,rowSpan=headerCell.rows.count,colSpan=headerCell.columns.count,minRowNumber=minRowNumber,maxRowNumber=maxRowNumber,minColumnNumber=minColumnNumber,maxColumnNumber=maxColumnNumber,name=fullName,isColumnHeader=isColumnHeader,isRowHeader=isRowHeader)

	def _get_headerCellTracker(self):
		self.headerCellTracker=HeaderCellTracker()
		self.populateHeaderCellTrackerFromNames(self.headerCellTracker)
		return self.headerCellTracker

	def setAsHeaderCell(self,cell,isColumnHeader=False,isRowHeader=False):
		oldInfo=self.headerCellTracker.getHeaderCellInfoAt(cell.rowNumber,cell.columnNumber)
		if oldInfo:
			if isColumnHeader and not oldInfo.isColumnHeader:
				oldInfo.isColumnHeader=True
				oldInfo.rowSpan=cell.rowSpan
			elif isRowHeader and not oldInfo.isRowHeader:
				oldInfo.isRowHeader=True
				oldInfo.colSpan=cell.colSpan
			else:
				return False
			isColumnHeader=oldInfo.isColumnHeader
			isRowHeader=oldInfo.isRowHeader
		if isColumnHeader and isRowHeader:
			name="Title_"
		elif isRowHeader:
			name="RowTitle_"
		elif isColumnHeader:
			name="ColumnTitle_"
		else:
			raise ValueError("One or both of isColumnHeader or isRowHeader must be True")
		name+=uuid.uuid4().hex
		relativeName=name
		name="%s!%s"%(cell.excelRangeObject.worksheet.name,name)
		if oldInfo:
			self.excelWorksheetObject.parent.names(oldInfo.name).delete()
			oldInfo.name=name
		else:
			maxColumnNumber=self._getMaxColumnNumberForHeaderCell(cell.excelCellObject)
			self.headerCellTracker.addHeaderCellInfo(rowNumber=cell.rowNumber,columnNumber=cell.columnNumber,rowSpan=cell.rowSpan,colSpan=cell.colSpan,maxColumnNumber=maxColumnNumber,name=name,isColumnHeader=isColumnHeader,isRowHeader=isRowHeader)
		self.excelWorksheetObject.names.add(relativeName,cell.excelRangeObject)
		return True

	def _getMaxColumnNumberForHeaderCell(self,excelCell):
		try:
			r=excelCell.currentRegion
		except COMError:
			return excelCell.column
		columns=r.columns
		return columns[columns.count].column+1

	def forgetHeaderCell(self,cell,isColumnHeader=False,isRowHeader=False):
		if not isColumnHeader and not isRowHeader: 
			return False
		info=self.headerCellTracker.getHeaderCellInfoAt(cell.rowNumber,cell.columnNumber)
		if not info:
			return False
		if isColumnHeader and info.isColumnHeader:
			info.isColumnHeader=False
		elif isRowHeader and info.isRowHeader:
			info.isRowHeader=False
		else:
			return False
		self.headerCellTracker.removeHeaderCellInfo(info)
		self.excelWorksheetObject.parent.names(info.name).delete()
		if info.isColumnHeader or info.isRowHeader:
			self.setAsHeaderCell(cell,isColumnHeader=info.isColumnHeader,isRowHeader=info.isRowHeader)
		return True

	def fetchAssociatedHeaderCellText(self,cell,columnHeader=False):
		# #4409: cell.currentRegion fails if the worksheet is protected.
		try:
			cellRegion=cell.excelCellObject.currentRegion
		except COMError:
			log.debugWarning("Possibly protected sheet")
			return None
		for info in self.headerCellTracker.iterPossibleHeaderCellInfosFor(cell.rowNumber,cell.columnNumber,columnHeader=columnHeader):
			textList=[]
			if columnHeader:
				for headerRowNumber in xrange(info.rowNumber,info.rowNumber+info.rowSpan): 
					headerCell=self.excelWorksheetObject.cells(headerRowNumber,cell.columnNumber)
					# The header could be  merged cells. 
					# if so, fetch text from the first in the merge as that always contains the content
					try:
						headerCell=headerCell.mergeArea.item(1)
					except (COMError,NameError,AttributeError):
						pass
					textList.append(headerCell.text)
			else:
				for headerColumnNumber in xrange(info.columnNumber,info.columnNumber+info.colSpan): 
					headerCell=self.excelWorksheetObject.cells(cell.rowNumber,headerColumnNumber)
					# The header could be  merged cells. 
					# if so, fetch text from the first in the merge as that always contains the content
					try:
						headerCell=headerCell.mergeArea.item(1)
					except (COMError,NameError,AttributeError):
						pass
					textList.append(headerCell.text)
			text=" ".join(textList)
			if text:
				return text

	def __init__(self,windowHandle=None,excelWindowObject=None,excelWorksheetObject=None):
		self.excelWindowObject=excelWindowObject
		self.excelWorksheetObject=excelWorksheetObject
		super(ExcelWorksheet,self).__init__(windowHandle=windowHandle)
		for gesture in self.__changeSelectionGestures:
			self.bindGesture(gesture, "changeSelection")

	def _get_name(self):
		return self.excelWorksheetObject.name

	def _isEqual(self, other):
		if not super(ExcelWorksheet, self)._isEqual(other):
			return False
		return self.excelWorksheetObject.index == other.excelWorksheetObject.index

	def _get_firstChild(self):
		cell=self.excelWorksheetObject.cells(1,1)
		return ExcelCell(windowHandle=self.windowHandle,excelWindowObject=self.excelWindowObject,excelCellObject=cell)

	def _get_states(self):
		states=super(ExcelWorksheet,self).states
		if self.excelWorksheetObject.ProtectContents:
			states.add(controlTypes.STATE_PROTECTED)
		return states

	def script_changeSelection(self,gesture):
		oldSelection=api.getFocusObject()
		gesture.send()
		import eventHandler
		import time
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
			if oldSelection.parent==newSelection.parent:
				newSelection.parent=oldSelection.parent
			eventHandler.executeEvent('gainFocus',newSelection)
	script_changeSelection.canPropagate=True

	__changeSelectionGestures = (
		"kb:tab",
		"kb:shift+tab",
		"kb:enter",
		"kb:numpadEnter",
		"kb:upArrow",
		"kb:downArrow",
		"kb:leftArrow",
		"kb:rightArrow",
		"kb:control+upArrow",
		"kb:control+downArrow",
		"kb:control+leftArrow",
		"kb:control+rightArrow",
		"kb:home",
		"kb:end",
		"kb:control+home",
		"kb:control+end",
		"kb:shift+upArrow",
		"kb:shift+downArrow",
		"kb:shift+leftArrow",
		"kb:shift+rightArrow",
		"kb:shift+control+upArrow",
		"kb:shift+control+downArrow",
		"kb:shift+control+leftArrow",
		"kb:shift+control+rightArrow",
		"kb:shift+home",
		"kb:shift+end",
		"kb:shift+control+home",
		"kb:shift+control+end",
		"kb:shift+space",
		"kb:control+space",
		"kb:pageUp",
		"kb:pageDown",
		"kb:shift+pageUp",
		"kb:shift+pageDown",
		"kb:alt+pageUp",
		"kb:alt+pageDown",
		"kb:alt+shift+pageUp",
		"kb:alt+shift+pageDown",
		"kb:control+shift+8",
		"kb:control+pageUp",
		"kb:control+pageDown",
		"kb:control+a",
		"kb:control+v",
		"kb:shift+f11",
	)

class ExcelCellTextInfo(NVDAObjectTextInfo):

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		formatField=textInfos.FormatField()
		if (self.obj.excelCellObject.Application.Version > "12.0"):
			cellObj=self.obj.excelCellObject.DisplayFormat
		else:
			cellObj=self.obj.excelCellObject
		fontObj=cellObj.font
		if formatConfig['reportAlignment']:
			value=alignmentLabels.get(self.obj.excelCellObject.horizontalAlignment)
			if value:
				formatField['text-align']=value
			value=alignmentLabels.get(self.obj.excelCellObject.verticalAlignment)
			if value:
				formatField['vertical-align']=value
		if formatConfig['reportFontName']:
			formatField['font-name']=fontObj.name
		if formatConfig['reportFontSize']:
			formatField['font-size']=str(fontObj.size)
		if formatConfig['reportFontAttributes']:
			formatField['bold']=fontObj.bold
			formatField['italic']=fontObj.italic
			underline=fontObj.underline
			formatField['underline']=False if underline is None or underline==xlUnderlineStyleNone else True
		if formatConfig['reportStyle']:
			try:
				styleName=self.obj.excelCellObject.style.nameLocal
			except COMError:
				styleName=None
			if styleName:
				formatField['style']=styleName
		if formatConfig['reportColor']:
			try:
				formatField['color']=colors.RGB.fromCOLORREF(int(fontObj.color))
			except COMError:
				pass
			try:
				pattern = cellObj.Interior.Pattern
				formatField['background-pattern'] = backgroundPatternLabels.get(pattern)
				if pattern in (xlPatternLinearGradient, xlPatternRectangularGradient):
					formatField['background-color']=(colors.RGB.fromCOLORREF(int(cellObj.Interior.Gradient.ColorStops(1).Color)))
					formatField['background-color2']=(colors.RGB.fromCOLORREF(int(cellObj.Interior.Gradient.ColorStops(2).Color)))
				else:
					formatField['background-color']=colors.RGB.fromCOLORREF(int(cellObj.interior.color))
			except COMError:
				pass
		if formatConfig["reportBorderStyle"]:
			borders = None
			hasMergedCells = self.obj.excelCellObject.mergeCells
			if hasMergedCells:
				mergeArea = self.obj.excelCellObject.mergeArea
				try:
					borders = mergeArea.DisplayFormat.borders # for later versions of office
				except COMError:
					borders = mergeArea.borders # for office 2007
			else:
				borders = cellObj.borders
			try:
				formatField['border-style']=getCellBorderStyleDescription(borders,reportBorderColor=formatConfig['reportBorderColor'])
			except COMError:
				pass
		return formatField,(self._startOffset,self._endOffset)

	def _get_locationText(self):
		return self.obj.getCellPosition()

class ExcelCell(ExcelBase):

	def doAction(self):
		pass

	def _get_columnHeaderText(self):
		return self.parent.fetchAssociatedHeaderCellText(self,columnHeader=True)

	def _get_rowHeaderText(self):
		return self.parent.fetchAssociatedHeaderCellText(self,columnHeader=False)

	def script_openDropdown(self,gesture):
		gesture.send()
		d=None
		curTime=startTime=time.time()
		while (curTime-startTime)<=0.25:
			if scriptHandler.isScriptWaiting():
				# Prevent lag if keys are pressed rapidly
				return
			if eventHandler.isPendingEvents('gainFocus'):
				return
			d=self._getDropdown()
			if d:
				break
			api.processPendingEvents(processEventQueue=False)
			time.sleep(0.025)
			curTime=time.time()
		if not d:
			log.debugWarning("Failed to get dropDown, giving up")
			return
		d.parent=self
		eventHandler.queueEvent("gainFocus",d)

	def script_setColumnHeader(self,gesture):
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if not config.conf['documentFormatting']['reportTableHeaders']:
			# Translators: a message reported in the SetColumnHeader script for Excel.
			ui.message(_("Cannot set headers. Please enable reporting of table headers in Document Formatting Settings"))
			return
		if scriptCount==0:
			if self.parent.setAsHeaderCell(self,isColumnHeader=True,isRowHeader=False):
				# Translators: a message reported in the SetColumnHeader script for Excel.
				ui.message(_("Set {address} as start of column headers").format(address=self.cellCoordsText))
			else:
				# Translators: a message reported in the SetColumnHeader script for Excel.
				ui.message(_("Already set {address} as start of column headers").format(address=self.cellCoordsText))
		elif scriptCount==1:
			if self.parent.forgetHeaderCell(self,isColumnHeader=True,isRowHeader=False):
				# Translators: a message reported in the SetColumnHeader script for Excel.
				ui.message(_("Removed {address}    from column headers").format(address=self.cellCoordsText))
			else:
				# Translators: a message reported in the SetColumnHeader script for Excel.
				ui.message(_("Cannot find {address}    in column headers").format(address=self.cellCoordsText))
	script_setColumnHeader.__doc__=_("Pressing once will set this cell as the first column header for any cells lower and to the right of it within this region. Pressing twice will forget the current column header for this cell.")

	def script_setRowHeader(self,gesture):
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		if not config.conf['documentFormatting']['reportTableHeaders']:
			# Translators: a message reported in the SetRowHeader script for Excel.
			ui.message(_("Cannot set headers. Please enable reporting of table headers in Document Formatting Settings"))
			return
		if scriptCount==0:
			if self.parent.setAsHeaderCell(self,isColumnHeader=False,isRowHeader=True):
				# Translators: a message reported in the SetRowHeader script for Excel.
				ui.message(_("Set {address} as start of row headers").format(address=self.cellCoordsText))
			else:
				# Translators: a message reported in the SetRowHeader script for Excel.
				ui.message(_("Already set {address} as start of row headers").format(address=self.cellCoordsText))
		elif scriptCount==1:
			if self.parent.forgetHeaderCell(self,isColumnHeader=False,isRowHeader=True):
				# Translators: a message reported in the SetRowHeader script for Excel.
				ui.message(_("Removed {address}    from row headers").format(address=self.cellCoordsText))
			else:
				# Translators: a message reported in the SetRowHeader script for Excel.
				ui.message(_("Cannot find {address}    in row headers").format(address=self.cellCoordsText))
	script_setRowHeader.__doc__=_("Pressing once will set this cell as the first row header for any cells lower and to the right of it within this region. Pressing twice will forget the current row header for this cell.")

	@classmethod
	def kwargsFromSuper(cls,kwargs,relation=None):
		windowHandle=kwargs['windowHandle']
		excelWindowObject=cls.excelWindowObjectFromWindow(windowHandle)
		if not excelWindowObject:
			return False
		if isinstance(relation,tuple):
			excelCellObject=excelWindowObject.rangeFromPoint(relation[0],relation[1])
		else:
			excelCellObject=excelWindowObject.ActiveCell
		if not excelCellObject:
			return False
		kwargs['excelWindowObject']=excelWindowObject
		kwargs['excelCellObject']=excelCellObject
		return True

	def __init__(self,windowHandle=None,excelWindowObject=None,excelCellObject=None):
		self.excelWindowObject=excelWindowObject
		self.excelCellObject=excelCellObject
		super(ExcelCell,self).__init__(windowHandle=windowHandle)

	def _get_excelRangeObject(self):
		return self.excelCellObject

	def _get_role(self):
		try:
			linkCount=self.excelCellObject.hyperlinks.count
		except (COMError,NameError,AttributeError):
			linkCount=None
		if linkCount:
			return controlTypes.ROLE_LINK
		return controlTypes.ROLE_TABLECELL

	TextInfo=ExcelCellTextInfo

	def _isEqual(self,other):
		if not super(ExcelCell,self)._isEqual(other):
			return False
		thisAddr=self.getCellAddress(self.excelCellObject,True)
		try:
			otherAddr=self.getCellAddress(other.excelCellObject,True)
		except COMError:
			#When cutting and pasting the old selection can become broken
			return False
		return thisAddr==otherAddr

	def _get_cellCoordsText(self):
		return self.getCellAddress(self.excelCellObject)

	def _get__rowAndColumnNumber(self):
		rc=self.excelCellObject.address(True,True,xlRC,False)
		return [int(x) if x else 1 for x in re_absRC.match(rc).groups()]

	def _get_rowNumber(self):
		return self._rowAndColumnNumber[0]

	rowSpan=1

	def _get_columnNumber(self):
		return self._rowAndColumnNumber[1]

	colSpan=1

	def getCellPosition(self):
		rowAndColumn = self.cellCoordsText
		sheet = self.excelWindowObject.ActiveSheet.name
		# Translators: a message reported in the get location text script for Excel. {0} is replaced with the name of the excel worksheet, and {1} is replaced with the row and column identifier EG "G4"
		return _(u"Sheet {0}, {1}").format(sheet, rowAndColumn)

	def _get_tableID(self):
		address=self.excelCellObject.address(1,1,0,1)
		ID="".join(address.split('!')[:-1])
		ID="%s %s"%(ID,self.windowHandle)
		return ID

	def _get_name(self):
		return self.excelCellObject.Text

	def _getCurSummaryRowState(self):
		try:
			row=self.excelCellObject.rows[1]
			if row.summary:
				return controlTypes.STATE_EXPANDED if row.showDetail else controlTypes.STATE_COLLAPSED
		except COMError:
			pass

	def _getCurSummaryColumnState(self):
		try:
			col=self.excelCellObject.columns[1]
			if col.summary:
				return controlTypes.STATE_EXPANDED if col.showDetail else controlTypes.STATE_COLLAPSED
		except COMError:
			pass

	def _get_states(self):
		states=super(ExcelCell,self).states
		summaryCellState=self._getCurSummaryRowState() or self._getCurSummaryColumnState()
		if summaryCellState:
			states.add(summaryCellState)
		if self.excelCellObject.HasFormula:
			states.add(controlTypes.STATE_HASFORMULA)
		try:
			validationType=self.excelCellObject.validation.type
		except (COMError,NameError,AttributeError):
			validationType=None
		if validationType==3:
			states.add(controlTypes.STATE_HASPOPUP)
		try:
			comment=self.excelCellObject.comment
		except (COMError,NameError,AttributeError):
			comment=None
		if comment:
			states.add(controlTypes.STATE_HASCOMMENT)
		if self._overlapInfo is not None:
			if self._overlapInfo['obscuredFromRightBy'] > 0:
				states.add(controlTypes.STATE_CROPPED)
			if self._overlapInfo['obscuringRightBy'] > 0:
				states.add(controlTypes.STATE_OVERFLOWING)
		if self.excelWindowObject.ActiveSheet.ProtectContents and (not self.excelCellObject.Locked):
			states.add(controlTypes.STATE_UNLOCKED)
		return states

	def event_typedCharacter(self,ch):
		# #6570: You cannot type into protected cells.
		# Apart from speaking characters being miss-leading, Office 2016 protected view doubles characters as well.
		# Therefore for any character from space upwards (not control characters)  on protected cells, play the default sound rather than speaking the character
		if ch>=" " and controlTypes.STATE_UNLOCKED not in self.states and controlTypes.STATE_PROTECTED in self.parent.states: 
			winsound.PlaySound("Default",winsound.SND_ALIAS|winsound.SND_NOWAIT|winsound.SND_ASYNC)
			return
		super(ExcelCell,self).event_typedCharacter(ch)

	def getCellTextWidth(self):
		#handle to Device Context
		hDC = ctypes.windll.user32.GetDC(self.windowHandle)
		tempDC = ctypes.windll.gdi32.CreateCompatibleDC(hDC)
		ctypes.windll.user32.ReleaseDC(self.windowHandle, hDC)
		#Compatible Bitmap for current Device Context
		hBMP = ctypes.windll.gdi32.CreateCompatibleBitmap(tempDC, 1, 1)
		#handle to the bitmap object
		hOldBMP = ctypes.windll.gdi32.SelectObject(tempDC, hBMP)
		#Pass Device Context and LOGPIXELSX, the horizontal resolution in pixels per unit inch
		dpi = ctypes.windll.gdi32.GetDeviceCaps(tempDC, LOGPIXELSX)
		#Fetching Font Size and Weight information
		iFontSize = self.excelCellObject.Font.Size
		iFontSize = 11 if iFontSize is None else int(iFontSize)
		#Font  Weight for Bold FOnt is 700 and for normal font it's 400
		iFontWeight = 700 if self.excelCellObject.Font.Bold else 400
		#Fetching Font Name and style information
		sFontName = self.excelCellObject.Font.Name
		sFontItalic = self.excelCellObject.Font.Italic
		sFontUnderline = True if self.excelCellObject.Font.Underline else False
		sFontStrikeThrough = self.excelCellObject.Font.Strikethrough
		#If FontSize is <0: The font mapper transforms this value into device units
		#and matches its absolute value against the character height of the available fonts.
		iFontHeight = iFontSize * -1
		#If Font Width is 0, the font mapper chooses a closest match value.
		iFontWidth = 0
		iEscapement = 0
		iOrientation = 0
		#Default CharSet based on System Locale is chosen
		iCharSet = 0
		#Default font mapper behavior
		iOutputPrecision = 0
		#Default clipping behavior
		iClipPrecision = 0
		#Default Quality
		iOutputQuality = 0
		#Default Pitch and default font family
		iPitchAndFamily = 0
		#Create a font object with the correct size, weight and style
		hFont = ctypes.windll.gdi32.CreateFontW(iFontHeight, iFontWidth, iEscapement, iOrientation, iFontWeight, sFontItalic, sFontUnderline, sFontStrikeThrough, iCharSet, iOutputPrecision, iClipPrecision, iOutputQuality, iPitchAndFamily, sFontName)
		#Load the font into the device context, storing the original font object
		hOldFont = ctypes.windll.gdi32.SelectObject(tempDC, hFont)
		sText = self.excelCellObject.Text
		textLength = len(sText)
		class structText(ctypes.Structure):
			_fields_ = [("width", ctypes.c_int), ("height",ctypes.c_int)]
		StructText = structText()
		getTextExtentPoint = ctypes.windll.gdi32.GetTextExtentPoint32W
		getTextExtentPoint.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int, ctypes.POINTER(structText)]
		getTextExtentPoint.restype = ctypes.c_int
		sText = unicode(sText)
		#Get the text dimensions
		ctypes.windll.gdi32.GetTextExtentPoint32W(tempDC, sText, textLength,ctypes.byref(StructText))
		#Restore the old Font Object
		ctypes.windll.gdi32.SelectObject(tempDC, hOldFont)
		#Delete the font object we created
		ctypes.windll.gdi32.DeleteObject(hFont)
		#Restore the old Bitmap Object
		ctypes.windll.gdi32.SelectObject(tempDC, hOldBMP)
		#Delete the temporary BitMap Object
		ctypes.windll.gdi32.DeleteObject(hBMP)
		#Release & Delete the device context
		ctypes.windll.gdi32.DeleteDC(tempDC)
		#Retrieve the text width
		textWidth = StructText.width
		return textWidth

	def _get__overlapInfo(self):
		textWidth = self.getCellTextWidth()
		if self.excelCellObject.WrapText or self.excelCellObject.ShrinkToFit:
			return None
		isMerged = self.excelWindowObject.Selection.MergeCells
		try:
			adjacentCell = self.excelCellObject.Offset(0,1)
		except COMError:
			# #5041: This cell is at the right edge.
			# For our purposes, treat this as if there is an empty cell to the right.
			isAdjacentCellEmpty = True
		else:
			isAdjacentCellEmpty = not adjacentCell.Text
		info = {}
		if isMerged:
			columns=self.excelCellObject.mergeArea.columns
			columnCount=columns.count
			firstColumn=columns.item(1)
			lastColumn=columns.item(columnCount)
			firstColumnLeft=firstColumn.left
			lastColumnLeft=lastColumn.left
			lastColumnWidth=lastColumn.width
			cellLeft=firstColumnLeft
			cellRight=lastColumnLeft+lastColumnWidth
		else:
			cellLeft=self.excelCellObject.left
			cellRight=cellLeft+self.excelCellObject.width
		pointsToPixels=self.excelCellObject.Application.ActiveWindow.PointsToScreenPixelsX
		cellLeft=pointsToPixels(cellLeft)
		cellRight=pointsToPixels(cellRight)
		cellWidth=(cellRight-cellLeft)
		if textWidth <= cellWidth:
			info = None
		else:
			if isAdjacentCellEmpty:
				info['obscuringRightBy']= textWidth - cellWidth
				info['obscuredFromRightBy'] = 0
			else:
				info['obscuredFromRightBy']= textWidth - cellWidth
				info['obscuringRightBy'] = 0
		self._overlapInfo = info
		return self._overlapInfo

	def _get_parent(self):
		worksheet=self.excelCellObject.Worksheet
		self.parent=ExcelWorksheet(windowHandle=self.windowHandle,excelWindowObject=self.excelWindowObject,excelWorksheetObject=worksheet)
		return self.parent

	def _get_next(self):
		try:
			next=self.excelCellObject.next
		except COMError:
			next=None
		if next:
			return ExcelCell(windowHandle=self.windowHandle,excelWindowObject=self.excelWindowObject,excelCellObject=next)

	def _get_previous(self):
		try:
			previous=self.excelCellObject.previous
		except COMError:
			previous=None
		if previous:
			return ExcelCell(windowHandle=self.windowHandle,excelWindowObject=self.excelWindowObject,excelCellObject=previous)

	def _get_description(self):
		try:
			inputMessageTitle=self.excelCellObject.validation.inputTitle
		except (COMError,NameError,AttributeError):
			inputMessageTitle=None
		try:
			inputMessage=self.excelCellObject.validation.inputMessage
		except (COMError,NameError,AttributeError):
			inputMessage=None
		if inputMessage and inputMessageTitle:
			return _("Input Message is {title}: {message}").format( title = inputMessageTitle , message = inputMessage)
		elif inputMessage:
			return _("Input Message is {message}").format( message = inputMessage)
		else:
			return None

	def _get_positionInfo(self):
		try:
			level=int(self.excelCellObject.rows[1].outlineLevel)-1
		except COMError:
			level=None
		if level==0:
			try:
				level=int(self.excelCellObject.columns[1].outlineLevel)-1
			except COMError:
				level=None
		if level==0:
			level=None
		return {'level':level}

	def script_reportComment(self,gesture):
		commentObj=self.excelCellObject.comment
		text=commentObj.text() if commentObj else None
		if text:
			ui.message(text)
		else:
			# Translators: A message in Excel when there is no comment
			ui.message(_("Not on a comment"))
	# Translators: the description  for a script for Excel
	script_reportComment.__doc__=_("Reports the comment on the current cell")

	def script_editComment(self,gesture):
		commentObj=self.excelCellObject.comment
		d = wx.TextEntryDialog(gui.mainFrame, 
			# Translators: Dialog text for 
			_("Editing comment for cell {address}").format(address=self.cellCoordsText),
			# Translators: Title of a dialog edit an Excel comment 
			_("Comment"),
			defaultValue=commentObj.text() if commentObj else u"",
			style=wx.TE_MULTILINE|wx.OK|wx.CANCEL)
		def callback(result):
			if result == wx.ID_OK:
				if commentObj:
					commentObj.text(d.Value)
				else:
					self.excelCellObject.addComment(d.Value)
		gui.runScriptModalDialog(d, callback)

	def reportFocus(self):
		# #4878: Excel specific code for speaking format changes on the focused object.
		info=self.makeTextInfo(textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_CHARACTER)
		formatField=textInfos.FormatField()
		formatConfig=config.conf['documentFormatting']
		for field in info.getTextWithFields(formatConfig):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField):
				formatField.update(field.field)
		if not hasattr(self.parent,'_formatFieldSpeechCache'):
			self.parent._formatFieldSpeechCache={}
		text=speech.getFormatFieldSpeech(formatField,attrsCache=self.parent._formatFieldSpeechCache,formatConfig=formatConfig) if formatField else None
		if text:
			speech.speakText(text)
		super(ExcelCell,self).reportFocus()

	__gestures = {
		"kb:NVDA+shift+c": "setColumnHeader",
		"kb:NVDA+shift+r": "setRowHeader",
		"kb:shift+f2":"editComment",
		"kb:alt+downArrow":"openDropdown",
		"kb:NVDA+alt+c":"reportComment",
	}

class ExcelSelection(ExcelBase):

	role=controlTypes.ROLE_TABLECELL

	def __init__(self,windowHandle=None,excelWindowObject=None,excelRangeObject=None):
		self.excelWindowObject=excelWindowObject
		self.excelRangeObject=excelRangeObject
		super(ExcelSelection,self).__init__(windowHandle=windowHandle)

	def _get_states(self):
		states=super(ExcelSelection,self).states
		states.add(controlTypes.STATE_SELECTED)
		return states

	def _get_name(self):
		firstCell=self.excelRangeObject.Item(1)
		lastCell=self.excelRangeObject.Item(self.excelRangeObject.Count)
		# Translators: This is presented in Excel to show the current selection, for example 'a1 c3 through a10 c10'
		return _("{firstAddress} {firstContent} through {lastAddress} {lastContent}").format(firstAddress=self.getCellAddress(firstCell),firstContent=firstCell.Text,lastAddress=self.getCellAddress(lastCell),lastContent=lastCell.Text)

	def _get_parent(self):
		worksheet=self.excelRangeObject.Worksheet
		return ExcelWorksheet(windowHandle=self.windowHandle,excelWindowObject=self.excelWindowObject,excelWorksheetObject=worksheet)

	def _get_rowNumber(self):
		return self.excelRangeObject.row

	def _get_rowSpan(self):
		return self.excelRangeObject.rows.count

	def _get_columnNumber(self):
		return self.excelRangeObject.column

	def _get_colSpan(self):
		return self.excelRangeObject.columns.count

	#Its useful for an excel selection to be announced with reportSelection script
	def makeTextInfo(self,position):
		if position==textInfos.POSITION_SELECTION:
			position=textInfos.POSITION_ALL
		return super(ExcelSelection,self).makeTextInfo(position)

class ExcelDropdownItem(Window):

	firstChild=None
	lastChild=None
	children=[]
	role=controlTypes.ROLE_LISTITEM

	def __init__(self,parent=None,name=None,states=None,index=None):
		self.name=name
		self.states=states
		self.parent=parent
		self.index=index
		super(ExcelDropdownItem,self).__init__(windowHandle=parent.windowHandle)

	def _get_previous(self):
		newIndex=self.index-1
		if newIndex>=0:
			return self.parent.getChildAtIndex(newIndex)

	def _get_next(self):
		newIndex=self.index+1
		if newIndex<self.parent.childCount:
			return self.parent.getChildAtIndex(newIndex)

	def _get_treeInterceptor(self):
		return self.parent.treeInterceptor

	def _get_positionInfo(self):
		return {'indexInGroup':self.index+1,'similarItemsInGroup':self.parent.childCount,}

class ExcelDropdown(Window):

	@classmethod
	def kwargsFromSuper(cls,kwargs,relation=None):
		return kwargs

	role=controlTypes.ROLE_LIST
	excelCell=None

	def _get__highlightColors(self):
		background=colors.RGB.fromCOLORREF(winUser.user32.GetSysColor(13))
		foreground=colors.RGB.fromCOLORREF(winUser.user32.GetSysColor(14))
		self._highlightColors=(background,foreground)
		return self._highlightColors

	def _get_children(self):
		children=[]
		index=0
		states=set()
		for item in DisplayModelTextInfo(self,textInfos.POSITION_ALL).getTextWithFields():
			if isinstance(item,textInfos.FieldCommand) and item.command=="formatChange":
				states=set([controlTypes.STATE_SELECTABLE])
				foreground=item.field.get('color',None)
				background=item.field.get('background-color',None)
				if (background,foreground)==self._highlightColors:
					states.add(controlTypes.STATE_SELECTED)
			if isinstance(item,basestring):
				obj=ExcelDropdownItem(parent=self,name=item,states=states,index=index)
				children.append(obj)
				index+=1
		return children

	def getChildAtIndex(self,index):
		return self.children[index]

	def _get_childCount(self):
		return len(self.children)

	def _get_firstChild(self):
		return self.children[0]
	def _get_selection(self):
		for child in self.children:
			if controlTypes.STATE_SELECTED in child.states:
				return child

	def script_selectionChange(self,gesture):
		gesture.send()
		newFocus=self.selection or self
		if eventHandler.lastQueuedFocusObject is newFocus: return
		eventHandler.queueEvent("gainFocus",newFocus)
	script_selectionChange.canPropagate=True

	def script_closeDropdown(self,gesture):
		gesture.send()
		eventHandler.queueEvent("gainFocus",self.parent)
	script_closeDropdown.canPropagate=True

	__gestures={
		"kb:downArrow":"selectionChange",
		"kb:upArrow":"selectionChange",
		"kb:leftArrow":"selectionChange",
		"kb:rightArrow":"selectionChange",
		"kb:home":"selectionChange",
		"kb:end":"selectionChange",
		"kb:escape":"closeDropdown",
		"kb:enter":"closeDropdown",
		"kb:space":"closeDropdown",
	}

	def event_gainFocus(self):
		child=self.selection
		if not child and self.childCount>0:
			child=self.children[0]
		if child:
			eventHandler.queueEvent("focusEntered",self)
			eventHandler.queueEvent("gainFocus",child)
		else:
			super(ExcelDropdown,self).event_gainFocus()

class ExcelMergedCell(ExcelCell):

	def _get_cellCoordsText(self):
		return self.getCellAddress(self.excelCellObject.mergeArea)

	def _get_rowSpan(self):
		return self.excelCellObject.mergeArea.rows.count

	def _get_colSpan(self):
		return self.excelCellObject.mergeArea.columns.count

class ExcelFormControl(ExcelBase):
	isFocusable=True
	_roleMap = {
		xlButtonControl: controlTypes.ROLE_BUTTON,
		xlCheckBox: controlTypes.ROLE_CHECKBOX,
		xlDropDown: controlTypes.ROLE_COMBOBOX,
		xlEditBox: controlTypes.ROLE_EDITABLETEXT,
		xlGroupBox: controlTypes.ROLE_BOX,
		xlLabel: controlTypes.ROLE_LABEL,
		xlListBox: controlTypes.ROLE_LIST,
		xlOptionButton: controlTypes.ROLE_RADIOBUTTON,
		xlScrollBar: controlTypes.ROLE_SCROLLBAR,
		xlSpinner: controlTypes.ROLE_SPINBUTTON,
	}

	def _get_excelControlFormatObject(self):
		return self.excelFormControlObject.controlFormat

	def _get_excelOLEFormatObject(self):
		return self.excelFormControlObject.OLEFormat.object

	def __init__(self,windowHandle=None,parent=None,excelFormControlObject=None):
		self.parent=parent
		self.excelFormControlObject=excelFormControlObject
		super(ExcelFormControl,self).__init__(windowHandle=windowHandle)

	def _get_role(self):
		try:
			if self.excelFormControlObject.Type==msoFormControl:
				formControlType=self.excelFormControlObject.FormControlType
			else:
				formControlType=None
		except:
			return None
		return self._roleMap[formControlType]

	def _get_states(self):
		states=super(ExcelFormControl,self).states
		if self is api.getFocusObject():
			states.add(controlTypes.STATE_FOCUSED)
		newState=None
		if self.role==controlTypes.ROLE_RADIOBUTTON:
			newState=controlTypes.STATE_CHECKED if self.excelOLEFormatObject.Value==checked else None
		elif self.role==controlTypes.ROLE_CHECKBOX:
			if self.excelOLEFormatObject.Value==checked:
				newState=controlTypes.STATE_CHECKED
			elif self.excelOLEFormatObject.Value==mixed:
				newState=controlTypes.STATE_HALFCHECKED
		if newState:
			states.add(newState)
		return states

	def _get_name(self):
		if self.excelFormControlObject.AlternativeText:
			return self.excelFormControlObject.AlternativeText+" "+self.excelFormControlObject.TopLeftCell.address(False,False,1,False) + "-" + self.excelFormControlObject.BottomRightCell.address(False,False,1,False)
		else:
			return self.excelFormControlObject.Name+" "+self.excelFormControlObject.TopLeftCell.address(False,False,1,False) + "-" + self.excelFormControlObject.BottomRightCell.address(False,False,1,False)

	def _get_index(self):
		return self.excelFormControlObject.ZOrderPosition

	def _get_topLeftCell(self):
		return self.excelFormControlObject.TopLeftCell

	def _get_bottomRightCell(self):
		return self.excelFormControlObject.BottomRightCell

	def _getFormControlScreenCoordinates(self):
		topLeftAddress=self.topLeftCell
		bottomRightAddress=self.bottomRightCell
		#top left cell's width in points
		topLeftCellWidth=topLeftAddress.Width
		#top left cell's height in points
		topLeftCellHeight=topLeftAddress.Height
		#bottom right cell's width in points
		bottomRightCellWidth=bottomRightAddress.Width
		#bottom right cell's height in points
		bottomRightCellHeight=bottomRightAddress.Height
		self.excelApplicationObject=self.parent.excelWorksheetObject.Application
		hDC = ctypes.windll.user32.GetDC(None)
		#pixels per inch along screen width
		px = ctypes.windll.gdi32.GetDeviceCaps(hDC, LOGPIXELSX)
		#pixels per inch along screen height
		py = ctypes.windll.gdi32.GetDeviceCaps(hDC, LOGPIXELSY)
		ctypes.windll.user32.ReleaseDC(None, hDC)
		zoom=self.excelApplicationObject.ActiveWindow.Zoom
		zoomRatio=zoom/100
		#Conversion from inches to Points, 1 inch=72points
		pointsPerInch = self.excelApplicationObject.InchesToPoints(1)
		#number of pixels from the left edge of the spreadsheet's window to the left edge the first column in the spreadsheet.
		X=self.excelApplicationObject.ActiveWindow.PointsToScreenPixelsX(0)
		#number of pixels from the top edge of the spreadsheet's window to the top edge the first row in the spreadsheet,
		Y=self.excelApplicationObject.ActiveWindow.PointsToScreenPixelsY(0)
		if topLeftAddress==bottomRightAddress:
			#Range.Left: The distance, in points, from the left edge of column A to the left edge of the range.
			X=int(X + (topLeftAddress.Left+topLeftCellWidth/2) * zoomRatio * px / pointsPerInch)
			#Range.Top: The distance, in points, from the top edge of Row 1 to the top edge of the range.
			Y=int(Y + (topLeftAddress.Top+topLeftCellHeight/2) * zoomRatio * py / pointsPerInch)
			return (X,Y)
		else:
			screenTopLeftX=int(X + (topLeftCellWidth/2 + topLeftAddress.Left) * zoomRatio * px / pointsPerInch)
			screenBottomRightX=int(X + (bottomRightCellWidth/2+bottomRightAddress.Left) * zoomRatio * px / pointsPerInch)
			screenTopLeftY = int(Y + (topLeftCellHeight/2+ topLeftAddress.Top) * zoomRatio * py / pointsPerInch)
			screenBottomRightY=int(Y + (bottomRightCellHeight/2+ bottomRightAddress.Top) * zoomRatio * py / pointsPerInch)
			return (int(0.5*(screenTopLeftX+screenBottomRightX)), int(0.5*(screenTopLeftY+screenBottomRightY)))

	def script_doAction(self,gesture):
		self.doAction()
	script_doAction.canPropagate=True

	def doAction(self):
		(x,y)=self._getFormControlScreenCoordinates()
		winUser.setCursorPos(x,y)
		#perform Mouse Left-Click
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		self.invalidateCache()
		wx.CallLater(100,eventHandler.executeEvent,"stateChange",self)

	__gestures= {
				"kb:enter":"doAction",
				"kb:space":"doAction",
				"kb(desktop):numpadEnter":"doAction",
				}

class ExcelFormControlQuickNavItem(ExcelQuickNavItem):

	def __init__( self , nodeType , document , formControlObject , formControlCollection, treeInterceptorObj ):
		super( ExcelFormControlQuickNavItem ,self).__init__( nodeType , document , formControlObject , formControlCollection )
		self.formControlObjectIndex = formControlObject.ZOrderPosition
		self.treeInterceptorObj=treeInterceptorObj

	_label=None
	@property
	def label(self):
		if self._label: return self._label
		alternativeText=self.excelItemObject.AlternativeText
		if alternativeText: 
			self._label=alternativeText+" "+self.excelItemObject.Name+" " + self.excelItemObject.TopLeftCell.address(False,False,1,False) + "-" + self.excelItemObject.BottomRightCell.address(False,False,1,False)
		else:
			self._label=self.excelItemObject.Name + " " + self.excelItemObject.TopLeftCell.address(False,False,1,False) + "-" + self.excelItemObject.BottomRightCell.address(False,False,1,False)
		return self._label

	_nvdaObj=None
	@property
	def nvdaObj(self):
		if self._nvdaObj: return self._nvdaObj
		formControlType=self.excelItemObject.formControlType
		if formControlType ==xlListBox:
			self._nvdaObj=ExcelFormControlListBox(windowHandle=self.treeInterceptorObj.rootNVDAObject.windowHandle,parent=self.treeInterceptorObj.rootNVDAObject,excelFormControlObject=self.excelItemObject)
		elif formControlType ==xlDropDown:
			self._nvdaObj=ExcelFormControlDropDown(windowHandle=self.treeInterceptorObj.rootNVDAObject.windowHandle,parent=self.treeInterceptorObj.rootNVDAObject,excelFormControlObject=self.excelItemObject)
		elif formControlType in (xlScrollBar,xlSpinner):
			self._nvdaObj=ExcelFormControlScrollBar(windowHandle=self.treeInterceptorObj.rootNVDAObject.windowHandle,parent=self.treeInterceptorObj.rootNVDAObject,excelFormControlObject=self.excelItemObject)
		else:
			self._nvdaObj=ExcelFormControl(windowHandle=self.treeInterceptorObj.rootNVDAObject.windowHandle,parent=self.treeInterceptorObj.rootNVDAObject,excelFormControlObject=self.excelItemObject)
		self._nvdaObj.treeInterceptor=self.treeInterceptorObj
		return self._nvdaObj

	def __lt__(self,other):
		return self.formControlObjectIndex < other.formControlObjectIndex

	def moveTo(self):
		self.excelItemObject.TopLeftCell.Select
		self.excelItemObject.TopLeftCell.Activate()
		if self.treeInterceptorObj.passThrough:
			self.treeInterceptorObj.passThrough=False
			browseMode.reportPassThrough(self.treeInterceptorObj)
		eventHandler.queueEvent("gainFocus",self.nvdaObj)

	@property
	def isAfterSelection(self):
		activeCell = self.document.Application.ActiveCell
		if self.excelItemObject.TopLeftCell.row == activeCell.row:
			if self.excelItemObject.TopLeftCell.column > activeCell.column:
				return False
		elif self.excelItemObject.TopLeftCell.row > activeCell.row:
			return False
		return True

class ExcelFormControlQuicknavIterator(ExcelQuicknavIterator):
	quickNavItemClass=ExcelFormControlQuickNavItem

	def __init__(self, itemType , document , direction , includeCurrent,treeInterceptorObj):
		super(ExcelFormControlQuicknavIterator,self).__init__(itemType , document , direction , includeCurrent)
		self.treeInterceptorObj=treeInterceptorObj

	def collectionFromWorksheet( self , worksheetObject ):
		try:
			return worksheetObject.Shapes
		except(COMError):
			return None

	def iterate(self, position):
		"""
		returns a generator that emits L{QuickNavItem} objects for this collection.
		@param position: an excelRangeObject representing either the TopLeftCell of the currently selected form control
		or ActiveCell in a worksheet
		"""
		# Returns the Row containing TopLeftCell of an item
		def topLeftCellRow(item):
			row=item.TopLeftCell.Row
			# Cache row on the COM object as we need it later
			item._comobj.excelRow=row
			return row
		items=self.collectionFromWorksheet(self.document)
		if not items:
			return
		items=sorted(items,key=topLeftCellRow)
		if position:
			rangeObj=position.excelRangeObject
			row = rangeObj.Row
			col = rangeObj.Column
			if self.direction=="next":
				for collectionItem in items:
					itemRow=collectionItem._comobj.excelRow
					if (itemRow>row or (itemRow==row and collectionItem.TopLeftCell.Column>col)) and self.filter(collectionItem):
						item=self.quickNavItemClass(self.itemType,self.document,collectionItem,items,self.treeInterceptorObj)
						yield item
			elif self.direction=="previous":
				for collectionItem in reversed(items):
					itemRow=collectionItem._comobj.excelRow
					if (itemRow<row or (itemRow==row and collectionItem.TopLeftCell.Column<col)) and self.filter(collectionItem):
						item=self.quickNavItemClass(self.itemType,self.document,collectionItem,items,self.treeInterceptorObj )
						yield item
		else:
			for collectionItem in items:
				if self.filter(collectionItem):
					item=self.quickNavItemClass(self.itemType,self.document,collectionItem , items,self.treeInterceptorObj )
					yield item

	def filter(self,shape):
		if shape.Type == msoFormControl:
			if shape.FormControlType == xlGroupBox or shape.Visible != msoTrue:
				return False
			else:
				return True
		else:
			return False

class ExcelFormControlListBox(ExcelFormControl):

	def __init__(self,windowHandle=None,parent=None,excelFormControlObject=None):
		super(ExcelFormControlListBox,self).__init__(windowHandle=windowHandle, parent=parent, excelFormControlObject=excelFormControlObject)
		try:
			self.listSize=int(self.excelControlFormatObject.ListCount)
		except:
			self.listSize=0
		try:
			self.selectedItemIndex= int(self.excelControlFormatObject.ListIndex)
		except:
			self.selectedItemIndex=0
		try:
			self.isMultiSelectable= self.excelControlFormatObject.multiSelect!=xlNone
		except:
			self.isMultiSelectable=False

	def getChildAtIndex(self,index):
		name=str(self.excelOLEFormatObject.List(index+1))
		states=set([controlTypes.STATE_SELECTABLE])
		if self.excelOLEFormatObject.Selected[index+1]==True:
			states.add(controlTypes.STATE_SELECTED)
		return ExcelDropdownItem(parent=self,name=name,states=states,index=index)

	def _get_childCount(self):
		return self.listSize

	def _get_firstChild(self):
		if self.listSize>0:
			return self.getChildAtIndex(0)

	def _get_lastChild(self):
		if self.listSize>0:
			return self.getChildAtIndex(self.listSize-1)

	def script_moveUp(self, gesture):
		if self.selectedItemIndex > 1:
			self.selectedItemIndex= self.selectedItemIndex - 1
			if not self.isMultiSelectable:
				try:
					self.excelOLEFormatObject.Selected[self.selectedItemIndex] = True
				except:
					pass
			child=self.getChildAtIndex(self.selectedItemIndex-1)
			if child:
				eventHandler.queueEvent("gainFocus",child)
	script_moveUp.canPropagate=True

	def script_moveDown(self, gesture):
		if self.selectedItemIndex < self.listSize:
			self.selectedItemIndex= self.selectedItemIndex + 1
			if not self.isMultiSelectable:
				try:
					self.excelOLEFormatObject.Selected[self.selectedItemIndex] = True
				except:
					pass
			child=self.getChildAtIndex(self.selectedItemIndex-1)
			if child:
				eventHandler.queueEvent("gainFocus",child)
	script_moveDown.canPropagate=True

	def doAction(self):
		if self.isMultiSelectable:
			try:
				lb=self.excelOLEFormatObject
				lb.Selected[self.selectedItemIndex] =not lb.Selected[self.selectedItemIndex] 
			except:
				return
			child=self.getChildAtIndex(self.selectedItemIndex-1)
			eventHandler.queueEvent("gainFocus",child)

	__gestures= {
		"kb:upArrow": "moveUp",
		"kb:downArrow":"moveDown",
	}

class ExcelFormControlDropDown(ExcelFormControl):

	def __init__(self,windowHandle=None,parent=None,excelFormControlObject=None):
		super(ExcelFormControlDropDown,self).__init__(windowHandle=windowHandle, parent=parent, excelFormControlObject=excelFormControlObject)
		try:
			self.listSize=self.excelControlFormatObject.ListCount
		except:
			self.listSize=0
		try:
			self.selectedItemIndex=self.excelControlFormatObject.ListIndex
		except:
			self.selectedItemIndex=0

	def script_moveUp(self, gesture):
		if self.selectedItemIndex > 1:
			self.selectedItemIndex= self.selectedItemIndex - 1
			self.excelOLEFormatObject.Selected[self.selectedItemIndex] = True
			eventHandler.queueEvent("valueChange",self)
	script_moveUp.canPropagate=True

	def script_moveDown(self, gesture):
		if self.selectedItemIndex < self.listSize:
			self.selectedItemIndex= self.selectedItemIndex + 1
			self.excelOLEFormatObject.Selected[self.selectedItemIndex] = True
			eventHandler.queueEvent("valueChange",self)
	script_moveDown.canPropagate=True

	def _get_value(self):
		if self.selectedItemIndex < self.listSize:
			return str(self.excelOLEFormatObject.List(self.selectedItemIndex))

	__gestures= {
		"kb:upArrow": "moveUp",
		"kb:downArrow":"moveDown",
	}

class ExcelFormControlScrollBar(ExcelFormControl):

	def __init__(self,windowHandle=None,parent=None,excelFormControlObject=None):
		super(ExcelFormControlScrollBar,self).__init__(windowHandle=windowHandle, parent=parent, excelFormControlObject=excelFormControlObject)
		try:
			self.minValue=self.excelControlFormatObject.min
		except:
			self.minValue=0
		try:
			self.maxValue=self.excelControlFormatObject.max
		except:
			self.maxValue=0
		try:
			self.smallChange=self.excelControlFormatObject.smallChange
		except:
			self.smallChange=0
		try:
			self.largeChange=self.excelControlFormatObject.largeChange
		except:
			self.largeChange=0

	def _get_value(self):
		try:
			return str(self.excelControlFormatObject.value)
		except COMError:
			return 0

	def moveValue(self,up=False,large=False):
		try:
			curValue=self.excelControlFormatObject.value
		except COMError:
			return
		if up:
			newValue=min(curValue+(self.largeChange if large else self.smallChange),self.maxValue)
		else:
			newValue=max(curValue-(self.largeChange if large else self.smallChange),self.minValue)
		self.excelControlFormatObject.value=newValue
		eventHandler.queueEvent("valueChange",self)

	def script_moveUpSmall(self,gesture):
		self.moveValue(True,False)

	def script_moveDownSmall(self,gesture):
		self.moveValue(False,False)

	def script_moveUpLarge(self,gesture):
		self.moveValue(True,True)

	def script_moveDownLarge(self,gesture):
		self.moveValue(False,True)

	__gestures={
		"kb:upArrow":"moveUpSmall",
		"kb:downArrow":"moveDownSmall",
		"kb:pageUp":"moveUpLarge",
		"kb:pageDown":"moveDownLarge",
	}
