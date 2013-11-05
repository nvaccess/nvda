#appModules/powerpnt.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012-2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import comtypes
from comtypes.automation import IDispatch
import comtypes.client
import ctypes
import oleacc
import comHelper
import queueHandler
import colors
import api
import speech
import sayAllHandler
import NVDAHelper
import winUser
from treeInterceptorHandler import TreeInterceptor
from NVDAObjects import NVDAObjectTextInfo
from displayModel import DisplayModelTextInfo, EditableTextDisplayModelTextInfo
import textInfos.offsets
import eventHandler
import appModuleHandler
from NVDAObjects.IAccessible import IAccessible, getNVDAObjectFromEvent
from NVDAObjects.window import Window
from NVDAObjects.behaviors import EditableTextWithoutAutoSelectDetection
import braille
from cursorManager import ReviewCursorManager
import controlTypes
from logHandler import log
import scriptHandler

# Window classes where PowerPoint's object model should be used 
# These also all request to have their (incomplete) UI Automation implementations  disabled. [MS Office 2013]
objectModelWindowClasses=set(["paneClassDC","mdiClass","screenClass"])

#comtypes COM interface definition for Powerpoint application object's events 
class EApplication(IDispatch):
	_iid_=comtypes.GUID('{914934C2-5A91-11CF-8700-00AA0060263B}')
	_methods_=[]
	_disp_methods_=[
		comtypes.DISPMETHOD([comtypes.dispid(2001)],None,"WindowSelectionChange",
			(['in'],ctypes.POINTER(IDispatch),'sel'),),
		comtypes.DISPMETHOD([comtypes.dispid(2013)],None,"SlideShowNextSlide",
			(['in'],ctypes.POINTER(IDispatch),'slideShowWindow'),),
	]

#Our implementation of the EApplication COM interface to receive application events
class ppEApplicationSink(comtypes.COMObject):
	_com_interfaces_=[EApplication,IDispatch]

	def SlideShowNextSlide(self,slideShowWindow=None):
		i=winUser.getGUIThreadInfo(0)
		oldFocus=api.getFocusObject()
		if not isinstance(oldFocus,SlideShowWindow) or i.hwndFocus!=oldFocus.windowHandle:
			return
		oldFocus.treeInterceptor.rootNVDAObject.handleSlideChange()

	def WindowSelectionChange(self,sel):
		i=winUser.getGUIThreadInfo(0)
		oldFocus=api.getFocusObject()
		if not isinstance(oldFocus,Window) or i.hwndFocus!=oldFocus.windowHandle:
			return
		if isinstance(oldFocus,DocumentWindow):
			documentWindow=oldFocus
		elif isinstance(oldFocus,PpObject):
			documentWindow=oldFocus.documentWindow
		else:
			return
		documentWindow.ppSelection=sel
		documentWindow.handleSelectionChange()

#Bullet types
ppBulletNumbered=2

# values for enumeration 'PpPlaceholderType'
ppPlaceholderMixed = -2
ppPlaceholderTitle = 1
ppPlaceholderBody = 2
ppPlaceholderCenterTitle = 3
ppPlaceholderSubtitle = 4
ppPlaceholderVerticalTitle = 5
ppPlaceholderVerticalBody = 6
ppPlaceholderObject = 7
ppPlaceholderChart = 8
ppPlaceholderBitmap = 9
ppPlaceholderMediaClip = 10
ppPlaceholderOrgChart = 11
ppPlaceholderTable = 12
ppPlaceholderSlideNumber = 13
ppPlaceholderHeader = 14
ppPlaceholderFooter = 15
ppPlaceholderDate = 16
ppPlaceholderVerticalObject = 17
ppPlaceholderPicture = 18

