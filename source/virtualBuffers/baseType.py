#virtualBuffers/baseType.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from textwrap import TextWrapper
from keyUtils import key
import audio
import globalVars
import debug
import config
import NVDAObjects

fieldType_other=0
fieldType_button=1
fieldType_link=2
fieldType_list=3
fieldType_listItem=4
fieldType_heading=5
fieldType_table=6
fieldType_row=7
fieldType_column=8
fieldType_edit=9
fieldType_comboBox=10
fieldType_graphic=11
fieldType_frame=12
fieldType_document=13
fieldType_blockQuote=14
fieldType_paragraph=15
fieldType_form=16
fieldType_checkBox=17
fieldType_radioButton=18
fieldType_editArea=19
fieldType_cell=20
fieldType_tableHeader=21
fieldType_tableFooter=22
fieldType_tableBody=23

fieldNames={
	fieldType_other:"",
	fieldType_button:_("button"),
	fieldType_link:_("link"),
	fieldType_list:_("list"),
	fieldType_listItem:_("list item"),
	fieldType_heading:_("heading"),
	fieldType_table:_("table"),
	fieldType_row:_("row"),
	fieldType_column:_("column"),
	fieldType_edit:_("edit"),
	fieldType_comboBox:_("combo box"),
	fieldType_graphic:_("graphic"),
	fieldType_frame:_("frame"),
	fieldType_document:_("document"),
	fieldType_blockQuote:_("block quote"),
	fieldType_paragraph:_("paragraph"),
	fieldType_form:_("form"),
	fieldType_checkBox:_("check box"),
	fieldType_radioButton:_("radio button"),
	fieldType_editArea:_("edit area"),
	fieldType_cell:_("cell"),
	fieldType_tableHeader:_("table header"),
	fieldType_tableFooter:_("table footer"),
	fieldType_tableBody:_("table body"),
}

