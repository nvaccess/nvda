import time
import win32com.client
import debug
import winUser
import api
import audio
import NVDAObjects

def getVirtualBuffer(window):
	className=winUser.getClassName(window)
	if dynamicMap.has_key(className):
		return dynamicMap[className](window)
	elif staticMap.has_key(className):
		return staticMap[className](window)
	else:
		return virtualBuffer(window)

class virtualBuffer(object):

	def __init__(self,window):
		self.window=window
		self.text=""
		self.caret=0

	def getWindowHandle(self):
		return self.window

	def getCaretPosition(self):
		return self.caret

	def getLineCount(self):
		return -1

	def getLineNumber(self,pos):
		return -1

	def getLineStart(self,pos):
		startPos=pos
		if startPos>0 and (self.text[startPos]=='\n'):
			startPos=startPos-1
		while (startPos>-1) and (self.text[startPos]!='\n'):
			startPos-=1
		return startPos+1

	def getLineLength(self,pos):
		startPos=self.getLineStart(pos)
		endPos=startPos
		while (endPos<=self.getTextLength()) and (self.text[endPos]!='\n'):
			endPos+=1
		return (endPos-startPos)

	def getLine(self,pos):
		startPos=self.getLineStart(pos)
		length=self.getLineLength(pos)
		endPos=startPos+length
		return self.getTextRange(startPos,endPos)

	def getTextRange(self,start,end):
		if (start>=end) or (end>len(self.text)):
			return None
		return self.text[start:end]

	def getTextLength(self):
		return len(self.text)

	def getText(self):
		return self.text

