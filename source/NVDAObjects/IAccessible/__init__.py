#NVDAObjects/IAccessible.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import os
import tones
import textInfos.offsets
import time
import IAccessibleHandler
import oleacc
import JABHandler
import winUser
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
from NVDAObjects.behaviors import ProgressBar, Dialog

def getNVDAObjectFromEvent(hwnd,objectID,childID):
	try:
		accHandle=IAccessibleHandler.accessibleObjectFromEvent(hwnd,objectID,childID)
	except:
		accHandle=None
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

class IA2TextTextInfo(textInfos.offsets.OffsetsTextInfo):

	def _getOffsetFromPoint(self,x,y):
		if self.obj.IAccessibleTextObject.nCharacters>0:
			return self.obj.IAccessibleTextObject.OffsetAtPoint(x,y,IAccessibleHandler.IA2_COORDTYPE_SCREEN_RELATIVE)
		else:
			raise NotImplementedError

	def _getPointFromOffset(self,offset):
		try:
			res=self.obj.IAccessibleTextObject.characterExtents(offset,IAccessibleHandler.IA2_COORDTYPE_SCREEN_RELATIVE)
		except:
			raise NotImplementedError
		point=textInfos.Point(res[0]+(res[2]/2),res[1]+(res[3]/2))
		return point

	def _get_unit_mouseChunk(self):
		return "mouseChunk"

	def expand(self,unit):
		if unit==self.unit_mouseChunk:
			isMouseChunkUnit=True
			oldStart=self._startOffset
			oldEnd=self._endOffset
			unit=super(IA2TextTextInfo,self).unit_mouseChunk
		else:
			isMouseChunkUnit=False
		super(IA2TextTextInfo,self).expand(unit)
		if isMouseChunkUnit:
			text=self._getTextRange(self._startOffset,self._endOffset)
			try:
				self._startOffset=text.rindex(u'\ufffc',0,oldStart-self._startOffset)
			except ValueError:
				pass
			try:
				self._endOffset=text.index(u'\ufffc',oldEnd-self._startOffset)
			except ValueError:
				pass

	def _getCaretOffset(self):
		try:
			offset=self.obj.IAccessibleTextObject.caretOffset
		except COMError:
			log.debugWarning("IAccessibleText::caretOffset failed", exc_info=True)
			raise RuntimeError("Retrieving caret offset failed")
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
			return textInfos.FormatField(),(self._startOffset,self._endOffset)
		formatField=textInfos.FormatField()
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
			log.debugWarning("IAccessibleText::textAtOffset failed",exc_info=True)
			return offset,offset+1

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
			return super(IA2TextTextInfo,self)._getParagraphOffsets(offset)

	def _lineNumFromOffset(self,offset):
		return -1

