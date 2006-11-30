import time
import ctypes
import comtypesClient
import comtypes.automation
import core
import MSAAHandler
import debug
import winUser
from constants import *
import api
import audio
import baseType

class virtualBuffer_MSHTML(baseType.virtualBuffer):

	class domEventsType(object):

		def __init__(self,virtualBufferObject):
			self.virtualBufferObject=virtualBufferObject

		def ondeactivate(self,arg,event):
			domNode=event.srcElement
			if domNode.tagName not in ["INPUT","SELECT","TEXTAREA"]:
				return
			ID=domNode.uniqueID
			IDs=self.virtualBufferObject.getIDsFromID(ID)
			if not IDs:
				return
			r=self.virtualBufferObject.getRangeFromID(ID)
			self.virtualBufferObject.removeText(ID)
			text=self.virtualBufferObject.getDomNodeText(domNode)
			if text:
				self.virtualBufferObject.insertText(r[0],IDs,text)

		def onreadystatechange(self,arg,event):
			audio.speakMessage("ready state changed")
			if self.virtualBufferObject.isDocumentComplete():
				self.virtualBufferObject.loadDocument()

		def onload(self,arg,event):
			audio.speakMessage("load")

	def __init__(self,NVDAObject):
		baseType.virtualBuffer.__init__(self,NVDAObject)
		#We sometimes need to cast com interfaces to another type so we need access directly to the MSHTML typelib
		self.MSHTMLLib=comtypesClient.GetModule('mshtml.tlb')
		#Create a html document com pointer and point it to the com object we receive from the internet explorer_server window
		domPointer=ctypes.POINTER(self.MSHTMLLib.DispHTMLDocument)()
		debug.writeMessage("vb internetExplorer_server: domPointer %s"%domPointer)
		wm=winUser.registerWindowMessage(u'WM_HTML_GETOBJECT')
		debug.writeMessage("vb internetExplorer_server: window message %s"%wm)
		lresult=winUser.sendMessage(NVDAObject.hwnd,wm,0,0)
		debug.writeMessage("vb internetExplorer_server: lresult %s"%lresult)
		res=ctypes.windll.oleacc.ObjectFromLresult(lresult,ctypes.byref(domPointer._iid_),0,ctypes.byref(domPointer))
		debug.writeMessage("vb internetExplorer_server: res %s, domPointer %s"%(res,domPointer))
		self.dom=domPointer
		debug.writeMessage("vb internetExplorer_server: body %s"%self.dom.body)
		#Set up events for the document, plus any sub frames
		self.domEventsObject=self.domEventsType(self)
		self._eventHolder=[]
		self._eventHolder.append(comtypesClient.GetEvents(self.dom,self.domEventsObject,interface=self.MSHTMLLib.HTMLDocumentEvents2))
		for frameNum in range(self.dom.frames.length):
			self._eventHolder.append(comtypesClient.GetEvents(self.dom.frames.item(frameNum).document,self.domEventsObject,interface=self.MSHTMLLib.HTMLDocumentEvents2))
		if self.isDocumentComplete():
			self.loadDocument()

	def event_gainFocus(self,hwnd,objectID,childID):
		if not self._allowCaretMovement:
			return
		domNode=self.dom.activeElement
		ID=domNode.uniqueID
		r=self.getRangeFromID(ID)
		if (r is not None) and (len(r)==2) and ((self.caretPosition<r[0]) or (self.caretPosition>r[1])):
			self.caretPosition=r[0]

	def loadDocument(self):
		if winUser.getAncestor(self.NVDAObject.hwnd,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			if api.isVirtualBufferPassThrough():
				api.toggleVirtualBufferPassThrough()
			audio.speakMessage(_("Loading document")+" "+self.dom.title+"...")
		self.resetBuffer()
		self._text="%s\n \n"%self.dom.title
		if self.dom.body.tagName=="FRAMESET":
			for frameNum in range(self.dom.frames.length):
				self._text+="%s frame\n"%self.dom.frames.item(frameNum).document.title
				self.fillBuffer(self.dom.frames.item(frameNum).document.body,())
				self._text+="%s frame end\n"%self.dom.frames.item(frameNum).document.title
		else:
			self.fillBuffer(self.dom.body,())
		self.caretPosition=0
		if winUser.getAncestor(self.NVDAObject.hwnd,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			self.caretPosition=0
			self._allowCaretMovement=False #sayAllGenerator will set this back to true when done
			core.newThread(self.sayAllGenerator())

	def activatePosition(self,pos):
		IDs=self.getIDsFromPosition(pos)
		if (IDs is None) or (len(IDs)<1):
			return
		domNode=self.getDomNodeFromID(IDs[-1])
		if domNode is None:
			return
		try:
			domNode.click()
		except:
			pass
		if domNode.tagName in ["INPUT","SELECT","TEXTAREA"]:
			domNode.focus()
			if not api.isVirtualBufferPassThrough() and not ((domNode.tagName=="INPUT") and (domNode.getAttribute('type') in["checkbox","radio"])): 
				api.toggleVirtualBufferPassThrough()
		elif domNode.tagName=="A":
			domNode.focus()

	def isDocumentComplete(self):
		documentComplete=True
		if self.dom.readyState!="complete":
			documentComplete=False
		for frameNum in range(self.dom.frames.length):
			if self.dom.frames.item(frameNum).document.readyState!="complete":
				documentComplete=False
		return documentComplete

	def fillBuffer(self,domNode,IDAncestors):
		if isinstance(domNode,ctypes.POINTER(self.MSHTMLLib.DispHTMLCommentElement)):
			return
		try:
			if domNode.tagName not in ["B","CENTER","EM","FONT","I","SPAN","STRONG","SUP","U"]:
				ID=domNode.uniqueID
				if ID not in IDAncestors:
					IDAncestors=tuple(list(IDAncestors)+[ID])
			else:
				ID=None
		except:
			pass
		text=self.getDomNodeText(domNode)
		if text:
			self.appendText(IDAncestors,text)
		child=domNode.firstChild
		while child:
			self.fillBuffer(child,IDAncestors)
			child=child.nextSibling

	def updateBuffer(self,domNode,pos):
		ID=domNode.uniqueID
		self.removeText(ID)
		(domNodeID,domNodeText)=self.getDomNodeTextAndID(domNode)
		self.insertText(pos,domNodeID,domNodeText)
		endPos=pos+len(domNodeText)
		child=domNode.firstChild
		while child:
			endPos=self.updateBuffer(child,endPos)
			child=child.nextSibling
		return endPos

	def getDomNodeFromID(self,ID):
		if ID is None:
			return None
		domNode=None
		if self.dom.body.tagName=="FRAMESET":
			for frameNum in range(self.dom.frames.length):
				try:
					domNode=self.dom.frames.item(frameNum).document.getElementById(ID)
					break
				except:
					pass
		else:
			try:
				domNode=self.dom.getElementById(ID)
			except:
				domNode=None
		if not domNode:
			return None
		#Usually we get back a generic IHTMLElement interface, which isn't specific to the element, we we have to let comtypes wrap it  with the correct interface
		domNode=comtypesClient.wrap(ctypes.cast(domNode,ctypes.POINTER(comtypes.automation.IDispatch)))
		return domNode

	def getIDFromDomNode(self,domNode):
		try:
			ID=domNode.uniqueID
			debug.writeMessage("vb mshtml IDFromDomNode %s from %s"%(ID,domNode.tagName))
		except:
			debug.writeMessage("vb mshtml IDFromDomNode failed on %s"%domNode)
			ID=None
		return ID

	def getDomNodeText(self,domNode):
		try:
			data=domNode.data
			parentNode=domNode.parentNode
			parentTagName=parentNode.tagName
			parentUniqueID=parentNode.uniqueID
		except:
			data=None
			parentNode=None
			parentTagName=None
			parentUniqueID=None
		try:
			tagName=domNode.tagName
			uniqueID=domNode.uniqueID
		except:
			tagName=None
			uniqueID=None
		if data and not data.isspace() and parentNode and (parentTagName not in ["OPTION"]):
			return data
		if tagName=="IMG":
			label=domNode.getAttribute('alt')
			if not label:
				label=domNode.getAttribute('src')
			return label
		elif tagName=="SELECT":
			itemText=comtypesClient.wrap(domNode.item(domNode.selectedIndex)).text
			return itemText
		elif tagName=="INPUT":
			inputType=domNode.getAttribute('type')
			if inputType=="text":
				return domNode.getAttribute('value')+" "
			elif inputType in ["button","reset","submit"]:
				return domNode.getAttribute('value')
			elif inputType in ["checkbox","radio"]:
				return " "

	def getIDEnterMessage(self,ID):
		domNode=self.getDomNodeFromID(ID)
		if not domNode:
			return ""
		tagName=domNode.tagName
		if tagName=="A":
			return MSAAHandler.getRoleName(ROLE_SYSTEM_LINK)
		elif tagName=="UL":
			return MSAAHandler.getRoleName(ROLE_SYSTEM_LIST)+" with %s items"%domNode.children.length
		elif tagName=="LI":
			return MSAAHandler.getRoleName(ROLE_SYSTEM_LISTITEM)
		elif tagName=="TEXTAREA":
			return MSAAHandler.getRoleName(ROLE_SYSTEM_TEXT)
		elif tagName=="STRONG":
			return _("strong")
		elif tagName=="EM":
			return _("emphisized")
		elif tagName=="IMG":
			return MSAAHandler.getRoleName(ROLE_SYSTEM_GRAPHIC)
		elif tagName in ["H1","H2","H3","H4","H5","H6"]:
			return _("heading")+" %s"%tagName[1]
		elif tagName=="BLOCKQUOTE":
			return _("block quote")
		elif tagName=="INPUT":
			inputType=domNode.getAttribute("type")
			if inputType=="text":
				return MSAAHandler.getRoleName(ROLE_SYSTEM_TEXT)
			elif inputType in ["button","reset","submit"]:
				return MSAAHandler.getRoleName(ROLE_SYSTEM_PUSHBUTTON)
			elif inputType=="radio":
				try:
					if domNode.checked:
						state=MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)
					else:
						state=_("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)
				except:
					state=""
				return MSAAHandler.getRoleName(ROLE_SYSTEM_RADIOBUTTON)+" "+state
			elif inputType=="checkbox":
				try:
					if domNode.checked:
						state=MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)
					else:
						state=_("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)
				except:
					state=""
				return MSAAHandler.getRoleName(ROLE_SYSTEM_CHECKBUTTON)+" "+state
		elif tagName=="SELECT":
			return MSAAHandler.getRoleName(ROLE_SYSTEM_COMBOBOX)
		else:
			return ""

	def getIDExitMessage(self,ID):
		domNode=self.getDomNodeFromID(ID)
		outOf=_("out of")
		tagName=domNode.tagName
		if tagName=="UL":
			return outOf+" "+MSAAHandler.getRoleName(ROLE_SYSTEM_LIST)
		elif tagName=="BLOCKQUOTE":
			return outOf+" "+_("block quote")
		else:
			return ""

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

