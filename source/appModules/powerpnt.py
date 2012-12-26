#appModules/powerpnt.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import comtypes
import comtypes.client
import oleacc
import api
import speech
import sayAllHandler
import winUser
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
ppSelectionSlides=0
ppSelectionShapes=2
ppSelectionText=3

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

	def findOverlayClasses(self,clsList):
		m=self.ppObjectModel
		if m:
			#If there is a selection then its an editable document (slide).
			#Otherwize it must be a slide show.
			try:
				m.selection
				clsList.append(DocumentWindow)
			except comtypes.COMError:
				clsList.append(SlideShowWindow)
		clsList.append(PaneClassDC)

	def __init__(self,windowHandle=None,ppObjectModel=None):
		if ppObjectModel:
			self.ppObjectModel=ppObjectModel
		super(PaneClassDC,self).__init__(windowHandle=windowHandle)

	def _get_ppObjectModel(self):
		"""Fetches and caches the Powerpoint DocumentWindow object for the current presentation."""
		m=getPpObjectModel(self.windowHandle)
		if m:
			self.ppObjectModel=m
			return self.ppObjectModel

class DocumentWindow(PaneClassDC):
	"""Represents the document window for a presentation. Bounces focus to the currently selected slide, shape or text frame."""

	def _get_ppSelection(self):
		"""Fetches and caches the current Powerpoint Selection object for the current presentation."""
		self.ppSelection=self.ppObjectModel.selection
		return self.ppSelection

	def _get_selection(self):
		"""Fetches an NVDAObject representing the current presentation's selected slide, shape or text frame.""" 
		sel=self.ppSelection
		selType=sel.type
		if selType==ppSelectionSlides: #Slide
			return Slide(windowHandle=self.windowHandle,documentWindow=self,ppObject=sel.slideRange[1])
		elif selType==ppSelectionShapes: #Shape
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
			#Usually its just the TextRange object's parent, nice and simple
			ppObj=sel.textRange.parent
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
			#Perhaps we're in the notes page for the current slide?
			#The TextFrame in this case will be located in the notes page's second shape.
			slide=sel.slideRange[1]
			notesPage=slide.notesPage[1]
			shape=notesPage.shapes[2]
			ppObj=shape.textFrame
			return TextFrame(windowHandle=self.windowHandle,documentWindow=self,ppObject=ppObj)

	def event_gainFocus(self):
		"""Bounces focus to the currently selected slide, shape or Text frame."""
		obj=self.selection
		if obj:
			eventHandler.queueEvent("gainFocus",obj)
		else:
			super(DocumentWindow,self).event_gainFocus()

class PpObject(Window):
	"""
	The base NVDAObject for slides, shapes and text frames.
	Accepts and holds references to the original Document window, and the current object's Powerpoint object. 
	Also has some utility functions and scripts for managing selection changes.
	Note No events are used to detect selection changes, its all keyboard commands for now.
	"""

	def __init__(self,windowHandle=None,documentWindow=None,ppObject=None):
		self.documentWindow=documentWindow
		self.ppObject=ppObject
		super(PpObject,self).__init__(windowHandle=windowHandle)

	def _get_parent(self):
		return self.documentWindow

	def handleSelectionChange(self):
		"""Pushes focus to the newly selected object."""
		obj=self.documentWindow.selection
		if obj and obj!=self:
			eventHandler.queueEvent("gainFocus",obj)

	def script_selectionChange(self,gesture):
		gesture.send()
		self.handleSelectionChange()

class Slide(PpObject):
	"""Represents a single slide in Powerpoint."""

	def _isEqual(self,other):
		return super(Slide,self)._isEqual(other) and self.ppObject.slideID==other.ppObject.slideID

	role=controlTypes.ROLE_PANE

	def _get_name(self):
		return "Slide %d"%self.ppObject.slideNumber

	def _get_children(self):
		return [Shape(windowHandle=self.windowHandle,documentWindow=self.documentWindow,ppObject=shape) for shape in self.ppObject.shapes]

	def _get_childCount(self):
		return self.ppObject.shapes.count

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
	}

