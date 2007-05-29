import debug
import api
import speech
import IA2Handler
import IAccessibleHandler
from keyUtils import sendKey, isKeyWaiting
from NVDAObjects.IAccessible import IAccessible

objWithCaret=None

class IA2(IAccessible):

	def __init__(self,pacc,childID,windowHandle=None,origChildID=None,objectID=None):
		IAccessible.__init__(self,pacc,childID,windowHandle=windowHandle,origChildID=origChildID,objectID=objectID)
		try:
			self.IAccessibleTextObject=pacc.QueryInterface(IA2Handler.IA2Lib.IAccessibleText)
			try:
				self.IAccessibleEditableTextObject=pacc.QueryInterface(IA2Handler.IA2Lib.IAccessibleEditableText)
				[self.bindKey_runtime(keyName,scriptName) for keyName,scriptName in [
					("ExtendedUp","text_moveByLine"),
					("ExtendedDown","text_moveByLine"),
					("ExtendedLeft","text_moveByCharacter"),
					("ExtendedRight","text_moveByCharacter"),
					("Control+ExtendedLeft","text_moveByWord"),
					("Control+ExtendedRight","text_moveByWord"),
					("Shift+ExtendedRight","text_changeSelection"),
					("Shift+ExtendedLeft","text_changeSelection"),
					("Shift+ExtendedHome","text_changeSelection"),
					("Shift+ExtendedEnd","text_changeSelection"),
					("Shift+ExtendedUp","text_changeSelection"),
					("Shift+ExtendedDown","text_changeSelection"),
					("Control+Shift+ExtendedLeft","text_changeSelection"),
					("Control+Shift+ExtendedRight","text_changeSelection"),
					("ExtendedHome","text_moveByCharacter"),
					("ExtendedEnd","text_moveByCharacter"),
					("control+extendedHome","text_moveByLine"),
					("control+extendedEnd","text_moveByLine"),
					("control+shift+extendedHome","text_changeSelection"),
					("control+shift+extendedEnd","text_changeSelection"),
					("ExtendedDelete","text_delete"),
					("Back","text_backspace"),
				]]
			except:
				pass
		except:
			pass

	def _get_text_characterCount(self):
		if not hasattr(self,"IAccessibleTextObject"):
			return IAccessible._get_text_characterCount(self)
		return self.IAccessibleTextObject.NCharacters

	def text_getText(self,start=None,end=None):
		if not hasattr(self,"IAccessibleTextObject"):
			return IAccessible.text_getText(self,start=start,end=end)
		start=start if start is not None else 0
		end=end if end is not None else self.text_characterCount
		if start<self.text_characterCount:
			return self.IAccessibleTextObject.Text(start,end)
		else:
			return None

	def _get_text_caretOffset(self):
		if not hasattr(self,"IAccessibleTextObject"):
			return IAccessible._get_text_caretOffset(self)
		return self.IAccessibleTextObject.CaretOffset

	def _get_text_selectionCount(self):
		if not hasattr(self,"IAccessibleTextObject"):
			return IAccessible._get_text_selectionCount(self)
		return self.IAccessibleTextObject.NSelections

	def text_getSelectionOffsets(self,index):
		if not hasattr(self,"IAccessibleTextObject"):
			return IAccessible.text_getSelectionOffsets(self,index)
		return self.IAccessibleTextObject.Selection(index)

	def text_getLineOffsets(self,offset):
		if not hasattr(self,"IAccessibleTextObject"):
			return IAccessible.text_getLineOffsets(self,offset)
		return self.IAccessibleTextObject.TextAtOffset(offset,  IA2Handler.TEXT_BOUNDARY_LINE)[:2]

	def event_caret(self):
		global objWithCaret
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_CARET:
			return
		objWithCaret=self

	def script_text_moveByLine(self,keyPress,nextScript):
		sendKey(keyPress)
		api.processPendingEvents()
		if not isKeyWaiting():
			objWithCaret.text_speakLine(objWithCaret.text_caretOffset)

	def script_text_moveByWord(self,keyPress,nextScript):
		sendKey(keyPress)
		api.processPendingEvents()
		if not isKeyWaiting():
			objWithCaret.text_speakWord(objWithCaret.text_caretOffset)

	def script_text_moveByCharacter(self,keyPress,nextScript):
		sendKey(keyPress)
		api.processPendingEvents()
		if not isKeyWaiting():
			objWithCaret.text_speakCharacter(objWithCaret.text_caretOffset)

