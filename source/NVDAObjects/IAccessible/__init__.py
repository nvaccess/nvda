# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2021 NV Access Limited, Babbage B.V.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import typing
from typing import (
	Optional,
	Union,
)

from comtypes.automation import IEnumVARIANT, VARIANT
from comtypes import (
	COMError,
	IServiceProvider,
	GUID,
	IUnknown,
	BSTR,
)
from comtypes.hresult import S_OK, S_FALSE
import comtypes.client
import ctypes
import os
import re
import sys
import itertools
import importlib
from comInterfaces.tom import ITextDocument
from comInterfaces import Accessibility as IA
from comInterfaces import IAccessible2Lib as IA2
import tones
import languageHandler
import textInfos.offsets
import textUtils
import colors
import time
import displayModel
import IAccessibleHandler
import oleacc
import JABHandler
import winUser
import globalVars
from logHandler import log
import speech
import braille
import api
import config
import controlTypes
from controlTypes import TextPosition
from NVDAObjects.window import Window
from NVDAObjects import NVDAObject, NVDAObjectTextInfo, InvalidNVDAObject
import NVDAObjects.JAB
import eventHandler
from NVDAObjects.behaviors import ProgressBar, Dialog, EditableTextWithAutoSelectDetection, FocusableUnfocusableContainer, ToolTip, Notification
from locationHelper import RectLTWH
import NVDAHelper


# Custom object ID used for clipboard pane in some versions of MS Office
MSO_COLLECT_AND_PASTE_OBJECT_ID = 21


def getNVDAObjectFromEvent(hwnd,objectID,childID):
	try:
		accHandle=IAccessibleHandler.accessibleObjectFromEvent(hwnd,objectID,childID)
	except WindowsError:
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

FORMAT_OBJECT_ATTRIBS = frozenset({"text-align"})
def normalizeIA2TextFormatField(formatField):
	try:
		textAlign=formatField.pop("text-align")
	except KeyError:
		textAlign=None
	if textAlign:
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
	if invalid:
		# aria-invalid can contain multiple values separated by a comma.
		invalidList = [x.lower().strip() for x in invalid.split(',')]
		if "spelling" in invalidList:
			formatField["invalid-spelling"]=True
		if "grammar" in invalidList:
			formatField["invalid-grammar"]=True
	color=formatField.get('color')
	if color:
		try:
			formatField['color']=colors.RGB.fromString(color)
		except ValueError:
			pass
	backgroundColor=formatField.get('background-color')
	if backgroundColor:
		try:
			formatField['background-color']=colors.RGB.fromString(backgroundColor)
		except ValueError:
			pass
	lineStyle=formatField.get("text-underline-style")
	lineType=formatField.get("text-underline-type")
	if lineStyle or lineType:
		formatField["underline"]=lineStyle!="none" and lineType!="none"
	lineStyle=formatField.get("text-line-through-style")
	lineType=formatField.get("text-line-through-type")
	if lineStyle or lineType:
		formatField["strikethrough"]=lineStyle!="none" and lineType!="none"
	language=formatField.get('language')
	if language:
		formatField['language']=languageHandler.normalizeLanguage(language)
	try:
		formatField["text-position"] = TextPosition(formatField.pop("text-position"))
	except KeyError:
		formatField["text-position"] = TextPosition.BASELINE

class IA2TextTextInfo(textInfos.offsets.OffsetsTextInfo):

	detectFormattingAfterCursorMaybeSlow=False

	def _get_encoding(self):
		return super().encoding

	def _getOffsetFromPoint(self,x,y):
		if self.obj.IAccessibleTextObject.nCharacters>0:
			offset = self.obj.IAccessibleTextObject.OffsetAtPoint(
				x, y, IA2.IA2_COORDTYPE_SCREEN_RELATIVE
			)
			# IA2 specifies that a result of -1 indicates that
			# the point is invalid or there is no character under the point.
			# Note that Chromium does not follow the spec and returns 0 for invalid or no character points.
			# As 0 is a valid offset, there's nothing we could do other than just returning it.
			if offset == -1:
				raise LookupError("Invalid point or no character under point")
			return offset
		else:
			raise LookupError

	@classmethod
	def _getBoundingRectFromOffsetInObject(cls,obj,offset):
		try:
			res = RectLTWH(*obj.IAccessibleTextObject.characterExtents(
				offset, IA2.IA2_COORDTYPE_SCREEN_RELATIVE
			))
		except COMError:
			raise NotImplementedError
		if not any(res[2:]):
			# Gecko tends to return (0,0,0,0) rectangles sometimes, for example in empty text fields.
			# Chromium could return rectangles that are positioned at the upper left corner of the object,
			# and they have a width and height of 0.
			# Other IA2 implementations, such as the one in LibreOffice,
			# tend to return the caret rectangle in this case, which is ok.
			raise LookupError
		return res

	def _getBoundingRectFromOffset(self,offset):
		return self._getBoundingRectFromOffsetInObject(self.obj, offset)

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
			if not text:
				return
			try:
				self._startOffset = text.rindex(textUtils.OBJ_REPLACEMENT_CHAR, 0, oldStart - self._startOffset)
			except ValueError:
				pass
			try:
				self._endOffset = text.index(textUtils.OBJ_REPLACEMENT_CHAR, oldEnd - self._startOffset)
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
		except COMError:
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
		if start!=end:
			self.obj.IAccessibleTextObject.AddSelection(start,end)
		else:
			# A collapsed selection is the caret.
			# Specifically handling it here as a setCaretOffset gets around some strange bugs in Chrome where setting a collapsed selection selects an entire table cell.
			self._setCaretOffset(start)

	def _getStoryLength(self):
		try:
			return self.obj.IAccessibleTextObject.NCharacters
		except COMError:
			log.debugWarning("IAccessibleText::nCharacters failed",exc_info=True)
			return 0

	def _getLineCount(self):
			return -1

	def _getTextRange(self,start,end):
		try:
			return self.obj.IAccessibleTextObject.text(start,end) or u""
		except COMError:
			return u""

	def _getFormatFieldAndOffsets(self,offset,formatConfig,calculateOffsets=True):
		try:
			startOffset,endOffset,attribsString=self.obj.IAccessibleTextObject.attributes(offset)
		except COMError:
			log.debugWarning("could not get attributes",exc_info=True)
			return textInfos.FormatField(),(self._startOffset,self._endOffset)
		formatField=textInfos.FormatField()
		if attribsString is None and offset>0:
			try:
				attribsString=self.obj.IAccessibleTextObject.attributes(offset-1)[2]
			except COMError:
				pass
		if attribsString:
			formatField.update(IAccessibleHandler.splitIA2Attribs(attribsString))
		objAttribs = self.obj.IA2Attributes
		for attr in FORMAT_OBJECT_ATTRIBS:
			try:
				formatField[attr] = objAttribs[attr]
			except KeyError:
				pass
		normalizeIA2TextFormatField(formatField)
		return formatField,(startOffset,endOffset)

	def _getCharacterOffsets(self,offset):
		try:
			if offset>=self.obj.IAccessibleTextObject.nCharacters:
				return offset,offset+1
		except COMError:
			pass
		try:
			start, end, text = self.obj.IAccessibleTextObject.TextAtOffset(offset, IA2.IA2_TEXT_BOUNDARY_CHAR)
		except COMError:
			return super(IA2TextTextInfo,self)._getCharacterOffsets(offset)
		if text and (textUtils.isHighSurrogate(text) or textUtils.isLowSurrogate(text)):
			# #8953: Some IA2 implementations, including Gecko and Chromium,
			# erroneously report one offset for surrogates.
			return super(IA2TextTextInfo,self)._getCharacterOffsets(offset)
		return start, end

	def _getWordOffsets(self,offset):
		try:
			if offset>=self.obj.IAccessibleTextObject.nCharacters:
				return offset,offset+1
		except COMError:
			pass
		try:
			start, end, text = self.obj.IAccessibleTextObject.TextAtOffset(offset, IA2.IA2_TEXT_BOUNDARY_WORD)
		except COMError:
			return super(IA2TextTextInfo,self)._getWordOffsets(offset)
		if start>offset or offset>end:
			# HACK: Work around buggy implementations which return a range that does not include offset.
			return offset,offset+1
		return start,end

	def _getLineOffsets(self,offset):
		try:
			start, end, text = self.obj.IAccessibleTextObject.TextAtOffset(offset, IA2.IA2_TEXT_BOUNDARY_LINE)
			return start,end
		except COMError:
			log.debugWarning("IAccessibleText::textAtOffset failed",exc_info=True)
			return offset,offset+1

	def _getSentenceOffsets(self,offset):
		try:
			if offset>=self.obj.IAccessibleTextObject.nCharacters:
				return offset,offset+1
		except COMError:
			pass
		try:
			start, end, text = self.obj.IAccessibleTextObject.TextAtOffset(offset, IA2.IA2_TEXT_BOUNDARY_SENTENCE)
			if start==end:
				raise NotImplementedError
			return start,end
		except COMError:
			return super(IA2TextTextInfo,self)._getSentenceOffsets(offset)

	def _getParagraphOffsets(self,offset):
		try:
			if offset>self.obj.IAccessibleTextObject.nCharacters:
				return offset,offset+1
		except COMError:
			pass
		try:
			start, end, text = self.obj.IAccessibleTextObject.TextAtOffset(offset, IA2.IA2_TEXT_BOUNDARY_PARAGRAPH)
			if start>=end:
				raise RuntimeError("did not expand to paragraph correctly")
			return start,end
		except (RuntimeError,COMError):
			return super(IA2TextTextInfo,self)._getParagraphOffsets(offset)

	def _lineNumFromOffset(self,offset):
		return -1

	def _iterTextWithEmbeddedObjects(
			self,
			withFields,
			formatConfig=None
	) -> typing.Generator[typing.Union[textInfos.FieldCommand, str, int], None, None]:
		"""Iterate through the text, splitting at embedded object characters.
		Where an embedded object character occurs, its offset is provided.
		@param withFields: Whether to output control/format fields.
		@type withFields: bool
		@param formatConfig: Document formatting configuration.
		@return: A generator of fields, text strings and numeric offsets of embedded object characters.
		"""
		if withFields:
			items = self.getTextWithFields(formatConfig=formatConfig)
		else:
			items = [self.text]
		offset = self._startOffset
		for item in items:
			if not isinstance(item, str):
				# This is a field.
				yield item
				continue
			itemLen = len(item)
			# The text consists of smaller chunks of text interspersed with embedded object characters.
			chunkStart = 0
			while chunkStart < itemLen:
				# Find the next embedded object character.
				try:
					chunkEnd = item.index(textUtils.OBJ_REPLACEMENT_CHAR, chunkStart)
				except ValueError:
					# This is the last chunk of text.
					yield item[chunkStart:]
					break
				if chunkStart != chunkEnd:
					yield item[chunkStart:chunkEnd]
				# We've hit an embedded object character, so yield its offset.
				yield offset + chunkEnd
				chunkStart = chunkEnd + 1
			offset += itemLen

