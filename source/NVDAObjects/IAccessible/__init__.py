#NVDAObjects/IAccessible.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import weakref
import re
from comtypes import COMError
import struct
import os
import tones
import textHandler
import time
import difflib
import ctypes
import comtypes.automation
import comtypes.client
import appModuleHandler
from keyUtils import sendKey, key 
import IAccessibleHandler
import JABHandler
import winUser
import winKernel
import globalVars
from logHandler import log
import speech
import api
import config
import controlTypes
from NVDAObjects.window import Window
from NVDAObjects import NVDAObject, NVDAObjectTextInfo, AutoSelectDetectionNVDAObject
import NVDAObjects.JAB
import eventHandler
import mouseHandler
import queueHandler

re_gecko_level=re.compile('.*?L([0-9]+).*')
re_gecko_position=re.compile('.*?([0-9]+) of ([0-9]+).*')
re_gecko_contains=re.compile('.*?with ([0-9]+).*')

def getNVDAObjectFromEvent(hwnd,objectID,childID):
	accHandle=IAccessibleHandler.accessibleObjectFromEvent(hwnd,objectID,childID)
	if not accHandle:
		return None
	(pacc,accChildID)=accHandle
	obj=IAccessible(IAccessibleObject=pacc,IAccessibleChildID=accChildID,event_windowHandle=hwnd,event_objectID=objectID,event_childID=childID)
	return obj

def getNVDAObjectFromPoint(x,y):
	accHandle=IAccessibleHandler.accessibleObjectFromPoint(x,y)
	if not accHandle:
		return None
	(pacc,child)=accHandle
	obj=IAccessible(IAccessibleObject=pacc,IAccessibleChildID=child)
	return obj

def processGeckoDescription(obj):
	#Don't do this if the description property is overridden
	if obj.__class__._get_description!=IAccessible._get_description:
		return 
	if not obj.windowClassName.startswith('Mozilla'):
		return
	rawDescription=obj.description
	if not isinstance(rawDescription,basestring):
		return
	if rawDescription.startswith('Description: '):
		obj.description=rawDescription[13:]
	else:
		obj.description=""

class IA2TextTextInfo(NVDAObjectTextInfo):

	def _getOffsetFromPoint(self,x,y):
		return self.obj.IAccessibleTextObject.OffsetAtPoint(x,y,IAccessibleHandler.IA2_COORDTYPE_SCREEN_RELATIVE)

	def _getPointFromOffset(self,offset):
		try:
			res=self.obj.IAccessibleTextObject.characterExtents(offset,IAccessibleHandler.IA2_COORDTYPE_SCREEN_RELATIVE)
		except:
			raise NotImplementedError
		point=textHandler.Point(res[0]+(res[2]/2),res[1]+(res[3]/2))
		return point

	def _getCaretOffset(self):
		offset=self.obj.IAccessibleTextObject.caretOffset
		if offset<0:
			raise RuntimeError("no active caret in this object")
		return offset

	def _setCaretOffset(self,offset):
		self.obj.IAccessibleTextObject.SetCaretOffset(offset)

	def _getSelectionOffsets(self):
		try:
			nSelections=self.obj.IAccessibleTextObject.nSelections
		except:
			nSelections=0
		if nSelections:
			(start,end)=self.obj.IAccessibleTextObject.Selection[0]
		else:
			start=self._getCaretOffset()
			end=start
		return [min(start,end),max(start,end)]

	def _setSelectionOffsets(self,start,end):
		for selIndex in range(self.obj.IAccessibleTextObject.NSelections):
			self.obj.IAccessibleTextObject.RemoveSelection(selIndex)
		self.obj.IAccessibleTextObject.AddSelection(start,end)

	def _getStoryLength(self):
		try:
			return self.obj.IAccessibleTextObject.NCharacters
		except:
			log.debugWarning("IAccessibleText::nCharacters failed",exc_info=True)
			return 0

	def _getLineCount(self):
			return -1

	def _getTextRange(self,start,end):
		try:
			return self.obj.IAccessibleTextObject.text(start,end)
		except:
			return ""

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		try:
			startOffset,endOffset,attribsString=self.obj.IAccessibleTextObject.attributes(offset)
		except COMError:
			log.debugWarning("could not get attributes",exc_info=True)
			return textHandler.FormatField(),(self._startOffset,self._endOffset)
		formatField=textHandler.FormatField()
		if not attribsString and offset>0:
			try:
				attribsString=self.obj.IAccessibleTextObject.attributes(offset-1)[2]
			except COMError:
				pass
		if attribsString:
			formatField.update(IAccessibleHandler.splitIA2Attribs(attribsString))
		try:
			textAlign=formatField.pop("text-align")
		except KeyError:
			textAlign=None
		if textAlign:
			if "right" in textAlign:
				textAlign="right"
			elif "center" in textAlign:
				textAlign="center"
			elif "justify" in textAlign:
				textAlign="justify"
			formatField["text-align"]=textAlign
		try:
			fontWeight=formatField.pop("font-weight")
		except KeyError:
			fontWeight=None
		if fontWeight is not None and (fontWeight.lower()=="bold" or (fontWeight.isdigit() and int(fontWeight)>=700)):
			formatField["bold"]=True
		else:
			formatField["bold"]=False
		try:
			fontStyle=formatField.pop("font-style")
		except KeyError:
			fontStyle=None
		if fontStyle is not None and fontStyle.lower()=="italic":
			formatField["italic"]=True
		else:
			formatField["italic"]=False
		try:
			invalid=formatField.pop("invalid")
		except KeyError:
			invalid=None
		if invalid and invalid.lower()=="spelling":
			formatField["invalid-spelling"]=True
		return formatField,(startOffset,endOffset)

	def _getCharacterOffsets(self,offset):
		try:
			if offset>=self.obj.IAccessibleTextObject.nCharacters:
				return offset,offset+1
		except:
			pass
		try:
			return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_CHAR)[0:2]
		except:
			return super(IA2TextTextInfo,self)._getCharacterOffsets(offset)

	def _getWordOffsets(self,offset):
		try:
			if offset>=self.obj.IAccessibleTextObject.nCharacters:
				return offset,offset+1
		except:
			pass
		try:
			return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_WORD)[0:2]
		except:
			return super(IA2TextTextInfo,self)._getWordOffsets(offset)

	def _getLineOffsets(self,offset):
		try:
			start,end,text=self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_LINE)
			return start,end
		except:
			return super(IA2TextTextInfo,self)._getLineOffsets(offset)

	def _getSentenceOffsets(self,offset):
		try:
			if offset>=self.obj.IAccessibleTextObject.nCharacters:
				return offset,offset+1
		except:
			pass
		try:
			start,end,text=self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_SENTENCE)
			if start==end:
				raise NotImplementedError
			return start,end
		except:
			return super(IA2TextTextInfo,self)._getSentenceOffsets(offset)

	def _getParagraphOffsets(self,offset):
		try:
			if offset>=self.obj.IAccessibleTextObject.nCharacters:
				return offset,offset+1
		except:
			pass
		try:
			start,end,text=self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_PARAGRAPH)
			if start>=end:
				raise RuntimeError("did not expand to paragraph correctly")
			return start,end
		except:
			super(IA2TextTextInfo,self)._getParagraphOffsets(offset)

	def _lineNumFromOffset(self,offset):
		return -1