ppPlaceholderLabels={
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderTitle:_("Title placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderBody:_("Text placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderCenterTitle:_("Center Title placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderSubtitle:_("Subtitle placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderVerticalTitle:_("Vertical Title placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderVerticalBody:_("Vertical Text placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderObject:_("Object placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderChart:_("Chart placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderBitmap:_("Bitmap placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderMediaClip:_("Media Clip placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderOrgChart:_("Org Chart placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderTable:_("Table placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderSlideNumber:_("Slide Number placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderHeader:_("Header placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderFooter:_("Footer placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderDate:_("Date placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderVerticalObject:_("Vertical Object placeholder"),
	# Translators: Describes a type of placeholder shape in Microsoft PowerPoint. 
	ppPlaceholderPicture:_("Picture placeholder"),
}

#selection types
ppSelectionNone=0
ppSelectionSlides=1
ppSelectionShapes=2
ppSelectionText=3

# values for enumeration 'PpViewType'
ppViewSlide = 1
ppViewSlideMaster = 2
ppViewNotesPage = 3
ppViewHandoutMaster = 4
ppViewNotesMaster = 5
ppViewOutline = 6
ppViewSlideSorter = 7
ppViewTitleMaster = 8
ppViewNormal = 9
ppViewPrintPreview = 10
ppViewThumbnails = 11
ppViewMasterThumbnails = 12

ppViewTypeLabels={
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewSlide:_("Slide view"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewSlideMaster:_("Slide Master view"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewNotesPage:_("Notes page"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewHandoutMaster:_("Handout Master view"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewNotesMaster:_("Notes Master view"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewOutline:_("Outline view"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewSlideSorter:_("Slide Sorter view"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewTitleMaster:_("Title Master view"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewNormal:_("Normal view"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewPrintPreview:_("Print Preview"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewThumbnails:_("Thumbnails"),
	# Translators: a label for a particular view or pane in Microsoft PowerPoint
	ppViewMasterThumbnails:_("Master Thumbnails"),
}

# values for enumeration 'MsoShapeType'
msoShapeTypeMixed = -2
msoAutoShape = 1
msoCallout = 2
msoChart = 3
msoComment = 4
msoFreeform = 5
msoGroup = 6
msoEmbeddedOLEObject = 7
msoFormControl = 8
msoLine = 9
msoLinkedOLEObject = 10
msoLinkedPicture = 11
msoOLEControlObject = 12
msoPicture = 13
msoPlaceholder = 14
msoTextEffect = 15
msoMedia = 16
msoTextBox = 17
msoScriptAnchor = 18
msoTable = 19
msoCanvas = 20
msoDiagram = 21
msoInk = 22
msoInkComment = 23
msoSmartArt = 24

msoShapeTypesToNVDARoles={
	msoChart:controlTypes.ROLE_CHART,
	msoGroup:controlTypes.ROLE_GROUPING,
	msoEmbeddedOLEObject:controlTypes.ROLE_EMBEDDEDOBJECT,
	msoLine:controlTypes.ROLE_LINE,
	msoLinkedOLEObject:controlTypes.ROLE_EMBEDDEDOBJECT,
	msoLinkedPicture:controlTypes.ROLE_GRAPHIC,
	msoPicture:controlTypes.ROLE_GRAPHIC,
	msoTextBox:controlTypes.ROLE_TEXTFRAME,
	msoTable:controlTypes.ROLE_TABLE,
	msoCanvas:controlTypes.ROLE_CANVAS,
	msoDiagram:controlTypes.ROLE_DIAGRAM,
}

def getBulletText(ppBulletFormat):
	t=ppBulletFormat.type
	if t==ppBulletNumbered:
		return "%d."%ppBulletFormat.number #(ppBulletFormat.startValue+(ppBulletFormat.number-1))
	elif t:
		return unichr(ppBulletFormat.character)

class PaneClassDC(Window):
	"""Handles fetching of the Powerpoint object model."""

	presentationType=Window.presType_content
	role=controlTypes.ROLE_PANE
	value=None
	TextInfo=DisplayModelTextInfo

	_cache_currentSlide=False
	def _get_currentSlide(self):
		try:
			ppSlide=self.ppObjectModel.view.slide
		except comtypes.COMError:
			return None
		self.currentSlide=SlideBase(windowHandle=self.windowHandle,documentWindow=self,ppObject=ppSlide)
		return self.currentSlide

	def _get_ppVersionMajor(self):
		self.ppVersionMajor=int(self.ppObjectModel.application.version.split('.')[0])
		return self.ppVersionMajor

class DocumentWindow(PaneClassDC):
	"""Represents the document window for a presentation. Bounces focus to the currently selected slide, shape or text frame."""

	def _get_ppDocumentViewType(self):
		try:
			viewType=self.ppObjectModel.viewType
		except comtypes.COMError:
			return None
		self.ppDocumentViewType=viewType
		return self.ppDocumentViewType

	def _get_ppActivePaneViewType(self):
		try:
			viewType=self.ppObjectModel.activePane.viewType
		except comtypes.COMError:
			return None
		self.ppActivePaneViewType=viewType
		return self.ppActivePaneViewType

	def _isEqual(self,other):
		return self.windowHandle==other.windowHandle and self.name==other.name

	def _get_name(self):
		label=ppViewTypeLabels.get(self.ppActivePaneViewType)
		if not label: 
			return super(PaneClassDC,self).name
		slide=self.currentSlide
		if slide:
			label=" - ".join([slide.name,label])
		return label

	def _get_currentSlide(self):
		if self.ppActivePaneViewType in (ppViewSlideSorter,ppViewThumbnails,ppViewMasterThumbnails): return None
		return super(DocumentWindow,self).currentSlide

	def _get_ppSelection(self):
		"""Fetches and caches the current Powerpoint Selection object for the current presentation."""
		self.ppSelection=self.ppObjectModel.selection
		return self.ppSelection

	def _get_selection(self):
		"""Fetches an NVDAObject representing the current presentation's selected slide, shape or text frame.""" 
		sel=self.ppSelection
		selType=sel.type
		#MS Powerpoint 2007 and below does not correctly indecate text selection in the notes page when in normal view
		if selType==0 and self.ppVersionMajor<=12:
			if self.ppActivePaneViewType==ppViewNotesPage and self.ppDocumentViewType==ppViewNormal:
				selType=ppSelectionText
		if selType==ppSelectionShapes: #Shape
			#The selected shape could be within a group shape
			if sel.hasChildShapeRange:
				ppObj=sel.childShapeRange[1]
			else: #a normal top level shape
				ppObj=sel.shapeRange[1]
			#Specifically handle shapes representing a table as they have row and column counts etc
			if ppObj.hasTable:
				return Table(windowHandle=self.windowHandle,documentWindow=self,ppObject=ppObj)
			else: #Generic shape
				return Shape(windowHandle=self.windowHandle,documentWindow=self,ppObject=ppObj)
		elif selType==ppSelectionText: #Text frame
			#TextRange objects in Powerpoint do not allow moving/expanding.
			#Therefore A full TextRange object must be fetched from the original TextFrame the selection is in.
			#MS Powerpoint 2003 also throws COMErrors when there is no TextRange.parent
			try:
				ppObj=sel.textRange.parent
			except comtypes.COMError:
				ppObj=None
			if ppObj:
				return TextFrame(windowHandle=self.windowHandle,documentWindow=self,ppObject=ppObj)
			#For TextRange objects for TextFrame objects in table cells and the notes page, TextRange object's parent does not work! 
			#For tables: Get the shape the selection is in -- should be the table.
			try:
				shape=sel.shapeRange[1]
			except comtypes.COMError:
				shape=None
			if shape and shape.hasTable:
				#Only way to find the selected cell in a table is to... walk through it.
				selectedTableCell=None
				colNum=0
				for col in shape.table.columns:
					colNum+=1
					rowNum=0
					for tableCell in col.cells:
						rowNum+=1
						if tableCell.selected:
							selectedTableCell=tableCell
							break
					if selectedTableCell:
						break
				if selectedTableCell:
					#We found the selected table cell
					#The TextFrame we want is within the shape in this table cell.
					#However, the shape in the table cell seems to always be rather broken -- hardly any properties work.
					#Therefore, Explicitly set the table cell as the TextFrame object's parent, skipping the broken shape
					ppObj=selectedTableCell.shape.textFrame
					obj=TableCellTextFrame(windowHandle=self.windowHandle,documentWindow=self,ppObject=ppObj)
					table=Table(windowHandle=self.windowHandle,documentWindow=self,ppObject=shape)
					obj.parent=TableCell(windowHandle=self.windowHandle,documentWindow=self,ppObject=selectedTableCell,table=table,rowNumber=rowNum,columnNumber=colNum)
					return obj
			#TextRange object did not have a parent, and we're not in a table.
			if self.ppActivePaneViewType==ppViewNotesPage and self.ppDocumentViewType==ppViewNormal:
				#We're in the notes page in normal view
				#The TextFrame in this case will be located in the notes page's second shape.
				slide=sel.slideRange[1]
				notesPage=slide.notesPage[1]
				shape=notesPage.shapes[2]
				ppObj=shape.textFrame
				return NotesTextFrame(windowHandle=self.windowHandle,documentWindow=self,ppObject=ppObj)
			if ppObj:
				return TextFrame(windowHandle=self.windowHandle,documentWindow=self,ppObject=ppObj)
		if selType==ppSelectionSlides:
			try:
				ppObj=sel.slideRange[1]
			except comtypes.COMError:
				#Master thumbnails sets the selected slide as view.slide but not selection.slideRange
				try:
					ppObj=self.ppObjectModel.view.slide
				except comtypes.COMError:
					ppObj=None
			if ppObj:
				return SlideBase(windowHandle=self.windowHandle,documentWindow=self,ppObject=ppObj)

	def _get_focusRedirect(self):
		return self.selection

	def _get_firstChild(self):
		return self.selection

	def handleSelectionChange(self):
		"""Pushes focus to the newly selected object."""
		if getattr(self,"_isHandlingSelectionChange",False):
			# #3394: A COM event can cause this function to run within itself.
			# This can cause double speaking, so stop here if we're already running.
			return
		self._isHandlingSelectionChange=True
		try:
			obj=self.selection
			if not obj:
				obj=IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=self.IAccessibleChildID)
			if obj and obj!=eventHandler.lastQueuedFocusObject:
				eventHandler.queueEvent("gainFocus",obj)
		finally:
			self._isHandlingSelectionChange=False

	def event_gainFocus(self):
		"""Bounces focus to the currently selected slide, shape or Text frame."""
		obj=self.selection
		if obj:
			eventHandler.queueEvent("focusEntered",self)
			eventHandler.queueEvent("gainFocus",obj)
		else:
			super(DocumentWindow,self).event_gainFocus()

	def script_selectionChange(self,gesture):
		gesture.send()
		if scriptHandler.isScriptWaiting():
			return
		self.handleSelectionChange()
	script_selectionChange.canPropagate=True

	__gestures={k:"selectionChange" for k in (
		"kb:tab","kb:shift+tab",
		"kb:leftArrow","kb:rightArrow","kb:upArrow","kb:downArrow",
		"kb:shift+leftArrow","kb:shift+rightArrow","kb:shift+upArrow","kb:shift+downArrow",
		"kb:pageUp","kb:pageDown",
		"kb:home","kb:control+home","kb:end","kb:control+end",
		"kb:shift+home","kb:shift+control+home","kb:shift+end","kb:shift+control+end",
		"kb:delete","kb:backspace",
	)}

class OutlinePane(EditableTextWithoutAutoSelectDetection,PaneClassDC):
	TextInfo=EditableTextDisplayModelTextInfo
	role=controlTypes.ROLE_EDITABLETEXT

class PpObject(Window):
	"""
	The base NVDAObject for slides, shapes and text frames.
	Accepts and holds references to the original Document window, and the current object's Powerpoint object. 
	Also has some utility functions and scripts for managing selection changes.
	Note No events are used to detect selection changes, its all keyboard commands for now.
	"""

	next=None
	previous=None

	def __init__(self,windowHandle=None,documentWindow=None,ppObject=None):
		self.documentWindow=documentWindow
		self.ppObject=ppObject
		super(PpObject,self).__init__(windowHandle=windowHandle)

	def _get_parent(self):
		return self.documentWindow

	def script_selectionChange(self,gesture):
		return self.documentWindow.script_selectionChange(gesture)

	__gestures={
		"kb:escape":"selectionChange",
	}

class SlideBase(PpObject):

	presentationType=Window.presType_content

	def findOverlayClasses(self,clsList):
		if isinstance(self.documentWindow,DocumentWindow) and self.documentWindow.ppActivePaneViewType in (ppViewSlideMaster,ppViewTitleMaster,ppViewNotesMaster,ppViewHandoutMaster,ppViewMasterThumbnails):
			clsList.append(Master)
		else:
			clsList.append(Slide)
		clsList.append(SlideBase)

	def _isEqual(self,other):
		return super(SlideBase,self)._isEqual(other) and self.name==other.name

	role=controlTypes.ROLE_PANE

class Slide(SlideBase):
	"""Represents a single slide in Powerpoint."""

	def _get_name(self):
		try:
			title=self.ppObject.shapes.title.textFrame.textRange.text
		except comtypes.COMError:
			title=None
		try:
			number=self.ppObject.slideNumber
		except comtypes.COMError:
			number=""
		# Translators: the label for a slide in Microsoft PowerPoint.
		name=_("Slide {slideNumber}").format(slideNumber=number)
		if title:
			name+=" (%s)"%title
		return name

	def _get_positionInfo(self):
		slideNumber=self.ppObject.slideNumber
		numSlides=self.ppObject.parent.slides.count
		return {'indexInGroup':slideNumber,'similarItemsInGroup':numSlides}

class Master(SlideBase):

	def _get_name(self):
		return self.ppObject.name

class Shape(PpObject):
	"""Represents a single shape (rectangle, group, picture, Text bos etc in Powerpoint."""

	presentationType=Window.presType_content

	def _get_ppPlaceholderType(self):
		try:
			return self.ppObject.placeholderFormat.type
		except comtypes.COMError:
			return None

	def _get_location(self):
		pointLeft=self.ppObject.left
		pointTop=self.ppObject.top
		pointWidth=self.ppObject.width
		pointHeight=self.ppObject.height
		left=self.documentWindow.ppObjectModel.pointsToScreenPixelsX(pointLeft)
		top=self.documentWindow.ppObjectModel.pointsToScreenPixelsY(pointTop)
		right=self.documentWindow.ppObjectModel.pointsToScreenPixelsX(pointLeft+pointWidth)
		bottom=self.documentWindow.ppObjectModel.pointsToScreenPixelsY(pointTop+pointHeight)
		width=right-left
		height=bottom-top
		return (left,top,width,height)

	def _get_ppShapeType(self):
		"""Fetches and caches the type of this shape."""
		self.ppShapeType=self.ppObject.type
		return self.ppShapeType

	def _get_name(self):
		"""The name is calculated firstly from the object's title, otherwize if its a generic shape, then  part of its programmatic name is used."""
		#Powerpoint 2003 shape objects do not have a title property 
		try:
			title=self.ppObject.title
		except comtypes.COMError:
			title=None
		if title:
			return title
		if self.ppShapeType==msoPlaceholder:
			label=ppPlaceholderLabels.get(self.ppPlaceholderType)
			if label:
				return label
		if self.role==controlTypes.ROLE_SHAPE:
			name=self.ppObject.name
			return " ".join(name.split(' ')[:-1])

	def _isEqual(self,other):
		return super(Shape,self)._isEqual(other) and self.ppObject.ID==other.ppObject.ID

	def _get_description(self):
		return self.ppObject.alternativeText

	def _get_role(self):
		return msoShapeTypesToNVDARoles.get(self.ppShapeType,controlTypes.ROLE_SHAPE)

	def _get_value(self):
		if self.ppObject.hasTextFrame:
			return self.ppObject.textFrame.textRange.text

	__gestures={
		"kb:enter":"selectionChange",
		"kb:f2":"selectionChange",
	}

class TextFrameTextInfo(textInfos.offsets.OffsetsTextInfo):

	def _getCaretOffset(self):
		return self.obj.documentWindow.ppSelection.textRange.start-1

	def _getSelectionOffsets(self):
		sel=self.obj.documentWindow.ppSelection.textRange
		start=sel.start-1
		end=start+sel.length
		return start,end

	def _getTextRange(self,start,end):
		text=self.obj.ppObject.textRange.text[start:end].replace('\x0b','\n')
		text=text.replace('\r','\n')
		return text

	def _getStoryLength(self):
		return self.obj.ppObject.textRange.length

	def _getLineOffsets(self,offset):
		#Seems to be no direct way to find the line offsets for a given offset.
		#Therefore walk through all the lines until one surrounds  the offset.
		lines=self.obj.ppObject.textRange.lines()
		length=lines.length
		# #3403: handle case where offset is at end of the text in in a control with only one line
		# The offset should be limited to the last offset in the text, but only if the text does not end in a line feed.
		if length and offset>=length and self._getTextRange(length-1,length)!='\n':
			offset=min(offset,length-1)
		for line in lines:
			start=line.start-1
			end=start+line.length
			if start<=offset<end:
				return start,end
		return offset,offset+1

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		formatField=textInfos.FormatField()
		curRun=None
		if calculateOffsets:
			runs=self.obj.ppObject.textRange.runs()
			for run in runs:
				start=run.start-1
				end=start+run.length
				if start<=offset<end:
					startOffset=start
					endOffset=end
					curRun=run
					break
		if not curRun:
			curRun=self.obj.ppObject.textRange.characters(offset+1)
			startOffset,endOffset=offset,self._endOffset
		if self._startOffset==0 or offset==self._startOffset and self._getTextRange(offset-1,offset).startswith('\n'):
			b=curRun.paragraphFormat.bullet
			bulletText=getBulletText(b)
			if bulletText:
				formatField['line-prefix']=bulletText
		font=curRun.font
		if formatConfig['reportFontName']:
			formatField['font-name']=font.name
		if formatConfig['reportFontSize']:
			formatField['font-size']=str(font.size)
		if formatConfig['reportFontAttributes']:
			formatField['bold']=bool(font.bold)
			formatField['italic']=bool(font.italic)
			formatField['underline']=bool(font.underline)
			if font.subscript:
				formatField['text-position']='sub'
			elif font.superscript:
				formatField['text-position']='super'
		if formatConfig['reportColor']:
			formatField['color']=colors.RGB.fromCOLORREF(font.color.rgb)
		return formatField,(startOffset,endOffset)

class Table(Shape):
	"""Represents the table shape in Powerpoint. Provides row and column counts."""
	def _get_ppTable(self):
		self.ppTable=self.ppObject.table
		return self.ppTable

	def _get_columnCount(self):
		return self.ppTable.columns.count

	def _get_rowCount(self):
		return self.ppTable.rows.count

class TableCell(PpObject):
	"""Represents a table cell in Powerpoint. Accepts a table and a row and column number as this cannot be calculated directly."""
	name=None
	role=controlTypes.ROLE_TABLECELL

	def _isEqual(self,other):
		return self.table==other.table and (self.columnNumber,self.rowNumber)==(other.columnNumber,other.rowNumber)

	def __init__(self,windowHandle=None,documentWindow=None,ppObject=None,table=None,rowNumber=None,columnNumber=None):
		self.parent=self.table=table
		self.columnNumber=columnNumber
		self.rowNumber=rowNumber
		super(TableCell,self).__init__(windowHandle=windowHandle,documentWindow=documentWindow,ppObject=ppObject)

class TextFrame(EditableTextWithoutAutoSelectDetection,PpObject):
	"""Represents a Text frame in Powerpoint. Provides a suitable TextInfo."""

	TextInfo=TextFrameTextInfo

	def __init__(self,windowHandle=None,documentWindow=None,ppObject=None):
		super(TextFrame,self).__init__(windowHandle=windowHandle,documentWindow=documentWindow,ppObject=ppObject)
		EditableTextWithoutAutoSelectDetection.initClass(self)

	def _isEqual(self,other):
		return super(TextFrame,self)._isEqual(other) and self.ppObject.parent.ID==other.ppObject.parent.ID

	name=None
	role=controlTypes.ROLE_EDITABLETEXT

	def _get_parent(self):
		parent=self.ppObject.parent
		if parent:
			return Shape(windowHandle=self.windowHandle,documentWindow=self.documentWindow,ppObject=parent)

class TableCellTextFrame(TextFrame):
	"""Represents a text frame inside a table cell in Powerpoint. Specifially supports the caret jumping into another cell with tab or arrows."""

	def _isEqual(self,other):
		return self.parent==other.parent

	__gestures={
		"kb:tab":"selectionChange",
		"kb:shift+tab":"selectionChange",
	}

class NotesTextFrame(TextFrame):

	def _get_parent(self):
		return self.documentWindow

class SlideShowTreeInterceptorTextInfo(NVDAObjectTextInfo):
	"""The TextInfo for Slide Show treeInterceptors. Based on NVDAObjectTextInfo but tweeked to work with TreeInterceptors by using basicText on the treeInterceptor's rootNVDAObject."""

	def _getStoryText(self):
		return self.obj.rootNVDAObject.basicText

	def _getOffsetsFromNVDAObject(self,obj):
		if obj==self.obj.rootNVDAObject:
			return (0,self._getStoryLength())
		raise LookupError

class SlideShowTreeInterceptor(TreeInterceptor):
	"""A TreeInterceptor for showing Slide show content. Has no caret navigation, a CursorManager must be used on top. """

	def _get_isAlive(self):
		return winUser.isWindow(self.rootNVDAObject.windowHandle)

	def __contains__(self,obj):
		return isinstance(obj,Window) and obj.windowHandle==self.rootNVDAObject.windowHandle

	hadFocusOnce=False

	def event_treeInterceptor_gainFocus(self):
		braille.handler.handleGainFocus(self)
		self.rootNVDAObject.reportFocus()
		if not self.hadFocusOnce:
			self.hadFocusOnce=True
			self.reportNewSlide()
		else:
			info = self.selection
			if not info.isCollapsed:
				speech.speakSelectionMessage(_("selected %s"), info.text)
			else:
				info.expand(textInfos.UNIT_LINE)
				speech.speakTextInfo(info, reason=controlTypes.REASON_CARET, unit=textInfos.UNIT_LINE)

	def event_gainFocus(self,obj,nextHandler):
		pass

	TextInfo=SlideShowTreeInterceptorTextInfo

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

	def reportNewSlide(self):
		self.makeTextInfo(textInfos.POSITION_FIRST).updateCaret()
		sayAllHandler.readText(sayAllHandler.CURSOR_CARET)

	def script_toggleNotesMode(self,gesture):
		self.rootNVDAObject.notesMode=not self.rootNVDAObject.notesMode
		self.rootNVDAObject.handleSlideChange()
	# Translators: The description for a script
	script_toggleNotesMode.__doc__=_("Toggles between reporting the speaker notes or the actual slide content. This does not change what is visible on-screen, but only what the user can read with NVDA")

	def script_slideChange(self,gesture):
		gesture.send()
		self.rootNVDAObject.handleSlideChange()

	__gestures={
		"kb:space":"slideChange",
		"kb:enter":"slideChange",
		"kb:backspace":"slideChange",
		"kb:pageUp":"slideChange",
		"kb:pageDown":"slideChange",
		"kb:control+shift+s":"toggleNotesMode",
	}

class ReviewableSlideshowTreeInterceptor(ReviewCursorManager,SlideShowTreeInterceptor):
	"""A TreeInterceptor for Slide show content but with caret navigation via ReivewCursorManager."""
	pass

class SlideShowWindow(PaneClassDC):

	_lastSlideChangeID=None

	treeInterceptorClass=ReviewableSlideshowTreeInterceptor
	notesMode=False #: If true then speaker notes will be exposed as this object's basicText, rather than the actual slide content.

	def _get_name(self):
		if self.currentSlide:
			if self.notesMode:
				# Translators: The title of the current slide (with notes) in a running Slide Show in Microsoft PowerPoint.
				return _("Slide show notes - {slideName}").format(slideName=self.currentSlide.name)
			else:
				# Translators: The title of the current slide in a running Slide Show in Microsoft PowerPoint.
				return _("Slide show - {slideName}").format(slideName=self.currentSlide.name)
		else:
			# Translators: The title for a Slide show in Microsoft PowerPoint that has completed.
			return _("Slide Show - complete")

	value=None

	def _getShapeText(self,shape,cellShape=False):
		if shape.hasTextFrame:
			for p in shape.textFrame.textRange.paragraphs(): 
				bulletText=getBulletText(p.paragraphFormat.bullet)
				text=p.text.replace('\x0b','\n')
				text=text.replace('\r','\n')
				text=text.rstrip()
				text=" ".join([t for t in (bulletText,text) if t])
				if text and not text.isspace():
					yield text
			return
		if cellShape: return
		shapeType=shape.type
		if shapeType==msoGroup:
			for childShape in shape.groupItems:
				for chunk in self._getShapeText(childShape):
					yield chunk
			return
		if shape.hasTable:
			table=shape.table
			for row in table.rows:
				for cell in row.cells:
					for chunk in self._getShapeText(cell.shape,cellShape=True):
						yield chunk
			return
		label=shape.alternativeText
		if not label:
			try:
				label=shape.title
			except comtypes.COMError:
				pass
		if label:
			typeName=" ".join(shape.name.split(' ')[:-1])
			if typeName and not typeName.isspace():
				yield "%s %s"%(typeName,label)
			else:
				yield label

	def _get_basicText(self):
		if not self.currentSlide:
			return self.name
		chunks=[]
		ppObject=self.currentSlide.ppObject
		if self.notesMode:
			ppObject=ppObject.notesPage
		for shape in ppObject.shapes:
			for chunk in self._getShapeText(shape):
				chunks.append(chunk)
		self.basicText="\n".join(chunks)
		if not self.basicText:
			if self.notesMode:
				# Translators: The message for no notes  for a slide in a slide show
				self.basicText=_("No notes")
			else:
				# Translators: The message for an empty slide in a slide show
				self.basicText=_("Empty slide")
		return self.basicText or _("Empty slide")

	def handleSlideChange(self):
		try:
			del self.__dict__['currentSlide']
		except KeyError:
			pass
		curSlideChangeID=self.name
		if curSlideChangeID==self._lastSlideChangeID:
			return
		self._lastSlideChangeID=curSlideChangeID
		try:
			del self.__dict__['basicText']
		except KeyError:
			pass
		self.reportFocus()
		self.treeInterceptor.reportNewSlide()

class AppModule(appModuleHandler.AppModule):

	hasTriedPpAppSwitch=False
	_ppApplicationWindow=None
	_ppApplication=None
	_ppEApplicationConnectionPoint=None

	def isBadUIAWindow(self,hwnd):
		# PowerPoint 2013 implements UIA support for its slides etc on an mdiClass window. However its far from complete.
		# We must disable it in order to fall back to our own code.
		if winUser.getClassName(hwnd) in objectModelWindowClasses:
			return True
		return super(AppModule,self).isBadUIAWindow(hwnd)

	def _registerCOMWithFocusJuggle(self):
		import wx
		import gui
		# Translators: A title for a dialog shown while Microsoft PowerPoint initializes
		d=wx.Dialog(None,title=_("Waiting for Powerpoint..."))
		gui.mainFrame.prePopup()
		d.Show()
		self.hasTriedPpAppSwitch=True
		#Make sure NVDA detects and reports focus on the waiting dialog
		api.processPendingEvents()
		comtypes.client.PumpEvents(1)
		d.Destroy()
		gui.mainFrame.postPopup()

	def _getPpObjectModelFromWindow(self,windowHandle):
		"""
		Fetches the Powerpoint object model from a given window.
		"""
		try:
			pDispatch=oleacc.AccessibleObjectFromWindow(windowHandle,winUser.OBJID_NATIVEOM,interface=comtypes.automation.IDispatch)
			return comtypes.client.dynamic.Dispatch(pDispatch)
		except: 
			log.debugWarning("Could not get MS Powerpoint object model",exc_info=True)
			return None

	_ppApplicationFromROT=None

	def _getPpObjectModelFromROT(self,useRPC=False):
		if not self._ppApplicationFromROT:
			try:
				self._ppApplicationFromROT=comHelper.getActiveObject(u'powerPoint.application',dynamic=True,appModule=self if useRPC else None)
			except:
				log.debugWarning("Could not get active object via RPC")
				return None
		try:
			pres=self._ppApplicationFromROT.activePresentation
		except (comtypes.COMError,NameError,AttributeError):
			log.debugWarning("No active presentation")
			return None
		try:
			ppSlideShowWindow=pres.slideShowWindow
		except (comtypes.COMError,NameError,AttributeError):
			log.debugWarning("Could not get slideShowWindow")
			ppSlideShowWindow=None
		isActiveSlideShow=False
		if ppSlideShowWindow:
			try:
				isActiveSlideShow=ppSlideShowWindow.active
			except comtypes.COMError:
				log.debugWarning("slideShowWindow.active",exc_info=True)
		if isActiveSlideShow:
			return ppSlideShowWindow
		try:
			window=pres.windows.item(1)
		except (comtypes.COMError,NameError,AttributeError):
			window=None
		return window

	def _fetchPpObjectModelHelper(self,windowHandle=None):
		m=None
		# Its only safe to get the object model from PowerPoint 2003 to 2010 windows.
		# In PowerPoint 2013 protected mode it causes security/stability issues
		if windowHandle and winUser.getClassName(windowHandle)=="paneClassDC":
			m=self._getPpObjectModelFromWindow(windowHandle)
		if not m:
			m=self._getPpObjectModelFromROT(useRPC=True)
		if not m:
			m=self._getPpObjectModelFromROT()
		return m

	def fetchPpObjectModel(self,windowHandle=None):
		m=self._fetchPpObjectModelHelper(windowHandle=windowHandle)
		if not m and not self.hasTriedPpAppSwitch:
			self._registerCOMWithFocusJuggle()
			m=self._fetchPpObjectModelHelper(windowHandle=windowHandle)
		if m:
			if windowHandle!=self._ppApplicationWindow or not self._ppApplication:
				self._ppApplicationWindow=windowHandle
				self._ppApplication=m.application
				sink=ppEApplicationSink().QueryInterface(comtypes.IUnknown)
				self._ppEApplicationConnectionPoint=comtypes.client._events._AdviseConnection(self._ppApplication,EApplication,sink)
		return m

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if obj.windowClassName in objectModelWindowClasses and isinstance(obj,IAccessible) and not isinstance(obj,PpObject) and obj.event_objectID==winUser.OBJID_CLIENT and controlTypes.STATE_FOCUSED in obj.states:
			m=self.fetchPpObjectModel(windowHandle=obj.windowHandle)
			if not m:
				log.debugWarning("no object model")
				return
			try:
				ppActivePaneViewType=m.activePane.viewType
			except comtypes.COMError:
				ppActivePaneViewType=None
			if ppActivePaneViewType is None:
				clsList.insert(0,SlideShowWindow)
			elif ppActivePaneViewType==ppViewOutline:
				clsList.insert(0,OutlinePane)
			else:
				clsList.insert(0,DocumentWindow)
			obj.ppActivePaneViewType=ppActivePaneViewType
			obj.ppObjectModel=m
