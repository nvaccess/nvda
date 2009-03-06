import eventHandler
import winUser
from . import IAccessible, getNVDAObjectFromEvent
from NVDAObjects import NVDAObjectTextInfo
import IAccessibleHandler

class AcrobatNode(IAccessible):

	def event_valueChange(self):
		if self.event_childID==0 and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			# This page may die and be replaced by another with the same event params, so always grab a new one.
			obj = getNVDAObjectFromEvent(self.windowHandle, -4, 0)
			if not obj:
				return
			eventHandler.queueEvent("gainFocus",obj)

class AcrobatTextInfo(NVDAObjectTextInfo):

	def _getStoryText(self):
		return self.obj.value or ""

	def _getCaretOffset(self):
		caret = getNVDAObjectFromEvent(self.obj.windowHandle, IAccessibleHandler.OBJID_CARET, 0)
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