class IAccessible(Window,AutoSelectDetectionNVDAObject):
	"""
the NVDAObject for IAccessible
@ivar IAccessibleChildID: the IAccessible object's child ID
@type IAccessibleChildID: int
"""

	def __new__(cls,windowHandle=None,IAccessibleObject=None,IAccessibleChildID=None,event_windowHandle=None,event_objectID=None,event_childID=None):
		"""
Checks the window class and IAccessible role against a map of IAccessible sub-types, and if a match is found, returns that rather than just IAccessible.
"""  
		if windowHandle and not IAccessibleObject:
			(IAccessibleObject,IAccessibleChildID)=IAccessibleHandler.accessibleObjectFromEvent(windowHandle,-4,0)
		elif not windowHandle and not IAccessibleObject:
			raise ArgumentError("Give either a windowHandle, or windowHandle, childID, objectID, or IAccessibleObject")
		if not windowHandle and isinstance(IAccessibleObject,IAccessibleHandler.IAccessible2):
			try:
				windowHandle=IAccessibleObject.windowHandle
			except:
				log.debugWarning("IAccessible2::windowHandle failed",exc_info=True)
			#Mozilla Gecko: we can never use a MozillaWindowClass window
			while windowHandle and winUser.getClassName(windowHandle)=="MozillaWindowClass":
				windowHandle=winUser.getAncestor(windowHandle,winUser.GA_PARENT)
		if not windowHandle:
			windowHandle=IAccessibleHandler.windowFromAccessibleObject(IAccessibleObject)
		if not windowHandle and event_windowHandle:
			windowHandle=event_windowHandle
		elif not windowHandle:
			return None #We really do need a window handle
		windowClassName=winUser.getClassName(windowHandle)
		try:
			IAccessibleRole=0
			if isinstance(IAccessibleObject,IAccessibleHandler.IAccessible2):
				IAccessibleRole=IAccessibleObject.role()
			if IAccessibleRole==0:
				IAccessibleRole=IAccessibleObject.accRole(IAccessibleChildID)
		except:
			IAccessibleRole=0
		classString=None
		if _staticMap.has_key((windowClassName,IAccessibleRole)):
			classString=_staticMap[(windowClassName,IAccessibleRole)]
		elif _staticMap.has_key((windowClassName,None)):
			classString=_staticMap[(windowClassName,None)]
		elif _staticMap.has_key((None,IAccessibleRole)):
			classString=_staticMap[(None,IAccessibleRole)]
		if classString is None:
			classString="IAccessible"
		if classString.find('.')>0:
			modString,classString=os.path.splitext(classString)
			classString=classString[1:]
			mod=__import__(modString,globals(),locals(),[])
			newClass=getattr(mod,classString)
		else:
			newClass=globals()[classString]
		obj=Window.__new__(newClass)
		obj.windowClassName=windowClassName
		obj.__init__(windowHandle=windowHandle,IAccessibleObject=IAccessibleObject,IAccessibleChildID=IAccessibleChildID,event_windowHandle=event_windowHandle,event_objectID=event_objectID,event_childID=event_childID)
		return obj

	def __init__(self,windowHandle=None,IAccessibleObject=None,IAccessibleChildID=None,event_windowHandle=None,event_objectID=None,event_childID=None):
		"""
@param pacc: a pointer to an IAccessible object
@type pacc: ctypes.POINTER(IAccessible)
@param child: A child ID that will be used on all methods of the IAccessible pointer
@type child: int
@param hwnd: the window handle, if known
@type hwnd: int
@param objectID: the objectID for the IAccessible Object, if known
@type objectID: int
"""
		if hasattr(self,"_doneInit"):
			return
		self.IAccessibleObject=IAccessibleObject
		self.IAccessibleChildID=IAccessibleChildID
		Identity=self.IAccessibleIdentity
		if event_windowHandle is None and Identity and 'windowHandle' in Identity:
			event_windowHandle=Identity['windowHandle']
		if event_objectID is None and Identity and 'objectID' in Identity:
			event_objectID=Identity['objectID']
		if event_childID is None and Identity and 'childID' in Identity:
			event_childID=Identity['childID']
		if event_childID is None:
			event_childID=IAccessibleChildID
		if event_windowHandle is None:
			event_windowHandle=windowHandle
		if event_objectID is None and isinstance(IAccessibleObject,IAccessibleHandler.IAccessible2):
			event_objectID=IAccessibleHandler.OBJID_CLIENT
		if event_childID is None and isinstance(IAccessibleObject,IAccessibleHandler.IAccessible2):
			try:
				event_childID=IAccessibleObject.uniqueID
			except:
				log.debugWarning("could not get IAccessible2::uniqueID to use as event_childID",exc_info=True)
		self.event_windowHandle=event_windowHandle
		self.event_objectID=event_objectID
		self.event_childID=event_childID
		Window.__init__(self,windowHandle=windowHandle)
		#Mozilla Gecko objects use the description property to report other info
		processGeckoDescription(self)
		try:
			self.IAccessibleActionObject=IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleAction)
		except:
			pass
		try:
			self.IAccessibleTextObject=IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleText)
			self.TextInfo=IA2TextTextInfo
			replacedTextInfo=True
			if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_TEXT:
				hasEditableState=True
			else:
				try:
					hasEditableState=bool(self.IAccessibleObject.states&IAccessibleHandler.IA2_STATE_EDITABLE)
				except:
					hasEditableState=False
			if  hasEditableState:
				[self.bindKey_runtime(keyName,scriptName) for keyName,scriptName in [
					("ExtendedUp","moveByLine"),
					("ExtendedDown","moveByLine"),
					("control+ExtendedUp","moveByLine"),
					("control+ExtendedDown","moveByLine"),
					("ExtendedLeft","moveByCharacter"),
					("ExtendedRight","moveByCharacter"),
					("Control+ExtendedLeft","moveByWord"),
					("Control+ExtendedRight","moveByWord"),
					("ExtendedHome","moveByCharacter"),
					("ExtendedEnd","moveByCharacter"),
					("control+extendedHome","moveByLine"),
					("control+extendedEnd","moveByLine"),
					("ExtendedDelete","delete"),
					("Back","backspace"),
				]]
		except:
			pass
		self._lastMouseTextOffsets=None
		if None not in (event_windowHandle,event_objectID,event_childID):
			IAccessibleHandler.liveNVDAObjectTable[(event_windowHandle,event_objectID,event_childID)]=self
		self._doneInit=True

	def _isEqual(self,other):
		if self.IAccessibleChildID!=other.IAccessibleChildID:
			return False
		if self.IAccessibleObject==other.IAccessibleObject: 
			return True
		try:
			if isinstance(self.IAccessibleObject,IAccessibleHandler.IAccessible2) and isinstance(other.IAccessibleObject,IAccessibleHandler.IAccessible2):
				# These are both IAccessible2 objects, so we can test unique ID.
				# Unique ID is only guaranteed to be unique within a given window, so we must check window handle as well.
				selfIA2Window=self.IAccessibleObject.windowHandle
				selfIA2ID=self.IAccessibleObject.uniqueID
				otherIA2Window=other.IAccessibleObject.windowHandle
				otherIA2ID=other.IAccessibleObject.uniqueID
				if selfIA2Window!=otherIA2Window:
					# The window handles are different, so these are definitely different windows.
					return False
				# At this point, we know that the window handles are equal.
				if selfIA2Window and (selfIA2ID or otherIA2ID):
					# The window handles are valid and one of the objects has a valid unique ID.
					# Therefore, we can safely determine equality or inequality based on unique ID.
					return selfIA2ID==otherIA2ID
		except:
			pass
		if self.event_windowHandle is not None and other.event_windowHandle is not None and self.event_windowHandle!=other.event_windowHandle:
			return False
		if self.event_objectID is not None and other.event_objectID is not None and self.event_objectID!=other.event_objectID:
			return False
		if self.event_childID is not None and other.event_childID is not None and self.event_childID!=other.event_childID:
			return False
		if not super(IAccessible,self)._isEqual(other):
			return False
		selfIden=self.IAccessibleIdentity
		otherIden=other.IAccessibleIdentity
		if selfIden!=otherIden:
			return False
		if self.location!=other.location:
			return False
 		if self.IAccessibleRole!=other.IAccessibleRole:
			return False
		if self.name!=other.name:
			return False
		return True

	def _get_name(self):
		try:
			res=self.IAccessibleObject.accName(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_value(self):
		try:
			res=self.IAccessibleObject.accValue(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_actionStrings(self):
		try:
			action=self.IAccessibleObject.accDefaultAction(self.IAccessibleChildID)
		except:
			action=None
		if action:
			return [action]
		else:
			return super(IAccessible,self)._get_actionStrings()

	def doAction(self,index):
		if index==0:
			self.IAccessibleObject.accDoDefaultAction()

	def _get_IAccessibleIdentity(self):
		if not hasattr(self,'_IAccessibleIdentity'):
			try:
				self._IAccessibleIdentity=IAccessibleHandler.getIAccIdentity(self.IAccessibleObject,self.IAccessibleChildID)
			except:
				self._IAccessibleIdentity=None
		return self._IAccessibleIdentity

	def _get_IAccessibleRole(self):
		if isinstance(self.IAccessibleObject,IAccessibleHandler.IAccessible2):
			try:
				role=self.IAccessibleObject.role()
			except:
				role=0
		else:
			role=0
		if role==0:
			try:
				role=self.IAccessibleObject.accRole(self.IAccessibleChildID)
			except:
				role=0
		return role


	def _get_role(self):
		IARole=self.IAccessibleRole
		if isinstance(IARole,basestring):
			IARole=IARole.split(',')[0].lower()
			log.debug("IARole: %s"%IARole)
		return IAccessibleHandler.IAccessibleRolesToNVDARoles.get(IARole,controlTypes.ROLE_UNKNOWN)

	def _get_IAccessibleStates(self):
		try:
			res=self.IAccessibleObject.accState(self.IAccessibleChildID)
		except:
			return 0
		return res if isinstance(res,int) else 0

	def _get_states(self):
		try:
			IAccessibleStates=self.IAccessibleStates
		except:
			log.debugWarning("could not get IAccessible states",exc_info=True)
			states=set()
		else:
			states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in (y for y in (1<<z for z in xrange(32)) if y&IAccessibleStates) if IAccessibleHandler.IAccessibleStatesToNVDAStates.has_key(x))
		if not hasattr(self.IAccessibleObject,'states'):
			return states
		try:
			IAccessible2States=self.IAccessibleObject.states
		except:
			log.debugWarning("could not get IAccessible2 states",exc_info=True)
			IAccessible2States=IAccessibleHandler.IA2_STATE_DEFUNCT
		states=states|set(IAccessibleHandler.IAccessible2StatesToNVDAStates[x] for x in (y for y in (1<<z for z in xrange(32)) if y&IAccessible2States) if IAccessibleHandler.IAccessible2StatesToNVDAStates.has_key(x))
		if controlTypes.STATE_HASPOPUP in states and controlTypes.STATE_AUTOCOMPLETE in states:
			states.remove(controlTypes.STATE_HASPOPUP)
		if controlTypes.STATE_HALFCHECKED in states:
			states.discard(controlTypes.STATE_CHECKED)
		return states

	def _get_description(self):
		try:
			res=self.IAccessibleObject.accDescription(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_keyboardShortcut(self):
		try:
			res=self.IAccessibleObject.accKeyboardShortcut(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_childCount(self):
		count=IAccessibleHandler.accChildCount(self.IAccessibleObject)
		return count

	def _get_location(self):
		location=IAccessibleHandler.accLocation(self.IAccessibleObject,self.IAccessibleChildID)
		return location

	def _get_labeledBy(self):
		try:
			(pacc,accChild)=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVRELATION_LABELLED_BY)
			obj=IAccessible(IAccessibleObject=pacc,IAccessibleChildID=accChild)
			return obj
		except:
			return None

	def _get_parent(self):
		if self.IAccessibleChildID>0:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=0,event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=0)
		#Special code to support Mozilla node_child_of relation (for comboboxes)
		if self.windowClassName.startswith('Mozilla'):
			res=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVRELATION_NODE_CHILD_OF)
			if res and res!=(self.IAccessibleObject,self.IAccessibleChildID):
				newObj=IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
				if newObj:
					return newObj
		#Support for groupbox windows
		groupboxObj=IAccessibleHandler.findGroupboxObject(self)
		if groupboxObj:
			return groupboxObj
		res=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
		if res:
			try:
				parentRole=res[0].accRole(res[1])
			except:
				log.debugWarning("parent has bad role",exc_info=True)
				return None
			if parentRole!=IAccessibleHandler.ROLE_SYSTEM_WINDOW or IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_NEXT) or IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_PREVIOUS): 
				return IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
			res=IAccessibleHandler.accParent(res[0],res[1])
			if res:
				return IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
		return super(IAccessible,self)._get_parent()

	def _get_next(self):
		next=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_NEXT)
		if not next:
			next=None
			parent=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
			if not IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_PREVIOUS) and (parent and parent[0].accRole(parent[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW): 
				parentNext=IAccessibleHandler.accNavigate(parent[0],parent[1],IAccessibleHandler.NAVDIR_NEXT)
				if parentNext and parentNext[0].accRole(parentNext[1])>0:
					next=parentNext
		if next and next[0]==self.IAccessibleObject:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=next[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=next[1])
		if next and next[0].accRole(next[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW:
			child=IAccessibleHandler.accChild(next[0],-4)
			if not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_PREVIOUS) and not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_NEXT):
				next=child
		if next and next[0].accRole(next[1])>0:
			return IAccessible(IAccessibleObject=next[0],IAccessibleChildID=next[1])
 
	def _get_previous(self):
		previous=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_PREVIOUS)
		if not previous:
			previous=None
			parent=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
			if not IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_NEXT) and (parent and parent[0].accRole(parent[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW): 
				parentPrevious=IAccessibleHandler.accNavigate(parent[0],parent[1],IAccessibleHandler.NAVDIR_PREVIOUS)
				if parentPrevious and parentPrevious[0].accRole(parentPrevious[1])>0:
					previous=parentPrevious
		if previous and previous[0]==self.IAccessibleObject:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=previous[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=previous[1])
		if previous and previous[0].accRole(previous[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW:
			child=IAccessibleHandler.accChild(previous[0],-4)
			if not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_PREVIOUS) and not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_NEXT):
				previous=child
		if previous and previous[0].accRole(previous[1])>0:
			return IAccessible(IAccessibleObject=previous[0],IAccessibleChildID=previous[1])

	def _get_firstChild(self):
		firstChild=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_FIRSTCHILD)
		if not firstChild and self.IAccessibleChildID==0:
			children=IAccessibleHandler.accessibleChildren(self.IAccessibleObject,0,1)
			if len(children)>0:
				firstChild=children[0]
		if firstChild and firstChild[0]==self.IAccessibleObject:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=firstChild[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=firstChild[1])
		if firstChild and firstChild[0].accRole(firstChild[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW:
			child=IAccessibleHandler.accChild(firstChild[0],-4)
			if not child:
				child=IAccessibleHandler.accNavigate(firstChild[0],firstChild[1],IAccessibleHandler.NAVDIR_FIRSTCHILD)
			if child and not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_PREVIOUS) and not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_NEXT):
				firstChild=child
		if firstChild and firstChild[0].accRole(firstChild[1])>0:
			obj=IAccessible(IAccessibleObject=firstChild[0],IAccessibleChildID=firstChild[1])
			if (obj and winUser.isDescendantWindow(self.windowHandle,obj.windowHandle)) or self.windowHandle==winUser.getDesktopWindow():
				return obj

	def _get_lastChild(self):
		lastChild=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_LASTCHILD)
		if lastChild and lastChild[0]==self.IAccessibleObject:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=lastChild[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=lastChild[1])
		if lastChild and lastChild[0].accRole(lastChild[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW:
			child=IAccessibleHandler.accChild(lastChild[0],-4)
			if not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_PREVIOUS) and not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_NEXT):
				lastChild=child
		if lastChild and lastChild[0].accRole(lastChild[1])>0:
			obj=IAccessible(IAccessibleObject=lastChild[0],IAccessibleChildID=lastChild[1])
			if (obj and winUser.isDescendantWindow(self.windowHandle,obj.windowHandle)) or self.windowHandle==winUser.getDesktopWindow():
				return obj

	def _get_children(self):
		try:
			if self.IAccessibleChildID>0:
				return []
			childCount= self.IAccessibleObject.accChildCount
			if childCount==0:
				return []
			children=[]
			for child in IAccessibleHandler.accessibleChildren(self.IAccessibleObject,0,childCount):
				if child[0]==self.IAccessibleObject:
					children.append(IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=child[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=child[1]))
				elif child[0].accRole(child[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW:
					children.append(getNVDAObjectFromEvent(IAccessibleHandler.windowFromAccessibleObject(child[0]),IAccessibleHandler.OBJID_CLIENT,0))
				else:
					children.append(IAccessible(IAccessibleObject=child[0],IAccessibleChildID=child[1]))
			children=[x for x in children if x and winUser.isDescendantWindow(self.windowHandle,x.windowHandle)]
			return children
		except:
			return []

	def doDefaultAction(self):
		IAccessibleHandler.accDoDefaultAction(self.IAccessibleObject,self.IAccessibleChildID)

	def _get_activeChild(self):
		if self.IAccessibleChildID==0:
			res=IAccessibleHandler.accFocus(self.IAccessibleObject)
			if res:
				if res[0]==self.IAccessibleObject:
					return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=res[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=res[1])
				return IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])

	def _get_hasFocus(self):
		if (self.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_FOCUSED):
			return True
		else:
			return False

	def setFocus(self):
		try:
			self.IAccessibleObject.accSelect(1,self.IAccessibleChildID)
		except:
			pass

	def scrollIntoView(self):
		if isinstance(self.IAccessibleObject, IAccessibleHandler.IAccessible2):
			try:
				self.IAccessibleObject.scrollTo(IAccessibleHandler.IA2_SCROLL_TYPE_ANYWHERE)
			except:
				log.debugWarning("IAccessible2::scrollTo failed", exc_info=True)

	def _get_positionInfo(self):
		info={}
		try:
			groupPosition=list(self.IAccessibleObject.groupPosition)
		except:
			groupPosition=[0,0,0]
		if groupPosition[2]==0 and self.IAccessibleChildID>0:
			groupPosition[2]=self.IAccessibleChildID
		if groupPosition[1]==0:
			parent=self.parent
			if parent:
				groupPosition[1]=parent.childCount
		if groupPosition[0]:
			info['level']=groupPosition[0]
		if groupPosition[2]>0 and groupPosition[1]>=groupPosition[2]:
			info['similarItemsInGroup']=groupPosition[1]
			info['indexInGroup']=groupPosition[2]
		return info

	def event_valueChange(self):
		if hasattr(self,'IAccessibleTextObject'):
			self._hasContentChangedSinceLastSelection=True
			return
		return super(IAccessible,self).event_valueChange()

	def event_alert(self):
		# If the focus is within the alert object, don't report anything for it.
		if eventHandler.isPendingEvents("gainFocus"):
			# The alert event might be fired before the focus.
			api.processPendingEvents()
		if self in api.getFocusAncestors():
			return
		speech.cancelSpeech()
		speech.speakObject(self, reason=speech.REASON_FOCUS)
		for child in self.recursiveDescendants:
			if controlTypes.STATE_FOCUSABLE in child.states:
				speech.speakObject(child, reason=speech.REASON_FOCUS)

	def event_caret(self):
		super(IAccessible, self).event_caret()
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_CARET:
			return
		if hasattr(self,'IAccessibleTextObject') and self is api.getFocusObject() and not eventHandler.isPendingEvents("gainFocus"):
			if globalVars.caretMovesReviewCursor:
				api.setReviewPosition(self.makeTextInfo(textHandler.POSITION_CARET))
			self.detectPossibleSelectionChange()
		focusObject=api.getFocusObject()
		if self!=focusObject and not self.virtualBuffer and hasattr(self,'IAccessibleTextObject'):
			inDocument=None
			for ancestor in reversed(api.getFocusAncestors()+[focusObject]):
				if ancestor.role==controlTypes.ROLE_DOCUMENT:
					inDocument=ancestor
					break
			if not inDocument:
				return
			parent=self
			caretInDocument=False
			while parent:
				if parent==inDocument:
 					caretInDocument=True
					break
				parent=parent.parent
			if not caretInDocument:
				return
			info=self.makeTextInfo(textHandler.POSITION_CARET)
			info.expand(textHandler.UNIT_CHARACTER)
			try:
				char=ord(info.text)
			except:
				char=0
			if char!=0xfffc:
				IAccessibleHandler.processFocusNVDAEvent(self)

	def _get_groupName(self):
		return None
		if self.IAccessibleChildID>0:
			return None
		else:
			return super(IAccessible,self)._get_groupName()

	def speakDescendantObjects(self,hashList=None):
		if hashList is None:
			hashList=[]
		child=self.firstChild
		while child and winUser.isDescendantWindow(self.windowHandle,child.windowHandle):
			h=hash(child)
			if h not in hashList:
				hashList.append(h)
				speech.speakObject(child,reason=speech.REASON_FOCUS)
				child.speakDescendantObjects(hashList=hashList)
			child=child.next

	def event_show(self):
		if not winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle) or not winUser.isWindowVisible(self.windowHandle) or controlTypes.STATE_INVISIBLE in self.states: 
			return
		try:
			attribs=self.IAccessibleObject.attributes
		except:
			return
		if attribs and 'live:' in attribs and 'live:off' not in attribs:
			text=IAccessibleHandler.getRecursiveTextFromIAccessibleTextObject(self.IAccessibleObject)
			if text and not text.isspace():
				if 'live:rude' in attribs:
					speech.cancelSpeech()
				speech.speakMessage(text)

	def event_gainFocus(self):
		if hasattr(self,'IAccessibleTextObject'):
			self.initAutoSelectDetection()
		Window.event_gainFocus(self)

	def event_selection(self):
		return self.event_stateChange()

	def event_selectionAdd(self):
		return self.event_stateChange()

	def event_selectionRemove(self):
		return self.event_stateChange()

	def event_selectionWithIn(self):
		return self.event_stateChange()

