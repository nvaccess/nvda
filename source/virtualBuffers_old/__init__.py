#virtualBuffers/baseType.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from new import instancemethod
from textwrap import TextWrapper
import weakref
from keyUtils import key
import speech
import globalVars
import config
import textBuffer
import gui.scriptUI
import controlTypes
import NVDAObjects
import virtualBufferHandler

class virtualBuffer(textBuffer.TextBufferObject):

	def isNVDAObjectInVirtualBuffer(self,obj):
		pass

	def isAlive(self):
		pass

	def event_focusEntered(self,obj,nextHandler):
		pass

	def event_virtualBuffer_gainFocus(self):
		virtualBufferHandler.reportPassThrough(self)

	fieldInfoTemplate={
		"role":controlTypes.ROLE_UNKNOWN,
		"node":None,
		"range":[0,0],
		"parent":None,
		"children":[],
		"labeledBy":None,
		"typeString":"",
		"stateTextFunc":None,
		"descriptionFunc":None,
		"accessKey":None,
}

	def __init__(self,NVDAObject):
		textBuffer.TextBufferObject.__init__(self)
		self.needsLoad=True
		self.rootNVDAObject=NVDAObject
		self._IDs={}
		self._textBuf=""
		self._lastReportedIDList=[]
		self._lastFindText=""
		self._findInProgress=False
		self.passThrough=False

	def getIDFromPosition(self,pos):
		IDs=self._IDs
		shortList=filter(lambda x: pos>=IDs[x]['range'][0] and pos<IDs[x]['range'][1],IDs)
		return min(shortList,key=lambda x: IDs[x]['range'][1]-IDs[x]['range'][0]) if shortList else None

	def getFullRangeFromID(self,ID):
		IDs=self._IDs
		if not IDs.has_key(ID):
			return None
		children=filter(lambda x: x is not None and IDs.has_key(x),IDs[ID]['children'])
		if len(children)==0:
			return IDs[ID]['range']
		else:
			return [IDs[ID]['range'][0],max([self.getFullRangeFromID(x)[1] for x in children]+[IDs[ID]['range'][1]])]

	def getIDAncestors(self,ID):
		IDs=self._IDs
		if not IDs.has_key(ID):
			return []
		curID=ID
		ancestors=[]
		ancestors_append=ancestors.append
		while IDs.has_key(curID) and IDs[curID]['parent']:
			curID=IDs[curID]['parent']
			ancestors_append(curID)
		ancestors.reverse()
		return ancestors

	def getIDZOrder(self,ID):
		IDs=self._IDs
		zOrder=[]
		ancestors=self.getIDAncestors(ID)
		ancestors.reverse()
		for parentID in ancestors:
			try:
				childNum=IDs[parentID]['children'].index(ID)
			except:
				childNum=0
			zOrder.insert(0,childNum)
			ID=parentID
		return zOrder

	def addText(self,ID,text,position=None):
		isAppending=False
		isMurging=False
		bufLen=self.text_characterCount
		IDs=self._IDs
		#If no position given, assume end of buffer
		if position is None:
			position=bufLen
			isAppending=True
		#If this ID path already has a range, expand it to fit the new text
		r=IDs[ID]['range']
		#clean up newLine characters  a bit
		text=text.replace('\r\n','\n')
		text=text.replace('\r','\n')
		#Force the text being added to wrap at a configurable length
		maxLineLength=config.conf["virtualBuffers"]["maxLineLength"]
		if len(text)>maxLineLength:
			wrapper = TextWrapper(width=maxLineLength, expand_tabs=False, replace_whitespace=False, break_long_words=False)
			text=wrapper.fill(text)
		textLen=len(text)
		self._textBuf= "".join([self._textBuf[0:position],text,'\n',self._textBuf[position:]])
		extraLength=textLen+1
		r[1]=position+extraLength
		#Recalculate the ranges of IDs that are before and after this ID in its family tree Z order
		if not isAppending:
			IDZOrder=self.getIDZOrder(ID)
			for i in IDs: 
				r=IDs[i]['range']
				if r[1]>position and r[0]<=position and self.getIDZOrder(i)<IDZOrder:
					r[1]=r[1]+extraLength
				elif r[0]>=position and self.getIDZOrder(i)>IDZOrder:
					(r[0],r[1])=(r[0]+extraLength,r[1]+extraLength)
		return position+extraLength

	def destroyIDDescendants(self,ID):
		if ID is None:
			return
		for item in self._IDs[ID]['children']:
			self.destroyIDDescendants(item)
		parent=self._IDs[ID]['parent']
		if parent is not None:
			self._IDs[parent]['children']=filter(lambda x: x!=ID,self._IDs[parent]['children'])
		del self._IDs[ID]
 
	def removeID(self,ID):
		IDs=self._IDs
		if not IDs.has_key(ID):
			return
		IDZOrder=self.getIDZOrder(ID)
		(start,end)=self.getFullRangeFromID(ID)
		if end>start:
			self._textBuf="".join([self._textBuf[0:start],self._textBuf[end:]])
			for i in IDs:
				r=IDs[i]['range']
				if r[1]>=end and r[0]<=start and self.getIDZOrder(i)<IDZOrder:
					r[1]=r[1]-(end-start)
				elif r[0]>=end and self.getIDZOrder(i)>IDZOrder:
					(r[0],r[1])=(r[0]-(end-start),r[1]-(end-start))
		self.destroyIDDescendants(ID)

	def resetBuffer(self):
		self._textBuf=""
		self._IDs={}
		self.text_reviewPosition=0
		self._lastCaretIDs=[]

	def addID(self,ID,info):
		self._IDs[ID]=info

	def getIDEnterMessage(self,ID):
		if not self._IDs.has_key(ID):
			return ""
		info=self._IDs[ID]
		role=info["role"]
		vbc=config.conf["documentFormatting"]
		if (role==controlTypes.ROLE_LINK and vbc["reportLinks"]) or (role==controlTypes.ROLE_LIST and vbc["reportLists"]) or (role==controlTypes.ROLE_LISTITEM and vbc["reportLists"]) or (role==controlTypes.ROLE_HEADING and vbc["reportHeadings"]) or (role==controlTypes.ROLE_HEADING1 and vbc["reportHeadings"]) or (role==controlTypes.ROLE_HEADING2 and vbc["reportHeadings"]) or (role==controlTypes.ROLE_HEADING3 and vbc["reportHeadings"]) or (role==controlTypes.ROLE_HEADING4 and vbc["reportHeadings"]) or (role==controlTypes.ROLE_HEADING5 and vbc["reportHeadings"]) or (role==controlTypes.ROLE_HEADING6 and vbc["reportHeadings"]) or (role==controlTypes.ROLE_TABLE and vbc["reportTables"]) or (role==controlTypes.ROLE_TABLEHEADER and vbc["reportTables"]) or (role==controlTypes.ROLE_TABLEFOOTER and vbc["reportTables"]) or (role==controlTypes.ROLE_TABLEROW and vbc["reportTables"]) or (role==controlTypes.ROLE_TABLECELL and vbc["reportTables"]) or (role==controlTypes.ROLE_GRAPHIC or (role in [controlTypes.ROLE_BUTTON,controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_COMBOBOX])) or (role==controlTypes.ROLE_BLOCKQUOTE and vbc["reportBlockQuotes"]) or (role==controlTypes.ROLE_FRAME):
			msg=info["typeString"] if info["typeString"] else controlTypes.speechRoleLabels[info["role"]]
			if callable(info["stateTextFunc"]):
				msg+=" "+info["stateTextFunc"](info["node"])
			if callable(info["descriptionFunc"]):
				msg+=" "+info["descriptionFunc"](info["node"])
			if info["accessKey"]:
				msg+=" "+info["accessKey"]
			return msg
		else:
			return ""

	def getIDExitMessage(self,ID):
		if not self._IDs.has_key(ID):
			return ""
		info=self._IDs[ID]
		role=info["role"]
		vbc=config.conf["documentFormatting"]
		if (role==controlTypes.ROLE_LIST and vbc["reportLists"]) or (role==controlTypes.ROLE_TABLE and vbc["reportTables"]) or (role==controlTypes.ROLE_EDITABLETEXT)  or (role==controlTypes.ROLE_BLOCKQUOTE and vbc["reportBlockQuotes"]) or (role==controlTypes.ROLE_FRAME): 
			typeString=info["typeString"] if info["typeString"] else controlTypes.speechRoleLabels[info["role"]]
			return _("out of %s")%typeString
		else:
			return ""

	def nextField(self,pos,*roles):
		if len(roles)==0:
			roles=fieldNames.keys()
		IDs=self._IDs
		posList=map(lambda x: x[0],filter(lambda x: (x is not None) and x[0]>pos,map(lambda x: IDs[x]['range'],filter(lambda x: IDs[x]["role"] in roles,IDs))))
		if len(posList)>0:
			return min(posList)
		else:
			return None

	def previousField(self,pos,*roles):
		if len(roles)==0:
			roles=fieldNames.keys()
		IDs=self._IDs
		posList=map(lambda x: x[0],filter(lambda x: (x is not None) and x[0]<pos,map(lambda x: IDs[x]['range'],filter(lambda x: IDs[x]["role"] in roles,IDs))))
		if len(posList)>0:
			return max(posList)
		else:
			return None

	def reportLabel(self,ID):
		if not self._IDs.has_key(ID):
			return
		labelID=self._IDs[ID]['labeledBy']
		if labelID is not None:
			r=self.getFullRangeFromID(labelID)
			oldReview=self.text_reviewPosition
			self.text_reviewPosition=r[0]
			self.text_reportNewPresentation(self.text_reviewPosition)
			speech.speakText(self.text_getText(r[0],r[1]))
			self.text_reviewPosition=oldReview

	def reportIDMessages(self,newIDs,oldIDs):
		msg=""
		for ID in filter(lambda x: x not in newIDs,oldIDs):
			msg+=" "+self.getIDExitMessage(ID)
		if msg and not msg.isspace():
			speech.speakMessage(msg)
			msg=""
		for ID in filter(lambda x: x not in oldIDs,newIDs):
			msg+=" "+self.getIDEnterMessage(ID)
		if msg and not msg.isspace():
			speech.speakMessage(msg)

	def text_reportNewPresentation(self,offset):
		ID=self.getIDFromPosition(offset)
		IDList=self.getIDAncestors(ID)
		IDList.append(ID)
		self.reportIDMessages(IDList,self._lastReportedIDList)
		self._lastReportedIDList=IDList
		super(virtualBuffer,self).text_reportNewPresentation(offset)

	def activatePosition(self,pos):
		pass

	def _get_text_characterCount(self):
		return len(self._textBuf)

	def text_getText(self,start=None,end=None):
		if start is None:
			start=0
		if end is None:
			end=self.text_characterCount
		return self._textBuf[start:end]

	def script_pageUp(self,keyPress):
		pageLength=config.conf["virtualBuffers"]["linesPerPage"]
		curPos=self.text_reviewPosition
		lineCount=0
		while (curPos>0) and (lineCount<=pageLength):
			curPos=curPos-1
			if self.text_getText(curPos,curPos+1)=='\n':
				lineCount+=1
		self.text_reviewPosition=curPos
		if self.text_reviewPosition==0:
			speech.speakMessage(_("top"))
		self.text_speakLine(self.text_reviewPosition)
	script_pageUp.__doc__ = _("moves one page up in the virtual buffer's current document")


	def script_pageDown(self,keyPress):
		pageLength=config.conf["virtualBuffers"]["linesPerPage"]
		curPos=self.text_reviewPosition
		lineCount=0
		while (curPos<self.text_characterCount-1) and (lineCount<=pageLength):
			curPos=curPos+1
			if self.text_getText(curPos,curPos+1)=='\n':
				lineCount+=1
		self.text_reviewPosition=curPos
		if self.text_reviewPosition>=self.text_characterCount-1:
			speech.speakMessage(_("bottom"))
		self.text_speakLine(self.text_reviewPosition)
	script_pageDown.__doc__ = _("moves one page down in the virtual buffer's current document")

	def script_activatePosition(self,keyPress):
		self.activatePosition(self.text_reviewPosition)
	script_activatePosition.__doc__ = _("activates the current object in the virtual buffer")
	
	def text_reportPresentation(self,offset):
		ID=self.getIDFromPosition(offset)
		IDs=self.getIDAncestors(ID)+[ID]
		for ID in IDs:
			info=self._IDs[ID]
			speech.speakMessage(info["typeString"])
			if callable(info["stateTextFunc"]):
				speech.speakMessage(info["stateTextFunc"](info["node"]))
			if callable(info["descriptionFunc"]):
				speech.speakMessage(info["descriptionFunc"](info["node"]))
		super(virtualBuffer,self).text_reportPresentation(offset)

	def script_nextHeading(self,keyPress):
		pos=self.nextField(self.text_reviewPosition,controlTypes.ROLE_HEADING,controlTypes.ROLE_HEADING1,controlTypes.ROLE_HEADING2,controlTypes.ROLE_HEADING3,controlTypes.ROLE_HEADING4,controlTypes.ROLE_HEADING5,controlTypes.ROLE_HEADING6)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more headings"))
	script_nextHeading.__doc__ = _("moves to the next heading")
	
	def script_previousHeading(self,keyPress):
		pos=self.previousField(self.text_reviewPosition,controlTypes.ROLE_HEADING,controlTypes.ROLE_HEADING1,controlTypes.ROLE_HEADING2,controlTypes.ROLE_HEADING3,controlTypes.ROLE_HEADING4,controlTypes.ROLE_HEADING5,controlTypes.ROLE_HEADING6)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more headings"))
	script_previousHeading.__doc__ = _("moves to the previous heading")

	def script_nextParagraph(self,keyPress):
		pos=self.nextField(self.text_reviewPosition,controlTypes.ROLE_PARAGRAPH)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more paragraphs"))
	script_nextParagraph.__doc__ = _("moves to the next paragraph")

	def script_previousParagraph(self,keyPress):
		pos=self.previousField(self.text_reviewPosition,controlTypes.ROLE_PARAGRAPH)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more paragraphs"))
	script_previousParagraph.__doc__ = _("moves to the previous paragraph")

	def script_nextTable(self,keyPress):
		pos=self.nextField(self.text_reviewPosition,controlTypes.ROLE_TABLE)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more tables"))
	script_nextTable.__doc__ = _("moves to the next table")

	def script_previousTable(self,keyPress):
		pos=self.previousField(self.text_reviewPosition,controlTypes.ROLE_TABLE)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more tables"))
	script_previousTable.__doc__ = _("moves to the previous table")

	def script_nextLink(self,keyPress):
		pos=self.nextField(self.text_reviewPosition,controlTypes.ROLE_LINK)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more links"))
	script_nextLink.__doc__ = _("moves to the next link")

	def script_previousLink(self,keyPress):
		pos=self.previousField(self.text_reviewPosition,controlTypes.ROLE_LINK)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more links"))
	script_previousLink.__doc__ = _("moves to the previous link")
	
	def script_nextList(self,keyPress):
		pos=self.nextField(self.text_reviewPosition,controlTypes.ROLE_LIST)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more lists"))
	script_nextList.__doc__ = _("moves to the next list")

	def script_previousList(self,keyPress):
		pos=self.previousField(self.text_reviewPosition,controlTypes.ROLE_LIST)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more lists"))
	script_previousList.__doc__ = _("moves to the previous list")

	def script_nextListItem(self,keyPress):
		pos=self.nextField(self.text_reviewPosition,controlTypes.ROLE_LISTITEM)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more list items"))
	script_nextListItem.__doc__ = _("moves to the next list item")

	def script_previousListItem(self,keyPress):
		pos=self.previousField(self.text_reviewPosition,controlTypes.ROLE_LISTITEM)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more list items"))
	script_previousListItem.__doc__ = _("moves to the previous list item")

	def script_nextFormField(self,keyPress):
		pos=self.nextField(self.text_reviewPosition,controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_COMBOBOX,controlTypes.ROLE_BUTTON)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more form fields"))
	script_nextFormField.__doc__ = _("Moves to the next form field")

	def script_previousFormField(self,keyPress):
		pos=self.previousField(self.text_reviewPosition,controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_RADIOBUTTON,controlTypes.ROLE_CHECKBOX,controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_COMBOBOX,controlTypes.ROLE_BUTTON)
		if isinstance(pos,int):
			self.text_reviewPosition=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewPosition))
			self.text_reportNewPresentation(self.text_reviewPosition)
			self.text_speakLine(self.text_reviewPosition)
		else:
			speech.speakMessage(_("no more form fields"))
	script_previousFormField.__doc__ = _("moves to the previous form field")

	def doFindTextDialog(self):
		findDialog=gui.scriptUI.TextEntryDialog(_("Type the text you wish to find"),title=_("Find"),default=self._lastFindText,callback=self.doFindTextDialogHelper)
		findDialog.run()

	def doFindTextDialogHelper(self,text):
	 	res=self._textBuf.find(text,self.text_reviewPosition+1)
		if res>=0:
			self.text_reviewPosition=res
			speech.cancelSpeech()
			self.text_speakLine(res)
		else:
			errorDialog=gui.scriptUI.MessageDialog(_("text: \"%s\" not found")%text,title=_("Find Error"))
			errorDialog.run()
		self._lastFindText=text

	def script_findText(self,keyPress): 
		self.doFindTextDialog()	
	script_findText.__doc__ = _("find a text pattern from the current cursor's position")

	def script_findNext(self,keyPress):
		self.doFindTextDialogHelper(self._lastFindText)
	script_findNext.__doc__ = _("find next occurrence of text")