class IAccessible(Window,AutoSelectDetectionNVDAObject):
	"""
the NVDAObject for IAccessible
@ivar IAccessibleChildID: the IAccessible object's child ID
@type IAccessibleChildID: int
"""

	IAccessibleTableUsesTableCellIndexAttrib=False #: Should the table-cell-index IAccessible2 object attribute be used rather than indexInParent?

	@classmethod
	def kwargsFromSuper(cls,relation=None,windowHandle=None):
		acc=None
		if isinstance(relation,tuple):
			acc=IAccessibleHandler.accessibleObjectFromPoint(relation[0],relation[1])
		elif relation=="focus":
			acc=IAccessibleHandler.accessibleObjectFromEvent(windowHandle,winUser.OBJID_CLIENT,0)
		elif relation!="parent":
			acc=IAccessibleHandler.accessibleObjectFromEvent(windowHandle,winUser.OBJID_WINDOW,0)
		else:
			acc=IAccessibleHandler.accessibleObjectFromEvent(windowHandle,winUser.OBJID_CLIENT,0)
		if not acc:
			raise RuntimeError
		return dict(windowHandle=windowHandle,IAccessibleObject=acc[0],IAccessibleChildID=acc[1])
 
	@classmethod
	def windowHasExtraIAccessibles(cls,windowHandle):
		"""Finds out whether this window has things such as a system menu / titleBar / scroll bars, which would be represented as extra IAccessibles"""
		style=winUser.getWindowStyle(windowHandle)
		return bool(style&winUser.WS_SYSMENU)

	def findOverlayClasses(self,clsList):
		if self.event_objectID==winUser.OBJID_CLIENT and JABHandler.isJavaWindow(self.windowHandle): 
			clsList.append(JavaVMRoot)

		windowClassName=self.windowClassName
		role=self.IAccessibleRole

		# Use window class name and role to search for a class match in our static map.
		keys=[(windowClassName,role),(None,role),(windowClassName,None)]
		normalizedWindowClassName=Window.normalizeWindowClassName(windowClassName)
		if normalizedWindowClassName!=windowClassName:
			keys.insert(1,(normalizedWindowClassName,role))
			keys.append((normalizedWindowClassName,None))
		for key in keys: 
			newCls=None
			classString=_staticMap.get(key,None)
			if classString and classString.find('.')>0:
				modString,classString=os.path.splitext(classString)
				classString=classString[1:]
				mod=__import__(modString,globals(),locals(),[])
				newCls=getattr(mod,classString)
			elif classString:
				newCls=globals()[classString]
			if newCls:
				clsList.append(newCls)

		# Some special cases.
		if (windowClassName in ("MozillaWindowClass", "GeckoPluginWindow") and not isinstance(self.IAccessibleObject, IAccessibleHandler.IAccessible2) and role == oleacc.ROLE_SYSTEM_TEXT) or windowClassName in ("MacromediaFlashPlayerActiveX", "ApolloRuntimeContentWindow", "ShockwaveFlash", "ShockwaveFlashLibrary"):
			# This is possibly a Flash object.
			from . import adobeFlash
			clsList = adobeFlash.findExtraOverlayClasses(self, clsList)
		if windowClassName=="Internet Explorer_Server" and (self.event_objectID is None or self.event_objectID==winUser.OBJID_CLIENT or self.event_objectID>0):
			from .mshtml import MSHTML
			clsList.append(MSHTML)
		elif windowClassName.startswith('Mozilla'):
			from .mozilla import Mozilla
			clsList.append( Mozilla)
		elif windowClassName.startswith('bosa_sdm'):
			from .msOffice import SDM
			clsList.append(SDM)
		if windowClassName.startswith('RichEdit') and winUser.getClassName(winUser.getAncestor(windowHandle,winUser.GA_PARENT)).startswith('bosa_sdm'):
			from .msOffice import RichEditSDMChild
			clsList.append(RichEditSDMChild)

		clsList.append(IAccessible)

		if self.event_objectID==winUser.OBJID_CLIENT and self.event_childID==0:
			# This is the main (client) area of the window, so we can use other classes at the window level.
			return super(IAccessible,self).findOverlayClasses(clsList)
		else:
			# This IAccessible does not represent the main part of the window, so we can only use IAccessible classes.
			return clsList

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
		# Try every trick in the book to get the window handle if we don't have it.
		if not windowHandle and isinstance(IAccessibleObject,IAccessibleHandler.IAccessible2):
			try:
				windowHandle=IAccessibleObject.windowHandle
			except COMError, e:
				log.debugWarning("IAccessible2::windowHandle failed: %s" % e)
			#Mozilla Gecko: we can never use a MozillaWindowClass window
			while windowHandle and winUser.getClassName(windowHandle)=="MozillaWindowClass":
				windowHandle=winUser.getAncestor(windowHandle,winUser.GA_PARENT)
		try:
			Identity=IAccessibleHandler.getIAccIdentity(IAccessibleObject,IAccessibleChildID)
		except:
			Identity=None
		if event_windowHandle is None and Identity and 'windowHandle' in Identity:
			event_windowHandle=Identity['windowHandle']
		if event_objectID is None and Identity and 'objectID' in Identity:
			event_objectID=Identity['objectID']
		if event_childID is None and Identity and 'childID' in Identity:
			event_childID=Identity['childID']
		if not windowHandle and event_windowHandle:
			windowHandle=event_windowHandle
		if not windowHandle:
			windowHandle=IAccessibleHandler.windowFromAccessibleObject(IAccessibleObject)
		if not windowHandle:
			log.debugWarning("Resorting to WindowFromPoint on accLocation")
			left,top,width,height = IAccessibleObject.accLocation(0)
			windowHandle=winUser.user32.WindowFromPoint(winUser.POINT(left,top))
		if not windowHandle:
			raise RuntimeError("Can't get a window handle from IAccessible")

		# Set the event params based on our calculated/construction info if we must.
		if event_windowHandle is None:
			event_windowHandle=windowHandle
		if event_objectID is None and isinstance(IAccessibleObject,IAccessibleHandler.IAccessible2):
			event_objectID=winUser.OBJID_CLIENT
		if event_childID is None and isinstance(IAccessibleObject,IAccessibleHandler.IAccessible2):
			try:
				event_childID=IAccessibleObject.uniqueID
			except:
				log.debugWarning("could not get IAccessible2::uniqueID to use as event_childID",exc_info=True)
		if event_childID is None:
			event_childID=IAccessibleChildID

		self.IAccessibleObject=IAccessibleObject
		self.IAccessibleChildID=IAccessibleChildID
		self.event_windowHandle=event_windowHandle
		self.event_objectID=event_objectID
		self.event_childID=event_childID
		super(IAccessible,self).__init__(windowHandle=windowHandle)

		try:
			self.IAccessibleActionObject=IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleAction)
		except:
			pass
		try:
			self.IAccessibleTableObject=self.IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleTable)
		except:
			pass
		try:
			self.IAccessibleTextObject=IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleText)
			if self.IAccessibleRole==oleacc.ROLE_SYSTEM_TEXT:
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
					("Back","backspaceCharacter"),
					("Control+Back","backspaceWord"),
				]]
		except:
			pass
		if None not in (event_windowHandle,event_objectID,event_childID):
			IAccessibleHandler.liveNVDAObjectTable[(event_windowHandle,event_objectID,event_childID)]=self

	def isDuplicateIAccessibleEvent(self,obj):
		"""Compaires the object of an event to self to see if the event should be treeted as duplicate."""
		#MSAA child elements do not have unique winEvent params as a childID could be reused if an element was deleted etc
		if self.IAccessibleChildID>0:
			return False
		return obj.event_windowHandle==self.event_windowHandle and obj.event_objectID==self.event_objectID and obj.event_childID==self.event_childID

	def _get_shouldAllowIAccessibleFocusEvent(self):
		"""Determine whether a focus event should be allowed for this object.
		Normally, this checks for the focused state to help eliminate redundant or invalid focus events.
		However, some implementations do not correctly set the focused state, so this must be overridden.
		@return: C{True} if the focus event should be allowed.
		@rtype: bool
		"""
		#this object or one of its ancestors must have state_focused.
		testObj = self
		while testObj:
			if controlTypes.STATE_FOCUSED in testObj.states:
				break
			parent = testObj.parent
			# Cache the parent.
			testObj.parent = parent
			testObj = parent
		else:
			return False
		return True

	def _get_TextInfo(self):
		if hasattr(self,'IAccessibleTextObject'):
			return IA2TextTextInfo
		return super(IAccessible,self).TextInfo

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
		#The edit field in a combo box should not have a label
		if self.role==controlTypes.ROLE_EDITABLETEXT:
			# The parent of the edit field is its window object, so the combo box is its grandparent.
			# Make sure to cache the parents.
			parent=self.parent=self.parent
			if parent:
				parent=self.parent.parent=self.parent.parent
			else:
				parent=None
			# Only scrap the label on the edit field if the parent combo box has a label.
			if parent and parent.role==controlTypes.ROLE_COMBOBOX and parent.name:
				return ""

		try:
			res=self.IAccessibleObject.accName(self.IAccessibleChildID)
		except:
			res=None
		if not res and hasattr(self,'IAccessibleTextObject'):
			try:
				res=self.makeTextInfo(textInfos.POSITION_CARET).text
				if res:
					return
			except (NotImplementedError, RuntimeError):
				try:
					res=self.makeTextInfo(textInfos.POSITION_ALL).text
				except (NotImplementedError, RuntimeError):
					res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_value(self):
		try:
			res=self.IAccessibleObject.accValue(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_actionCount(self):
		if hasattr(self,'IAccessibleActionObject'):
			try:
				return self.IAccessibleActionObject.nActions()
			except COMError:
				return 0
		return 1

	def getActionName(self,index=None):
		if not index:
			index=self.defaultActionIndex
		if hasattr(self,'IAccessibleActionObject'):
			try:
				return self.IAccessibleActionObject.name(index)
			except COMError:
				raise NotImplementedError
		elif index==0:
			try:
				action=self.IAccessibleObject.accDefaultAction(self.IAccessibleChildID)
			except COMError:
				action=None
			if action:
				return action
		raise NotImplementedError

	def doAction(self,index=None):
		if not index:
			index=self.defaultActionIndex
		if hasattr(self,'IAccessibleActionObject'):
			try:
				self.IAccessibleActionObject.doAction(index)
				return
			except COMError:
				raise NotImplementedError
		elif index==0:
			try:
				self.IAccessibleObject.accDoDefaultAction(self.IAccessibleChildID)
				return
			except COMError:
				raise NotImplementedError
		raise NotImplementedError

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
		if IARole==oleacc.ROLE_SYSTEM_CLIENT:
			superRole=super(IAccessible,self).role
			if superRole!=controlTypes.ROLE_WINDOW:
					return superRole
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
		states=set()
		if self.event_objectID in (winUser.OBJID_CLIENT, winUser.OBJID_WINDOW) and self.event_childID == 0:
			states.update(super(IAccessible, self).states)
		try:
			IAccessibleStates=self.IAccessibleStates
		except:
			log.debugWarning("could not get IAccessible states",exc_info=True)
		else:
			states.update(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in (y for y in (1<<z for z in xrange(32)) if y&IAccessibleStates) if IAccessibleHandler.IAccessibleStatesToNVDAStates.has_key(x))
		if not hasattr(self.IAccessibleObject,'states'):
			# Not an IA2 object.
			return states
		try:
			IAccessible2States=self.IAccessibleObject.states
		except:
			log.debugWarning("could not get IAccessible2 states",exc_info=True)
			IAccessible2States=IAccessibleHandler.IA2_STATE_DEFUNCT
		states=states|set(IAccessibleHandler.IAccessible2StatesToNVDAStates[x] for x in (y for y in (1<<z for z in xrange(32)) if y&IAccessible2States) if IAccessibleHandler.IAccessible2StatesToNVDAStates.has_key(x))
		try:
			IA2Attribs=self.IA2Attributes
		except COMError:
			log.debugWarning("could not get IAccessible2 attributes",exc_info=True)
			IA2Attribs=None
		if IA2Attribs:
			grabbed = IA2Attribs.get("grabbed")
			if grabbed == "false":
				states.add(controlTypes.STATE_DRAGGABLE)
			elif grabbed == "true":
				states.add(controlTypes.STATE_DRAGGING)
			if IA2Attribs.get("dropeffect", "none") != "none":
				states.add(controlTypes.STATE_DROPTARGET)
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
		try:
			return self.IAccessibleObject.accChildCount
		except COMError:
			return 0

	def _get_location(self):
		try:
			return self.IAccessibleObject.accLocation(self.IAccessibleChildID)
		except COMError:
			return None

	def isPointInObject(self,x,y):
		if self.windowHandle and not super(IAccessible,self).isPointInObject(x,y):
			return False
		res=IAccessibleHandler.accHitTest(self.IAccessibleObject,self.IAccessibleChildID,x,y)
		if not res or res[0]!=self.IAccessibleObject or res[1]!=self.IAccessibleChildID:
			return False
		return True

	def _get_labeledBy(self):
		try:
			(pacc,accChild)=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVRELATION_LABELLED_BY)
			obj=IAccessible(IAccessibleObject=pacc,IAccessibleChildID=accChild)
			return obj
		except:
			return None

	def _get_parent(self):
		if self.IAccessibleChildID>0:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=0,event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=0) or super(IAccessible,self).parent
		#Support for groupbox windows
		groupboxObj=IAccessibleHandler.findGroupboxObject(self)
		if groupboxObj:
			return groupboxObj
		if self.IAccessibleRole==oleacc.ROLE_SYSTEM_WINDOW:
			return super(IAccessible,self).parent
		res=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
		if res:
			return self.correctAPIForRelation(IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1]),relation="parent") or super(IAccessible,self).parent
		return super(IAccessible,self).parent

	def _get_next(self):
		if self.IAccessibleRole==oleacc.ROLE_SYSTEM_WINDOW:
			return super(IAccessible,self).next 
		res=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,oleacc.NAVDIR_NEXT)
		if not res:
			return None
		if res[0]==self.IAccessibleObject:
			return self.correctAPIForRelation(IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=res[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=res[1]))
		return self.correctAPIForRelation(IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1]))

	def _get_previous(self):
		if self.IAccessibleRole==oleacc.ROLE_SYSTEM_WINDOW:
			return super(IAccessible,self).previous
		res=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,oleacc.NAVDIR_PREVIOUS)
		if not res:
			return None
		if res[0]==self.IAccessibleObject:
			return self.correctAPIForRelation(IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=res[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=res[1]))
		return self.correctAPIForRelation(IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1]))

	def _get_firstChild(self):
		child=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,oleacc.NAVDIR_FIRSTCHILD)
		if not child and self.IAccessibleChildID==0:
			children=IAccessibleHandler.accessibleChildren(self.IAccessibleObject,0,1)
			if len(children)>0:
				child=children[0]
		if not child and self.IAccessibleChildID==0:
			return super(IAccessible,self).firstChild
		if child and child[0]==self.IAccessibleObject:
			return self.correctAPIForRelation(IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=child[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=child[1]))
		if child:
			obj=IAccessible(IAccessibleObject=child[0],IAccessibleChildID=child[1])
			if (obj and winUser.isDescendantWindow(self.windowHandle,obj.windowHandle)) or self.windowHandle==winUser.getDesktopWindow():
				return self.correctAPIForRelation(obj)

	def _get_lastChild(self):
		child=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,oleacc.NAVDIR_LASTCHILD)
		if not child and self.event_objectID==winUser.OBJID_CLIENT and self.IAccessibleChildID==0:
			return super(IAccessible,self).lastChild
		if child and child[0]==self.IAccessibleObject:
			return self.correctAPIForRelation(IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=child[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=child[1]))
		if child:
			obj=IAccessible(IAccessibleObject=child[0],IAccessibleChildID=child[1])
			if (obj and winUser.isDescendantWindow(self.windowHandle,obj.windowHandle)) or self.windowHandle==winUser.getDesktopWindow():
				return self.correctAPIForRelation(obj)

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
				elif child[0].accRole(child[1])==oleacc.ROLE_SYSTEM_WINDOW:
					children.append(self.correctAPIForRelation(getNVDAObjectFromEvent(IAccessibleHandler.windowFromAccessibleObject(child[0]),winUser.OBJID_CLIENT,0)))
				else:
					children.append(self.correctAPIForRelation(IAccessible(IAccessibleObject=child[0],IAccessibleChildID=child[1])))
			children=[x for x in children if x and winUser.isDescendantWindow(self.windowHandle,x.windowHandle)]
			return children
		except:
			return []

	def _get_IA2Attributes(self):
		try:
			attribs = self.IAccessibleObject.attributes
		except COMError as e:
			log.debugWarning("IAccessibleObject.attributes COMError %s"%e)
			attribs=None
		if attribs:
			return IAccessibleHandler.splitIA2Attribs(attribs)
		return {}

	def event_IA2AttributeChange(self):
		# We currently only care about changes to the accessible drag and drop attributes, which we map to states, so treat this as a stateChange.
		self.event_stateChange()

	def _get_rowNumber(self):
		table=self.table
		if table:
			if self.IAccessibleTableUsesTableCellIndexAttrib:
				try:
					index=self.IA2Attributes['table-cell-index']
				except KeyError:
					raise NotImplementedError
			else:
				index=self.IAccessibleObject.indexInParent
			index=int(index)
			try:
				return table.IAccessibleTableObject.rowIndex(index)+1
			except COMError:
				log.debugWarning("IAccessibleTable::rowIndex failed", exc_info=True)
		raise NotImplementedError

	def _get_columnNumber(self):
		table=self.table
		if table:
			if self.IAccessibleTableUsesTableCellIndexAttrib:
				try:
					index=self.IA2Attributes['table-cell-index']
				except KeyError:
					raise NotImplementedError
			else:
				index=self.IAccessibleObject.indexInParent
			index=int(index)
			try:
				return table.IAccessibleTableObject.columnIndex(index)+1
			except COMError:
				log.debugWarning("IAccessibleTable::columnIndex failed", exc_info=True)
		raise NotImplementedError

	def _get_rowCount(self):
		if hasattr(self,'IAccessibleTableObject'):
			try:
				return self.IAccessibleTableObject.nRows
			except COMError:
				log.debugWarning("IAccessibleTable::nRows failed", exc_info=True)
		raise NotImplementedError

	def _get_columnCount(self):
		if hasattr(self,'IAccessibleTableObject'):
			try:
				return self.IAccessibleTableObject.nColumns
			except COMError:
				log.debugWarning("IAccessibleTable::nColumns failed", exc_info=True)
		raise NotImplementedError

	def _get_table(self):
		if not isinstance(self.IAccessibleObject,IAccessibleHandler.IAccessible2):
			return None
		table=getattr(self,'_table',None)
		if table:
			return table
		checkAncestors=False
		if self.IAccessibleTableUsesTableCellIndexAttrib:
			try:
				attribs=self.IAccessibleObject.attributes
			except COMError:
				attribs=None
			if attribs and 'table-cell-index:' in attribs:
				checkAncestors=True
		obj=self.parent
		while checkAncestors and obj and not hasattr(obj,'IAccessibleTableObject'):
			parent=obj.parent=obj.parent
			obj=parent
		if not obj or not hasattr(obj,'IAccessibleTableObject'):
			return None
		self._table=obj
		return obj

	def _get_activeChild(self):
		if self.IAccessibleChildID==0:
			res=IAccessibleHandler.accFocus(self.IAccessibleObject)
			if res:
				if res[0]==self.IAccessibleObject:
					return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=res[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=res[1])
				return IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])

	def _get_hasFocus(self):
		if (self.IAccessibleStates&oleacc.STATE_SYSTEM_FOCUSED):
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
		level=similarItemsInGroup=indexInGroup=0
		if isinstance(self.IAccessibleObject,IAccessibleHandler.IAccessible2):
			try:
				level,similarItemsInGroup,indexInGroup=self.IAccessibleObject.groupPosition
				gotVars=True
			except COMError:
				pass
		if indexInGroup==0:
			indexInGroup=self.IAccessibleChildID
		if indexInGroup>0 and similarItemsInGroup<indexInGroup:
			parent=self.parent=self.parent
			similarItemsInGroup=parent.childCount
		if level>0:
			info['level']=level
		if indexInGroup<=similarItemsInGroup and indexInGroup>0:
			info['similarItemsInGroup']=similarItemsInGroup
			info['indexInGroup']=indexInGroup
		return info

	def event_valueChange(self):
		if hasattr(self,'IAccessibleTextObject'):
			self._hasContentChangedSinceLastSelection=True
			return
		return super(IAccessible,self).event_valueChange()

	def event_alert(self):
		if self.role != controlTypes.ROLE_ALERT:
			# Ignore alert events on objects that aren't alerts.
			return
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
		if self.IAccessibleRole==oleacc.ROLE_SYSTEM_CARET:
			return
		if hasattr(self,'IAccessibleTextObject') and self is api.getFocusObject() and not eventHandler.isPendingEvents("gainFocus"):
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
			try:
				info=self.makeTextInfo(textInfos.POSITION_CARET)
			except RuntimeError:
				return
			info.expand(textInfos.UNIT_CHARACTER)
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

	def event_gainFocus(self):
		if hasattr(self,'IAccessibleTextObject'):
			self.initAutoSelectDetection()
		super(IAccessible,self).event_gainFocus()

	def event_selection(self):
		return self.event_stateChange()

	def event_selectionAdd(self):
		return self.event_stateChange()

	def event_selectionRemove(self):
		return self.event_stateChange()

	def event_selectionWithIn(self):
		return self.event_stateChange()

	def _get_presentationType(self):
		if not self.windowHasExtraIAccessibles(self.windowHandle) and self.role==controlTypes.ROLE_WINDOW:
			return self.presType_layout
		return super(IAccessible,self).presentationType

	def _get_isPresentableFocusAncestor(self):
		IARole = self.IAccessibleRole
		if IARole == oleacc.ROLE_SYSTEM_CLIENT and self.windowStyle & winUser.WS_SYSMENU:
			return True
		if IARole == oleacc.ROLE_SYSTEM_WINDOW:
			return False
		return super(IAccessible, self).isPresentableFocusAncestor