class IAccessible(Window):
	"""
the NVDAObject for IAccessible
@ivar IAccessibleChildID: the IAccessible object's child ID
@type IAccessibleChildID: int
"""

	IAccessibleTableUsesTableCellIndexAttrib=False #: Should the table-cell-index IAccessible2 object attribute be used rather than indexInParent?
	IA2UniqueID=None #: The cached IAccessible2::uniqueID if its implemented

	@classmethod
	def getPossibleAPIClasses(cls,kwargs,relation=None):
		from . import MSHTML
		yield MSHTML.MSHTML

	@classmethod
	def kwargsFromSuper(cls,kwargs,relation=None):
		acc=None
		objID=None
		windowHandle=kwargs['windowHandle']
		if isinstance(relation,tuple):
			acc=IAccessibleHandler.accessibleObjectFromPoint(relation[0],relation[1])
		elif relation=="focus":
			objID=winUser.OBJID_CLIENT
			acc=IAccessibleHandler.accessibleObjectFromEvent(windowHandle,objID,0)
			if not acc:
				return False
			testAccFocus=acc
			usedAccFocus=False
			# Keep doing accFocus until we can't anymore or until accFocus keeps returning the same object.
			while True:
				testAccFocus=IAccessibleHandler.accFocus(testAccFocus[0])
				# Only set the acc variable if we get something useful using accFocus.
				if testAccFocus and testAccFocus!=acc:
					acc=testAccFocus
					usedAccFocus=True
				else:
					# We can't go any further.
					break
			if usedAccFocus:
				# We don't know the event parameters for this object.
				objID=None
				# This object may also be in a different window, so we need to recalculate the window handle.
				kwargs['windowHandle']=None
		elif relation in ("parent","foreground"):
			objID=winUser.OBJID_CLIENT
		else:
			objID=winUser.OBJID_WINDOW
		if not acc and objID is not None:
			acc=IAccessibleHandler.accessibleObjectFromEvent(windowHandle,objID,0)
		if not acc:
			return False
		kwargs['IAccessibleObject']=acc[0]
		kwargs['IAccessibleChildID']=acc[1]
		if objID:
			# We know the event parameters, so pass them to the NVDAObject.
			kwargs['event_windowHandle']=windowHandle
			kwargs['event_objectID']=objID
			kwargs['event_childID']=0
		return True

	def findOverlayClasses(self,clsList):
		if self.event_objectID==winUser.OBJID_CLIENT and JABHandler.isJavaWindow(self.windowHandle): 
			clsList.append(JavaVMRoot)

		windowClassName=self.windowClassName
		role=self.IAccessibleRole

		if self.role in (controlTypes.Role.APPLICATION, controlTypes.Role.DIALOG) and not self.isFocusable:
			# Make unfocusable applications focusable.
			# This is particularly useful for ARIA applications.
			# We use the NVDAObject role instead of IAccessible role here
			# because of higher API classes; e.g. MSHTML.
			clsList.insert(0, FocusableUnfocusableContainer)

		if hasattr(self, "IAccessibleTextObject"):
			if role==oleacc.ROLE_SYSTEM_TEXT or controlTypes.State.EDITABLE in self.states:
				clsList.append(EditableTextWithAutoSelectDetection)

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
				# #8712: Python 3 wants a dot (.) when loading a module from the same folder via relative imports, and this is done via package argument.
				mod=importlib.import_module("NVDAObjects.IAccessible.%s"%modString, package="NVDAObjects.IAccessible")
				newCls=getattr(mod,classString)
			elif classString:
				newCls=globals()[classString]
			if newCls:
				clsList.append(newCls)

		# Some special cases.
		if windowClassName=="Frame Notification Bar" and role==oleacc.ROLE_SYSTEM_CLIENT:
			clsList.append(IEFrameNotificationBar)
		elif self.event_objectID==winUser.OBJID_CLIENT and self.event_childID==0 and windowClassName=="_WwG":
			from .winword import WordDocument 
			clsList.append(WordDocument)
		elif self.event_objectID==winUser.OBJID_CLIENT and self.event_childID==0 and windowClassName in ("_WwN","_WwO"):
			if self.windowControlID==18:
				from .winword import SpellCheckErrorField
				clsList.append(SpellCheckErrorField)
			else:
				from .winword import WordDocument_WwN
				clsList.append(WordDocument_WwN)
		elif windowClassName=="DirectUIHWND" and role==oleacc.ROLE_SYSTEM_TOOLBAR:
			parentWindow=winUser.getAncestor(self.windowHandle,winUser.GA_PARENT)
			if parentWindow and winUser.getClassName(parentWindow)=="Frame Notification Bar":
				clsList.append(IENotificationBar)
		if (
			windowClassName.lower().startswith('mscandui')
			or windowClassName in (
				"Microsoft.IME.CandidateWindow.View",
				"Microsoft.IME.UIManager.CandidateWindow.Host"
		)):
			from . import mscandui
			mscandui.findExtraOverlayClasses(self,clsList)
		elif windowClassName=="GeckoPluginWindow" and self.event_objectID==0 and self.IAccessibleChildID==0:
			from .mozilla import GeckoPluginWindowRoot
			clsList.append(GeckoPluginWindowRoot)
		elif windowClassName.startswith('Mozilla'):
			from . import mozilla
			mozilla.findExtraOverlayClasses(self, clsList)
		elif(
			self.event_objectID in (None, winUser.OBJID_CLIENT, MSO_COLLECT_AND_PASTE_OBJECT_ID)
			and windowClassName.startswith('bosa_sdm')
		):
			if role==oleacc.ROLE_SYSTEM_GRAPHIC and controlTypes.State.FOCUSED in self.states:
				from .msOffice import SDMSymbols
				clsList.append(SDMSymbols)
			else:
				from .msOffice import SDM
				clsList.append(SDM)
		elif windowClassName == "DirectUIHWND" and role == oleacc.ROLE_SYSTEM_TEXT:
			from NVDAObjects.window import DisplayModelEditableText
			clsList.append(DisplayModelEditableText)
		elif windowClassName in ("ListBox","ComboLBox")  and role == oleacc.ROLE_SYSTEM_LISTITEM:
			windowStyle = self.windowStyle
			if (windowStyle & winUser.LBS_OWNERDRAWFIXED or windowStyle & winUser.LBS_OWNERDRAWVARIABLE) and not windowStyle & winUser.LBS_HASSTRINGS:
				# This is an owner drawn ListBox and text has not been set for the items.
				# See http://msdn.microsoft.com/en-us/library/ms971352.aspx#msaa_sa_listbxcntrls
				clsList.append(InaccessibleListBoxItem)
		elif windowClassName == "ComboBox" and role == oleacc.ROLE_SYSTEM_COMBOBOX:
			windowStyle = self.windowStyle
			if (windowStyle & winUser.CBS_OWNERDRAWFIXED or windowStyle & winUser.CBS_OWNERDRAWVARIABLE) and not windowStyle & winUser.CBS_HASSTRINGS:
				# This is an owner drawn ComboBox and text has not been set for the items.
				# See http://msdn.microsoft.com/en-us/library/ms971352.aspx#msaa_sa_listbxcntrls
				clsList.append(InaccessibleComboBox)
		elif windowClassName == "MsoCommandBar":
			from .msOffice import BrokenMsoCommandBar
			if BrokenMsoCommandBar.appliesTo(self):
				clsList.append(BrokenMsoCommandBar)
			if role==oleacc.ROLE_SYSTEM_TOOLBAR:
				from .msOffice import MsoCommandBarToolBar
				clsList.append(MsoCommandBarToolBar)
		if windowClassName.startswith("Internet Explorer_"):
			from . import MSHTML
			MSHTML.findExtraIAccessibleOverlayClasses(self, clsList)
		elif windowClassName in ("AVL_AVView", "FoxitDocWnd"):
			from . import adobeAcrobat
			adobeAcrobat.findExtraOverlayClasses(self, clsList)
		elif windowClassName == "WebViewWindowClass":
			from . import webKit
			webKit.findExtraOverlayClasses(self, clsList)
		elif windowClassName.startswith("Chrome_"):
			from . import chromium
			chromium.findExtraOverlayClasses(self, clsList)
		if (
			windowClassName == "ConsoleWindowClass"
			and role == oleacc.ROLE_SYSTEM_CLIENT
		):
			from . import winConsole
			winConsole.findExtraOverlayClasses(self,clsList)


		#Support for Windowless richEdit
		if not hasattr(IAccessible,"IID_ITextServices"):
			try:
				IAccessible.IID_ITextServices=ctypes.cast(ctypes.windll.msftedit.IID_ITextServices,ctypes.POINTER(GUID)).contents
			except WindowsError:
				log.debugWarning("msftedit not available, couldn't retrieve IID_ITextServices")
				IAccessible.IID_ITextServices=None
		if IAccessible.IID_ITextServices:
			try:
				pDoc=self.IAccessibleObject.QueryInterface(IServiceProvider).QueryService(IAccessible.IID_ITextServices,ITextDocument)
			except COMError:
				pDoc=None
			if pDoc:
				self._ITextDocumentObject=pDoc
				self.editAPIVersion=2
				from NVDAObjects.window.edit import Edit
				clsList.append(Edit)

		#Window root IAccessibles
		if self.event_childID==0 and self.IAccessibleRole==oleacc.ROLE_SYSTEM_WINDOW:
			clsList.append(WindowRoot if self.event_objectID==winUser.OBJID_WINDOW else GenericWindow)

		if self.event_objectID==winUser.OBJID_TITLEBAR and self.event_childID==0:
			clsList.append(Titlebar)

		clsList.append(IAccessible)

		if(
			self.event_objectID == winUser.OBJID_CLIENT
			and self.event_childID == 0
			and not isinstance(self.IAccessibleObject, IA2.IAccessible2)
		):
			# This is the main (client) area of the window, so we can use other classes at the window level.
			# #3872: However, don't do this for IAccessible2 because
			# IA2 supersedes window level APIs and might conflict with them.
			super(IAccessible,self).findOverlayClasses(clsList)
			#Generic client IAccessibles with no children should be classed as content and should use displayModel 
			if clsList[0]==IAccessible and len(clsList)==3 and self.IAccessibleRole==oleacc.ROLE_SYSTEM_CLIENT and self.childCount==0:
				clsList.insert(0,ContentGenericClient)

	# C901: 'IAccessible.__init__' is too complex
	def __init__(  # noqa: C901
			self,
			windowHandle: Optional[int] = None,
			IAccessibleObject: Optional[Union[IUnknown, IA.IAccessible, IA2.IAccessible2]] = None,
			IAccessibleChildID: Optional[int] = None,
			event_windowHandle: Optional = None,
			event_objectID: Optional = None,
			event_childID: Optional = None
	):
		"""
		@param windowHandle: the window handle, if known
		@param IAccessibleChildID: A child ID that will be used on all methods of the IAccessible pointer
		"""
		self.IAccessibleObject=IAccessibleObject
		self.IAccessibleChildID=IAccessibleChildID

		# Try every trick in the book to get the window handle if we don't have it.
		if not windowHandle and isinstance(IAccessibleObject, IA2.IAccessible2):
			windowHandle=self.IA2WindowHandle
		try:
			Identity=IAccessibleHandler.getIAccIdentity(IAccessibleObject,IAccessibleChildID)
		except COMError:
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
			try:
				left,top,width,height = IAccessibleObject.accLocation(0)
				windowHandle=winUser.user32.WindowFromPoint(winUser.POINT(left,top))
			except COMError as e:
				log.debugWarning("accLocation failed: %s" % e)
		if not windowHandle:
			raise InvalidNVDAObject("Can't get a window handle from IAccessible")

		if isinstance(IAccessibleObject, IA2.IAccessible2):
			try:
				self.IA2UniqueID=IAccessibleObject.uniqueID
			except COMError:
				log.debugWarning("could not get IAccessible2::uniqueID to use as IA2UniqueID",exc_info=True)

		# Set the event params based on our calculated/construction info if we must.
		if event_windowHandle is None:
			event_windowHandle=windowHandle
		if event_objectID is None and isinstance(IAccessibleObject, IA2.IAccessible2):
			event_objectID=winUser.OBJID_CLIENT
		if event_childID is None:
			if self.IA2UniqueID is not None:
				event_childID=self.IA2UniqueID
			else:
				event_childID=IAccessibleChildID

		self.event_windowHandle=event_windowHandle
		self.event_objectID=event_objectID
		self.event_childID=event_childID
		super(IAccessible,self).__init__(windowHandle=windowHandle)

		try:
			self.IAccessibleActionObject = IAccessibleObject.QueryInterface(IA2.IAccessibleAction)
		except COMError:
			pass
		try:
			self.IAccessibleTable2Object = self.IAccessibleObject.QueryInterface(IA2.IAccessibleTable2)
		except COMError:
			try:
				self.IAccessibleTableObject = self.IAccessibleObject.QueryInterface(IA2.IAccessibleTable)
			except COMError:
				pass
		try:
			self.IAccessibleTextObject = IAccessibleObject.QueryInterface(IA2.IAccessibleText)
		except COMError:
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
		#this object or one of its ancestors must have State.FOCUSED.
		testObj = self
		while testObj:
			if controlTypes.State.FOCUSED in testObj.states:
				break
			parent = testObj.parent
			# Cache the parent.
			testObj.parent = parent
			testObj = parent
		else:
			return False
		return True

	def _get_shouldAllowIAccessibleMenuStartEvent(self) -> bool:
		"""Determine whether an IAccessible menu start or menu popup start event should be allowed
		for this object.
		@return: C{True} if the event should be allowed.
		"""
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
		if (
			isinstance(self.IAccessibleObject, IA2.IAccessible2)
			and isinstance(other.IAccessibleObject, IA2.IAccessible2)
		):
			# These are both IAccessible2 objects, so we can test unique ID.
			# Unique ID is only guaranteed to be unique within a given window, so we must check window handle as well.
			selfIA2Window=self.IA2WindowHandle
			selfIA2ID=self.IA2UniqueID
			otherIA2Window=other.IA2WindowHandle
			otherIA2ID=other.IA2UniqueID
			if selfIA2Window!=otherIA2Window:
				# The window handles are different, so these are definitely different windows.
				return False
			# At this point, we know that the window handles are equal.
			if selfIA2Window and (selfIA2ID or otherIA2ID):
				# The window handles are valid and one of the objects has a valid unique ID.
				# Therefore, we can safely determine equality or inequality based on unique ID.
				return selfIA2ID==otherIA2ID
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
		if self.role==controlTypes.Role.EDITABLETEXT:
			# Make sure to cache the parents.
			parent=self.parent=self.parent
			if parent and parent.role==controlTypes.Role.WINDOW:
				# The parent of the edit field is a window, so try the next ancestor.
				parent=self.parent.parent=self.parent.parent
			# Only scrap the label on the edit field if the parent combo box has a label.
			if parent and parent.role==controlTypes.Role.COMBOBOX and parent.name:
				return ""

		try:
			res=self.IAccessibleObject.accName(self.IAccessibleChildID)
		except COMError:
			res=None
		return res if isinstance(res,str) and not res.isspace() else None

	def _get_value(self):
		try:
			res=self.IAccessibleObject.accValue(self.IAccessibleChildID)
		except COMError:
			res=None
		return res if isinstance(res,str) and not res.isspace() else None

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
				if self.IAccessibleObject.accDoDefaultAction(self.IAccessibleChildID)!=0:
					raise NotImplementedError
				return
			except COMError:
				raise NotImplementedError
		raise NotImplementedError

	def _get_IAccessibleIdentity(self):
		if not hasattr(self,'_IAccessibleIdentity'):
			try:
				self._IAccessibleIdentity=IAccessibleHandler.getIAccIdentity(self.IAccessibleObject,self.IAccessibleChildID)
			except COMError:
				self._IAccessibleIdentity=None
		return self._IAccessibleIdentity

	IAccessibleRole: int
	"""Type definition for auto prop '_get_IAccessibleRole'
	"""

	def _get_IAccessibleRole(self) -> int:
		if isinstance(self.IAccessibleObject, IA2.IAccessible2):
			try:
				role=self.IAccessibleObject.role()
			except COMError:
				role=0
		else:
			role=0
		if role==0:
			try:
				role=self.IAccessibleObject.accRole(self.IAccessibleChildID)
			except COMError as e:
				log.debugWarning("accRole failed: %s" % e)
				role=0
		return role

	def _get_role(self):
		IARole=self.IAccessibleRole
		if IARole==oleacc.ROLE_SYSTEM_CLIENT:
			superRole=super(IAccessible,self).role
			if superRole!=controlTypes.Role.WINDOW:
					return superRole
		if isinstance(IARole, str):  # todo: when can this be a string?
			IARole=IARole.split(',')[0].lower()
			log.debug("IARole: %s"%IARole)
		# must not create interdependence between role and states properties. Use IARole / IAStates.
		NVDARole = IAccessibleHandler.calculateNvdaRole(IARole, self.IAccessibleStates)
		return NVDARole
	# #2569: Don't cache role,
	# as it relies on other properties which might change when overlay classes are applied.
	_cache_role = False

	IAccessibleStates: int
	"""Type info for auto property: _get_IAccessibleStates
	"""

	def _get_IAccessibleStates(self) -> int:
		try:
			res=self.IAccessibleObject.accState(self.IAccessibleChildID)
		except COMError:
			return 0
		return res if isinstance(res,int) else 0

	states: typing.Set[controlTypes.State]
	"""Type info for auto property: _get_states
	"""

	# C901 '_get_states' is too complex. Look for opportunities to break this method down.
	def _get_states(self) -> typing.Set[controlTypes.State]:  # noqa: C901
		states=set()
		if self.event_objectID in (winUser.OBJID_CLIENT, winUser.OBJID_WINDOW) and self.event_childID == 0:
			states.update(super(IAccessible, self).states)
		try:
			IAccessibleStates=self.IAccessibleStates
		except COMError:
			log.debugWarning("could not get IAccessible states",exc_info=True)
		else:
			states.update(
				IAccessibleHandler.calculateNvdaStates(self.IAccessibleRole, IAccessibleStates)
			)

		if not isinstance(self.IAccessibleObject, IA2.IAccessible2):
			# Not an IA2 object.
			return states
		IAccessible2States = self.IA2States
		states |= IAccessibleHandler.getStatesSetFromIAccessible2States(IAccessible2States)

		# Readonly should override editable
		if controlTypes.State.READONLY in states:
			states.discard(controlTypes.State.EDITABLE)
		try:
			IA2Attribs=self.IA2Attributes
		except COMError:
			log.debugWarning("could not get IAccessible2 attributes",exc_info=True)
			IA2Attribs=None
		if IA2Attribs:
			grabbed = IA2Attribs.get("grabbed")
			if grabbed == "false":
				states.add(controlTypes.State.DRAGGABLE)
			elif grabbed == "true":
				states.add(controlTypes.State.DRAGGING)
			if IA2Attribs.get("dropeffect", "none") != "none":
				states.add(controlTypes.State.DROPTARGET)
			sorted = IA2Attribs.get("sort")
			if sorted=="ascending":
				states.add(controlTypes.State.SORTED_ASCENDING)
			elif sorted=="descending":
				states.add(controlTypes.State.SORTED_DESCENDING)
			elif sorted=="other":
				states.add(controlTypes.State.SORTED)
		if controlTypes.State.HASPOPUP in states and controlTypes.State.AUTOCOMPLETE in states:
			states.remove(controlTypes.State.HASPOPUP)
		if controlTypes.State.HALFCHECKED in states:
			states.discard(controlTypes.State.CHECKED)
		return states

	re_positionInfoEncodedAccDescription=re.compile(r"L(?P<level>\d+)(?:, (?P<indexInGroup>\d+) of (?P<similarItemsInGroup>\d+))?")

	def _get_decodedAccDescription(self):
		try:
			description=self.IAccessibleObject.accDescription(self.IAccessibleChildID)
		except COMError:
			return None
		if not description:
			return None
		if description.lower().startswith('description:'):
			return description[12:].strip()
		m=self.re_positionInfoEncodedAccDescription.match(description)
		if m:
			return m
		return description

	hasEncodedAccDescription=False #:If true, accDescription contains info such as level, and number of items etc.

	def _get_description(self):
		if self.hasEncodedAccDescription:
			d=self.decodedAccDescription
			if isinstance(d,str):
				return d
			else:
				return ""
		try:
			res=self.IAccessibleObject.accDescription(self.IAccessibleChildID)
		except COMError:
			res=None
		return res if isinstance(res,str) and not res.isspace() else None

	def _get_keyboardShortcut(self):
		try:
			res=self.IAccessibleObject.accKeyboardShortcut(self.IAccessibleChildID)
		except COMError:
			res=None
		return res if isinstance(res,str) and not res.isspace() else None

	def _get_childCount(self):
		if self.IAccessibleChildID!=0:
			return 0
		try:
			return max(self.IAccessibleObject.accChildCount,0)
		except COMError:
			return 0

	def _get_location(self):
		try:
			return RectLTWH(*self.IAccessibleObject.accLocation(self.IAccessibleChildID))
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
		except COMError:
			return None

	def _get_parent(self):
		if self.IAccessibleChildID!=0:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=0,event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=0) or super(IAccessible,self).parent
		res=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
		if res:
			parentObj=IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
			if parentObj:
				#Hack around bad MSAA implementations that deliberately skip the window root IAccessible in the ancestry (Skype, iTunes)
				if parentObj.windowHandle!=self.windowHandle and self.IAccessibleRole!=oleacc.ROLE_SYSTEM_WINDOW and winUser.getAncestor(self.windowHandle,winUser.GA_PARENT)==parentObj.windowHandle:
					windowObj=Window(windowHandle=self.windowHandle)
					if windowObj and isinstance(windowObj,IAccessible) and windowObj.IAccessibleRole==oleacc.ROLE_SYSTEM_WINDOW and windowObj.parent==parentObj:
						return windowObj
			return self.correctAPIForRelation(parentObj,relation="parent") or super(IAccessible,self).parent
		return super(IAccessible,self).parent

	def _get_next(self):
		res=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,oleacc.NAVDIR_NEXT)
		if not res:
			return None
		if res[0]==self.IAccessibleObject:
			#A sanity check for childIDs.
			if self.IAccessibleChildID>0 and res[1]>self.IAccessibleChildID:
				return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=res[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=res[1])
		else:
			return self.correctAPIForRelation(IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1]))

	def _get_previous(self):
		res=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,oleacc.NAVDIR_PREVIOUS)
		if not res:
			return None
		if res[0]==self.IAccessibleObject:
			#A sanity check for childIDs.
			if self.IAccessibleChildID>1 and res[1]<self.IAccessibleChildID:
				return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=res[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=res[1])
		else:
			return self.correctAPIForRelation(IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1]))

	def _get_firstChild(self):
		child=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,oleacc.NAVDIR_FIRSTCHILD)
		if not child and self.IAccessibleChildID==0:
			children=IAccessibleHandler.accessibleChildren(self.IAccessibleObject,0,1)
			if len(children)>0:
				child=children[0]
		if child and child[0]==self.IAccessibleObject:
			#A sanity check for childIDs.
			if self.IAccessibleChildID==0 and child[1]>0: 
				return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=child[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=child[1])
		elif child:
			obj=IAccessible(IAccessibleObject=child[0],IAccessibleChildID=child[1])
			if (obj and winUser.isDescendantWindow(self.windowHandle,obj.windowHandle)) or self.windowHandle==winUser.getDesktopWindow():
				return self.correctAPIForRelation(obj)

	def _get_lastChild(self):
		child=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,oleacc.NAVDIR_LASTCHILD)
		if not child and self.IAccessibleChildID==0:
			try:
				childCount=self.IAccessibleObject.accChildCount
			except COMError:
				childCount=0
			if childCount>0:
				children=IAccessibleHandler.accessibleChildren(self.IAccessibleObject,childCount-1,1)
				if len(children)>0:
					child=children[-1]
		if child and child[0]==self.IAccessibleObject:
			#A sanity check for childIDs.
			if self.IAccessibleChildID==0 and child[1]>0: 
				return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=child[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=child[1])
		elif child:
			obj=IAccessible(IAccessibleObject=child[0],IAccessibleChildID=child[1])
			if (obj and winUser.isDescendantWindow(self.windowHandle,obj.windowHandle)) or self.windowHandle==winUser.getDesktopWindow():
				return self.correctAPIForRelation(obj)

	def _get_children(self):
		if self.IAccessibleChildID!=0:
			return []
		try:
			childCount= self.IAccessibleObject.accChildCount
		except COMError:
			childCount=0
		if childCount<=0:
			return []
		children=[]
		for IAccessibleObject,IAccessibleChildID in IAccessibleHandler.accessibleChildren(self.IAccessibleObject,0,childCount):
			if IAccessibleObject==self.IAccessibleObject:
				children.append(IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=IAccessibleChildID,event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=IAccessibleChildID))
				continue
			try:
				identity=IAccessibleHandler.getIAccIdentity(IAccessibleObject,0)
			except COMError:
				identity=None
			#For Window root IAccessibles, we just want to use the new window handle, but use the best API for that window, rather than IAccessible
			#If it does happen to be IAccessible though, we only want the client, not the window root IAccessible
			if identity and identity.get('objectID',None)==0 and identity.get('childID',None)==0:
				windowHandle=identity.get('windowHandle',None)
				if windowHandle:
					kwargs=dict(windowHandle=windowHandle)
					APIClass=Window.findBestAPIClass(kwargs,relation="parent") #Need a better relation type for this, but parent works ok -- gives the client
					children.append(APIClass(**kwargs))
					continue
			children.append(IAccessible(IAccessibleObject=IAccessibleObject,IAccessibleChildID=IAccessibleChildID))
		children=[x for x in children if x and winUser.isDescendantWindow(self.windowHandle,x.windowHandle)]
		return children

	def getChild(self, index):
		if self.IAccessibleChildID != 0:
			return None
		child = IAccessibleHandler.accChild(self.IAccessibleObject, index + 1)
		if not child:
			if index < self.childCount:
				return super(IAccessible, self).getChild(index)
			return None
		if child[0] == self.IAccessibleObject:
			return IAccessible(windowHandle=self.windowHandle, IAccessibleObject=self.IAccessibleObject, IAccessibleChildID=child[1],
				event_windowHandle=self.event_windowHandle, event_objectID=self.event_objectID, event_childID=child[1])
		return self.correctAPIForRelation(IAccessible(IAccessibleObject=child[0], IAccessibleChildID=child[1]))

	#: Type definition for auto prop '_get_IA2Attributes'
	IA2Attributes: typing.Dict[str, str]

	def _get_IA2Attributes(self) -> typing.Dict[str, str]:
		if not isinstance(self.IAccessibleObject, IA2.IAccessible2):
			return {}
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
		tableCell=self._IATableCell
		if tableCell:
			return tableCell.rowIndex+1
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

	def _get_presentationalRowNumber(self):
		index=self.IA2Attributes.get('rowindex')
		if index is None and isinstance(self.parent,IAccessible):
			index=self.parent.IA2Attributes.get('rowindex')
		if index is None:
			raise NotImplementedError
		try:
			index=int(index)
		except (ValueError,TypeError):
			log.debugWarning("value %s is not an int"%index,exc_info=True)
			raise NotImplementedError
		return index

	def _get_rowSpan(self):
		if self._IATableCell:
			return self._IATableCell.rowExtent
		raise NotImplementedError

	def _get_columnNumber(self):
		tableCell=self._IATableCell
		if tableCell:
			return tableCell.columnIndex+1
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

	def _get_cellCoordsText(self):
		colText=self.IA2Attributes.get('coltext')
		rowText=self.IA2Attributes.get('rowtext')
		if rowText is None and isinstance(self.parent,IAccessible):
			rowText=self.parent.IA2Attributes.get('rowtext')
		if not rowText and not colText:
			return
		if not colText:
			colText=self.columnNumber
		if not rowText:
			rowText=self.rowNumber
		return "%s %s"%(colText,rowText)

	def _get_presentationalColumnNumber(self):
		index=self.IA2Attributes.get('colindex')
		if index is None:
			raise NotImplementedError
		try:
			index=int(index)
		except (ValueError,TypeError):
			log.debugWarning("value %s is not an int"%index,exc_info=True)
			raise NotImplementedError
		return index

	def _get_columnSpan(self):
		if self._IATableCell:
			return self._IATableCell.columnExtent
		raise NotImplementedError

	def _get_rowCount(self):
		if hasattr(self,'IAccessibleTable2Object'):
			try:
				return self.IAccessibleTable2Object.nRows
			except COMError:
				log.debugWarning("IAccessibleTable2::nRows failed", exc_info=True)
		if hasattr(self,'IAccessibleTableObject'):
			try:
				return self.IAccessibleTableObject.nRows
			except COMError:
				log.debugWarning("IAccessibleTable::nRows failed", exc_info=True)
		raise NotImplementedError

	def _get_presentationalRowCount(self):
		count=self.IA2Attributes.get('rowcount')
		if count is None:
			raise NotImplementedError
		try:
			count=int(count)
		except (ValueError,TypeError):
			log.debugWarning("value %s is not an int"%count,exc_info=True)
			raise NotImplementedError
		return count

	def _get_columnCount(self):
		if hasattr(self,'IAccessibleTable2Object'):
			try:
				return self.IAccessibleTable2Object.nColumns
			except COMError:
				log.debugWarning("IAccessibleTable2::nColumns failed", exc_info=True)
		if hasattr(self,'IAccessibleTableObject'):
			try:
				return self.IAccessibleTableObject.nColumns
			except COMError:
				log.debugWarning("IAccessibleTable::nColumns failed", exc_info=True)
		raise NotImplementedError

	def _get_presentationalColumnCount(self):
		count=self.IA2Attributes.get('colcount')
		if count is None:
			raise NotImplementedError
		try:
			count=int(count)
		except (ValueError,TypeError):
			log.debugWarning("value %s is not an int"%count,exc_info=True)
			raise NotImplementedError
		return count

	def _get__IATableCell(self):
		# Permanently cache the result.
		try:
			self._IATableCell = self.IAccessibleObject.QueryInterface(IA2.IAccessibleTableCell)
		except COMError:
			self._IATableCell = None
		return self._IATableCell

	def _tableHeaderTextHelper(self, axis):
		cell = self._IATableCell
		if not cell:
			return None
		try:
			headers, nHeaders = getattr(cell, axis + "HeaderCells")
		except COMError:
			return None
		if not headers:
			return None
		try:
			ret = []
			# Each header must be fetched from the headers array once and only once,
			# as it gets released when it gets garbage collected.
			for i in range(nHeaders):
				try:
					text = headers[i].QueryInterface(IA2.IAccessible2).accName(0)
				except COMError:
					continue
				if not text:
					continue
				ret.append(text)
			return "\n".join(ret)
		finally:
			ctypes.windll.ole32.CoTaskMemFree(headers)

	def _get_rowHeaderText(self):
		return self._tableHeaderTextHelper("row")

	def _get_columnHeaderText(self):
		return self._tableHeaderTextHelper("column")

	def _get_selectionContainer(self):
		if self.table:
			return self.table
		return super(IAccessible,self).selectionContainer

	def _getSelectedItemsCount_accSelection(self, maxCount: int) -> int:
		sel=self.IAccessibleObject.accSelection
		if not sel:
			raise NotImplementedError
		# accSelection can return a child ID of a simple element, for instance in QT tree tables. 
		# Therefore treat this as a single selection unless the child ID is CHILDID_SELF (0).
		if isinstance(sel, int) and sel != 0:
			return 1
		# accSelection can return IDispatch for a single selected child object
		if isinstance(sel, comtypes.client.dynamic._Dispatch):
			return 1
		enumObj=sel.QueryInterface(IEnumVARIANT)
		if not enumObj:
			raise NotImplementedError
		# Some implementations of accSelection (e.g. in Symphony based products) don't return
		# a fresh IEnumVARIANT. Reset it to ensure we enumerate from the start.
		enumObj.Reset()
		# Call the rawmethod for IEnumVARIANT::Next as COMTypes' overloaded version does not allow limiting the amount of items returned
		numItemsFetched=ctypes.c_ulong()
		itemsBuf=(VARIANT*(maxCount+1))()
		res=enumObj._IEnumVARIANT__com_Next(maxCount,itemsBuf,ctypes.byref(numItemsFetched))
		# IEnumVARIANT returns S_FALSE  if the buffer is too small, although it still writes as many as it can.
		# For our purposes, we can treat both S_OK and S_FALSE as success.
		if res!=S_OK and res!=S_FALSE:
			raise COMError(res,None,None)
		return numItemsFetched.value if numItemsFetched.value <= maxCount else sys.maxsize

	def getSelectedItemsCount(self, maxCount=2):
		# To fetch the number of selected items, we first try MSAA's accSelection,
		# but if that fails in any way, we fall back to using IAccessibleTable2's nSelectedCells,
		# if we are on an IAccessible2 table, or IAccessibleTable's nSelectedChildren,
		# if we are on an IAccessible table.
		# Currently Chrome does not implement accSelection, thus for Google Sheets we must use nSelectedCells when on a table.
		# For older symphony based products, we use nSelectedChildren.
		try:
			return self._getSelectedItemsCount_accSelection(maxCount)
		except (COMError,NotImplementedError) as e:
			log.debug("Cannot fetch selected items count using accSelection, %s"%e)
			pass
		if hasattr(self, 'IAccessibleTable2Object'):
			try:
				return self.IAccessibleTable2Object.nSelectedCells
			except COMError as e:
				log.debug(f"Error calling IAccessibleTable2::nSelectedCells, {e}")
			pass
		elif hasattr(self, 'IAccessibleTableObject'):
			try:
				return self.IAccessibleTableObject.nSelectedChildren
			except COMError as e:
				log.debug(f"Error calling IAccessibleTable::nSelectedCells, {e}")
			pass
		else:
			log.debug("No means of getting a selection count from this IAccessible")
		return super().getSelectedItemsCount(maxCount)

	def _get_table(self):
		if not isinstance(self.IAccessibleObject, IA2.IAccessible2):
			return None
		table=getattr(self,'_table',None)
		if table:
			return table
		checkAncestors=False
		if self.IAccessibleTableUsesTableCellIndexAttrib and "table-cell-index" in self.IA2Attributes:
			checkAncestors=True
		obj=self.parent
		while checkAncestors and obj and not hasattr(obj,'IAccessibleTable2Object') and not hasattr(obj,'IAccessibleTableObject'):
			parent=obj.parent=obj.parent
			obj=parent
		if not obj or (not hasattr(obj,'IAccessibleTable2Object') and not hasattr(obj,'IAccessibleTableObject')):
			return None
		self._table=obj
		return obj

	def _get_tableID(self):
		table = self.table
		if not table:
			return super(IAccessible, self).tableID
		return (self.windowHandle, self.table.IA2UniqueID)

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
		except COMError:
			pass

	def scrollIntoView(self):
		if isinstance(self.IAccessibleObject, IA2.IAccessible2):
			try:
				self.IAccessibleObject.scrollTo(IA2.IA2_SCROLL_TYPE_ANYWHERE)
			except COMError:
				log.debugWarning("IAccessible2::scrollTo failed", exc_info=True)

	def _get_allowIAccessibleChildIDAndChildCountForPositionInfo(self):
		"""if true position info should fall back to using the childID and the parent's accChildCount for position information if there is nothing better available."""
		return config.conf["presentation"]["guessObjectPositionInformationWhenUnavailable"]

	def _get_positionInfo(self):
		if isinstance(self.IAccessibleObject, IA2.IAccessible2):
			try:
				info={}
				info["level"],info["similarItemsInGroup"],info["indexInGroup"]=self.IAccessibleObject.groupPosition
				# Object's with an IAccessibleTableCell interface should not expose indexInGroup/similarItemsInGroup as the cell's 2d info is much more useful.
				if self._IATableCell:
					del info['indexInGroup']
					del info['similarItemsInGroup']
				# 0 means not applicable, so remove it.
				# Wrap the call of items inside a list call, as the dictionary changes during iteration.
				for key, val in list(info.items()):
					if not val:
						del info[key]
				return info
			except COMError:
				pass
		if self.hasEncodedAccDescription:
			d=self.decodedAccDescription
			if d and not isinstance(d,str):
				groupdict=d.groupdict()
				return {x:int(y) for x,y in groupdict.items() if y is not None}
		if self.allowIAccessibleChildIDAndChildCountForPositionInfo and self.IAccessibleChildID>0:
			indexInGroup=self.IAccessibleChildID
			parent=self.parent
			if parent:
				similarItemsInGroup=parent.childCount
				return dict(indexInGroup=indexInGroup,similarItemsInGroup=similarItemsInGroup)
		return {}

	def _get_indexInParent(self):
		if isinstance(self.IAccessibleObject, IA2.IAccessible2):
			try:
				return self.IAccessibleObject.indexInParent
			except COMError:
				pass
		raise NotImplementedError

	#: Type definition for auto prop '_get__IA2Relations'
	_IA2Relations: typing.List[IA2.IAccessibleRelation]

	def _get__IA2Relations(self) -> typing.List[IA2.IAccessibleRelation]:
		if not isinstance(self.IAccessibleObject, IA2.IAccessible2):
			log.debug("Not an IA2.IAccessible2")
			raise NotImplementedError
		import ctypes
		import comtypes.hresult
		try:
			size = self.IAccessibleObject.nRelations
		except COMError:
			log.debug("Unable to get nRelations")
			raise NotImplementedError
		if size <= 0:
			return list()
		relations = (ctypes.POINTER(IA2.IAccessibleRelation) * size)()
		count = ctypes.c_int()
		# The client allocated relations array is an [out] parameter instead of [in, out], so we need to use the raw COM method.
		res = self.IAccessibleObject._IAccessible2__com__get_relations(size, relations, ctypes.byref(count))
		if res != comtypes.hresult.S_OK:
			log.debug("Unable to get relations")
			raise NotImplementedError
		return list(relations)

	def _getIA2TargetsForRelationsOfType(
			self,
			relationType: "IAccessibleHandler.RelationType",
			maxRelations: int = 1,
	) -> typing.List[IUnknown]:
		"""Gets the target IAccessible (actually IUnknown; use QueryInterface or
		normalizeIAccessible to resolve) for the relations with given type.
		Allows escape of exception: COMError(-2147417836, 'Requested object does not exist.'),
		callers should handle this, for this reason consider using _getIA2RelationFirstTarget
		if only the first target is required, and you wish the target to be converted to an IAccessible
		"""
		acc = self.IAccessibleObject
		if not isinstance(acc, IA2.IAccessible2):
			raise NotImplementedError
		if not isinstance(relationType, IAccessibleHandler.RelationType):
			raise NotImplementedError
		if 1 > maxRelations:
			raise ValueError
		if not isinstance(acc, IA2.IAccessible2_2):
			acc = acc.QueryInterface(IA2.IAccessible2_2)
		targets, count = acc.relationTargetsOfType(
			relationType.value,
			maxRelations
		)
		if count == 0:
			return list()
		relationsGen = (
			targets[i]
			for i in range(min(maxRelations, count))
		)
		return list(relationsGen)

	def _getIA2RelationFirstTarget(
			self,
			relationType: typing.Union[str, "IAccessibleHandler.RelationType"]
	) -> typing.Optional["IAccessible"]:
		""" Get the first target for the relation of type.
		@param relationType: The type of relation to fetch.
		"""
		if not isinstance(relationType, IAccessibleHandler.RelationType):
			if isinstance(relationType, str):
				relationType = IAccessibleHandler.RelationType(relationType)
			else:
				raise TypeError(f"Bad type for 'relationType' arg, got: {type(relationType)}")

		relationType = typing.cast(IAccessibleHandler.RelationType, relationType)

		try:
			# rather than fetch all the relations and querying the type, do that in process for performance reasons
			targets = self._getIA2TargetsForRelationsOfType(relationType, maxRelations=1)
			if targets:
				ia2Object = IAccessibleHandler.normalizeIAccessible(targets[0])
				return IAccessible(
					IAccessibleObject=ia2Object,
					IAccessibleChildID=0
				)
		except (NotImplementedError, COMError):
			log.debugWarning("Unable to use _getIA2TargetsForRelationsOfType, fallback to _IA2Relations.")

		# eg IA2_2 is not available, fall back to old approach
		try:
			for relation in self._IA2Relations:
				if relation.relationType == relationType:
					# Take the first of 'relation.nTargets' see IAccessibleRelation._methods_
					target = relation.target(0)
					ia2Object = IAccessibleHandler.normalizeIAccessible(target)
					return IAccessible(
						IAccessibleObject=ia2Object,
						IAccessibleChildID=0
					)
		except (NotImplementedError, COMError):
			log.debug("Unable to fetch _IA2Relations", exc_info=True)
			pass
		return None

	#: Type definition for auto prop '_get_detailsRelations'
	detailsRelations: typing.Iterable["IAccessible"]

	def _get_detailsRelations(self) -> typing.Iterable["IAccessible"]:
		relationTarget = self._getIA2RelationFirstTarget(IAccessibleHandler.RelationType.DETAILS)
		if not relationTarget:
			return ()
		return (relationTarget, )

	#: Type definition for auto prop '_get_flowsTo'
	flowsTo: typing.Optional["IAccessible"]

	def _get_flowsTo(self) -> typing.Optional["IAccessible"]:
		return self._getIA2RelationFirstTarget(IAccessibleHandler.RelationType.FLOWS_TO)

	#: Type definition for auto prop '_get_flowsFrom'
	flowsFrom: typing.Optional["IAccessible"]

	def _get_flowsFrom(self) -> typing.Optional["IAccessible"]:
		return self._getIA2RelationFirstTarget(IAccessibleHandler.RelationType.FLOWS_FROM)

	def event_valueChange(self):
		if isinstance(self, EditableTextWithAutoSelectDetection):
			self.hasContentChangedSinceLastSelection = True
			return
		return super(IAccessible, self).event_valueChange()

	def event_alert(self):
		if self.role != controlTypes.Role.ALERT:
			# Ignore alert events on objects that aren't alerts.
			return
		if not self.name and not self.description and self.childCount == 0:
			# Don't report if there's no content.
			return
		# If the focus is within the alert object, don't report anything for it.
		if eventHandler.isPendingEvents("gainFocus"):
			# The alert event might be fired before the focus.
			api.processPendingEvents()
		if self in api.getFocusAncestors():
			return
		speech.speakObject(self, reason=controlTypes.OutputReason.FOCUS, priority=speech.Spri.NOW)
		for child in self.recursiveDescendants:
			if controlTypes.State.FOCUSABLE in child.states:
				speech.speakObject(child, reason=controlTypes.OutputReason.FOCUS, priority=speech.Spri.NOW)

	def event_caret(self):
		focus = api.getFocusObject()
		if self is not focus and hasattr(self, "IAccessibleTextObject"):
			import compoundDocuments
			if issubclass(focus.TextInfo, compoundDocuments.CompoundTextInfo) and self in focus:
				# This object is part of the focused compound text editor, so notify it.
				focus.event_caret()
				return
		super(IAccessible, self).event_caret()

	def _get_groupName(self):
		return None
		if self.IAccessibleChildID>0:
			return None
		else:
			return super(IAccessible,self)._get_groupName()

	def event_selection(self):
		return self.event_stateChange()

	def event_selectionAdd(self):
		return self.event_stateChange()

	def event_selectionRemove(self):
		return self.event_stateChange()

	def event_selectionWithIn(self):
		return self.event_stateChange()

	def _get_isPresentableFocusAncestor(self):
		IARole = self.IAccessibleRole
		# This is the root object of a top level window.
		# #4300: We check the object and child ids as well because there can be "clients" other than the root.
		if IARole == oleacc.ROLE_SYSTEM_CLIENT and self.event_objectID==winUser.OBJID_CLIENT and self.event_childID==0 and self.windowStyle & winUser.WS_SYSMENU:
			return True
		return super(IAccessible, self).isPresentableFocusAncestor

	def _get_devInfo(self):
		info = super(IAccessible, self).devInfo
		iaObj = self.IAccessibleObject
		info.append("IAccessibleObject: %r" % iaObj)
		childID = self.IAccessibleChildID
		info.append("IAccessibleChildID: %r" % childID)
		info.append("IAccessible event parameters: windowHandle=%r, objectID=%r, childID=%r" % (self.event_windowHandle, self.event_objectID, self.event_childID))
		formatLong = self._formatLongDevInfoString
		try:
			ret = formatLong(iaObj.accName(childID))
		except Exception as e:
			ret = "exception: %s" % e
		info.append("IAccessible accName: %s" % ret)
		try:
			ret = iaObj.accRole(childID)
			for name, const in oleacc.__dict__.items():
				if not name.startswith("ROLE_"):
					continue
				if ret == const:
					ret = name
					break
			else:
				ret = repr(ret)
		except Exception as e:
			ret = "exception: %s" % e
		info.append("IAccessible accRole: %s" % ret)
		try:
			temp = iaObj.accState(childID)
			ret = ", ".join(
				name for name, const in oleacc.__dict__.items()
				if name.startswith("STATE_") and temp & const
			) + " (%d)" % temp
		except Exception as e:
			ret = "exception: %s" % e
		info.append("IAccessible accState: %s" % ret)
		try:
			ret = formatLong(iaObj.accDescription(childID))
		except Exception as e:
			ret = "exception: %s" % e
		info.append("IAccessible accDescription: %s" % ret)
		try:
			ret = formatLong(iaObj.accValue(childID))
		except Exception as e:
			ret = "exception: %s" % e
		info.append("IAccessible accValue: %s" % ret)
		if isinstance(iaObj, IA2.IAccessible2):
			try:
				ret = iaObj.windowHandle
			except Exception as e:
				ret = "exception: %s" % e
			info.append("IAccessible2 windowHandle: %s" % ret)
			try:
				ret = iaObj.uniqueID
			except Exception as e:
				ret = "exception: %s" % e
			info.append("IAccessible2 uniqueID: %s" % ret)
			try:
				ret = iaObj.role()
				for name, const in itertools.chain(oleacc.__dict__.items(), IA2.__dict__.items()):
					if not name.startswith("ROLE_") and not name.startswith("IA2_ROLE_"):
						continue
					if ret == const:
						ret = name
						break
				else:
					ret = repr(ret)
			except Exception as e:
				ret = "exception: %s" % e
			info.append("IAccessible2 role: %s" % ret)
			try:
				temp = iaObj.states
				ret = ", ".join(
					name for name, const in IA2.__dict__.items()
					if name.startswith("IA2_STATE_") and temp & const
				) + " (%d)" % temp
			except Exception as e:
				ret = "exception: %s" % e
			info.append("IAccessible2 states: %s" % ret)
			try:
				ret = repr(iaObj.attributes)
			except Exception as e:
				ret = "exception: %s" % e
			info.append("IAccessible2 attributes: %s" % ret)
			try:
				ret = ", ".join(r.RelationType for r in self._IA2Relations)
			except Exception as e:
				ret = f"exception: {e}"
			info.append(f"IAccessible2 relations: {ret}")
		return info

	def _get_language(self):
		try:
			ia2Locale = self.IAccessibleObject.locale
		except (AttributeError, COMError):
			return None
		if ia2Locale.language and ia2Locale.country:
			return "%s_%s" % (ia2Locale.language, ia2Locale.country)
		elif ia2Locale.language:
			return ia2Locale.language
		return None

	def _get_iaHypertext(self):
		ht = self.IAccessibleTextObject.QueryInterface(IA2.IAccessibleHypertext)
		self.iaHypertext = ht # Cache forever.
		return ht

	def _get_IA2WindowHandle(self):
		window = None
		if isinstance(self.IAccessibleObject, IA2.IAccessible2):
			try:
				window = self.IAccessibleObject.windowHandle
			except COMError as e:
				log.debugWarning("IAccessible2::windowHandle failed: %s" % e)
		self.IA2WindowHandle = window # Cache forever.
		return window
	# We forceably cache this forever, so we don't need temporary caching.
	# Temporary caching breaks because the cache isn't initialised when this is first called.
	_cache_IA2WindowHandle = False

	IA2States: int
	"""Type info for auto property: _get_IA2States
	"""

	def _get_IA2States(self) -> int:
		if not isinstance(self.IAccessibleObject, IA2.IAccessible2):
			return 0
		try:
			return self.IAccessibleObject.states
		except COMError:
			log.debugWarning("could not get IAccessible2 states", exc_info=True)
			return IA2.IA2_STATE_DEFUNCT

	def __contains__(self, obj):
		if not isinstance(obj, IAccessible) or not isinstance(obj.IAccessibleObject, IA2.IAccessible2):
			return False
		try:
			self.IAccessibleObject.accChild(obj.IA2UniqueID)
			return True
		except COMError:
			return False

	def summarizeInProcess(self) -> str:
		"""Uses nvdaInProcUtils to get the text for an IAccessible.
		Can be used without a virtual buffer loaded.
		"""
		text = BSTR()
		log.debug("Calling nvdaInProcUtils_getTextFromIAccessible")
		res = NVDAHelper.localLib.nvdaInProcUtils_getTextFromIAccessible(
			# [in] handle_t bindingHandle
			self.appModule.helperLocalBindingHandle,
			# [in] const unsigned long hwnd
			self.windowHandle,
			# [in] long parentID
			self.IAccessibleObject.uniqueID,
			# // Params for getTextFromIAccessible
			# [out, string] BSTR* textBuf
			ctypes.byref(text),
			# [in, defaultvalue(TRUE)] const boolean recurse,
			True,
			# [in, defaultvalue(TRUE)] const boolean includeTopLevelText
			True,
		)
		if res != 0:
			log.error(f"Error calling nvdaInProcUtils_getTextFromIAccessible, res: {res}")
			raise ctypes.WinError(res)
		return text.value