class IAccessibleWindow(IAccessible):

	def _get_firstChild(self):
		child=super(IAccessibleWindow,self)._get_firstChild()
		if child:
			return child
		if JABHandler.isJavaWindow(self.windowHandle):
			jabContext=JABHandler.JABContext(hwnd=self.windowHandle)
			return NVDAObjects.JAB.JAB(jabContext=jabContext)
		return None

	def _get_lastChild(self):
		child=super(IAccessibleWindow,self)._get_lastChild()
		if child:
			return child
		if JABHandler.isJavaWindow(self.windowHandle):
			jabContext=JABHandler.JABContext(hwnd=self.windowHandle)
			return NVDAObjects.JAB.JAB(jabContext=jabContext)
		return None

	def _get_children(self):
		children=super(IAccessibleWindow,self)._get_children()
		if children:
			return children
		children=[]
		if JABHandler.isJavaWindow(self.windowHandle):
			jabContext=JABHandler.JABContext(hwnd=self.windowHandle)
			obj=NVDAObjects.JAB.JAB(jabContext=jabContext)
			if obj:
				children.append(obj)
		return children

class Groupbox(IAccessible):

	def _get_description(self):
		next=self.next
		if next and next.name==self.name and next.role==controlTypes.ROLE_GRAPHIC:
			next=next.next
		if next and next.role==controlTypes.ROLE_STATICTEXT:
			nextNext=next.next
			if nextNext and nextNext.name!=next.name:
				return next.name
		return super(Groupbox,self)._get_description()