[virtualBuffer.bindKey(keyName,scriptName) for keyName,scriptName in [
	("control+f","findText"),
	("F3","findNext"),
	("extendedDown","text_review_nextLine"),
	("extendedUp","text_review_prevLine"),
	("extendedLeft","text_review_prevCharacter"),
	("extendedRight","text_review_nextCharacter"),
	("extendedHome","text_review_startOfLine"),
	("extendedEnd","text_review_endOfLine"),
	("control+extendedLeft","text_review_prevWord"),
	("control+extendedRight","text_review_nextWord"),
	("control+extendedHome","text_review_top"),
	("control+extendedEnd","text_review_bottom"),
	("return","activatePosition"),
	("space","activatePosition"),
	("extendedPrior","pageUp"),
	("extendedNext","pageDown"),
	("%s"%_("h=headingQuickKey")[0],"nextHeading"),
	("Shift+%s"%_("h=headingQuickKey")[0],"previousHeading"),
	("%s"%_("f=formFieldQuickKey")[0],"nextFormField"),
	("Shift+%s"%_("f=formFieldQuickKey")[0],"previousFormField"),
	("%s"%_("p=paragraphQuickKey")[0],"nextParagraph"),
	("Shift+%s"%_("p=paragraphQuickKey")[0],"previousParagraph"),
	("%s"%_("t=tableQuickKey")[0],"nextTable"),
	("Shift+%s"%_("t=tableQuickKey")[0],"previousTable"),
	("%s"%_("k=linkQuickKey")[0],"nextLink"),
	("Shift+%s"%_("k=linkQuickKey")[0],"previousLink"),
	("%s"%_("l=listQuickKey")[0],"nextList"),
	("Shift+%s"%_("l=listQuickKey")[0],"previousList"),
	("%s"%_("i=listItemQuickKey")[0],"nextListItem"),
	("Shift+%s"%_("i=listItemQuickKey")[0],"previousListItem"),
]]