class ContentGenericClient(IAccessible):

	TextInfo=displayModel.DisplayModelTextInfo
	presentationType=IAccessible.presType_content
	role=controlTypes.Role.UNKNOWN

	def _get_value(self):
		val=self.displayText
		truncate=len(val)>200
		if truncate:
			return u"%s\u2026"%val[:200]
		return val

class GenericWindow(IAccessible):

	TextInfo=displayModel.DisplayModelTextInfo
	isPresentableFocusAncestor=False

class WindowRoot(GenericWindow):

	parentUsesSuperOnWindowRootIAccessible=True #: on a window root IAccessible, super should be used instead of accParent

	@classmethod
	def windowHasExtraIAccessibles(cls,windowHandle):
		"""Finds out whether this window has things such as a system menu / titleBar / scroll bars, which would be represented as extra IAccessibles"""
		style=winUser.getWindowStyle(windowHandle)
		return bool(style&winUser.WS_SYSMENU)

	def _get_presentationType(self):
		states=self.states
		if controlTypes.State.INVISIBLE in states or controlTypes.State.UNAVAILABLE in states:
			return self.presType_unavailable
		if not self.windowHasExtraIAccessibles(self.windowHandle):
			return self.presType_layout
		return self.presType_content

	def _get_parent(self):
		if self.parentUsesSuperOnWindowRootIAccessible:
			return super(IAccessible,self).parent
		return super(WindowRoot,self).parent

	def _get_next(self):
		return super(IAccessible,self).next 

	def _get_previous(self):
		return super(IAccessible,self).previous

	def _get_container(self):
		#Support for groupbox windows
		groupboxObj=IAccessibleHandler.findGroupboxObject(self)
		if groupboxObj:
			return groupboxObj
		return super(WindowRoot,self).container