fieldInfo={
	"fieldType":fieldType_other,
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

class virtualBuffer(NVDAObjects.baseType.NVDAObject):

	def __init__(self,NVDAObject):
		self.needsLoad=True
		self.NVDAObject=NVDAObject
		self._keyMap={}
		self._IDs={}
		self._text_lastReportedPresentation={}
		self._textBuf=""
		self._lastReportedIDList=[]
		self.registerScriptKeys({
			key("extendedDown"):self.script_text_review_nextLine,
			key("extendedUp"):self.script_text_review_prevLine,
			key("extendedLeft"):self.script_text_review_prevCharacter,
			key("extendedRight"):self.script_text_review_nextCharacter,
			key("extendedHome"):self.script_text_review_startOfLine,
			key("extendedEnd"):self.script_text_review_endOfLine,
			key("control+extendedLeft"):self.script_text_review_prevWord,
			key("control+extendedRight"):self.script_text_review_nextWord,
			key("control+extendedHome"):self.script_text_review_top,
			key("control+extendedEnd"):self.script_text_review_bottom,
			key("return"):self.script_activatePosition,
			key("space"):self.script_activatePosition,
			key("extendedPrior"):self.script_pageUp,
			key("extendedNext"):self.script_pageDown,
			key("%s"%_("h=headingQuickKey")[0]):self.script_nextHeading,
			key("Shift+%s"%_("h=headingQuickKey")[0]):self.script_previousHeading,
			key("%s"%_("f=formFieldQuickKey")[0]):self.script_nextFormField,
			key("Shift+%s"%_("f=formFieldQuickKey")[0]):self.script_previousFormField,
			key("%s"%_("p=paragraphQuickKey")[0]):self.script_nextParagraph,
			key("Shift+%s"%_("p=paragraphQuickKey")[0]):self.script_previousParagraph,
			key("%s"%_("t=tableQuickKey")[0]):self.script_nextTable,
			key("Shift+%s"%_("t=tableQuickKey")[0]):self.script_previousTable,
			key("%s"%_("k=linkQuickKey")[0]):self.script_nextLink,
			key("Shift+%s"%_("k=linkQuickKey")[0]):self.script_previousLink,
			key("%s"%_("l=listQuickKey")[0]):self.script_nextList,
			key("Shift+%s"%_("l=listQuickKey")[0]):self.script_previousList,
			key("%s"%_("i=listItemQuickKey")[0]):self.script_nextListItem,
			key("Shift+%s"%_("i=listItemQuickKey")[0]):self.script_previousListItem,
		})

	def getIDFromPosition(self,pos):
		IDs=self._IDs
		shortList=filter(lambda x: pos>=IDs[x]['range'][0] and pos<IDs[x]['range'][1],IDs)
		return min(shortList,key=lambda x: IDs[x]['range'][1]-IDs[x]['range'][0]) if shortList else None

	def getFullRangeFromID(self,ID):
		IDs=self._IDs
		if not IDs.has_key(ID):
			return None
		children=filter(lambda x: x is not None and IDs.has_key(x),IDs[ID]['children'])
		#debug.writeMessage("virtualBuffers.baseType.getFullRangeFromID: ID %s, children %s"%(ID,children))
		if len(children)==0:
			#debug.writeMessage("virtualBuffers.baseType.getFullRangeFromID: ID %s, range %s"%(ID,IDs[ID]['range']))
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
		while IDs[curID]['parent']:
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
			childNum=IDs[parentID]['children'].index(ID)
			zOrder.insert(0,childNum)
			ID=parentID
		return zOrder

	def addText(self,ID,text,position=None):
		isAppending=False
		isMurging=False
		text=text.replace('\r\n','\n')
		text=text.replace('\r','\n')
		maxLineLength=config.conf["virtualBuffers"]["maxLineLength"]
		if len(text)>maxLineLength:
			wrapper = TextWrapper(width=config.conf["virtualBuffers"]["maxLineLength"], expand_tabs=False, replace_whitespace=False, break_long_words=False)
		 	text=wrapper.fill(text)
		bufLen=self.text_characterCount
		textLen=len(text)
		IDs=self._IDs
		#If no position given, assume end of buffer
		if position is None:
			position=bufLen
			isAppending=True
		#If this ID path already has a range, expand it to fit the new text
		r=IDs[ID]['range']
		if (r[1]==position) and (r[1]>r[0]):
			position=position-1
			isMurging=True
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
		self.text_reviewOffset=0
		self._lastCaretIDs=[]

	def addID(self,ID,info):
		self._IDs[ID]=info

	def getIDEnterMessage(self,ID):
		if not self._IDs.has_key(ID):
			return ""
		info=self._IDs[ID]
		fieldType=info["fieldType"]
		vbc=config.conf["virtualBuffers"]
		if (fieldType==fieldType_link and vbc["reportLinks"]) or (fieldType==fieldType_list and vbc["reportLists"]) or (fieldType==fieldType_listItem and vbc["reportListItems"]) or (fieldType==fieldType_heading and vbc["reportHeadings"]) or (fieldType==fieldType_table and vbc["reportTables"]) or (fieldType==fieldType_tableHeader and vbc["reportTables"]) or (fieldType==fieldType_tableFooter and vbc["reportTables"]) or (fieldType==fieldType_row and vbc["reportTables"]) or (fieldType==fieldType_cell and vbc["reportTables"]) or (fieldType==fieldType_graphic and vbc["reportGraphics"]) or (fieldType==fieldType_form and vbc["reportForms"]) or ((fieldType in [fieldType_button,fieldType_edit,fieldType_editArea,fieldType_checkBox,fieldType_radioButton,fieldType_comboBox]) and vbc["reportFormFields"]) or (fieldType==fieldType_paragraph and vbc["reportParagraphs"]) or (fieldType==fieldType_blockQuote and vbc["reportBlockQuotes"]) or (fieldType==fieldType_frame and vbc["reportFrames"]):
			msg=info["typeString"]
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
		fieldType=info["fieldType"]
		vbc=config.conf["virtualBuffers"]
		if (fieldType==fieldType_list and vbc["reportLists"]) or (fieldType==fieldType_table and vbc["reportTables"]) or (fieldType==fieldType_form and vbc["reportForms"]) or (fieldType==fieldType_editArea and vbc["reportFormFields"]) or (fieldType==fieldType_blockQuote and vbc["reportBlockQuotes"]) or (fieldType==fieldType_paragraph and vbc["reportParagraphs"]) or (fieldType==fieldType_frame and vbc["reportFrames"]):
			return _("out of %s")%info["typeString"]
		else:
			return ""

	def nextField(self,pos,*fieldTypes):
		if len(fieldTypes)==0:
			fieldTypes=fieldNames.keys()
		IDs=self._IDs
		posList=map(lambda x: x[0],filter(lambda x: (x is not None) and x[0]>pos,map(lambda x: IDs[x]['range'],filter(lambda x: IDs[x]["fieldType"] in fieldTypes,IDs))))
		if len(posList)>0:
			return min(posList)
		else:
			return None

	def previousField(self,pos,*fieldTypes):
		if len(fieldTypes)==0:
			fieldTypes=fieldNames.keys()
		IDs=self._IDs
		posList=map(lambda x: x[0],filter(lambda x: (x is not None) and x[0]<pos,map(lambda x: IDs[x]['range'],filter(lambda x: IDs[x]["fieldType"] in fieldTypes,IDs))))
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
			oldReview=self.text_reviewOffset
			self.text_reviewOffset=r[0]
			self.text_reportNewPresentation(self.text_reviewOffset)
			audio.speakText(self.text_getText(r[0],r[1]))
			self.text_reviewOffset=oldReview

	def reportIDMessages(self,newIDs,oldIDs):
		msg=""
		for ID in filter(lambda x: x not in newIDs,oldIDs):
			msg+=" "+self.getIDExitMessage(ID)
		if msg and not msg.isspace():
			audio.speakMessage(msg)
			msg=""
		for ID in filter(lambda x: x not in oldIDs,newIDs):
			msg+=" "+self.getIDEnterMessage(ID)
		if msg and not msg.isspace():
			audio.speakMessage(msg)

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

	def script_pageUp(self,keyPress,nextScript):
		pageLength=config.conf["virtualBuffers"]["linesPerPage"]
		curPos=self.text_reviewOffset
		lineCount=0
		while (curPos>0) and (lineCount<=pageLength):
			curPos=curPos-1
			if self.text_getText(curPos,curPos+1)=='\n':
				lineCount+=1
		self.text_reviewOffset=curPos
		if self.text_reviewOffset==0:
			audio.speakMessage(_("top"))
		self.text_speakLine(self.text_reviewOffset)

	def script_pageDown(self,keyPress,nextScript):
		pageLength=config.conf["virtualBuffers"]["linesPerPage"]
		curPos=self.text_reviewOffset
		lineCount=0
		while (curPos<self.text_characterCount-1) and (lineCount<=pageLength):
			curPos=curPos+1
			if self.text_getText(curPos,curPos+1)=='\n':
				lineCount+=1
		self.text_reviewOffset=curPos
		if self.text_reviewOffset>=self.text_characterCount-1:
			audio.speakMessage(_("bottom"))
		self.text_speakLine(self.text_reviewOffset)

	def script_activatePosition(self,keyPress,nextScript):
		self.activatePosition(self.text_reviewOffset)

	def text_reportPresentation(self,offset):
		ID=self.getIDFromPosition(offset)
		IDs=self.getIDAncestors(ID)+[ID]
		for ID in IDs:
			info=self._IDs[ID]
			audio.speakMessage(info["typeString"])
			debug.writeMessage("ID typeString: %s"%info["typeString"])
			if callable(info["stateTextFunc"]):
				audio.speakMessage(info["stateTextFunc"](info["node"]))
			if callable(info["descriptionFunc"]):
				audio.speakMessage(info["descriptionFunc"](info["node"]))
		super(virtualBuffer,self).text_reportPresentation(offset)

	def script_nextHeading(self,keyPress,nextScript):
		pos=self.nextField(self.text_reviewOffset,fieldType_heading)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more headings"))

	def script_previousHeading(self,keyPress,nextScript):
		pos=self.previousField(self.text_reviewOffset,fieldType_heading)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more headings"))

	def script_nextParagraph(self,keyPress,nextScript):
		pos=self.nextField(self.text_reviewOffset,fieldType_paragraph)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more paragraphs"))

	def script_previousParagraph(self,keyPress,nextScript):
		pos=self.previousField(self.text_reviewOffset,fieldType_paragraph)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more paragraphs"))

	def script_nextTable(self,keyPress,nextScript):
		pos=self.nextField(self.text_reviewOffset,fieldType_table)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more tables"))

	def script_previousTable(self,keyPress,nextScript):
		pos=self.previousField(self.text_reviewOffset,fieldType_table)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more tables"))

	def script_nextLink(self,keyPress,nextScript):
		pos=self.nextField(self.text_reviewOffset,fieldType_link)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more links"))

	def script_previousLink(self,keyPress,nextScript):
		pos=self.previousField(self.text_reviewOffset,fieldType_link)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more links"))

	def script_nextList(self,keyPress,nextScript):
		pos=self.nextField(self.text_reviewOffset,fieldType_list)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more lists"))

	def script_previousList(self,keyPress,nextScript):
		pos=self.previousField(self.text_reviewOffset,fieldType_list)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more lists"))

	def script_nextListItem(self,keyPress,nextScript):
		pos=self.nextField(self.text_reviewOffset,fieldType_listItem)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more list items"))

	def script_previousListItem(self,keyPress,nextScript):
		pos=self.previousField(self.text_reviewOffset,fieldType_listItem)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more list items"))

	def script_nextFormField(self,keyPress,nextScript):
		pos=self.nextField(self.text_reviewOffset,fieldType_edit,fieldType_radioButton,fieldType_checkBox,fieldType_editArea,fieldType_comboBox,fieldType_button)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more form fields"))

	def script_previousFormField(self,keyPress,nextScript):
		pos=self.previousField(self.text_reviewOffset,fieldType_edit,fieldType_radioButton,fieldType_checkBox,fieldType_editArea,fieldType_comboBox,fieldType_button)
		if isinstance(pos,int):
			self.text_reviewOffset=pos
			self.reportLabel(self.getIDFromPosition(self.text_reviewOffset))
			self.text_reportNewPresentation(self.text_reviewOffset)
			self.text_speakLine(self.text_reviewOffset)
		else:
			audio.speakMessage(_("no more form fields"))