class ShellDocObjectView(IAccessible):

	def event_gainFocus(self):
		#Sometimes Shell DocObject View gets focus, when really the document inside it should
		#Adobe Reader 9 licence agreement
		if eventHandler.isPendingEvents("gainFocus") or self.childCount!=1:
			return super(ShellDocObjectView,self).event_gainFocus()
		child=self.firstChild
		if not child or child.windowClassName!="Internet Explorer_Server" or child.role!=controlTypes.ROLE_PANE:
			return super(ShellDocObjectView,self).event_gainFocus()
		child=child.firstChild
		if not child or child.windowClassName!="Internet Explorer_Server" or child.role!=controlTypes.ROLE_DOCUMENT:
			return super(ShellDocObjectView,self).event_gainFocus()
		eventHandler.queueEvent("gainFocus",child)

class JavaVMRoot(IAccessible):

	def _get_firstChild(self):
		jabContext=JABHandler.JABContext(hwnd=self.windowHandle)
		return NVDAObjects.JAB.JAB(jabContext=jabContext)

	def _get_lastChild(self):
		jabContext=JABHandler.JABContext(hwnd=self.windowHandle)
		return NVDAObjects.JAB.JAB(jabContext=jabContext)

	def _get_children(self):
		children=[]
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
		if (config.conf["presentation"]["reportTooltips"] and (self.IAccessibleRole==oleacc.ROLE_SYSTEM_TOOLTIP)) or (config.conf["presentation"]["reportHelpBalloons"] and (self.IAccessibleRole==oleacc.ROLE_SYSTEM_HELPBALLOON)):
			speech.speakObject(self,reason=speech.REASON_FOCUS)