class ShellDocObjectView(IAccessible):

	def event_gainFocus(self):
		#Sometimes Shell DocObject View gets focus, when really the document inside it should
		#Adobe Reader 9 licence agreement
		if eventHandler.isPendingEvents("gainFocus") or self.childCount!=1:
			return super(ShellDocObjectView,self).event_gainFocus()
		child=self.firstChild
		if not child or child.windowClassName!="Internet Explorer_Server" or child.role!=controlTypes.Role.PANE:
			return super(ShellDocObjectView,self).event_gainFocus()
		child=child.firstChild
		if not child or child.windowClassName!="Internet Explorer_Server" or child.role!=controlTypes.Role.DOCUMENT:
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

class NUIDialogClient(Dialog):
	role=controlTypes.Role.DIALOG

class Groupbox(IAccessible):

	def _getNextSkipWindows(self, obj):
		res = obj.next
		if res:
			return res
		res = obj.parent
		if not res or res.role != controlTypes.Role.WINDOW:
			return None
		res = res.next
		if not res or res.role != controlTypes.Role.WINDOW:
			return None
		return res.firstChild

	def _get_description(self):
		next=self._getNextSkipWindows(self)
		if next and next.name==self.name and next.role==controlTypes.Role.GRAPHIC:
			next=self._getNextSkipWindows(next)
		if next and next.role==controlTypes.Role.STATICTEXT:
			nextNext=self._getNextSkipWindows(next)
			if nextNext and nextNext.name!=next.name:
				return next.name
		return super(Groupbox,self).description

	def _get_isPresentableFocusAncestor(self):
		# Only fetch this the first time it is requested,
		# as it is a bit slow due to the description property
		# and the answer shouldn't change anyway.
		self.isPresentableFocusAncestor = res = super(Groupbox, self).isPresentableFocusAncestor
		return res

