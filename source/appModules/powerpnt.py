#appModules/powerpnt.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import comtypes
import comtypes.client
import oleacc
import colors
import api
import speech
import sayAllHandler
import winUser
from NVDAObjects import NVDAObjectTextInfo
from displayModel import DisplayModelTextInfo, EditableTextDisplayModelTextInfo
import textInfos.offsets
import eventHandler
import appModuleHandler
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.window import Window
from NVDAObjects.behaviors import EditableTextWithoutAutoSelectDetection
from cursorManager import ReviewCursorManager
import controlTypes
from logHandler import log

#Bullet types
ppBulletNumbered=2

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
	ppViewSlide:_("Slide view"),
	ppViewSlideMaster:_("Slide Master view"),
	ppViewNotesPage:_("Notes page"),
	ppViewHandoutMaster:_("Handout Master view"),
	ppViewNotesMaster:_("Notes Master view"),
	ppViewOutline:_("Outline view"),
	ppViewSlideSorter:_("Slide Sorter view"),
	ppViewTitleMaster:_("Title Master view"),
	ppViewNormal:_("Normal view"),
	ppViewPrintPreview:_("Print Preview"),
	ppViewThumbnails:_("Thumbnails"),
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

def getPpObjectModel(windowHandle):
	"""
	Fetches the Powerpoint object model from a given PaneClassDC window.
	"""
	try:
		pDispatch=oleacc.AccessibleObjectFromWindow(windowHandle,winUser.OBJID_NATIVEOM,interface=comtypes.automation.IDispatch)
	except (comtypes.COMError, WindowsError):
		log.debugWarning("Could not get MS Powerpoint object model",exc_info=True)
		return None
	return comtypes.client.dynamic.Dispatch(pDispatch)

class PaneClassDC(Window):
	"""Handles fetching of the Powerpoint object model."""

	presentationType=Window.presType_content
	role=controlTypes.ROLE_PANE
	value=None
	TextInfo=DisplayModelTextInfo

	def _get_ppObjectModel(self):
		"""Fetches and caches the Powerpoint DocumentWindow object for the current presentation."""
		m=getPpObjectModel(self.windowHandle)
		if m:
			self.ppObjectModel=m
			return self.ppObjectModel

	def _get_currentSlide(self):
		try:
			ppSlide=self.ppObjectModel.view.slide
		except comtypes.COMError:
			return None
		self.currentSlide=SlideBase(windowHandle=self.windowHandle,documentWindow=self,ppObject=ppSlide)
		return self.currentSlide

	def event_gainFocus(self):
		if not self.ppObjectModel and not self.appModule.hasTriedPpAppSwitch:
			#We failed to get the powerpoint object model, and we havn't yet tried fixing this by switching apps back and forth
			#As Powerpoint may have just been opened, it can take up to 10 seconds for the object model to be ready.
			#However, switching away to another application and back again forces the object model to be registered.
			#This call of ppObjectModel will be None, but the next event_gainFocus should work
			import wx
			import gui
			d=wx.Dialog(None,title=_("Waiting for Powerpoint..."))
			gui.mainFrame.prePopup()
			d.Show()
			self.appModule.hasTriedPpAppSwitch=True
			#Make sure NVDA detects and reports focus on the waiting dialog
			api.processPendingEvents()
			comtypes.client.PumpEvents(1)
			d.Destroy()
			gui.mainFrame.postPopup()
			#Focus would have now landed back on this window causing a new event_gainFocus, nothing more to do here.
			return
		super(PaneClassDC,self).event_gainFocus()

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
		if selType==0:
			if self.ppActivePaneViewType==ppViewNotesPage and self.ppDocumentViewType==ppViewNormal:
				#MS Powerpoint 2007 and below does not correctly indecate text selection in the notes page when in normal view
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

	def _get_firstChild(self):
		return self.selection

	def handleSelectionChange(self):
		"""Pushes focus to the newly selected object."""
		obj=self.selection
		if not obj:
			obj=DocumentWindow(windowHandle=self.windowHandle)
		if obj and obj!=api.getFocusObject():
			eventHandler.queueEvent("gainFocus",obj)

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
		self.handleSelectionChange()
	script_selectionChange.canPropagate=True

	__gestures={
		"kb:downArrow":"selectionChange",
		"kb:upArrow":"selectionChange",
		"kb:leftArrow":"selectionChange",
		"kb:rightArrow":"selectionChange",
		"kb:home":"selectionChange",
		"kb:end":"selectionChange",
		"kb:pageUp":"selectionChange",
		"kb:pageDown":"selectionChange",
		"kb:tab":"selectionChange",
		"kb:shift+tab":"selectionChange",
		"kb:control+enter":"selectionChange",
		"kb:enter":"selectionChange",
		"kb:f2":"selectionChange",
		"kb:escape":"selectionChange",
		"kb:delete":"selectionChange",
		"kb:control+c":"selectionChange",
		"kb:control+x":"selectionChange",
		"kb:control+v":"selectionChange",
	}

