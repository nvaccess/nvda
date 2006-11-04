import time
import ctypes
import comtypes.automation
import comtypesClient
import debug
import winUser
import api
import audio
import NVDAObjects

runningTable={}

def isVirtualBufferWindow(window):
	return runningTable.has_key(window)

def removeVirtualBuffer(window):
	del runningTable[window]

def getVirtualBuffer(window):
	if not runningTable.has_key(window):
		className=winUser.getClassName(window)
		if dynamicMap.has_key(className):
			virtualBufferClass=dynamicMap[className]
		elif staticMap.has_key(className):
			virtualBufferClass=staticMap[className]
		else:
			virtualBufferClass=None
		if virtualBufferClass:
			virtualBufferObject=virtualBufferClass(window)
			runningTable[window]=virtualBufferObject
			return runningTable[window]
	else:
		return runningTable[window]

def registerVirtualBufferClass(windowClass,cls):
	dynamicMap[windowClass]=cls

def unregisterVirtualBufferClass(windowClass):
	del dynamicMap[windowClass]

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

	class domEventsType(object):

		def __init__(self,virtualBufferObject):
			self.virtualBufferObject=virtualBufferObject

		def ondeactivate(self,arg,event):
			debug.writeMessage("vb event onfocusout: %s"%event.srcElement)
			self.virtualBufferObject.refreshNode(event.srcElement.uniqueID)

		def onreadystatechange(self,arg,event):
			readyState=self.virtualBufferObject.dom.readyState
			if readyState!="complete":
				self.virtualBufferObject.text="Loading...\n"
				self.virtualBufferObject.nodes=[]
			else:
				self.virtualBufferObject.loadDocument()

		def __getattr__(self,name):
			pass #debug.writeMessage("vb event getattr %s"%name)

	def __init__(self,window):
		virtualBuffer.__init__(self,window)
		mshtml=comtypesClient.GetModule('mshtml.tlb')
		domPointer=ctypes.POINTER(mshtml.DispHTMLDocument)()
		debug.writeMessage("vb internetExplorer_server: domPointer %s"%domPointer)
		wm=winUser.registerWindowMessage(u'WM_HTML_GETOBJECT')
		debug.writeMessage("vb internetExplorer_server: window message %s"%wm)
		lresult=winUser.sendMessage(window,wm,0,0)
		debug.writeMessage("vb internetExplorer_server: lresult %s"%lresult)
		res=ctypes.windll.oleacc.ObjectFromLresult(lresult,ctypes.byref(domPointer._iid_),0,ctypes.byref(domPointer))
		debug.writeMessage("vb internetExplorer_server: res %s, domPointer %s"%(res,domPointer))
		self.dom=domPointer
		debug.writeMessage("vb internetExplorer_server: body %s"%self.dom.body)
		self.domEventsObject=self.domEventsType(self)
		self.eventConnection=comtypesClient.GetEvents(self.dom,self.domEventsObject,interface=mshtml.HTMLDocumentEvents2)
		self.nodes=[]
		self.text=""
		if self.dom.readyState!="complete":
			self.text="Loading...\n"
		else:
			self.loadDocument()

	def event_gainFocus(self,objectID,childID):
		if len(self.nodes)==0:
			return
		focusDomNode=self.getFocusDomNode()
		uniqueID=self.getUniqueID(focusDomNode)
		index=self.getNodesIndexByUniqueID(uniqueID)
		if index==-1:
			return
		self.caret=self.nodes[index][2]

	def loadDocument(self):
		if self.getWindowHandle()==api.getFocusLocator()[0]:
			audio.speakMessage("Loading document...")
		self.addNode(self.dom.body)
		self.caret=0
		if self.getWindowHandle()==api.getFocusLocator()[0]:
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
		debug.writeMessage("refresh node uniqueID %s"%uniqueID)
		domNode=self.getDomNodeByUniqueID(uniqueID)
		debug.writeMessage("refresh node domNode %s"%domNode)
		index=self.getNodesIndexByUniqueID(uniqueID)
		debug.writeMessage("refresh node index %s"%index)
		preText=self.text[0:self.nodes[index][2]]
		postText=self.text[self.nodes[index][3]:]
		preNodes=self.nodes[0:index]
		postNodes=self.nodes[index+self.nodes[index][1]:]
		(newNodes,newText)=self.generateNode(domNode)
		if (len(preText)>0) and (len(newText)>0) and (preText[-1]=='\n') and (newText[0]=='\n'):
			preText=preText[:-1]
		for j in range(len(newNodes)):
			newNodes[j][2]+=len(preText)
			newNodes[j][3]+=len(preText)
		self.text=preText+newText+postText
		audio.speakMessage(self.text)
		self.nodes=preNodes+newNodes+postNodes

	def getDomNodeByMSAA(self,objectID,childID):
		obj=NVDAObjects.getNVDAObjectByLocator(self.getWindowHandle(),objectID,childID)
		if not obj:
			return None
		(left,top,right,bottom)=obj.getLocation()
		domNode=self.dom.elementFromPoint(left,top)
		return domNode

	def getDomNodeByUniqueID(self,uniqueID):
		return self.dom.getElementById(uniqueID)

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
			return "\nlist with %s items "%domNode.children.length
		elif tagName=="OL":
			return "\nlist with %s items "%domNode.children.length
		elif tagName=="DL":
			return "\ndefinition list with %s items "%domNode.children.length
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
				if domNode.checked:
					text+="checked "
			elif type=="radio":
				text="radioButton "
				if domNode.checked:
					text+="checked "
			elif type=="submit":
				text="%s button"%domNode.getAttribute('value')
			else:
				text=type
			return "\n%s\n"%text
		elif tagName=="SELECT":
			#item seems to return an IDispatch that hasn't been wrapped in a comtypes typelib automatically yet.
			itemText=comtypesClient.wrap(domNode.item(domNode.selectedIndex)).text
			return "\nCombo box %s\n"%itemText
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
		if not data or data.isspace():
			return ""
		if parentTagName in ["OPTION"]:
			return ""
		return "%s "%data

	def getUniqueID(self,domNode):
		try:
			return domNode.uniqueID
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
			if (len(text)>0) and (len(childText)>0) and (text[-1]=='\n') and (childText[0]=='\n'):
				text=text[:-1]
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
		if (len(text)>0) and (text[0]=='\n'):
			start=1
		else:
			start=0
		nodes.insert(0,[uniqueID,childCount,start,len(text)])
		return (nodes,text)

staticMap={
"Internet Explorer_Server":virtualBuffer_internetExplorerServer,
}

dynamicMap={}