CHAR_LTR_MARK = u'\u200E'
CHAR_RTL_MARK = u'\u200F'
class TrayClockWClass(IAccessible):
	"""
	Based on NVDAObject but the role is changed to clock.
	Depending on the version of Windows name or value contains left-to-right or right-to-left characters, so remove them from both.
	"""

	def _get_role(self):
		# On Windows 10 Anniversary update and later the text 'clock' is included in the name so having clock in the control type is redundant.
		if super(TrayClockWClass, self).value is None:
			return controlTypes.Role.BUTTON
		return controlTypes.Role.CLOCK

	def _get_name(self):
	# #4364 On some versions of Windows name contains redundant information that is available either in the role or the value, however on Windows 10 Anniversary Update and later the value is empty, so we cannot simply dismiss the name.
		if super(TrayClockWClass, self).value is None:
			clockName = super(TrayClockWClass, self).name
			return clockName.replace(CHAR_LTR_MARK,'').replace(CHAR_RTL_MARK,'')
		return None

	def _get_value(self):
		clockValue = super(TrayClockWClass, self).value
		if clockValue is not None:
			clockValue = clockValue.replace(CHAR_LTR_MARK,'').replace(CHAR_RTL_MARK,'')
		return clockValue

class OutlineItem(IAccessible):

	def _get_value(self):
		val=super(OutlineItem,self)._get_value()
		try:
			int(val)
		except (ValueError, TypeError):
			return val

