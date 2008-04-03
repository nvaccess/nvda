import ctypes
import comtypes
import winsound
import globalVars
import api
import speech
import textHandler
import controlTypes
import IAccessibleHandler
from keyUtils import sendKey
from .. import IAccessible
from ... import NVDAObjectTextInfo
from ...window import Window

class IA2TextTextInfo(NVDAObjectTextInfo):

	def _getCaretOffset(self):
		try:
			return self.obj.IAccessibleTextObject.CaretOffset
		except:
			return 0

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
		if not hasattr(self,'_storyLength'):
			self._storyLength=self.obj.IAccessibleTextObject.NCharacters
		return self._storyLength

	def _getLineCount(self):
			return -1

	def _getTextRange(self,start,end):
		try:
			return self.obj.IAccessibleTextObject.Text(start,end)
		except:
			return ""

	def _getCharacterOffsets(self,offset):
		try:
			return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_CHAR)[0:2]
		except:
			return super(IA2TextTextInfo,self)._getCharacterOffsets(offset)


	def _getWordOffsets(self,offset):
		try:
			return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_WORD)[0:2]
		except:
			return super(IA2TextTextInfo,self)._getWordOffsets(offset)


	def _getLineOffsets(self,offset):
		try:
			return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_LINE)[0:2]
		except:
			return super(IA2TextTextInfo,self)._getLineOffsets(offset)

	def _getSentenceOffsets(self,offset):
		try:
			start,end=self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_SENTENCE)[0:2]
			if start==end:
				raise NotImplementedError
			return (start,end)
		except:
			return super(IA2TextTextInfo,self)._getSentenceOffsets(offset)

	def _getParagraphOffsets(self,offset):
		return self.obj.IAccessibleTextObject.TextAtOffset(offset,IAccessibleHandler.IA2_TEXT_BOUNDARY_PARAGRAPH)[0:2]

	def _lineNumFromOffset(self,offset):
		return -1