class Dialog(IAccessible):
	"""Overrides the description property to obtain dialog text.
	"""

	@classmethod
	def getDialogText(cls,obj):
		"""This classmethod walks through the children of the given object, and collects up and returns any text that seems to be  part of a dialog's message text.
		@param obj: the object who's children you want to collect the text from
		@type obj: L{IAccessible}
		"""
		children=obj.children
		textList=[]
		childCount=len(children)
		for index in xrange(childCount):
			child=children[index]
			childStates=child.states
			childRole=child.role
			#We don't want to handle invisible or unavailable objects
			if controlTypes.STATE_INVISIBLE in childStates or controlTypes.STATE_UNAVAILABLE in childStates: 
				continue
			#For particular objects, we want to descend in to them and get their children's message text
			if childRole in (controlTypes.ROLE_PROPERTYPAGE,controlTypes.ROLE_PANE,controlTypes.ROLE_PANEL,controlTypes.ROLE_WINDOW):
				textList.append(cls.getDialogText(child))
				continue
			# We only want text from certain controls.
			if not (
				 # Static text, labels and links
				 childRole in (controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_LABEL,controlTypes.ROLE_LINK)
				# Read-only, non-multiline edit fields
				or (childRole==controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_READONLY in childStates and controlTypes.STATE_MULTILINE not in childStates)
			):
				continue
			#We should ignore a text object directly after a grouping object, as it's probably the grouping's description
			if index>0 and children[index-1].role==controlTypes.ROLE_GROUPING:
				continue
			#Like the last one, but a graphic might be before the grouping's description
			if index>1 and children[index-1].role==controlTypes.ROLE_GRAPHIC and children[index-2].role==controlTypes.ROLE_GROUPING:
				continue
			childName=child.name
			#Ignore objects that have another object directly after them with the same name, as this object is probably just a label for that object.
			#However, graphics, static text, separators and Windows are ok.
			if childName and index<(childCount-1) and children[index+1].role not in (controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_SEPARATOR,controlTypes.ROLE_WINDOW) and children[index+1].name==childName:
				continue
			childText=child.makeTextInfo(textHandler.POSITION_ALL).text
			if not childText or childText.isspace() and child.TextInfo!=NVDAObjectTextInfo:
				childText=child.basicText
			textList.append(childText)
		return " ".join(textList)

	def _get_description(self):
		return self.getDialogText(self)