class List(IAccessible):

	def _get_role(self):
		return controlTypes.Role.LIST

class SysLinkClient(IAccessible):

	def reportFocus(self):
		pass

	def _get_role(self):
		if self.childCount==0:
			return controlTypes.Role.LINK
		return super(SysLinkClient,self).role

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

	allowIAccessibleChildIDAndChildCountForPositionInfo=True

	def _get_role(self):
		return controlTypes.Role.ICON

	def reportFocus(self):
		if controlTypes.State.INVISIBLE in self.states:
			return
		super(TaskListIcon,self).reportFocus()

class MenuItem(IAccessible):

	def _get_description(self):
		name=self.name
		description=super(MenuItem,self)._get_description()
		if description!=name:
			return description
		else:
			return None

	def _get_name(self):
		return super(MenuItem,self).name or self.displayText

	def event_gainFocus(self):
		if eventHandler.isPendingEvents("gainFocus"):
			return
		super(MenuItem, self).event_gainFocus()

class Taskbar(IAccessible):
	name = _("Taskbar")

	def event_gainFocus(self):
		api.processPendingEvents(False)
		# Sometimes before Windows 7 start menu opens taskbar gains focus for a moment producing annoying speech.
		if eventHandler.isPendingEvents("gainFocus"):
			return
		super().event_gainFocus()