class OutlinePane(EditableTextWithoutAutoSelectDetection,DocumentWindow):
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
		number=self.ppObject.slideNumber
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

class TextFrameTextInfo(textInfos.offsets.OffsetsTextInfo):

	def _getCaretOffset(self):
		return self.obj.documentWindow.ppSelection.textRange.start-1

	def _getSelectionOffsets(self):
		sel=self.obj.documentWindow.ppSelection.textRange
		start=sel.start-1
		end=start+sel.length
		return start,end

	def _getTextRange(self,start,end):
		text=self.obj.ppObject.textRange.text[start:end].replace('\x0b','\n')+'\n'
		text=text.replace('\r','\n')
		return text

	def _getStoryLength(self):
		return self.obj.ppObject.textRange.length

	def _getLineOffsets(self,offset):
		#Seems to be no direct way to find the line offsets for a given offset.
		#Therefore walk through all the lines until one surrounds  the offset.
		lines=self.obj.ppObject.textRange.lines()
		length=lines.length
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

	def _caretScriptPostMovedHelper(self, speakUnit, info=None):
		if not self.parent.ppObject.selected:
			self.documentWindow.handleSelectionChange()
		else:
			super(TableCellTextFrame,self)._caretScriptPostMovedHelper(speakUnit, info=None)

	__gestures={
		"kb:tab":"selectionChange",
		"kb:shift+tab":"selectionChange",
	}

class NotesTextFrame(TextFrame):

	def _get_parent(self):
		return self.documentWindow

class SlideShowWindow(ReviewCursorManager,PaneClassDC):

	TextInfo=NVDAObjectTextInfo

	def _get_name(self):
		if self.currentSlide:
			return _("Slide show - {slideName}").format(slideName=self.currentSlide.name)
		else:
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
		chunks=[self.name]
		for shape in self.currentSlide.ppObject.shapes:
			for chunk in self._getShapeText(shape):
				chunks.append(chunk)
		self.basicText="\n".join(chunks)
		return self.basicText

	def handleNewSlide(self):
		speech.cancelSpeech()
		self.makeTextInfo(textInfos.POSITION_FIRST).updateCaret()
		sayAllHandler.readText(sayAllHandler.CURSOR_CARET)

	def event_gainFocus(self):
		self.handleNewSlide()

	def script_changeSlide(self,gesture):
		slideIndex=self.currentSlide.ppObject.slideIndex if self.currentSlide else None
		gesture.send()
		if slideIndex is not None:
			del self.__dict__['currentSlide']
			del self.__dict__['basicText']
		newSlideIndex=self.currentSlide.ppObject.slideIndex if self.currentSlide else None
		if newSlideIndex!=slideIndex:
			self.handleNewSlide()

	__gestures={
		"kb:space":"changeSlide",
		"kb:pageUp":"changeSlide",
		"kb:pageDown":"changeSlide",
	}

class AppModule(appModuleHandler.AppModule):

	hasTriedPpAppSwitch=False

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if obj.windowClassName=="paneClassDC" and isinstance(obj,IAccessible) and not isinstance(obj,PpObject) and obj.event_objectID==winUser.OBJID_CLIENT and controlTypes.STATE_FOCUSED in obj.states:
			m=getPpObjectModel(obj.windowHandle)
			if m:
				try:
					ppActivePaneViewType=m.activePane.viewType
				except comtypes.COMError:
					ppActivePaneViewType=None
				if ppActivePaneViewType is None:
					clsList.insert(0,SlideShowWindow)
				else:
					if ppActivePaneViewType==ppViewOutline:
						clsList.insert(0,OutlinePane)
					else:
						clsList.insert(0,DocumentWindow)
					self.ppActivePaneViewType=ppActivePaneViewType
			else:
				clsList.insert(0,PaneClassDC)
			self.ppObjectModel=m