class PropertyPage(Dialog):

	def _get_role(self):
		return controlTypes.ROLE_PROPERTYPAGE

class TrayClockWClass(IAccessible):
	"""
	Based on NVDAObject but the role is changed to clock.
	"""

	def _get_role(self):
		return controlTypes.ROLE_CLOCK

class OutlineItem(IAccessible):

	def _get_value(self):
		val=super(OutlineItem,self)._get_value()
		try:
			int(val)
		except:
			return val

class Tooltip(IAccessible):

	def event_show(self):
		if (config.conf["presentation"]["reportTooltips"] and (self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_TOOLTIP)) or (config.conf["presentation"]["reportHelpBalloons"] and (self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON)):
			speech.speakObject(self,reason=speech.REASON_FOCUS)

class ConsoleWindowClass(IAccessible):

	def event_nameChange(self):
		pass

class MozillaUIWindowClass_application(IAccessible):

	def _get_value(self):
		return None

	def event_nameChange(self):
		if self.windowHandle==api.getForegroundObject().windowHandle:
			speech.speakObjectProperties(self,name=True,reason=speech.REASON_QUERY)

class MozillaDocument(IAccessible):

	def _get_value(self):
		return 

class MozillaListItem(IAccessible):

	def _get_name(self):
		name=super(MozillaListItem,self)._get_name()
		if self.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_READONLY:
			children=super(MozillaListItem,self)._get_children()
			if len(children)>0 and (children[0].IAccessibleRole in ["bullet",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT]):
				name=children[0].value
		return name

	def _get_children(self):
		children=super(MozillaListItem,self)._get_children()
		if self.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_READONLY and len(children)>0 and (children[0].IAccessibleRole in ("bullet",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT)):
			del children[0]
		return children