class Button(IAccessible):

	def _get_name(self):
		name=super(Button,self).name
		if not name or name.isspace():
			name=self.displayText
		return name

class InaccessibleListBoxItem(IAccessible):
	"""
	Used for list item IAccessibles in inaccessible owner drawn ListBox controls.
	Overrides name to use display model text as MSAA doesn't provide a suitable name (it's usually either empty or contains garbage).
	"""

	def _get_name(self):
		return self.displayText

class InaccessibleComboBox(IAccessible):
	"""
	Used for inaccessible owner drawn ComboBox controls.
	Overrides value  to use display model text as MSAA doesn't provide a suitable vale (it's usually either empty or contains garbage).
	"""

	def _get_value(self):
		return self.displayText

class StaticText(IAccessible):
	"""Support for owner-drawn staticText controls where accName is empty."""

	def _get_name(self):
		name=super(StaticText,self).name
		if not name or name.isspace():
				name=self.displayText
		return name


class Titlebar(IAccessible):
	"""A class for the standard MSAA titlebar, which shortcuts presentationType to be layout (for performance) and  makes the description property empty, as the standard accDescription is rather annoying."""

	presentationType=IAccessible.presType_layout

	def _get_description(self):
		return ""

class ReBarWindow32Client(IAccessible):
	"""
	The client IAccessible for a ReBarWindow32 window.
	Overrides firstChild/lastChild as accNavigate is not implemented, and IEnumVariant (children) gives back some strange buttons beside each child window with no accNavigate.
	"""

	def _get_firstChild(self):
		return super(IAccessible,self).firstChild

	def _get_lastChild(self):
		return super(IAccessible,self).lastChild

