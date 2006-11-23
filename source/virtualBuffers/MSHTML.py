import time
import ctypes
import comtypesClient
import debug
import winUser
from constants import *
import audio
import baseType

class virtualBuffer_MSHTML(baseType.virtualBuffer):

	class domEventsType(object):

		def __init__(self,virtualBufferObject):
			self.virtualBufferObject=virtualBufferObject

		def ondeactivate(self,arg,event):
			debug.writeMessage("vb event ondeactive: %s"%event.srcElement)
			#self.virtualBufferObject.refreshNode(event.srcElement.uniqueID)

		def onreadystatechange(self,arg,event):
			readyState=self.virtualBufferObject.dom.readyState
			if readyState!="complete":
				self.virtualBufferObject.text="Loading...\n"
				self.virtualBufferObject.nodes=[]
			else:
				self.virtualBufferObject.loadDocument()

		def __getattr__(self,name):
			pass #debug.writeMessage("vb event getattr %s"%name)

	def __init__(self,NVDAObject):
		baseType.virtualBuffer.__init__(self,NVDAObject)
		MSHTMLLib=comtypesClient.GetModule('mshtml.tlb')
		domPointer=ctypes.POINTER(MSHTMLLib.DispHTMLDocument)()
		debug.writeMessage("vb internetExplorer_server: domPointer %s"%domPointer)
		wm=winUser.registerWindowMessage(u'WM_HTML_GETOBJECT')
		debug.writeMessage("vb internetExplorer_server: window message %s"%wm)
		lresult=winUser.sendMessage(NVDAObject.hwnd,wm,0,0)
		debug.writeMessage("vb internetExplorer_server: lresult %s"%lresult)
		res=ctypes.windll.oleacc.ObjectFromLresult(lresult,ctypes.byref(domPointer._iid_),0,ctypes.byref(domPointer))
		debug.writeMessage("vb internetExplorer_server: res %s, domPointer %s"%(res,domPointer))
		self.dom=domPointer
		debug.writeMessage("vb internetExplorer_server: body %s"%self.dom.body)
		self.domEventsObject=self.domEventsType(self)
		self.eventConnection=comtypesClient.GetEvents(self.dom,self.domEventsObject,interface=MSHTMLLib.HTMLDocumentEvents2)
		self.nodes=[]
		self.text=""
		if self.dom.readyState!="complete":
			self.text="Loading...\n"
		else:
			self.loadDocument()

	def event_gainFocus(self,hwnd,objectID,childID):
		if len(self.nodes)==0:
			return
		focusDomNode=self.getFocusDomNode()
		uniqueID=self.getUniqueID(focusDomNode)
		index=self.getNodesIndexByUniqueID(uniqueID)
		if index==-1:
			return
		self.caretPosition=self.nodes[index][2]

	def loadDocument(self):
		if winUser.getAncestor(self.NVDAObject.hwnd,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			audio.speakMessage(_("Loading document")+" "+self.dom.title+"...")
		self.addNode(self.dom.body)
		self.caretPosition=0
		if winUser.getAncestor(self.NVDAObject.hwnd,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			audio.speakText(self.text)

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
		if len(text)>0 and (text[0]=='\n'):
			text=text[1:]
			for num in range(len(nodes)):
				nodes[num][2]-=1
				nodes[num][3]-=1
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
		for j in range(len(postNodes)):
			postNodes[j][2]=postNodes[0][2]+len(preText)+len(newText)
			postNodes[j][3]=postNodes[0][3]+len(preText)+len(newText)
		self.text=preText+newText+postText
		self.nodes=preNodes+newNodes+postNodes

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