class Shape(PpObject):
	"""Represents a single shape (rectangle, group, picture, Text bos etc in Powerpoint."""

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

	def _get_children(self):
		if self.ppShapeType==msoGroup:
			return [Shape(windowHandle=self.windowHandle,documentWindow=self.documentWindow,ppObject=shape) for shape in self.ppObject.groupItems]
		children=[]
		if self.ppObject.hasTextFrame:
			children.append(TextFrame(windowHandle=self.windowHandle,documentWindow=self.documentWindow,ppObject=self.ppObject.textFrame))
		if self.ppObject.hasTable:
			children.append(Table(windowHandle=self.windowHandle,documentWindow=self.documentWindow,ppObject=self.ppObject.table))
		return children

	def _get_childCount(self):
		if self.ppShapeType==msoGroup:
			return self.ppObject.groupItems.count
		childCount=0
		if self.ppObject.hasTextFrame:
			childCount+=1
		if self.ppObject.hasTable:
			childCount+=1
		return childCount

	def _get_parent(self):
		#Child shapes should have the group shape as its parent. But normal shapes should have the slide as its parent.
		if self.ppObject.child:
			parentGroup=self.ppObject.parentGroup
			return Shape(windowHandle=self.windowHandle,documentWindow=self.documentWindow,ppObject=parentGroup)
		parent=self.ppObject.parent
		if parent:
			return Slide(windowHandle=self.windowHandle,documentWindow=self.documentWindow,ppObject=parent)
		return super(Shape,self).parent

	def _get_value(self):
		if self.ppObject.hasTextFrame:
			return self.ppObject.textFrame.textRange.text

	__gestures={
		"kb:tab":"selectionChange",
		"kb:shift+tab":"selectionChange",
		"kb:escape":"selectionChange",
		"kb:enter":"selectionChange",
		"kb:space":"selectionChange",
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
		startOffset,endOffset=self._startOffset,self._endOffset
		if startOffset==0 or self._getTextRange(offset-1,offset).startswith('\n'):
			b=self.obj.ppObject.textRange.characters(offset+1,offset+1).paragraphFormat.bullet
			bulletText=getBulletText(b)
			if bulletText:
				formatField['line-prefix']=bulletText
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

	__gestures={
		"kb:escape":"selectionChange",
	}

class TableCellTextFrame(TextFrame):
	"""Represents a text frame inside a table cell in Powerpoint. Specifially supports the caret jumping into another cell with tab or arrows."""

	def _isEqual(self,other):
		return self.parent==other.parent

	def _caretScriptPostMovedHelper(self, speakUnit, info=None):
		if not self.parent.ppObject.selected:
			self.handleSelectionChange()
		else:
			super(TableCellTextFrame,self)._caretScriptPostMovedHelper(speakUnit, info=None)

	__gestures={
		"kb:tab":"selectionChange",
		"kb:shift+tab":"selectionChange",
	}

class SlideShowWindow(ReviewCursorManager,PaneClassDC):

	def _get_name(self):
		if self.ppSlide:
			return _("Slide show - Slide {slideNumber}").format(slideNumber=self.ppSlide.slideNumber)
		else:
			return _("Slide Show - complete")

	value=None

	def _get_ppSlide(self):
		try:
			self.ppSlide=self.ppObjectModel.view.slide
		except comtypes.COMError:
			log.debugWarning("end of slide show",exc_info=True)
			return None
		return self.ppSlide

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
		if not self.ppSlide:
			return self.name
		chunks=[self.name]
		for shape in self.ppSlide.shapes:
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
		slideIndex=self.ppSlide.slideIndex if self.ppSlide else None
		gesture.send()
		if slideIndex is not None:
			del self.__dict__['ppSlide']
			del self.__dict__['basicText']
		newSlideIndex=self.ppSlide.slideIndex if self.ppSlide else None
		if newSlideIndex!=slideIndex:
			self.handleNewSlide()

	__gestures={
		"kb:space":"changeSlide",
		"kb:pageUp":"changeSlide",
		"kb:pageDown":"changeSlide",
	}

class AppModule(appModuleHandler.AppModule):

	hasTriedPpAppSwitch=False

	def event_gainFocus(self,obj,nextHandler):
		if obj.windowClassName=="paneClassDC" and isinstance(obj,IAccessible) and not isinstance(obj,PpObject) and obj.event_objectID==winUser.OBJID_CLIENT:
			#We can get a powerpoint object model from this window.
			#Note that we fetch the object model outside of any NVDAObject as if it fails we may need to bounce focus out of Powerpoint and then back in to force it to register the model 
			m=getPpObjectModel(obj.windowHandle)
			if m:
				#We successfully got an object model
				#Create an NVDAObject that makes use of the object model to handle Document windows and Slide Show windows
				#And bounce focus to it.
				newObj=PaneClassDC(windowHandle=obj.windowHandle,ppObjectModel=m)
				eventHandler.queueEvent("gainFocus",newObj)
				return
			elif not self.hasTriedPpAppSwitch:
				#We failed to get the powerpoint object model, and we havn't yet tried fixing this by switching apps back and forth
				#As Powerpoint may have just been opened, it can take up to 10 seconds for the object model to be ready.
				#However, switching away to another application and back again forces the object model to be registered.
				#This call of ppObjectModel will be None, but the next event_gainFocus should work
				import wx
				import gui
				d=wx.Dialog(None,title=_("Waiting for Powerpoint..."))
				gui.mainFrame.prePopup()
				d.Show()
				self.hasTriedPpAppSwitch=True
				#Make sure NVDA detects and reports focus on the waiting dialog
				api.processPendingEvents()
				comtypes.client.PumpEvents(1)
				d.Destroy()
				gui.mainFrame.postPopup()
				#Focus would have now landed back on this window causing a new event_gainFocus, nothing more to do here.
				return
			else:
				log.error("Could not fetch Powerpoint object model")
		nextHandler()