#A class for the listview window class, found sof ar only in the Cygwin Setup program.
#Makes sure its available in simple review mode, and uses display model
class ListviewPane(IAccessible):
	presentationType=IAccessible.presType_content
	role=controlTypes.Role.LIST
	TextInfo=displayModel.DisplayModelTextInfo
	name=""

class IEFrameNotificationBar(IAccessible):

	def event_show(self):
		child=self.simpleFirstChild
		if isinstance(child,Dialog):
			child.event_alert()

#The Internet Explorer notification toolbar should be handled as an alert
class IENotificationBar(Dialog,IAccessible):
	name=""
	role=controlTypes.Role.ALERT

	def event_alert(self):
		speech.cancelSpeech()
		speech.speakObject(self, reason=controlTypes.OutputReason.FOCUS)
		child=self.simpleFirstChild
		while child:
			if child.role!=controlTypes.Role.STATICTEXT:
				speech.speakObject(child, reason=controlTypes.OutputReason.FOCUS)
			child=child.simpleNext


class UIItem(IAccessible):
	"""List items in Windows Explorer repeat the name as the value"""

	def _get_value(self):
		return ""


###class mappings

_staticMap={
	("ReBarWindow32",oleacc.ROLE_SYSTEM_CLIENT):"ReBarWindow32Client",
	("Static",oleacc.ROLE_SYSTEM_STATICTEXT):"StaticText",
	("msctls_statusbar32",oleacc.ROLE_SYSTEM_STATICTEXT):"StaticText",
	(None,oleacc.ROLE_SYSTEM_PUSHBUTTON):"Button",
	("tooltips_class32",oleacc.ROLE_SYSTEM_TOOLTIP):"ToolTip",
	("tooltips_class32",oleacc.ROLE_SYSTEM_HELPBALLOON):"Notification",
	(None,oleacc.ROLE_SYSTEM_DIALOG):"Dialog",
	(None,oleacc.ROLE_SYSTEM_ALERT):"Dialog",
	(None,oleacc.ROLE_SYSTEM_PROPERTYPAGE):"Dialog",
	(None,oleacc.ROLE_SYSTEM_GROUPING):"Groupbox",
	("TrayClockWClass",oleacc.ROLE_SYSTEM_PUSHBUTTON):"TrayClockWClass",
	("TrayClockWClass",oleacc.ROLE_SYSTEM_CLOCK):"TrayClockWClass",
	("TRxRichEdit",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TRxRichEdit",
	(None,oleacc.ROLE_SYSTEM_OUTLINEITEM):"OutlineItem",
	(None,oleacc.ROLE_SYSTEM_LIST):"List",
	(None,oleacc.ROLE_SYSTEM_PROGRESSBAR):"ProgressBar",
	("TRichView",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TRichView",
	("TRichViewEdit",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TRichViewEdit",
	("TTntDrawGrid.UnicodeClass",oleacc.ROLE_SYSTEM_CLIENT):"List",
	("SysListView32",oleacc.ROLE_SYSTEM_LIST):"sysListView32.List",
	("SysListView32",oleacc.ROLE_SYSTEM_GROUPING):"sysListView32.List",
	("SysListView32",oleacc.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("DirectUIHWND", oleacc.ROLE_SYSTEM_LISTITEM): "UIItem",
	("SysListView32",oleacc.ROLE_SYSTEM_MENUITEM):"sysListView32.ListItemWithoutColumnSupport",
	("SysListView32", oleacc.ROLE_SYSTEM_CHECKBUTTON): "sysListView32.ListItem",
	("SysTreeView32",oleacc.ROLE_SYSTEM_OUTLINE):"sysTreeView32.TreeView",
	("SysTreeView32",oleacc.ROLE_SYSTEM_OUTLINEITEM):"sysTreeView32.TreeViewItem",
	("SysTreeView32",oleacc.ROLE_SYSTEM_MENUITEM):"sysTreeView32.TreeViewItem",
	("SysTreeView32",0):"sysTreeView32.BrokenCommctrl5Item",
	("ATL:SysListView32",oleacc.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("TWizardForm",oleacc.ROLE_SYSTEM_CLIENT):"delphi.Form",
	("SysLink",oleacc.ROLE_SYSTEM_CLIENT):"SysLinkClient",
	("SysLink",oleacc.ROLE_SYSTEM_LINK):"SysLink",
	("ATL:4FAE8088",oleacc.ROLE_SYSTEM_LINK):"SysLink",
	("#32771",oleacc.ROLE_SYSTEM_LIST):"TaskList",
	("TaskSwitcherWnd",oleacc.ROLE_SYSTEM_LIST):"TaskList",
	("#32771",oleacc.ROLE_SYSTEM_LISTITEM):"TaskListIcon",
	("TaskSwitcherWnd",oleacc.ROLE_SYSTEM_LISTITEM):"TaskListIcon",
	("TGroupBox",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TGroupBox",
	("TFormOptions",oleacc.ROLE_SYSTEM_CLIENT):"delphi.Form",
	("TMessageForm",oleacc.ROLE_SYSTEM_CLIENT):"delphi.Form",
	("TFormOptions",oleacc.ROLE_SYSTEM_WINDOW):"delphi.Form",
	("TTabSheet",oleacc.ROLE_SYSTEM_CLIENT):"delphi.TabSheet",
	("MsiDialogCloseClass",oleacc.ROLE_SYSTEM_CLIENT):"Dialog",
	(None,oleacc.ROLE_SYSTEM_MENUITEM):"MenuItem",
	("TPTShellList",oleacc.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("TProgressBar",oleacc.ROLE_SYSTEM_PROGRESSBAR):"ProgressBar",
	("AcrobatSDIWindow",oleacc.ROLE_SYSTEM_CLIENT):"adobeAcrobat.AcrobatSDIWindowClient",
	("SysMonthCal32",oleacc.ROLE_SYSTEM_CLIENT):"SysMonthCal32.SysMonthCal32",
	("hh_kwd_vlist",oleacc.ROLE_SYSTEM_LIST):"hh.KeywordList",
	("Scintilla",oleacc.ROLE_SYSTEM_CLIENT):"scintilla.Scintilla",
	("TScintilla",oleacc.ROLE_SYSTEM_CLIENT):"scintilla.Scintilla",
	("AkelEditW",oleacc.ROLE_SYSTEM_CLIENT):"akelEdit.AkelEdit",
	("AkelEditA",oleacc.ROLE_SYSTEM_CLIENT):"akelEdit.AkelEdit",
	("MSOUNISTAT",oleacc.ROLE_SYSTEM_CLIENT):"msOffice.MSOUNISTAT",
	("NetUIHWND", oleacc.ROLE_SYSTEM_PROPERTYPAGE): "msOffice.StatusBar",
	("NetUIHWND", oleacc.ROLE_SYSTEM_TOOLBAR): "msOffice.RibbonSection",
	("QWidget",oleacc.ROLE_SYSTEM_CLIENT):"qt.Client",
	("QWidget",oleacc.ROLE_SYSTEM_LIST):"qt.Container",
	("Qt5QWindowIcon",oleacc.ROLE_SYSTEM_LIST):"qt.Container",
	("QWidget",oleacc.ROLE_SYSTEM_OUTLINE):"qt.Container",
	("Qt5QWindowIcon",oleacc.ROLE_SYSTEM_OUTLINE):"qt.Container",
	("QWidget",oleacc.ROLE_SYSTEM_MENUBAR):"qt.Container",
	("QWidget",oleacc.ROLE_SYSTEM_ROW):"qt.TableRow",
	("QWidget",oleacc.ROLE_SYSTEM_CELL):"qt.TableCell",
	("QWidget",oleacc.ROLE_SYSTEM_OUTLINEITEM):"qt.TreeViewItem",
	("QPopup",oleacc.ROLE_SYSTEM_MENUPOPUP):"qt.Menu",
	("QWidget",oleacc.ROLE_SYSTEM_IPADDRESS):"qt.LayeredPane",
	("QWidget",oleacc.ROLE_SYSTEM_APPLICATION):"qt.Application",
	("Qt5QWindowIcon",oleacc.ROLE_SYSTEM_APPLICATION):"qt.Application",
	("Shell_TrayWnd",oleacc.ROLE_SYSTEM_CLIENT):"Taskbar",
	("Shell DocObject View",oleacc.ROLE_SYSTEM_CLIENT):"ShellDocObjectView",
	("listview",oleacc.ROLE_SYSTEM_CLIENT):"ListviewPane",
	("NUIDialog",oleacc.ROLE_SYSTEM_CLIENT):"NUIDialogClient",
	("_WwB",oleacc.ROLE_SYSTEM_CLIENT):"winword.ProtectedDocumentPane",
    ("MsoCommandBar",oleacc.ROLE_SYSTEM_LISTITEM):"msOffice.CommandBarListItem",
}
