#NVDAObjects/MSHTML.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2015 NV Access Limited, Aleksey Sadovoy
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
from comtypes import COMError
import comtypes.client
import comtypes.automation
from comtypes import IServiceProvider
import ctypes
import ctypes.wintypes
import contextlib
import winUser
import oleacc
import UIAHandler
import IAccessibleHandler
import aria
from keyboardHandler import KeyboardInputGesture
import api
import textInfos
from logHandler import log
import controlTypes
from . import IAccessible
from ..behaviors import EditableTextWithoutAutoSelectDetection, Dialog
from .. import InvalidNVDAObject
from ..window import Window
from NVDAObjects.UIA import UIA, UIATextInfo
from locationHelper import RectLTRB
from typing import Dict

IID_IHTMLElement=comtypes.GUID('{3050F1FF-98B5-11CF-BB82-00AA00BDCE0B}')

class UIAMSHTMLTextInfo(UIATextInfo):

	# #4174: MSHTML's UIAutomation implementation does not handle the insertion point at the end of the control correcly.
	# Therefore get around it by detecting when the TextInfo is instanciated on it, and ensure that expand and move do the expected thing.
	
	_atEndOfStory=False

	def __init__(self,obj,position,_rangeObj=None):
		super(UIAMSHTMLTextInfo,self).__init__(obj,position,_rangeObj)
		if position==textInfos.POSITION_CARET:
			tempRange=self._rangeObj.clone()
			tempRange.ExpandToEnclosingUnit(UIAHandler.TextUnit_Character)
			if self._rangeObj.CompareEndpoints(UIAHandler.TextPatternRangeEndpoint_Start,tempRange,UIAHandler.TextPatternRangeEndpoint_Start)>0:
				self._atEndOfStory=True

	def copy(self):
		info=super(UIAMSHTMLTextInfo,self).copy()
		info._atEndOfStory=self._atEndOfStory
		return info

	def expand(self,unit):
		if unit in (textInfos.UNIT_CHARACTER,textInfos.UNIT_WORD) and self._atEndOfStory:
			return
		self._atEndOfStory=False
		return super(UIAMSHTMLTextInfo,self).expand(unit)

	def move(self,unit,direction,endPoint=None):
		if direction==0:
			return 0
		if self._atEndOfStory and direction<0:
			direction+=1
		self._atEndOfStory=False
		if direction==0:
			return -1
		return super(UIAMSHTMLTextInfo,self).move(unit,direction,endPoint=endPoint)

class HTMLAttribCache(object):

	def __init__(self,HTMLNode):
		self.HTMLNode=HTMLNode
		self.cache={}
		self.containsCache={}

	def __getitem__(self,item):
		try:
			return self.cache[item]
		except LookupError:
			pass
		try:
			value=self.HTMLNode.getAttribute(item)
		except (COMError,NameError):
			value=None
		self.cache[item]=value
		return value

	def __contains__(self,item):
		try:
			return self.containsCache[item]
		except LookupError:
			pass
		contains=item in self.cache
		if not contains:
			try:
				contains=self.HTMLNode.hasAttribute(item)
			except (COMError,NameError):
				pass
		self.containsCache[item]=contains
		return contains


nodeNamesToNVDARoles: Dict[str, int] = {
	"FRAME":controlTypes.Role.FRAME,
	"IFRAME":controlTypes.Role.INTERNALFRAME,
	"FRAMESET":controlTypes.Role.DOCUMENT,
	"BODY":controlTypes.Role.DOCUMENT,
	"TH":controlTypes.Role.TABLECELL,
	"IMG":controlTypes.Role.GRAPHIC,
	"A":controlTypes.Role.LINK,
	"LABEL":controlTypes.Role.LABEL,
	"#text":controlTypes.Role.STATICTEXT,
	"#TEXT":controlTypes.Role.STATICTEXT,
	"H1":controlTypes.Role.HEADING,
	"H2":controlTypes.Role.HEADING,
	"H3":controlTypes.Role.HEADING,
	"H4":controlTypes.Role.HEADING,
	"H5":controlTypes.Role.HEADING,
	"H6":controlTypes.Role.HEADING,
	"DIV":controlTypes.Role.SECTION,
	"P":controlTypes.Role.PARAGRAPH,
	"FORM":controlTypes.Role.FORM,
	"UL":controlTypes.Role.LIST,
	"OL":controlTypes.Role.LIST,
	"DL":controlTypes.Role.LIST,
	"LI":controlTypes.Role.LISTITEM,
	"DD":controlTypes.Role.LISTITEM,
	"DT":controlTypes.Role.LISTITEM,
	"TR":controlTypes.Role.TABLEROW,
	"THEAD":controlTypes.Role.TABLEHEADER,
	"TBODY":controlTypes.Role.TABLEBODY,
	"HR":controlTypes.Role.SEPARATOR,
	"OBJECT":controlTypes.Role.EMBEDDEDOBJECT,
	"APPLET":controlTypes.Role.EMBEDDEDOBJECT,
	"EMBED":controlTypes.Role.EMBEDDEDOBJECT,
	"FIELDSET": controlTypes.Role.GROUPING,
	"OPTION":controlTypes.Role.LISTITEM,
	"BLOCKQUOTE":controlTypes.Role.BLOCKQUOTE,
	"MATH":controlTypes.Role.MATH,
	"NAV": controlTypes.Role.LANDMARK,
	"HEADER": controlTypes.Role.LANDMARK,
	"MAIN": controlTypes.Role.LANDMARK,
	"ASIDE": controlTypes.Role.LANDMARK,
	"FOOTER": controlTypes.Role.LANDMARK,
	"SECTION": controlTypes.Role.REGION,
	"ARTICLE": controlTypes.Role.ARTICLE,
	"FIGURE": controlTypes.Role.FIGURE,
	"FIGCAPTION": controlTypes.Role.CAPTION,
	"MARK": controlTypes.Role.MARKED_CONTENT,
}