class SHELLDLL_DefView_client(IAccessible):

	speakOnGainFocus=False

class List(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_LIST

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			speech.speakObject(child,reason=speech.REASON_FOCUS)

class ComboBox(IAccessible):

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			speech.speakObject(child,reason=speech.REASON_FOCUS)

class Outline(IAccessible):

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			speech.speakObject(child,reason=speech.REASON_FOCUS)

class ProgressBar(IAccessible):
	BASE_BEEP_FREQ=110

	def event_valueChange(self):
		if config.conf["presentation"]["reportProgressBarUpdates"]=="off":
			return super(ProgressBar,self).event_valueChange()
		val=self.value
		if val:
			val=val.rstrip('%\x00')
		if not val or val==globalVars.lastProgressValue:
			return
		if config.conf["presentation"]["reportProgressBarUpdates"] =="all" or (config.conf["presentation"]["reportProgressBarUpdates"] =="visible" and controlTypes.STATE_INVISIBLE not in self.states and winUser.isWindowVisible(self.windowHandle) and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle)):
			tones.beep(self.BASE_BEEP_FREQ*2**(float(val)/25.0),40)
		elif config.conf["presentation"]["reportProgressBarUpdates"] =="speak" and (int(val)%10)==0 and controlTypes.STATE_INVISIBLE not in self.states and winUser.isWindowVisible(self.windowHandle) and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			queueHandler.queueFunction(queueHandler.eventQueue,speech.speakMessage,_("%d percent")%int(val))
		globalVars.lastProgressValue=val

