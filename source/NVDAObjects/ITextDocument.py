import lang
import textBuffer

class NVDAObject_ITextDocument(textBuffer.NVDAObject_editableTextBuffer):

	class constants:
		#Units
		tomCharacter=1
		tomWord=2
		tomParagraph=4
		tomLine=5
		tomStory=6
		tomWindow=11
		#Paragraph alignment
		tomAlignLeft=0
		tomAlignCenter=1
		tomAlignRight=2
		tomAlignJustify=3

	def __init__(self,*args):
		self.dom=self.getDocumentObjectModel()
		textBuffer.NVDAObject_editableTextBuffer.__init__(self,*args)
		self._presentationTable+=[
			[self.msgFontName,["documentFormatting","reportFontName"],None,None],
			[self.msgFontSize,["documentFormatting","reportFontSize"],None,None],
			[self.msgBold,["documentFormatting","reportFontAttributes"],None,None],
			[self.msgItalic,["documentFormatting","reportFontAttributes"],None,None],
			[self.msgUnderline,["documentFormatting","reportFontAttributes"],None,None],
			[self.msgParagraphAlignment,["documentFormatting","reportAlignment"],None,None],
		]

	def __del__(self):
		self.destroyObjectModel(self.dom)
		NVDAObject_edit.__del__(self)

	def getDocumentObjectModel(self):
		abstract

	def destroyObjectModel(self,om):
		pass

	def _duplicateDocumentRange(self,rangeObj):
		abstract


	def getCaretRange(self):
		start=self.dom.Selection.Start
		end=self.dom.Selection.End
		if start!=end:
			return (start,end)
		else:
			return None
	caretRange=property(fget=getCaretRange)

	def getCaretPosition(self):
		return self.dom.Selection.Start

	def setCaretPosition(self,pos):
		self.dom.Selection.Start=pos
		self.dom.Selection.End=pos

	caretPosition=property(fget=getCaretPosition,fset=setCaretPosition)

	def getVisibleRange(self):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Expand(self.constants.tomWindow)
		return (rangeObj.Start,rangeObj.End)
	visibleRange=property(fget=getVisibleRange)

	def getStartPosition(self):
		return 0
	startPosition=property(fget=getStartPosition)

	def getEndPosition(self):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Expand(self.constants.tomStory)
		return rangeObj.End
	endPosition=property(fget=getEndPosition)

	def getLineNumber(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=0
		rangeObj.Move(self.constants.tomCharacter,pos)
		return rangeObj.GetIndex(self.constants.tomLine)-1

	def getLineStart(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(self.constants.tomLine)
		return rangeObj.Start

	def nextLine(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		delta=rangeObj.Move(self.constants.tomLine,1)
		if delta:
			return rangeObj.Start
		else:
			return None

	def previousLine(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		delta=rangeObj.Move(self.constants.tomLine,-1)
		if delta:
			return rangeObj.Start
		else:
			return None

	def getLine(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(self.constants.tomLine)
		text=rangeObj.Text
		if text!='\r':
			return text
		else:
			return None

	def getLineCount(self):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=0
		rangeObj.Expand(self.constants.tomStory)
		return self.getLineNumber(rangeObj.End)

	def nextWord(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		delta=rangeObj.Move(self.constants.tomWord,1)
		if delta:
			return rangeObj.Start
		else:
			return None

	def previousWord(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		delta=rangeObj.Move(self.constants.tomWord,-1)
		if delta:
			return rangeObj.Start
		else:
			return None

	def getParagraph(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(self.constants.tomParagraph)
		return self.getTextRange(rangeObj.Start,rangeObj.End)

	def getCurrentParagraph(self):
		return self.getParagraph(self.getCaretPosition())

	def getTextRange(self,start,end):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=start
		rangeObj.End=end
		return rangeObj.Text

	def getWord(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		rangeObj.Expand(self.constants.tomWord)
		return self.getTextRange(rangeObj.Start,rangeObj.End)

	def getFontName(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Name

	def msgFontName(self,pos):
		return "font %s"%self.getFontName(pos)

	def getFontSize(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return int(rangeObj.Font.Size)

	def msgFontSize(self,pos):
		return "%s point"%self.getFontSize(pos)

	def getParagraphAlignment(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		align=rangeObj.Para.Alignment
		if align==self.constants.tomAlignLeft:
			return "left"
		elif align==self.constants.tomAlignCenter:
			return "centered"
		elif align==self.constants.tomAlignRight:
			return "right"
		elif align>=self.constants.tomAlignJustify:
			return "justified"

	def msgParagraphAlignment(self,pos):
		return "alignment %s"%self.getParagraphAlignment(pos)

	def isBold(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Bold

	def msgBold(self,pos):
		if self.isBold(pos):
			bold="on"
		else:
			bold="off"
		return "bold %s"%bold

	def isItalic(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Italic

	def msgItalic(self,pos):
		if self.isItalic(pos):
			italic="on"
		else:
			italic="off"
		return "italic %s"%italic

	def isUnderline(self,pos):
		rangeObj=self._duplicateDocumentRange(self.dom.Selection)
		rangeObj.Start=rangeObj.End=pos
		return rangeObj.Font.Underline

	def msgUnderline(self,pos):
		if self.isUnderline(pos):
			underline="on"
		else:
			underline="off"
		return "underline %s"%underline