def getZoomFactorsFromHTMLDocument(HTMLDocument):
	try:
		scr=HTMLDocument.parentWindow.screen
	except (COMError,NameError,AttributeError):
		log.debugWarning("no screen object for MSHTML document")
		return (1,1)
	try:
		devX=float(scr.deviceXDPI)
		devY=float(scr.deviceYDPI)
		logX=float(scr.logicalXDPI)
		logY=float(scr.logicalYDPI)
	except (COMError,NameError,AttributeError,TypeError):
		log.debugWarning("unable to fetch DPI factors")
		return (1,1)
	return (devX // logX, devY // logY)

def IAccessibleFromHTMLNode(HTMLNode):
	try:
		s=HTMLNode.QueryInterface(IServiceProvider)
		return s.QueryService(oleacc.IAccessible._iid_,oleacc.IAccessible)
	except COMError:
		raise NotImplementedError

def HTMLNodeFromIAccessible(IAccessibleObject):
	try:
		s=IAccessibleObject.QueryInterface(IServiceProvider)
		i=s.QueryService(IID_IHTMLElement,comtypes.automation.IDispatch)
		if not i:
			# QueryService should fail if IHTMLElement is not supported, but some applications misbehave and return a null COM pointer.
			raise NotImplementedError
		return comtypes.client.dynamic.Dispatch(i)
	except COMError:
		raise NotImplementedError

def locateHTMLElementByID(document,ID):
	try:
		elements=document.getElementsByName(ID)
		if elements is not None:
			element=elements.item(0)
		else: #probably IE 10 in standards mode (#3151)
			try:
				element=document.all.item(ID)
			except:
				element=None
		if element is None: #getElementsByName doesn't return element with specified ID in IE11 (#5784)
			try:
				element=document.getElementByID(ID)
			except COMError as e:
				log.debugWarning("document.getElementByID failed with COMError %s"%e)
				element=None
	except COMError as e:
		log.debugWarning("document.getElementsByName failed with COMError %s"%e)
		element=None
	if element:
		return element
	try:
		nodeName=document.body.nodeName
	except COMError as e:
		log.debugWarning("document.body.nodeName failed with COMError %s"%e)
		return None
	if nodeName:
		nodeName=nodeName.upper()
	if nodeName=="FRAMESET":
		tag="frame"
	else:
		tag="iframe"
	try:
		frames=document.getElementsByTagName(tag)
	except COMError as e:
		log.debugWarning("document.getElementsByTagName failed with COMError %s"%e)
		return None
	if not frames: #frames can be None in IE 10
		return None
	for frame in frames:
		childElement=getChildHTMLNodeFromFrame(frame)
		if not childElement:
			continue
		childElement=locateHTMLElementByID(childElement.document,ID)
		if not childElement: continue
		return childElement

def getChildHTMLNodeFromFrame(frame):
	try:
		pacc=IAccessibleFromHTMLNode(frame)
	except NotImplementedError:
		# #1569: It's not possible to get an IAccessible from frames marked with an ARIA role of presentation.
		# In this case, just skip this frame.
		return
	res=IAccessibleHandler.accChild(pacc,1)
	if not res: return
	return HTMLNodeFromIAccessible(res[0])

class MSHTMLTextInfo(textInfos.TextInfo):

	def _expandToLine(self,textRange):
		#Try to calculate the line range by finding screen coordinates and using moveToPoint
		parent=textRange.parentElement()
		if not parent.isMultiline: #fastest solution for single line edits (<input type="text">)
			textRange.expand("textEdit")
			return
		parentRect=parent.getBoundingClientRect()
		#This can be simplified when comtypes is fixed
		lineTop=comtypes.client.dynamic._Dispatch(textRange._comobj).offsetTop
		lineLeft=parentRect.left+parent.clientLeft
		#editable documents have a different right most boundary to <textarea> elements.
		if self.obj.HTMLNode.document.body.isContentEditable:
			lineRight=parentRect.right 
		else:
			lineRight=parentRect.left+parent.clientWidth
		tempRange=textRange.duplicate()
		try:
			tempRange.moveToPoint(lineLeft,lineTop)
			textRange.setEndPoint("startToStart",tempRange)
			tempRange.moveToPoint(lineRight,lineTop)
			textRange.setEndPoint("endToStart",tempRange)
			return
		except COMError:
			pass
		#MoveToPoint fails on Some (possibly floated) textArea elements.
		#Instead use the physical selection, by moving it with key presses, to work out the line.
		#This approach is somewhat slower, and less accurate.
		with self.obj.suspendCaretEvents():
			selObj=parent.document.selection
			oldSelRange=selObj.createRange().duplicate()
			# #1566: Calling textRange.select() sometimes throws focus onto the document,
			# so create a new range from the selection and move the selection using that.
			selObj.createRange().moveToBookmark(textRange.getBookmark())
			KeyboardInputGesture.fromName("home").send()
			api.processPendingEvents(False)
			newSelStartMark=selObj.createRange().getBookmark()
			KeyboardInputGesture.fromName("end").send()
			api.processPendingEvents(False)
			newSelEndMark=selObj.createRange().getBookmark()
			tempRange.moveToBookmark(newSelStartMark)
			textRange.setEndPoint("startToStart",tempRange)
			tempRange.moveToBookmark(newSelEndMark)
			textRange.setEndPoint("endToStart",tempRange)
			oldSelRange.select()

	def __init__(self,obj,position,_rangeObj=None):
		super(MSHTMLTextInfo,self).__init__(obj,position)
		if _rangeObj:
			self._rangeObj=_rangeObj.duplicate()
			return
		try:
			editableBody=self.obj.HTMLNodeName=="BODY" and self.obj.isContentEditable
		except:
			editableBody=False
		if editableBody:
			self._rangeObj=self.obj.HTMLNode.document.selection.createRange()
		else:
			self._rangeObj=self.obj.HTMLNode.createTextRange()
		if position in (textInfos.POSITION_CARET,textInfos.POSITION_SELECTION):
			try:
				activeElement=self.obj.HTMLNode.document.activeElement
			except COMError:
				activeElement=None
			if not activeElement or self.obj.HTMLNode.uniqueNumber!=activeElement.uniqueNumber:
				raise RuntimeError("Only works with currently selected element")
			if not editableBody:
				mark=self.obj.HTMLNode.document.selection.createRange().GetBookmark()
				self._rangeObj.MoveToBookmark(mark)
			if position==textInfos.POSITION_CARET:
				self._rangeObj.collapse()
			return
		if position==textInfos.POSITION_FIRST:
			self._rangeObj.collapse()
		elif position==textInfos.POSITION_LAST:
			self._rangeObj.expand("textedit")
			self.collapse(True)
			self._rangeObj.move("character",-1)
		elif position==textInfos.POSITION_ALL:
			self._rangeObj.expand("textedit")
		elif isinstance(position,textInfos.Bookmark):
			if position.infoClass==self.__class__:
				self._rangeObj.moveToBookmark(position.data)
			else:
				raise TypeError("Bookmark was for %s type, not for %s type"%(position.infoClass.__name__,self.__class__.__name__))
		else:
			raise NotImplementedError("position: %s" % (position,))

	def expand(self,unit):
		if unit==textInfos.UNIT_PARAGRAPH:
			unit=textInfos.UNIT_LINE
		if unit==textInfos.UNIT_LINE and self.basePosition not in [textInfos.POSITION_SELECTION,textInfos.POSITION_CARET]:
			unit=textInfos.UNIT_SENTENCE
		if unit==textInfos.UNIT_READINGCHUNK:
			unit=textInfos.UNIT_SENTENCE
		if unit==textInfos.UNIT_CHARACTER:
			self._rangeObj.expand("character")
		elif unit==textInfos.UNIT_WORD:
			#Expand to word at the start of a control is broken in MSHTML
			#Unless we expand to character first.
			self._rangeObj.expand("character")
			self._rangeObj.expand("word")
		elif unit==textInfos.UNIT_SENTENCE:
			self._rangeObj.expand("sentence")
		elif unit==textInfos.UNIT_LINE:
			self._expandToLine(self._rangeObj)
		elif unit==textInfos.UNIT_STORY:
			self._rangeObj.expand("textedit")
		else:
			raise NotImplementedError("unit: %s"%unit)

	def _get_isCollapsed(self):
		if self._rangeObj.compareEndPoints("startToEnd",self._rangeObj)==0:
			return True
		else:
			return False

	def collapse(self,end=False):
		self._rangeObj.collapse(not end)

	def copy(self):
		return self.__class__(self.obj,None,_rangeObj=self._rangeObj.duplicate())

	def compareEndPoints(self,other,which):
		return self._rangeObj.compareEndPoints(which,other._rangeObj)

	def setEndPoint(self,other,which):
		self._rangeObj.setEndPoint(which,other._rangeObj)

	def _get_text(self):
		text=self._rangeObj.text
		if not text:
			text=u""
		if controlTypes.State.PROTECTED in self.obj.states:
			text=u'*'*len(text)
		return text

	def move(self,unit,direction, endPoint=None):
		if unit in [textInfos.UNIT_READINGCHUNK,textInfos.UNIT_LINE]:
			unit=textInfos.UNIT_SENTENCE
		if unit==textInfos.UNIT_STORY:
			unit="textedit"
		if endPoint=="start":
			moveFunc=self._rangeObj.moveStart
		elif endPoint=="end":
			moveFunc=self._rangeObj.moveEnd
		else:
			moveFunc=self._rangeObj.move
			if direction<0:
				# #1605: If at the end of a line, moving back seems to land on a blank unit,
				# which breaks backspacing.
				# Expanding first seems to fix this.
				self._rangeObj.expand("character")
		res=moveFunc(unit,direction)
		return res

	def updateCaret(self):
		self._rangeObj.select()

	def updateSelection(self):
		self._rangeObj.select()

	def _get_bookmark(self):
		return textInfos.Bookmark(self.__class__,self._rangeObj.getBookmark())

class MSHTML(IAccessible):

	def _get__UIAControl(self):
		if UIAHandler.handler and self.role==controlTypes.Role.EDITABLETEXT and controlTypes.State.FOCUSED in self.states:
			e=UIAHandler.handler.clientObject.getFocusedElementBuildCache(UIAHandler.handler.baseCacheRequest)
			obj=UIA(UIAElement=e)
			if isinstance(obj,EditableTextWithoutAutoSelectDetection):
				obj.parent=self.parent
				obj.TextInfo=UIAMSHTMLTextInfo
				self._UIAControl=obj
				return obj

	def makeTextInfo(self,position):
		if self._UIAControl:
			return self._UIAControl.makeTextInfo(position)
		return super(MSHTML,self).makeTextInfo(position)

	HTMLNodeNameNavSkipList=['#comment','SCRIPT','HEAD','HTML','PARAM','STYLE']
	HTMLNodeNameEmbedList=['OBJECT','EMBED','APPLET','FRAME','IFRAME']

	_ignoreCaretEvents=False #:Set to true when moving the caret to calculate lines, event_caret will be disabled.

	@contextlib.contextmanager
	def suspendCaretEvents(self):
		"""Suspends caret events while you need to move the caret to calculate things."""
		oldVal=self._ignoreCaretEvents
		self._ignoreCaretEvents=True
		yield oldVal
		self._ignoreCaretEvents=oldVal

	def event_caret(self):
		if self._ignoreCaretEvents: return
		if self.TextInfo is not MSHTMLTextInfo and not self._UIAControl:
			return
		try:
			newCaretBookmark=self.makeTextInfo(textInfos.POSITION_CARET).bookmark
		except RuntimeError: #caret events can be fired on the object (focus) when  its not the real MSHTML selection 
			newCaretBookmark=None
		if not newCaretBookmark or newCaretBookmark==getattr(self,'_oldCaretBookmark',None):
			return
		self._oldCaretBookmark=newCaretBookmark
		return super(MSHTML,self).event_caret()

	@classmethod
	def kwargsFromSuper(cls,kwargs,relation=None):
		IAccessibleObject=kwargs['IAccessibleObject']
		#MSHTML should not be used for MSAA child elements.
		#However, objectFromPoint can hit an MSAA child element but we still should try MSHTML's own elementFromPoint even in this case.
		if kwargs.get('IAccessibleChildID') and not isinstance(relation,tuple):
			return False
		HTMLNode=None
		try:
			HTMLNode=HTMLNodeFromIAccessible(IAccessibleObject)
		except NotImplementedError:
			pass
		if not HTMLNode:
			return False

		if relation=="focus":
			# #4045: we must recurse into frames ourselves when fetching the active element of a document. 
			while True:
				try:
					HTMLNode=HTMLNode.document.activeElement
				except:
					log.exception("Error getting activeElement")
					break
				nodeName=HTMLNode.nodeName or ""
				if nodeName.lower() not in ("frame","iframe"):
					# The IAccessibleObject may be incorrect now, so let the constructor recalculate it.
					del kwargs['IAccessibleObject']
					break
				childElement=getChildHTMLNodeFromFrame(HTMLNode)
				if not childElement:
					break
				HTMLNode=childElement
			
		elif isinstance(relation,tuple):
			windowHandle=kwargs.get('windowHandle')
			p=ctypes.wintypes.POINT(x=relation[0],y=relation[1])
			ctypes.windll.user32.ScreenToClient(windowHandle,ctypes.byref(p))
			# #3494: MSHTML's internal coordinates are always at a hardcoded DPI (usually 96) no matter the system DPI or zoom level.
			xFactor,yFactor=getZoomFactorsFromHTMLDocument(HTMLNode.document)
			try:
				HTMLNode=HTMLNode.document.elementFromPoint(p.x // xFactor, p.y // yFactor)
			except:
				HTMLNode=None
			if not HTMLNode:
				log.debugWarning("Error getting HTMLNode with elementFromPoint")
				return False
			del kwargs['IAccessibleObject']
			del kwargs['IAccessibleChildID']
		kwargs['HTMLNode']=HTMLNode
		return True

	def findOverlayClasses(self,clsList):
		if self.TextInfo == MSHTMLTextInfo or self._UIAControl:
			clsList.append(EditableTextWithoutAutoSelectDetection)
		nodeName = self.HTMLNodeName
		if nodeName:
			if nodeName=="SELECT" and self.windowStyle&winUser.WS_POPUP:
				clsList.append(PopupList)
			elif nodeNamesToNVDARoles.get(nodeName) == controlTypes.Role.DOCUMENT:
				try:
					isBodyNode=self.HTMLNodeUniqueNumber==self.HTMLNode.document.body.uniqueNumber
				except (COMError,NameError):
					isBodyNode=False
				if isBodyNode:
					clsList.append(Body)
			elif nodeName == "OBJECT":
				clsList.append(Object)
			elif nodeName=="FIELDSET":
				clsList.append(Fieldset)
			elif nodeName=="MATH":
				clsList.append(Math)
		clsList.append(MSHTML)
		if not self.HTMLNodeHasAncestorIAccessible:
			# The IAccessibleObject is for this node (not an ancestor), so IAccessible overlay classes are relevant.
			super(MSHTML,self).findOverlayClasses(clsList)
			if self.IAccessibleRole == oleacc.ROLE_SYSTEM_DIALOG:
				ariaRoles = (self.HTMLAttributes["role"] or "").split(" ")
				if "dialog" in ariaRoles:
					# #2390: Don't try to calculate text for ARIA dialogs.
					try:
						clsList.remove(Dialog)
					except ValueError:
						pass

	def _get_treeInterceptorClass(self):
		if self.role in (controlTypes.Role.DOCUMENT, controlTypes.Role.APPLICATION, controlTypes.Role.DIALOG) and not self.isContentEditable:
			import virtualBuffers.MSHTML
			return virtualBuffers.MSHTML.MSHTML
		return super(MSHTML,self).treeInterceptorClass

	def _get_isCurrent(self) -> controlTypes.IsCurrent:
		try:
			isCurrent = self.HTMLAttributes["aria-current"]
		except LookupError:
			return controlTypes.IsCurrent.NO

		# key may be in HTMLAttributes with a value of None
		if isCurrent is None:
			return controlTypes.IsCurrent.NO

		try:
			return controlTypes.IsCurrent(isCurrent)
		except ValueError:
			log.debugWarning(f"Unknown aria-current value: {isCurrent}")
			return controlTypes.IsCurrent.NO

	#: Typing for autoproperty _get_HTMLAttributes
	HTMLAttributes: HTMLAttribCache

	def _get_HTMLAttributes(self):
		return HTMLAttribCache(self.HTMLNode)

	def _get_placeholder(self):
		return self.HTMLAttributes["aria-placeholder"]

	def __init__(self,HTMLNode=None,IAccessibleObject=None,IAccessibleChildID=None,**kwargs):
		self.HTMLNodeHasAncestorIAccessible=False
		if not IAccessibleObject:
			# Find an IAccessible for HTMLNode and determine whether it is for an ancestor.
			tempNode=HTMLNode
			while tempNode:
				try:
					IAccessibleObject=IAccessibleFromHTMLNode(tempNode)
				except NotImplementedError:
					IAccessibleObject=None
				if IAccessibleObject:
					IAccessibleChildID=0
					if tempNode is not HTMLNode:
						self.HTMLNodeHasAncestorIAccessible=True
					break
				try:
					tempNode=tempNode.parentNode
				except COMError:
					tempNode=None

		if not IAccessibleObject:
			raise InvalidNVDAObject("Couldn't get IAccessible, probably dead object")

		super(MSHTML,self).__init__(IAccessibleObject=IAccessibleObject,IAccessibleChildID=IAccessibleChildID,**kwargs)
		self.HTMLNode=HTMLNode

		#object and embed nodes give back an incorrect IAccessible via queryService, so we must treet it as an ancestor IAccessible
		if self.HTMLNodeName in ("OBJECT","EMBED"):
			self.HTMLNodeHasAncestorIAccessible=True

	def _get_zoomFactors(self):
		return getZoomFactorsFromHTMLDocument(self.HTMLNode.document)

	def _get_location(self):
		if self.HTMLNodeName and not self.HTMLNodeName.startswith('#'):
			try:
				r=self.HTMLNode.getBoundingClientRect()
			except COMError:
				return None
			# #3494: MSHTML's internal coordinates are always at a hardcoded DPI (usually 96) no matter the system DPI or zoom level.
			xFactor,yFactor=self.zoomFactors
			left=int(r.left*xFactor)
			top=int(r.top*yFactor)
			right=int(r.right*xFactor)
			bottom=int(r.bottom*yFactor)
			return RectLTRB(left,top,right,bottom).toScreen(self.windowHandle).toLTWH()
		return None

	def _get_TextInfo(self):
		if not hasattr(self,'_HTMLNodeSupportsTextRanges'):
			try:
				self.HTMLNode.createTextRange()
				self._HTMLNodeSupportsTextRanges=True
			except (COMError,NameError):
				self._HTMLNodeSupportsTextRanges=False
		if self._HTMLNodeSupportsTextRanges:
			return MSHTMLTextInfo
		return super(MSHTML,self).TextInfo

	def isDuplicateIAccessibleEvent(self,obj):
		if not super(MSHTML,self).isDuplicateIAccessibleEvent(obj):
			return False
		#MSHTML winEvents can't be trusted for uniqueness, so just do normal object comparison.
		return self==obj


	def _isEqual(self, other):
		if self.HTMLNode and other.HTMLNode:
			try:
				return self.windowHandle == other.windowHandle and self.HTMLNodeUniqueNumber == other.HTMLNodeUniqueNumber
			except (COMError,NameError):
				pass
		return super(MSHTML, self)._isEqual(other)

	def _get_presentationType(self):
		presType=super(MSHTML,self).presentationType
		if presType==self.presType_content and self.HTMLAttributes['role']=="presentation":
			presType=self.presType_layout
		if presType==self.presType_content and self.role in (controlTypes.Role.TABLECELL,controlTypes.Role.TABLEROW,controlTypes.Role.TABLE,controlTypes.Role.TABLEBODY):
			ti=self.treeInterceptor
			try:
				if ti and ti.isReady and ti.isNVDAObjectPartOfLayoutTable(self):
					presType=self.presType_layout
			except LookupError:
				pass
		return presType


	def _get_shouldAllowIAccessibleFocusEvent(self):
		ariaRole=self.HTMLAttributes['aria-role']
		if ariaRole=="gridcell":
			return True
		return super(MSHTML,self).shouldAllowIAccessibleFocusEvent

	def _get_name(self):
		ariaLabelledBy=self.HTMLAttributes['aria-labelledBy']
		if ariaLabelledBy:
			try:
				labelNode=self.HTMLNode.document.getElementById(ariaLabelledBy)
			except (COMError,NameError):
				labelNode=None
			if labelNode:
				try:
					return labelNode.innerText
				except (COMError,NameError):
					pass
		ariaLabel=self.HTMLAttributes['aria-label']
		if ariaLabel:
			return ariaLabel
		if self.IAccessibleRole==oleacc.ROLE_SYSTEM_TABLE:
			summary=self.HTMLAttributes['summary']
			if summary:
				return summary
		if (
			self.HTMLNodeHasAncestorIAccessible or
			#IE inappropriately generates the name from descendants on some controls
			self.IAccessibleRole in (oleacc.ROLE_SYSTEM_MENUBAR,oleacc.ROLE_SYSTEM_TOOLBAR,oleacc.ROLE_SYSTEM_LIST,oleacc.ROLE_SYSTEM_TABLE,oleacc.ROLE_SYSTEM_DOCUMENT,oleacc.ROLE_SYSTEM_DIALOG) or
			#Adding an ARIA landmark or unknown role to a DIV or NAV node makes an IAccessible with role_system_grouping and a name calculated from descendants.
			# This name should also be ignored, but check NVDA's role, not accRole as its possible that NVDA chose a better role
			# E.g. row (#2780)
			(self.HTMLNodeName in ("DIV","NAV") and self.role==controlTypes.Role.GROUPING)
		):
			title=self.HTMLAttributes['title']
			# #2121: MSHTML sometimes returns a node for the title attribute.
			# This doesn't make any sense, so ignore it.
			if title and isinstance(title,str):
				return title
			return ""
		return super(MSHTML,self).name

	def _get_landmark(self):
		if self.HTMLNode:
			ariaRoles = []
			ariaRolesString = self.HTMLAttributes['role']
			if ariaRolesString:
				ariaRoles.append(ariaRolesString.split(" ")[0])
			lRole = aria.htmlNodeNameToAriaRoles.get(self.HTMLNodeName.lower())
			if lRole:
				ariaRoles.append(lRole)
			if ariaRoles and ariaRoles[0] in aria.landmarkRoles:
				return ariaRoles[0]
		return super().landmark

	def _get_value(self):
		if self.HTMLNodeHasAncestorIAccessible:
			try:
				value=self.HTMLNode.data
			except (COMError,NameError):
				value=""
			return value
		IARole=self.IAccessibleRole
		# value is not useful on certain nodes that just expose a URL, or they  have other ways of getting their content (#4976 - editble combos).
		if IARole in (oleacc.ROLE_SYSTEM_PANE,oleacc.ROLE_SYSTEM_TEXT) or (IARole==oleacc.ROLE_SYSTEM_COMBOBOX and controlTypes.State.EDITABLE in self.states):
			return ""
		else:
			return super(MSHTML,self).value

	def _get_description(self):
		ariaDescribedBy=self.HTMLAttributes['aria-describedBy']
		if ariaDescribedBy:
			try:
				descNode=self.HTMLNode.document.getElementById(ariaDescribedBy)
			except (COMError,NameError):
				descNode=None
			if descNode:
				try:
					return descNode.innerText
				except (COMError,NameError):
					pass
		if self.HTMLNodeHasAncestorIAccessible:
			return ""
		return super(MSHTML,self).description

	def _get_basicText(self):
		if self.HTMLNode and not self.HTMLNodeName=="SELECT":
			try:
				return self.HTMLNode.data or ""
			except (COMError, AttributeError, NameError):
				pass
			try:
				return self.HTMLNode.innerText or super(MSHTML,self).basicText
			except (COMError, AttributeError, NameError):
				pass
		return super(MSHTML,self).basicText

	def _get_role(self):
		if self.HTMLNode:
			ariaRole = (self.HTMLAttributes["role"] or "").split(" ")[0]
			if ariaRole:
				role=aria.ariaRolesToNVDARoles.get(ariaRole)
				if role:
					return role
			nodeName=self.HTMLNodeName
			if nodeName:
				if nodeName in ("OBJECT","EMBED","APPLET"):
					return controlTypes.Role.EMBEDDEDOBJECT
				if self.HTMLNodeHasAncestorIAccessible or nodeName in (
					"BODY",
					"FRAMESET",
					"FRAME",
					"IFRAME",
					"LABEL",
					"NAV",
					"SECTION",
					"ARTICLE",
					"FIELDSET",
				):
					return nodeNamesToNVDARoles.get(nodeName,controlTypes.Role.SECTION)
		if self.IAccessibleChildID>0:
			states=super(MSHTML,self).states
			if controlTypes.State.LINKED in states:
				return controlTypes.Role.LINK
		role=super(MSHTML,self).role
		#IE uses a MSAA role of ROLE_SYSTEM_TEXT with no readonly state for unsupported or future tags with an explicit ARIA role.
		#If this is the case, force the role to staticText so this is not confused as a real edit field.
		if role==controlTypes.Role.EDITABLETEXT and ariaRole and ariaRole!="textbox":
			role=controlTypes.Role.STATICTEXT
		return role

	def _get_states(self):
		if not self.HTMLNodeHasAncestorIAccessible:
			states=super(MSHTML,self).states
		else:
			states=set()
		ariaSort=self.HTMLAttributes['aria-sort']
		state=aria.ariaSortValuesToNVDAStates.get(ariaSort)
		if state is not None:
			states.add(state)
		htmlRequired='required' in self.HTMLAttributes
		ariaRequired=self.HTMLAttributes['aria-required']
		if htmlRequired or ariaRequired=="true":
			states.add(controlTypes.State.REQUIRED)
		ariaSelected=self.HTMLAttributes['aria-selected']
		if ariaSelected=="true":
			states.add(controlTypes.State.SELECTED)
		elif ariaSelected=="false":
			states.discard(controlTypes.State.SELECTED)
		ariaExpanded=self.HTMLAttributes['aria-expanded']
		if ariaExpanded=="true":
			states.add(controlTypes.State.EXPANDED)
		elif ariaExpanded=="false":
			states.add(controlTypes.State.COLLAPSED)
		ariaInvalid=self.HTMLAttributes['aria-invalid']
		if ariaInvalid=="true":
			states.add(controlTypes.State.INVALID_ENTRY)
		ariaGrabbed=self.HTMLAttributes['aria-grabbed']
		if ariaGrabbed=="true":
			states.add(controlTypes.State.DRAGGING)
		elif ariaGrabbed=="false":
			states.add(controlTypes.State.DRAGGABLE)
		ariaDropeffect=self.HTMLAttributes['aria-dropeffect']
		if ariaDropeffect and ariaDropeffect!="none":
			states.add(controlTypes.State.DROPTARGET)
		if self.HTMLAttributes["aria-hidden"]=="true":
			states.add(controlTypes.State.INVISIBLE)
		if self.isContentEditable:
			states.add(controlTypes.State.EDITABLE)
			states.discard(controlTypes.State.READONLY)
		nodeName=self.HTMLNodeName
		if nodeName=="TEXTAREA":
			states.add(controlTypes.State.MULTILINE)
		# #4667: Internet Explorer 11 correctly fires focus events for aria-activeDescendant, but fails to set the focused state.
		# Therefore check aria-activeDescendant manually and set these states if this is the active descendant. 
		try:
			activeElement=self.HTMLNode.document.activeElement
		except COMError:
			activeElement=None
		if activeElement:
			activeID=activeElement.getAttribute('aria-activedescendant')
			if activeID and activeID==self.HTMLNode.ID:
				states.add(controlTypes.State.FOCUSABLE)
				states.add(controlTypes.State.FOCUSED)
		return states

	def _get_isContentEditable(self):
		try:
			return bool(self.HTMLNode.isContentEditable)
		except:
			return False

	def _get_parent(self):
		if self.HTMLNode:
			try:
				parentNode=self.HTMLNode.parentElement
			except (COMError,NameError):
				parentNode=None
			if not parentNode and self.HTMLNodeHasAncestorIAccessible:
				try:
					parentNode=self.HTMLNode.parentNode
				except (COMError,NameError):
					parentNode=None
			if parentNode:
				obj=MSHTML(HTMLNode=parentNode)
				if obj and obj.HTMLNodeName not in self.HTMLNodeNameNavSkipList:
					return obj
		return super(MSHTML,self).parent

	def _get_previous(self):
		if self.HTMLNode:
			try:
				previousNode=self.HTMLNode.previousSibling
			except COMError:
				previousNode=None
			if not previousNode:
				return None
			obj=MSHTML(HTMLNode=previousNode)
			if obj and obj.HTMLNodeName in self.HTMLNodeNameNavSkipList:
				obj=obj.previous
			return obj
		return super(MSHTML,self).previous

	def _get_next(self):
		if self.HTMLNode:
			try:
				nextNode=self.HTMLNode.nextSibling
			except COMError:
				nextNode=None
			if not nextNode:
				return None
			obj=MSHTML(HTMLNode=nextNode)
			if obj and obj.HTMLNodeName in self.HTMLNodeNameNavSkipList:
				obj=obj.next
			return obj
		return super(MSHTML,self).next

	def _get_firstChild(self):
		if self.HTMLNode:
			if self.HTMLNodeName in ("FRAME","IFRAME"):
				return super(MSHTML,self).firstChild
			try:
				childNode=self.HTMLNode.firstChild
			except COMError:
				childNode=None
			if not childNode:
				return None
			obj=MSHTML(HTMLNode=childNode)
			if obj and obj.HTMLNodeName in self.HTMLNodeNameNavSkipList:
				return obj.next
			return obj
		if self.HTMLNodeHasAncestorIAccessible:
			return None
		return super(MSHTML,self).firstChild

	def _get_lastChild(self):
		if self.HTMLNode:
			if self.HTMLNodeName in ("FRAME","IFRAME"):
				return super(MSHTML,self).lastChild
			try:
				childNode=self.HTMLNode.lastChild
			except COMError:
				childNode=None
			if not childNode:
				return None
			obj=MSHTML(HTMLNode=childNode)
			if obj and obj.HTMLNodeName in self.HTMLNodeNameNavSkipList:
				return obj.previous
			return obj
		if self.HTMLNodeHasAncestorIAccessible:
			return None
		return super(MSHTML,self).lastChild

	def _get_columnNumber(self):
		if not self.role==controlTypes.Role.TABLECELL or not self.HTMLNode:
			raise NotImplementedError
		try:
			return self.HTMLNode.cellIndex+1
		except:
			raise NotImplementedError

	def _get_rowNumber(self):
		if not self.role==controlTypes.Role.TABLECELL or not self.HTMLNode:
			raise NotImplementedError
		HTMLNode=self.HTMLNode
		while HTMLNode:
			try:
				return HTMLNode.rowIndex+1
			except:
				pass
			HTMLNode=HTMLNode.parentNode
		raise NotImplementedError

	def _get_rowCount(self):
		if self.role!=controlTypes.Role.TABLE or not self.HTMLNode:
			raise NotImplementedError
		try:
			return len([x for x in self.HTMLNode.rows])
		except:
			raise NotImplementedError

	def scrollIntoView(self):
		if not self.HTMLNode:
			return
		try:
			self.HTMLNode.scrollInToView()
		except (COMError,NameError):
			pass

	def doAction(self, index=None):
		if self.HTMLNode:
			try:
				self.HTMLNode.click()
				return
			except COMError:
				return
			except NameError:
				pass
		super(MSHTML,self).doAction(index=index)

	def _get_isFocusable(self):
		nodeName = self.HTMLNodeName
		attribs = self.HTMLAttributes
		if nodeName in ("BUTTON", "INPUT", "ISINDEX", "SELECT", "TEXTAREA"):
			return not attribs["disabled"]
		if nodeName == "A":
			return bool(attribs["href"])
		if nodeName in ( "BODY", "OBJECT", "APPLET"):
			return True
		if nodeName=="IMG" and not self.HTMLNodeHasAncestorIAccessible and self.IAccessibleRole==oleacc.ROLE_SYSTEM_GRAPHIC and self.IAccessibleStates&oleacc.STATE_SYSTEM_FOCUSABLE:
			return True
		return self.HTMLNode.hasAttribute("tabindex")

	def setFocus(self):
		if self.HTMLNodeHasAncestorIAccessible:
			try:
				self.HTMLNode.focus()
			except (COMError, AttributeError, NameError):
				pass
			return
		super(MSHTML,self).setFocus()

	def _get_table(self):
		if self.role not in (controlTypes.Role.TABLECELL,controlTypes.Role.TABLEROW) or not self.HTMLNode:
			return None
		HTMLNode=self.HTMLNode
		while HTMLNode:
			nodeName=HTMLNode.nodeName
			if nodeName:
				nodeName=nodeName.upper()
			if nodeName=="TABLE": return MSHTML(HTMLNode=HTMLNode)
			HTMLNode=HTMLNode.parentNode
		return None

	def _get_HTMLNodeUniqueNumber(self):
		if not hasattr(self,'_HTMLNodeUniqueNumber'):
			try:
				self._HTMLNodeUniqueNumber=self.HTMLNode.uniqueNumber
			except COMError:
				return None
		return self._HTMLNodeUniqueNumber

	def _get_HTMLNodeName(self):
		if not hasattr(self,'_HTMLNodeName'):
			try:
				self._HTMLNodeName=self.HTMLNode.nodeName
			except (COMError,NameError):
				return ""
			if self._HTMLNodeName:
				self._HTMLNodeName=self._HTMLNodeName.upper()
		return self._HTMLNodeName

	def _get_devInfo(self):
		info = super(MSHTML, self).devInfo
		info.append("MSHTML node has ancestor IAccessible: %r" % self.HTMLNodeHasAncestorIAccessible)
		htmlNode = self.HTMLNode
		try:
			ret = repr(htmlNode.nodeName)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("MSHTML nodeName: %s" % ret)
		return info

	def _get_language(self):
		ti = self.treeInterceptor
		if not ti:
			# This is too slow to calculate without a buffer.
			# This case should be pretty rare anyway.
			return None
		try:
			return ti.getControlFieldForNVDAObject(self)["language"]
		except LookupError:
			return None

	def _get_liveRegionPoliteness(self) -> aria.AriaLivePoliteness:
		politeness = self.HTMLAttributes["aria-live"] or "off"
		try:
			return aria.AriaLivePoliteness(politeness.lower())
		except ValueError:
			log.error(f"Unknown live politeness of {politeness}", exc_info=True)
			super().liveRegionPoliteness

	def event_liveRegionChange(self):
		# MSHTML live regions are currently handled with custom code in-process
		pass

	def _get_roleText(self):
		roleText = self.HTMLAttributes['aria-roledescription']
		if roleText:
			return roleText
		return super().roleText


class V6ComboBox(IAccessible):
	"""The object which receives value change events for combo boxes in MSHTML/IE 6.
	"""

	def event_valueChange(self):
		focus = api.getFocusObject()
		if controlTypes.State.FOCUSED not in self.states or focus.role != controlTypes.Role.COMBOBOX:
			# This combo box is not focused.
			return super(V6ComboBox, self).event_valueChange()
		# This combo box is focused. However, the value change is not fired on the real focus object.
		# Therefore, redirect this event to the real focus object.
		focus.event_valueChange()

class Fieldset(MSHTML):

	def _get_name(self):
		try:
			child=self.HTMLNode.children[0]
		except (COMError,NameError):
			child=None
		if not child:
			return super(Fieldset,self).name
		try:
			nodeName=child.nodeName
		except (COMError,NameError):
			return super(Fieldset,self).name
		if nodeName:
			nodeName=nodeName.upper()
		if nodeName!="LEGEND":
			return super(Fieldset,self).name
		try:
			text=child.innerText
		except (COMError,NameError):
			return super(Fieldset,self).name
		return text

class Body(MSHTML):

	def _get_parent(self):
		# The parent of the body accessible may be an irrelevant client object (description: MSAAHTML Registered Handler).
		# This object isn't returned when requesting OBJID_CLIENT, nor is it returned as a child of its parent.
		# Therefore, eliminate it from the ancestry completely.
		# However it is possible that this body is a child document of a parent frame. In this case don't skip it.
		parent = super(Body, self).parent
		if parent and not isinstance(parent,MSHTML):
			return parent.parent
		else:
			return parent

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# We must override this because we override parent to skip the MSAAHTML Registered Handler client,
		# which might have the focused state.
		if controlTypes.State.FOCUSED in self.states:
			return True
		parent = super(Body, self).parent
		if not parent:
			return False
		return parent.shouldAllowIAccessibleFocusEvent

class Object(MSHTML):

	def _get_firstChild(self):
		# We want firstChild to return the accessible for the embedded object.
		from objidl import IOleWindow
		# Try to get the window for the embedded object.
		try:
			window = self.HTMLNode.object.QueryInterface(IOleWindow).GetWindow()
		except COMError:
			window = None
		if not window or window == self.windowHandle:
			return super(Object, self).firstChild
		return Window(windowHandle=window)

class PluginWindow(IAccessible):
	"""A window for a plugin.
	"""

	# MSHTML fires focus on this window after the plugin may already have fired a focus event.
	# We don't want this to override the focus event fired by the plugin.
	shouldAllowIAccessibleFocusEvent = False

class PopupList(MSHTML):
	"""
	Temporary popup lists created when expanding a combo box have a correct accParent which points back to the combobox, so use that. The parentElement  points to a temporary document fragment which is not useful.
	"""

	def _get_parent(self):
		return super(MSHTML,self).parent

class RootClient(IAccessible):
	"""The top level client of an MSHTML control.
	"""

	# Get rid of the URL.
	name = None
	# Get rid of "MSAAHTML Registered Handler".
	description = None

class MSAATextLeaf(IAccessible):
	role=controlTypes.Role.STATICTEXT

class Math(MSHTML):
	role = controlTypes.Role.MATH

	def _get_mathMl(self):
		import mathPres
		mathMl = mathPres.stripExtraneousXml(self.HTMLNode.outerHTML)
		if not mathPres.getLanguageFromMath(mathMl) and self.language:
			mathMl = mathPres.insertLanguageIntoMath(mathMl, self.language)
		return mathMl

def findExtraIAccessibleOverlayClasses(obj, clsList):
	"""Determine the most appropriate class for MSHTML objects.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	windowClass = obj.windowClassName
	iaRole = obj.IAccessibleRole
	if windowClass == "Internet Explorer_TridentCmboBx" and iaRole == oleacc.ROLE_SYSTEM_COMBOBOX:
		clsList.append(V6ComboBox)
		return

	if windowClass != "Internet Explorer_Server":
		return

	if obj.IAccessibleChildID>0 and iaRole==oleacc.ROLE_SYSTEM_TEXT:
		clsList.append(MSAATextLeaf)
		return

	if iaRole == oleacc.ROLE_SYSTEM_WINDOW and obj.event_objectID is not None and obj.event_objectID > 0:
		clsList.append(PluginWindow)
	elif iaRole == oleacc.ROLE_SYSTEM_CLIENT and obj.event_objectID == winUser.OBJID_CLIENT:
		clsList.append(RootClient)
