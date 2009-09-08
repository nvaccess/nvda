import controlTypes
import eventHandler
import winUser
from . import IAccessible, getNVDAObjectFromEvent
from NVDAObjects import NVDAObjectTextInfo

class AcrobatNode(IAccessible):

	def _get_IAccessibleFocusEventNeedsFocusedState(self):
		#Acrobat document root objects do not have their focused state set when they have the focus.
		if self.event_childID==0:
			return False
		return super(AcrobatNode,self).IAccessibleFocusEventNeedsFocusedState

	def event_valueChange(self):
		# If this event indicates that a page is being replaced, this object will be an old object fetched from the IAccessible cache.
		# ROLE_UNKNOWN indicates a dead page object.
		# A read only edit field is probably the status text which is presented while a document is being rendered.
		if (self.event_childID==0 and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle)
			and (self.role==controlTypes.ROLE_UNKNOWN or (self.role == controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_READONLY in self.states))
		):
			# Acrobat has indicated that a page has died and been replaced by a new one.
			# The new page has the same event params, so we must bypass NVDA's IAccessible caching.
			obj = getNVDAObjectFromEvent(self.windowHandle, -4, 0)
			if not obj:
				return
			eventHandler.queueEvent("gainFocus",obj)

class AcrobatTextInfo(NVDAObjectTextInfo):

	def _getStoryText(self):
		return self.obj.value or ""

	def _getCaretOffset(self):
		caret = getNVDAObjectFromEvent(self.obj.windowHandle, winUser.OBJID_CARET, 0)
		if not caret:
			raise RuntimeError("No caret")
		try:
			return int(caret.description)
		except (ValueError, TypeError):
			raise RuntimeError("Bad caret index")

class AcrobatTextNode(AcrobatNode):
	TextInfo = AcrobatTextInfo

[AcrobatTextNode.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","moveByLine"),
	("ExtendedDown","moveByLine"),
	("ExtendedLeft","moveByCharacter"),
	("ExtendedRight","moveByCharacter"),
	("ExtendedPrior","moveByLine"),
	("ExtendedNext","moveByLine"),
	("Control+ExtendedLeft","moveByWord"),
	("Control+ExtendedRight","moveByWord"),
	("control+extendedDown","moveByParagraph"),
	("control+extendedUp","moveByParagraph"),
	("ExtendedHome","moveByCharacter"),
	("ExtendedEnd","moveByCharacter"),
	("control+extendedHome","moveByLine"),
	("control+extendedEnd","moveByLine"),
	("ExtendedDelete","delete"),
	("Back","backspace"),
]]

class AcrobatSDIWindowClient(IAccessible):

	def __init__(self, **kwargs):
		super(AcrobatSDIWindowClient, self).__init__(**kwargs)
		if not self.name and self.parent:
			# There are two client objects, one with a name and one without.
			# The unnamed object (probably manufactured by Acrobat) has broken next and previous relationships.
			# The unnamed object's parent is the named object, but when descending into the named object, the unnamed object is skipped.
			# Given the brokenness of the unnamed object, just skip it completely and use the parent when it is encountered.
			self.IAccessibleObject = self.IAccessibleObject.accParent