class virtualBuffer_internetExplorerServer(virtualBuffer):

	clsid_shellWindows='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'

	def __init__(self,window):
		virtualBuffer.__init__(self,window)
		shellWindows=win32com.client.Dispatch(self.clsid_shellWindows)
		foundNum=0
		try:
			for i in range(100):
				if shellWindows[i].Hwnd==winUser.getForegroundWindow():
					foundNum=i
					break
		except:
			pass
		if foundNum:
			self.app=shellWindows[foundNum]
			self.dom=self.app.document
		else:
			self.app=None
			self.dom=None
		self.nodes=[]
		self.text=""

	def event_gainFocus(self,objectID,childID):
		if self.dom:
			if objectID==-4:
				self.loadDocument()
			else:
				focus=self.getFocusDomNode()
				index=self.getNodesIndexByUniqueID(self.getUniqueID(focus))
				if index==-1:
					return
				self.caret=self.nodes[index][2]

	def loadDocument(self):
		oldStatusText=None
		while self.app.busy:
			time.sleep(0.01)
			statusText=self.app.statusText
			if statusText!=oldStatusText:
				audio.cancel()
				audio.speakMessage(statusText)
				oldStatusText=statusText
		audio.speakMessage("Loading document...")
		self.addNode(self.dom.body)
		self.caret=0
		audio.cancel()
		audio.speakText(self.getText())

	def activatePosition(self,pos):
		index=self.getNodesIndexByPosition(pos)
		if index==-1:
			return
		uniqueID=self.nodes[index][0]
		domNode=self.getDomNodeByUniqueID(uniqueID)
		if not domNode:
			return
		domNode.click()

	def addNode(self,domNode):
		(nodes,text)=self.generateNode(domNode)
		self.nodes=nodes
		self.text=text

	def refreshNode(self,uniqueID):
		domNode=self.getDomNodeByUniqueID(uniqueID)
		index=self.getNodesIndexByUniqueID(uniqueID)
		preText=self.text[0:self.nodes[index][2]]
		postText=self.text[self.nodes[index][3]:]
		preNodes=self.nodes[0:index]
		postNodes=self.nodes[index+self.nodes[index][1]:]
		(newNodes,newText)=self.generateNode(domNode)
		for j in range(len(newNodes)):
			newNodes[index][2]+=len(preText)
			newNodes[index][3]+=len(preText)
		self.text=preText+newText+postText
		self.nodes=preNodes+newNodes+postNodes

	def getDomNodeByMSAA(self,objectID,childID):
		obj=NVDAObjects.getNVDAObjectByLocator(self.getWindowHandle(),objectID,childID)
		if not obj:
			return None
		(left,top,right,bottom)=obj.getLocation()
		domNode=self.dom.elementFromPoint(left,top)
		return domNode

	def getDomNodeByUniqueID(self,uniqueID):
		for num in range(self.dom.all.length):
			if int(self.dom.all[num].uniqueID[6:])==uniqueID:
				return self.dom.all[num]
		else:
			return

	def getNodesIndexByUniqueID(self,uniqueID):
		for i in range(len(self.nodes)):
			if self.nodes[i][0]==uniqueID:
				return i
		else:
			return -1

	def getFocusDomNode(self):
		return self.dom.activeElement

	def getStartTag(self,domNode):
		tagName=self.getTagName(domNode)
		if tagName=="A":
			return "\nlink "
		elif tagName=="TABLE":
			return "\ntable\n"
		elif tagName=="UL":
			return "\nlist with %s items "%domNode.Children.length
		elif tagName=="OL":
			return "\nlist with %s items "%domNode.Children.length
		elif tagName=="DL":
			return "\ndefinition list with %s items "%domNode.Children.length
		elif tagName=="LI":
			return "\n"
		elif tagName=="DT":
			return "\n"
		elif tagName=="DD":
			return "="
		elif tagName=="IMG":
			label=domNode.getAttribute('alt')
			if not label:
				label=domNode.getAttribute('src')
			return "graphic %s"%domNode.getAttribute('alt')
		elif tagName in ["H1","H2","H3","H4","H5","H6"]:
			return "\n%s "%tagName 
		elif tagName in ["BR","P","DIV"]:
			return "\n"
		elif tagName=="BLOCKQUOTE":
			return "\nblockQuote\n"
		elif tagName=="INPUT":
			type=domNode.getAttribute('type')
			if type=="hidden":
				text=""
			elif type=="text":
				text="edit %s"%domNode.getAttribute('value')
			elif type=="checkbox":
				text="checkbox "
			elif type=="radio":
				text="radioButton "
			elif type=="submit":
				text="%s button"%domNode.getAttribute('value')
			else:
				text=type
			return "\n%s\n"%text
		elif tagName=="SELECT":
			return "\nCombo box %s\n"%domNode.getAttribute('value')
		else:
			return ""

	def getEndTag(self,domNode):
		tagName=self.getTagName(domNode)
		if tagName=="A":
			return "\n"
		if tagName=="TABLE":
			return "\ntable end\n"
		elif tagName=="UL":
			return "\nlist end\n"
		elif tagName=="OL":
			return "\nlist end\n"
		elif tagName=="DL":
			return "\nlist end\n"
		elif tagName in ["P","DIV","TH","TD"]:
			return "\n"
		elif tagName=="BLOCKQUOTE":
			return "\nblockQuote end\n"
		else:
			return ""

	def getData(self,domNode):
		tagName=self.getTagName(domNode)
		if tagName=="TEXT":
			parentTagName=self.getTagName(domNode.parentNode)
		else:
			parentTagName=""
		try:
			data="%s "%domNode.data
		except:
			return ""
		if data and not data.isspace():
			return "%s "%data
		if parentTagName in ["A","B","EM","FONT","H1","H2","H3","H4","H5","h6","I","STRONG"]:
			return "%s "%data
		elif data and (not data.isspace()):
			return "\n%s "%data
		else:
			return ""

	def getUniqueID(self,domNode):
		try:
			return int(domNode.uniqueID[6:])
		except:
			return -1

	def getNodesIndexByPosition(self,pos):
		for i in range(len(self.nodes))[::-1]:
			if (pos>=self.nodes[i][2]) and (pos<=self.nodes[i][3]):
				return i
		else:
			return -1

	def getTagName(self,domNode):
		try:
			return domNode.tagName
		except:
			return "TEXT"

	def generateNode(self,domNode):
		uniqueID=self.getUniqueID(domNode)
		text=""
		nodes=[]
		text+=self.getStartTag(domNode)
		text+=self.getData(domNode)
		childCount=0
		try:
			childDomNode=domNode.firstChild
		except:
			childDomNode=None
		while childDomNode:
			childCount+=1
			(childNodes,childText)=self.generateNode(childDomNode)
			for j in range(len(childNodes)):
				childNodes[j][2]+=len(text)
				childNodes[j][3]+=len(text)
			text+=childText
			nodes+=childNodes
			try:
				childDomNode=childDomNode.nextSibling
			except:
				childDomNode=None
		text+=self.getEndTag(domNode)
		nodes.insert(0,[uniqueID,childCount,0,len(text)])
		return (nodes,text)

staticMap={
"Internet Explorer_Server":virtualBuffer_internetExplorerServer,
}

dynamicMap={}