class ConsoleWindowClass(IAccessible):

	def event_nameChange(self):
		pass


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

class InternetExplorerClient(IAccessible):

	def _get_description(self):
		return None

class SysLinkClient(IAccessible):

	def reportFocus(self):
		pass

class SysLink(IAccessible):

	def _get_name(self):
		#Workaround for #451 - explorer returns incorrect string length, thus it can contain garbage characters
		name=super(SysLink,self).name
		if name: 
			#Remove any data after the null character
			i=name.find('\0')
			if i>=0: name=name[:i]
		return name

class TaskList(IAccessible):
	isPresentableFocusAncestor = False

	def event_gainFocus(self):
		# Normally, we don't want to act on this focus event.
		if self.childCount == 0:
			# However, in Windows 7, the task list gets focus even if alt+tab is pressed with no applications open.
			# In this case, we must report the focus so the user knows where the focus has landed.
			return super(TaskList, self).event_gainFocus()

class TaskListIcon(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_ICON

	def reportFocus(self):
		if controlTypes.STATE_INVISIBLE in self.states:
			return
		super(TaskListIcon,self).reportFocus()

class ToolbarWindow32(IAccessible):

	def event_gainFocus(self):
		toolbarParent = self.parent
		if toolbarParent and self.IAccessibleRole != oleacc.ROLE_SYSTEM_TOOLBAR:
			toolbarParent = toolbarParent.parent
		if toolbarParent and toolbarParent.windowClassName == "SysPager":
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

		if self.IAccessibleRole == oleacc.ROLE_SYSTEM_TOOLBAR:
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

class Taskbar(IAccessible):
	name = _("Taskbar")

###class mappings

_staticMap={
	("tooltips_class32",oleacc.ROLE_SYSTEM_TOOLTIP):"Tooltip",
	("tooltips_class32",oleacc.ROLE_SYSTEM_HELPBALLOON):"Tooltip",
	(None,oleacc.ROLE_SYSTEM_DIALOG):"Dialog",
	(None,oleacc.ROLE_SYSTEM_ALERT):"Dialog",
	(None,oleacc.ROLE_SYSTEM_PROPERTYPAGE):"Dialog",
	(None,oleacc.ROLE_SYSTEM_GROUPING):"Groupbox",
	("TrayClockWClass",oleacc.ROLE_SYSTEM_CLIENT):"TrayClockWClass",
	("TRxRichEdit",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TRxRichEdit",
	(None,oleacc.ROLE_SYSTEM_OUTLINEITEM):"OutlineItem",
	("MozillaUIWindowClass",oleacc.ROLE_SYSTEM_APPLICATION):"mozilla.application",
	("MozillaDialogClass",oleacc.ROLE_SYSTEM_ALERT):"Dialog",
	("MozillaContentWindowClass",oleacc.ROLE_SYSTEM_COMBOBOX):"mozilla.ComboBox",
	("MozillaContentWindowClass",oleacc.ROLE_SYSTEM_LIST):"mozilla.List",
	("MozillaWindowClass",oleacc.ROLE_SYSTEM_LISTITEM):"mozilla.ListItem",
	("MozillaContentWindowClass",oleacc.ROLE_SYSTEM_LISTITEM):"mozilla.ListItem",
	("MozillaContentWindowClass",oleacc.ROLE_SYSTEM_DOCUMENT):"mozilla.Document",
	("MozillaWindowClass",oleacc.ROLE_SYSTEM_DOCUMENT):"mozilla.Document",
	("MozillaUIWindowClass",oleacc.ROLE_SYSTEM_TABLE):"mozilla.Table",
	("MozillaUIWindowClass",oleacc.ROLE_SYSTEM_OUTLINE):"mozilla.Tree",
	("ConsoleWindowClass",oleacc.ROLE_SYSTEM_WINDOW):"ConsoleWindowClass",
	(None,oleacc.ROLE_SYSTEM_LIST):"List",
	(None,oleacc.ROLE_SYSTEM_COMBOBOX):"ComboBox",
	(None,oleacc.ROLE_SYSTEM_OUTLINE):"Outline",
	(None,oleacc.ROLE_SYSTEM_PROGRESSBAR):"ProgressBar",
	("TRichView",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TRichView",
	("TRichViewEdit",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TRichViewEdit",
	("TTntDrawGrid.UnicodeClass",oleacc.ROLE_SYSTEM_CLIENT):"List",
	("SysListView32",oleacc.ROLE_SYSTEM_LIST):"sysListView32.List",
	("SysListView32",oleacc.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("SysListView32",oleacc.ROLE_SYSTEM_MENUITEM):"sysListView32.ListItem",
	("SysTreeView32",oleacc.ROLE_SYSTEM_OUTLINE):"sysTreeView32.TreeView",
	("SysTreeView32",oleacc.ROLE_SYSTEM_OUTLINEITEM):"sysTreeView32.TreeViewItem",
	("SysTreeView32",oleacc.ROLE_SYSTEM_MENUITEM):"sysTreeView32.TreeViewItem",
	("SysTreeView32",0):"sysTreeView32.BrokenCommctrl5Item",
	("ATL:SysListView32",oleacc.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("TWizardForm",oleacc.ROLE_SYSTEM_CLIENT):"Dialog",
	("SysLink",oleacc.ROLE_SYSTEM_CLIENT):"SysLinkClient",
	("SysLink",oleacc.ROLE_SYSTEM_LINK):"SysLink",
	("#32771",oleacc.ROLE_SYSTEM_LIST):"TaskList",
	("TaskSwitcherWnd",oleacc.ROLE_SYSTEM_LIST):"TaskList",
	("#32771",oleacc.ROLE_SYSTEM_LISTITEM):"TaskListIcon",
	("TaskSwitcherWnd",oleacc.ROLE_SYSTEM_LISTITEM):"TaskListIcon",
	("ToolbarWindow32",None):"ToolbarWindow32",
	("TGroupBox",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TGroupBox",
	("TFormOptions",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TFormOptions",
	("TFormOptions",oleacc.ROLE_SYSTEM_WINDOW):"delphi.TFormOptions",
	("TTabSheet",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TTabSheet",
	("MsiDialogCloseClass",oleacc.ROLE_SYSTEM_CLIENT):"Dialog",
	("#32768",oleacc.ROLE_SYSTEM_MENUITEM):"MenuItem",
	("ToolbarWindow32",oleacc.ROLE_SYSTEM_MENUITEM):"MenuItem",
	("TPTShellList",oleacc.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("TProgressBar",oleacc.ROLE_SYSTEM_PROGRESSBAR):"ProgressBar",
	("AVL_AVView",None):"adobe.AcrobatNode",
	("AVL_AVView",oleacc.ROLE_SYSTEM_TEXT):"adobe.AcrobatTextNode",
	("AcrobatSDIWindow",oleacc.ROLE_SYSTEM_CLIENT):"adobe.AcrobatSDIWindowClient",
	("mscandui21.candidate",oleacc.ROLE_SYSTEM_PUSHBUTTON):"IME.IMECandidate",
	("SysMonthCal32",oleacc.ROLE_SYSTEM_CLIENT):"SysMonthCal32.SysMonthCal32",
	("hh_kwd_vlist",oleacc.ROLE_SYSTEM_LIST):"hh.KeywordList",
	("Scintilla",oleacc.ROLE_SYSTEM_CLIENT):"scintilla.Scintilla",
	("MSOUNISTAT",oleacc.ROLE_SYSTEM_CLIENT):"msOffice.MSOUNISTAT",
	("QWidget",oleacc.ROLE_SYSTEM_CLIENT):"qt.Client",
	("QWidget",oleacc.ROLE_SYSTEM_LIST):"qt.Container",
	("QWidget",oleacc.ROLE_SYSTEM_OUTLINE):"qt.Container",
	("QWidget",oleacc.ROLE_SYSTEM_MENUBAR):"qt.Container",
	("QWidget",oleacc.ROLE_SYSTEM_OUTLINEITEM):"qt.TreeViewItem",
	("QPopup",oleacc.ROLE_SYSTEM_MENUPOPUP):"qt.Menu",
	("QWidget",oleacc.ROLE_SYSTEM_IPADDRESS):"qt.LayeredPane",
	("QWidget",oleacc.ROLE_SYSTEM_APPLICATION):"qt.Application",
	("Shell_TrayWnd",oleacc.ROLE_SYSTEM_CLIENT):"Taskbar",
	("Internet Explorer_TridentCmboBx",oleacc.ROLE_SYSTEM_COMBOBOX):"MSHTML.V6ComboBox",
	("Shell DocObject View",oleacc.ROLE_SYSTEM_CLIENT):"ShellDocObjectView",
}
