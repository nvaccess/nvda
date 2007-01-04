from autoPropertyType import autoPropertyType
from keyboardHandler import key

class NVDAObjectExt_ITextDocument:

	__metaclass__=autoPropertyType

	class constants:
		#Units
		tomCharacter=1
		tomWord=2
		tomSentence=3
		tomParagraph=4
		tomLine=5
		tomStory=6
		tomScreen=7
		tomSection=8
		tomColumn=9
		tomRow=10
		tomWindow=11
		tomCell=12
		tomCharFormat=13
		tomParaFormat=14
		tomTable=15
		tomObject=16
		tomPage=17
		#Paragraph alignment
		tomAlignLeft=0
		tomAlignCenter=1
		tomAlignRight=2
		tomAlignJustify=3

	def __init__(self,*args,**vars):
		self.dom=self.getDocumentObjectModel()
		self.registerScriptKeys({
			key("ExtendedUp"):self.script_text_moveByLine,
			key("ExtendedDown"):self.script_text_moveByLine,
			key("ExtendedLeft"):self.script_text_moveByCharacter,
			key("ExtendedRight"):self.script_text_moveByCharacter,
			key("Control+ExtendedUp"):self.script_text_prevParagraph,
			key("Control+ExtendedDown"):self.script_text_nextParagraph,
			key("Control+ExtendedLeft"):self.script_text_moveByWord,
			key("Control+ExtendedRight"):self.script_text_moveByWord,
			key("Shift+ExtendedRight"):self.script_text_changeSelection,
			key("Shift+ExtendedLeft"):self.script_text_changeSelection,
			key("Shift+ExtendedHome"):self.script_text_changeSelection,
			key("Shift+ExtendedEnd"):self.script_text_changeSelection,
			key("Shift+ExtendedUp"):self.script_text_changeSelection,
			key("Shift+ExtendedDown"):self.script_text_changeSelection,
			key("Control+Shift+ExtendedLeft"):self.script_text_changeSelection,
			key("Control+Shift+ExtendedRight"):self.script_text_changeSelection,
			key("ExtendedHome"):self.script_text_moveByCharacter,
			key("ExtendedEnd"):self.script_text_moveByCharacter,
			key("control+extendedHome"):self.script_text_moveByLine,
			key("control+extendedEnd"):self.script_text_moveByLine,
			key("control+shift+extendedHome"):self.script_text_changeSelection,
			key("control+shift+extendedEnd"):self.script_text_changeSelection,
			key("ExtendedDelete"):self.script_text_delete,
			key("Back"):self.script_text_backspace,
		})

	def __del__(self):
		self.destroyObjectModel(self.dom)

	def getDocumentObjectModel(self):
		abstract

	def destroyObjectModel(self,om):
		pass

	def _get_text_characterCount(self):
		r=self.dom.Range(0,0)
		r.Expand(self.constants.tomStory)
		return r.End

	def text_getText(self,start=None,end=None):
		start=start if isinstance(start,int) else 0
		end=end if isinstance(end,int) else self.text_characterCount
		r=self.dom.Range(start,end)
		return r.text

	def _get_text_selectionCount(self):
		if self.dom.Selection.Start!=self.dom.Selection.End:
			return 1
		else:
			return 0

	def text_getSelectionOffsets(self,index):
		if index!=0:
			return None
		start=self.dom.Selection.Start
		end=self.dom.Selection.End
		if start!=end:
			return (start,end)
		else:
			return None

	def _get_text_caretOffset(self):
		return self.dom.Selection.Start

	def _set_text_caretOffset(self,offset):
		self.dom.Selection.Start=offset
		self.dom.Selection.End=offset

	def text_getLineNumber(self,offset):
		return self.dom.Range(offset,offset).GetIndex(self.constants.tomLine)

	def text_getPageNumber(self,offset):
		pageNum=self.dom.Range(offset,offset).GetIndex(self.constants.tomPage)
		if pageNum>0:
			return pageNum
		else:
			return None

	def text_getLineOffsets(self,offset):
		r=self.dom.Range(offset,offset)
		r.Expand(self.constants.tomLine)
		return (r.Start,r.End)

	def text_getNextLineOffsets(self,offset):
		(start,end)=self.text_getLineOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomLine,1)
		if res!=0:
			return self.text_getLineOffsets(r.Start)
		else:
			return None

	def text_getPrevLineOffsets(self,offset):
		(start,end)=self.text_getLineOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomLine,-1)
		if res!=0:
			return self.text_getLineOffsets(r.Start)
		else:
			return None

	def text_getWordOffsets(self,offset):
		r=self.dom.Range(offset,offset)
		r.Expand(self.constants.tomWord)
		return (r.Start,r.End)

	def text_getNextWordOffsets(self,offset):
		(start,end)=self.text_getWordOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomWord,1)
		if res:
			return self.text_getWordOffsets(r.Start)
		else:
			return None

	def text_getPrevWordOffsets(self,offset):
		(start,end)=self.text_getWordOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomWord,-1)
		if res:
			return self.text_getWordOffsets(r.Start)
		else:
			return None

	def text_getSentenceOffsets(self,offset):
		r=self.dom.Range(offset,offset)
		r.Expand(self.constants.tomSentence)
		return (r.Start,r.End)

	def text_getNextSentenceOffsets(self,offset):
		(start,end)=self.text_getSentenceOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomSentence,1)
		if res:
			return self.text_getSentenceOffsets(r.Start)
		else:
			return None

	def text_getPrevSentenceOffsets(self,offset):
		(start,end)=self.text_getSentenceOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomSentence,-1)
		if res:
			return self.text_getSentenceOffsets(r.Start)
		else:
			return None

	def text_getParagraphOffsets(self,offset):
		r=self.dom.Range(offset,offset)
		r.Expand(self.constants.tomParagraph)
		return (r.Start,r.End)

	def text_getNextParagraphOffsets(self,offset):
		(start,end)=self.text_getParagraphOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomParagraph,1)
		if res:
			return self.text_getParagraphOffsets(r.Start)
		else:
			return None

	def text_getPrevParagraphOffsets(self,offset):
		(start,end)=self.text_getParagraphOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomParagraph,-1)
		if res:
			return self.text_getParagraphOffsets(r.Start)
		else:
			return None

	def text_getFieldOffsets(self,offset):
		r=self.dom.Range(offset,offset)
		r.Expand(self.constants.tomCharFormat)
		return (r.Start,r.End)

	def text_getNextFieldOffsets(self,offset):
		(start,end)=self.text_getFieldOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomCharFormat,1)
		if res:
			return self.text_getFieldOffsets(r.Start)
		else:
			return None

	def text_getPrevFieldOffsets(self,offset):
		(start,end)=self.text_getFieldOffsets(offset)
		r=self.dom.Range(start,start)
		res=r.Move(self.constants.tomCharFormat,-1)
		if res:
			return self.text_getFieldOffsets(r.Start)
		else:
			return None

	def text_getFontName(self,offset):
		return self.dom.Range(offset,offset).Font.Name

	def text_getFontSize(self,offset):
		return int(self.dom.Range(offset,offset).Font.Size)

	def text_getAlignment(self,offset):
		alignment=self.dom.Range(offset,offset).Para.Alignment
		if alignment==self.constants.tomAlignLeft:
			return "left"
		elif alignment==self.constants.tomAlignCenter:
			return "centered"
		elif alignment==self.constants.tomAlignRight:
			return "right"
		elif alignment==self.constants.tomAlignJustify:
			return "justified"

	def text_isBold(self,offset):
		return bool(self.dom.Range(offset,offset).Font.Bold)

	def text_isItalic(self,offset):
		return bool(self.dom.Range(offset,offset).Font.Italic)

	def text_isUnderline(self,offset):
		return bool(self.dom.Range(offset,offset).Font.Underline)

	def text_isSuperscript(self,offset):
		return bool(self.dom.Range(offset,offset).Font.Superscript)

	def text_isSubscript(self,offset):
		return bool(self.dom.Range(offset,offset).Font.Subscript)