class IA2(IAccessible):

	def __init__(self,windowHandle=None,IAccessibleObject=None,IAccessibleChildID=None,event_windowHandle=None,event_objectID=None,event_childID=None):
		replacedTextInfo=False
		if not windowHandle:
			windowHandle=IAccessibleHandler.windowFromAccessibleObject(IAccessibleObject) #windowHandle=IAccessibleObject.windowHandle
		try:
			self.IAccessibleActionObject=IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleAction)
		except:
			pass
		try:
			self.IAccessibleTextObject=IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleText)
			self.TextInfo=IA2TextTextInfo
			replacedTextInfo=True
			try:
				self.IAccessibleEditableTextObject=IAccessibleObject.QueryInterface(IAccessibleHandler.IAccessibleEditableText)
				[self.bindKey_runtime(keyName,scriptName) for keyName,scriptName in [
					("ExtendedUp","moveByLine"),
					("ExtendedDown","moveByLine"),
					("ExtendedLeft","moveByCharacter"),
					("ExtendedRight","moveByCharacter"),
					("Control+ExtendedLeft","moveByWord"),
					("Control+ExtendedRight","moveByWord"),
					("Shift+ExtendedRight","changeSelection"),
					("Shift+ExtendedLeft","changeSelection"),
					("Shift+ExtendedHome","changeSelection"),
					("Shift+ExtendedEnd","changeSelection"),
					("Shift+ExtendedUp","changeSelection"),
					("Shift+ExtendedDown","changeSelection"),
					("Control+Shift+ExtendedLeft","changeSelection"),
					("Control+Shift+ExtendedRight","changeSelection"),
					("ExtendedHome","moveByCharacter"),
					("ExtendedEnd","moveByCharacter"),
					("control+extendedHome","moveByLine"),
					("control+extendedEnd","moveByLine"),
					("control+shift+extendedHome","changeSelection"),
					("control+shift+extendedEnd","changeSelection"),
					("ExtendedDelete","delete"),
					("Back","backspace"),
				]]
			except:
				pass
		except:
			pass
		IAccessible.__init__(self,windowHandle=windowHandle,IAccessibleObject=IAccessibleObject,IAccessibleChildID=IAccessibleChildID,event_windowHandle=event_windowHandle,event_objectID=event_objectID,event_childID=event_childID)
		self._lastMouseTextOffsets=None
		if replacedTextInfo:
			self.reviewPosition=self.makeTextInfo(textHandler.POSITION_CARET)

	def _isEqual(self,other):
		try:
			if isinstance(other,IA2) and self.IAccessibleObject.UniqueID==other.IAccessibleObject.UniqueID and self.IAccessibleObject.windowHandle==other.IAccessibleObject.windowHandle:
				return True
		except:
			pass

		return super(IA2,self)._isEqual(other)

	def _get_role(self):
		try:
			IA2Role=self.IAccessibleObject.role()
		except:
			IA2Role=0
		if IA2Role>IAccessibleHandler.IA2_ROLE_UNKNOWN and IAccessibleHandler.IAccessibleRolesToNVDARoles.has_key(IA2Role):
			return IAccessibleHandler.IAccessibleRolesToNVDARoles[IA2Role]
		else:
			return super(IA2,self)._get_role()

	def _get_states(self):
		try:
			IAccessible2States=self.IAccessibleObject.states
		except:
			globalVars.log.warning("could not get IAccessible2 states",exc_info=True)
			IAccessible2States=IAccessibleHandler.IA2_STATE_DEFUNCT
		states=super(IA2,self)._get_states()|set(IAccessibleHandler.IAccessible2StatesToNVDAStates[x] for x in (y for y in (1<<z for z in xrange(32)) if y&IAccessible2States) if IAccessibleHandler.IAccessible2StatesToNVDAStates.has_key(x))
		if controlTypes.STATE_HASPOPUP in states and controlTypes.STATE_AUTOCOMPLETE in states:
			states.remove(controlTypes.STATE_HASPOPUP)
		return states

	def _get_actionStrings(self):
		if not hasattr(self,'IAccessibleActionObject'):
			return super(IA2,self)._get_actionStrings()
		actions=[]
		for index in range(self.IAccessibleActionObject.nActions()):
			try:
				name=self.IAccessibleActionObject.localizedName(index)
			except:
				name=None
			if not name:
				try:
					name=self.IAccessibleActionObject.name(index)
				except:
					name=None
			if name:
				actions.append(name)
		return actions

	def doAction(self,index):
		if not hasattr(self,'IAccessibleActionObject'):
			return super(IA2,self).doAction(index)
		self.IAccessibleActionObject.doAction(index)

	def _get_value(self):
		if not hasattr(self,'IAccessibleTextObject'):
			return super(IA2,self)._get_value()

	def event_alert(self):
		speech.cancelSpeech()
		speech.speakObject(self)
		self.speakDescendantObjects()



	def event_caret(self):
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_CARET:
			return
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
				IAccessibleHandler.focus_manageEvent(self)

	def event_mouseMove(self,x,y):
		#As Gecko 1.9 still has MSAA text node objects, these get hit by accHitTest, so
		#We must find the real object and cache it
		obj=getattr(self,'_realMouseObject',None)
		if not obj:
			obj=self
			while obj and not hasattr(obj,'IAccessibleTextObject'):
				obj=obj.parent
			if obj:
				self._realMouseObject=obj
			else:
				obj=self
		mouseEntered=obj._mouseEntered
		super(IA2,obj).event_mouseMove(x,y)
		if not hasattr(obj,'IAccessibleTextObject'):
			return 
		(left,top,width,height)=obj.location
		offset=obj.IAccessibleTextObject.OffsetAtPoint(x,y,IAccessibleHandler.IA2_COORDTYPE_SCREEN_RELATIVE)
		if obj._lastMouseTextOffsets is None or offset<obj._lastMouseTextOffsets[0] or offset>=obj._lastMouseTextOffsets[1]:   
			if mouseEntered:
				speech.cancelSpeech()
			info=obj.makeTextInfo(textHandler.Bookmark(obj.TextInfo,(offset,offset)))
			info.expand(textHandler.UNIT_WORD)
			speech.speakText(info.text)
			obj._lastMouseTextOffsets=(info._startOffset,info._endOffset)