class InternetExplorerClient(IAccessible):

	def _get_description(self):
		return None

class SysLink(IAccessible):

	def reportFocus(self):
		pass

class TaskListIcon(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_ICON

	def reportFocus(self):
		if controlTypes.STATE_INVISIBLE in self.states:
			return
		super(TaskListIcon,self).reportFocus()

class ToolbarWindow32(IAccessible):

	def event_gainFocus(self):
		if (self.parent if self.IAccessibleRole == IAccessibleHandler.ROLE_SYSTEM_TOOLBAR else self.parent.parent).windowClassName == "SysPager":
			# This is the system tray.
			if not self.sysTrayGainFocus():
				return
		super(ToolbarWindow32, self).event_gainFocus()

	def sysTrayGainFocus(self):
		if mouseHandler.lastMouseEventTime < time.time() - 0.2:
			# This focus change was not caused by a mouse event.
			# If the mouse is on another toolbar control, the system tray toolbar will rudely
			# bounce the focus back to the object under the mouse after a brief pause.
			# Moving the mouse to the focus object isn't a good solution because
			# sometimes, the focus can't be moved away from the object under the mouse.
			# Therefore, move the mouse out of the way.
			winUser.setCursorPos(0, 0)

		if self.IAccessibleRole == IAccessibleHandler.ROLE_SYSTEM_TOOLBAR:
			# Sometimes, the toolbar itself receives the focus instead of the focused child.
			# However, the focused child still has the focused state.
			for child in self.children:
				if child.hasFocus:
					# Redirect the focus to the focused child.
					eventHandler.executeEvent("gainFocus", child)
					return False
			# We've really landed on the toolbar itself.
			# This was probably caused by moving the mouse out of the way in a previous focus event.
			# This previous focus event is no longer useful, so cancel speech.
			speech.cancelSpeech()

		return not eventHandler.isPendingEvents("gainFocus")

class MenuItem(IAccessible):

	def _get_description(self):
		name=self.name
		description=super(MenuItem,self)._get_description()
		if description!=name:
			return description
		else:
			return None

	def event_gainFocus(self):
		if eventHandler.isPendingEvents("gainFocus"):
			return
		super(MenuItem, self).event_gainFocus()

###class mappings

_staticMap={
	(None,IAccessibleHandler.ROLE_SYSTEM_WINDOW):"IAccessibleWindow",
	(None,IAccessibleHandler.ROLE_SYSTEM_CLIENT):"IAccessibleWindow",
	("tooltips_class32",IAccessibleHandler.ROLE_SYSTEM_TOOLTIP):"Tooltip",
	("tooltips_class32",IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON):"Tooltip",
	(None,IAccessibleHandler.ROLE_SYSTEM_DIALOG):"Dialog",
	(None,IAccessibleHandler.ROLE_SYSTEM_ALERT):"Dialog",
	(None,IAccessibleHandler.ROLE_SYSTEM_PROPERTYPAGE):"PropertyPage",
	(None,IAccessibleHandler.ROLE_SYSTEM_GROUPING):"Groupbox",
	(None,IAccessibleHandler.ROLE_SYSTEM_ALERT):"Dialog",
	("TrayClockWClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"TrayClockWClass",
	("Edit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TRxRichEdit",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TRxRichEdit",
	("RichEdit20",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit20",
	("RichEdit20A",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit20",
	("RichEdit20W",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit20",
	("RICHEDIT50W",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit50",
	(None,IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM):"OutlineItem",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_APPLICATION):"MozillaUIWindowClass_application",
	("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_APPLICATION):"MozillaUIWindowClass_application",
	("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):"Dialog",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"MozillaListItem",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"MozillaListItem",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):"MozillaDocument",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):"MozillaDocument",
	("ConsoleWindowClass",IAccessibleHandler.ROLE_SYSTEM_WINDOW):"ConsoleWindowClass",
	("ConsoleWindowClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"winConsole.WinConsole",
	("SHELLDLL_DefView",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"SHELLDLL_DefView_client",
	(None,IAccessibleHandler.ROLE_SYSTEM_LIST):"List",
	(None,IAccessibleHandler.ROLE_SYSTEM_COMBOBOX):"ComboBox",
	(None,IAccessibleHandler.ROLE_SYSTEM_OUTLINE):"Outline",
	(None,IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):"ProgressBar",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_TEXT):"MSHTML.MSHTML",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_PANE):"MSHTML.MSHTML",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"InternetExplorerClient",
	("TTntEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TMaskEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TTntMemo.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TRichView",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TRichView",
	("TRichViewEdit",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TRichViewEdit",
	("TRichEdit",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"edit.Edit",
	("TTntDrawGrid.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"List",
	("SysListView32",IAccessibleHandler.ROLE_SYSTEM_LIST):"sysListView32.List",
	("SysListView32",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("SysTreeView32",IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM):"sysTreeView32.TreeViewItem",
	("ATL:SysListView32",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("TWizardForm",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"Dialog",
	("SysLink",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"SysLink",
	("_WwG",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"winword.WordDocument",
	("EXCEL7",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"excel.ExcelGrid",
	("Scintilla",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"scintilla.Scintilla",
	("#32771",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"TaskListIcon",
	("TInEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("ToolbarWindow32",None):"ToolbarWindow32",
	("TFilenameEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TSpinEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TGroupBox",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TGroupBox",
	("TFormOptions",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TFormOptions",
	("TFormOptions",IAccessibleHandler.ROLE_SYSTEM_WINDOW):"delphi.TFormOptions",
	("TTabSheet",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TTabSheet",
	("ThunderRT6TextBox",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TMemo",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("RICHEDIT",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("MsiDialogCloseClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"Dialog",
	("TPasswordEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("#32768",IAccessibleHandler.ROLE_SYSTEM_MENUITEM):"MenuItem",
	("ToolbarWindow32",IAccessibleHandler.ROLE_SYSTEM_MENUITEM):"MenuItem",
	("TPTShellList",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("TProgressBar",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):"ProgressBar",
	("THppEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TUnicodeTextEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TTextEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TPropInspEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TFilterbarEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("EditControl",None):"edit.Edit",
	("AkelEditW",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"akelEdit.AkelEdit",
	("AkelEditA",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"akelEdit.AkelEdit",
	("TRichEditViewer",None):"edit.RichEdit",
	("AVL_AVView","Page"):"adobe.Page",
	("AVL_AVView",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):"adobe.Document",
	("TNavigableTntMemo.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TNavigableTntEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TskRichEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit20",
	("ATL:EDIT",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("mscandui21.candidate",IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON):"IME.IMECandidate",
	("RichEdit20WPT",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit20",
	("WindowsForms10.RichEdit20W.app.0.378734a",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit20",
	("WindowsForms10.EDIT.app.0.11c7a8c",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
}
