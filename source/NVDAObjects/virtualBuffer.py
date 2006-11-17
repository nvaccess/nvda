from keyboardHandler import key
import audio
import virtualBuffers
import textBuffer

class NVDAObject_virtualBuffer(textBuffer.NVDAObject_editableTextBuffer):

	focusInteractionMode=False

	def __init__(self,*args):
		textBuffer.NVDAObject_editableTextBuffer.__init__(self,*args)
		self.registerScriptKeys({
			key("insert+space"):self.script_toggleFocusInteractionMode,
			key("Return"):self.script_enter,
			key("Space"):self.script_space,
		})

	def getCaretPosition(self):
		return virtualBuffers.getVirtualBuffer(self.hwnd).caretPosition

	def setCaretPosition(self,pos):
		virtualBuffers.getVirtualBuffer(self.hwnd).setCaretPosition(pos)

	caretPosition=property(fget=getCaretPosition,fset=setCaretPosition)

	def getLineCount(self):
		return virtualBuffers.getVirtualBuffer(self.hwnd).getLineCount()
	lineCount=property(fget=getLineCount)

	def getLineNumber(self,pos):
		return virtualBuffers.getVirtualBuffer(self.hwnd).getLineNumber(pos)

	def getLineStart(self,pos):
		return virtualBuffers.getVirtualBuffer(self.hwnd).getLineStart(pos)

	def getLineLength(self,pos):
		return virtualBuffers.getVirtualBuffer(self.hwnd).getLineLength(pos)

	def getLine(self,pos):
		return virtualBuffers.getVirtualBuffer(self.hwnd).getLine(pos)

	def getText(self):
		return virtualBuffers.getVirtualBuffer(self.hwnd).getText()
	text=property(fget=getText)

	def script_toggleFocusInteractionMode(self,keyPress):
		"""Toggles focus interaction mode on and off"""
		if not self.focusInteractionMode:
			audio.speakMessage("Focus interaction mode on")
			self.focusInteractionMode=True
		else:
			audio.speakMessage("Focus interaction mode off")
			self.focusInteractionMode=False

	def script_moveByCharacter(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		virtualBuffers.getVirtualBuffer(self.hwnd).processKey(keyPress)
		audio.speakText(self.getCharacter(self.caretPosition))

	def script_moveByWord(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		virtualBuffers.getVirtualBuffer(self.hwnd).processKey(keyPress)
		audio.speakText(self.getWord(self.caretPosition))

	def script_moveByLine(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		virtualBuffers.getVirtualBuffer(self.hwnd).processKey(keyPress)
		audio.speakText(self.getLine(self.caretPosition))

	def script_enter(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		virtualBuffers.getVirtualBuffer(self.hwnd).activatePosition(self.caretPosition)

	def script_space(self,keyPress):
		if self.focusInteractionMode:
			sendKey(keyPress)
			return
		virtualBuffers.getVirtualBuffer(self.hwnd).activatePosition(self.caretPosition)

