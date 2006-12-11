import time
import thread
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
			if domNode.nodeName not in ["INPUT","SELECT","TEXTAREA"]:
				return
			ID=self.virtualBufferObject.getDomNodeID(domNode)
			IDs=self.virtualBufferObject.getIDsFromID(ID)
			(start,end)=self.virtualBufferObject.getRangeFromID(ID)
			self.virtualBufferObject.removeID(ID)
			self.virtualBufferObject.fillBuffer(domNode,IDs,position=start)


		def onreadystatechange(self,arg,event):
			if self.virtualBufferObject.isDocumentComplete():
				self.virtualBufferObject.loadDocument()

	def __init__(self,NVDAObject):
		#We sometimes need to cast com interfaces to another type so we need access directly to the MSHTML typelib
		self.MSHTMLLib=comtypesClient.GetModule('mshtml.tlb')
		#Create a html document com pointer and point it to the com object we receive from the internet explorer_server window
		#domPointer=ctypes.POINTER(self.MSHTMLLib.DispHTMLDocument)()
		domPointer=ctypes.POINTER(comtypes.automation.IDispatch)()
		debug.writeMessage("vb internetExplorer_server: domPointer %s"%domPointer)
		wm=winUser.registerWindowMessage(u'WM_HTML_GETOBJECT')
		debug.writeMessage("vb internetExplorer_server: window message %s"%wm)
		lresult=winUser.sendMessage(NVDAObject.windowHandle,wm,0,0)
		debug.writeMessage("vb internetExplorer_server: lresult %s"%lresult)
		res=ctypes.windll.oleacc.ObjectFromLresult(lresult,ctypes.byref(domPointer._iid_),0,ctypes.byref(domPointer))
		debug.writeMessage("vb internetExplorer_server: res %s, domPointer %s"%(res,domPointer))
		self.dom=comtypesClient.wrap(domPointer)
		debug.writeMessage("vb internetExplorer_server: domPointer %s"%self.dom)
		debug.writeMessage("vb internetExplorer_server: body %s"%self.dom.body)
		baseType.virtualBuffer.__init__(self,NVDAObject)
		#Set up events for the document, plus any sub frames
		self.domEventsObject=self.domEventsType(self)
		comtypesClient.GetEvents(self.dom,self.domEventsObject,interface=self.MSHTMLLib.HTMLDocumentEvents2)
		if self.isDocumentComplete():
			self.loadDocument()

	def event_MSAA_gainFocus(self,hwnd,objectID,childID):
		nodeName=self.dom.activeElement.nodeName
		if (self.dom.body.isContentEditable is False) and (nodeName not in ["INPUT","SELECT","TEXTAREA"]) and api.isVirtualBufferPassThrough():
			api.toggleVirtualBufferPassThrough()
		if not self._allowCaretMovement:
			return
		domNode=self.dom.activeElement
		ID=self.getDomNodeID(domNode)
		r=self.getRangeFromID(ID)
		if (r is not None) and (len(r)==2) and ((self.caretPosition<r[0]) or (self.caretPosition>=r[1])):
			self.caretPosition=r[0]

	def activatePosition(self,pos):
		IDs=self.getIDsFromPosition(pos)
		if (IDs is None) or (len(IDs)<1):
			return
		domNode=self._IDs[IDs[-1]]["node"]
		if domNode is None:
			return
		nodeName=domNode.nodeName
		nodeInfo=self.getDomNodeInfo(domNode)
		if nodeName in ["SELECT","TEXTAREA"]:
			if not api.isVirtualBufferPassThrough() and not ((nodeName=="INPUT") and (domNode.getAttribute('type') in["checkbox","radio"])): 
				api.toggleVirtualBufferPassThrough()
			domNode.focus()
		elif nodeName =="INPUT":
			inputType=domNode.getAttribute('type')
			if inputType in ["checkbox","radio"]:
				domNode.click()
				audio.speakMessage("%s"%(MSAAHandler.getStateName(STATE_SYSTEM_CHECKED) if domNode.checked else _("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)))
			elif inputType in ["text","password"]:
				if not api.isVirtualBufferPassThrough() and not ((nodeName=="INPUT") and (domNode.getAttribute('type') in["checkbox","radio"])): 
					api.toggleVirtualBufferPassThrough()
				domNode.focus()
			elif inputType in ["button","image","reset","submit"]:
				domNode.click()
		elif (nodeName in ["A","IMG"]) or domNode.onclick:
			domNode.click()
			try:
				domNode.focus()
			except:
				pass

	def loadDocument(self):
		if self.dom.body.isContentEditable is True: #This is an editable document and will not be managed by this virtualBuffer
			return
		if winUser.getAncestor(self.NVDAObject.windowHandle,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			if api.isVirtualBufferPassThrough():
				api.toggleVirtualBufferPassThrough()
			audio.speakMessage(_("Loading document")+" "+self.dom.title+"...")
		self.resetBuffer()
		self.fillBuffer(self.dom)
		self.caretPosition=0
		if winUser.getAncestor(self.NVDAObject.windowHandle,GA_ROOT)==winUser.getForegroundWindow():
			audio.cancel()
			self.caretPosition=0
			self._allowCaretMovement=False #sayAllGenerator will set this back to true when done
			time.sleep(0.01)
			self.dom.focus()
			core.newThread(self.sayAllGenerator())

	def isDocumentComplete(self):
		documentComplete=True
		if self.dom.readyState!="complete":
			audio.cancel()
			audio.speakMessage(str(self.dom.readyState))
			documentComplete=False
		for frameNum in range(self.dom.frames.length):
			try:
				if self.dom.frames.item(frameNum).document.readyState!="complete":
					audio.cancel()
					audio.speakMessage(str(self.dom.frames.item(frameNum).document.readyState))
					documentComplete=False
			except:
				pass
		return documentComplete

	def fillBuffer(self,domNode,IDAncestors=(),position=None):
		#We don't want comments in the buffer
		if isinstance(domNode,ctypes.POINTER(self.MSHTMLLib.DispHTMLCommentElement)):
			return position
		#We don't want non-displayed elements in the buffer 
		try:
			display=domNode.currentStyle.display
		except:
			display=None
		if display==u'none':
			return position
		#We don't want option elements in the buffer
		if domNode.nodeName=="OPTION":
			return position
		info=self.getDomNodeInfo(domNode)
		ID=self.getDomNodeID(domNode)
		if ID and ID not in IDAncestors:
			IDAncestors=tuple(list(IDAncestors)+[ID])
		if ID and not self._IDs.has_key(ID):
			self.addID(ID,**info)
		text=self.getDomNodeText(domNode)
		if text:
			position=self.addText(IDAncestors,text,position=position)
		if isinstance(domNode,self.MSHTMLLib.DispHTMLFrameElement):
			try:
				position=self.fillBuffer(domNode.contentWindow.document,IDAncestors,position=position)
			except:
				pass
		elif isinstance(domNode,self.MSHTMLLib.DispHTMLDocument):
			try:
				comtypesClient.ReleaseEvents(domNode,self.domEventsObject,interface=self.MSHTMLLib.HTMLDocumentEvents2)
			except:
				passs
			comtypesClient.GetEvents(domNode,self.domEventsObject,interface=self.MSHTMLLib.HTMLDocumentEvents2)
			position=self.fillBuffer(domNode.body,IDAncestors,position=position)
		else:
			child=domNode.firstChild
			while child:
				debug.writeMessage("node %s"%child)
				position=self.fillBuffer(child,IDAncestors,position=position)
				try:
					child=child.nextSibling
				except:
					child=None
		return position

	def getDomNodeID(self,domNode):
		#We don't want certain inline nodes like span, font etc to have their own IDs
		while domNode:
			if (domNode.nodeName not in ["B","CENTER","EM","FONT","I","SPAN","STRONG","SUP","U"]) or domNode.onclick:
				break
			domNode=domNode.parentNode
		#document nodes have broken uniqueIDs so we use its html node's uniqueID
		if isinstance(domNode,self.MSHTMLLib.DispHTMLDocument):
			try:
				domNode=domNode.firstChild
			except:
				pass
		#We return the uniqueID for the node if it has one
		try:
			return domNode.uniqueID
		except:
			return None

	def getDomNodeText(self,domNode):
		nodeName=domNode.nodeName
		if nodeName=="#text":
			data=domNode.data
			if data and not data.isspace():
				return "%s"%domNode.data
		elif isinstance(domNode,self.MSHTMLLib.DispHTMLDocument):
			return domNode.title+"\n "
		elif nodeName=="IMG":
			label=domNode.getAttribute('alt')
			if not label:
				label=domNode.getAttribute('title')
			if not label:
				label=domNode.getAttribute('name')
			if not label:
				label=domNode.getAttribute('src')
			return label
		elif nodeName=="SELECT":
			itemText=comtypesClient.wrap(domNode.item(domNode.selectedIndex)).text
			return itemText
		elif (nodeName=="TEXTAREA") and (domNode.children.length==0):
			return " "
		elif nodeName=="INPUT":
			inputType=domNode.getAttribute('type')
			if inputType=="text":
				return domNode.getAttribute('value')+" "
			if inputType=="password":
				return "*"*len(domNode.getAttribute('value'))+" "
			elif inputType in ["button","image","reset","submit"]:
				return domNode.getAttribute('value')
			elif inputType in ["checkbox","radio"]:
				return " "

	def getDomNodeInfo(self,domNode):
		info={"node":domNode,"typeString":"","stateTextFunc":None,"descriptionFunc":None,"reportOnEnter":False,"reportOnExit":False}
		if not domNode:
			return info
		nodeName=domNode.nodeName
		if isinstance(domNode,self.MSHTMLLib.DispHTMLFrameElement):
			info["typeString"]=_("frame")
			info["reportOnEnter"]=True
			info["reportOnExit"]=True
		elif isinstance(domNode,self.MSHTMLLib.DispHTMLDocument):
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_DOCUMENT)
		elif nodeName=="A":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_LINK)
			info["reportOnEnter"]=True
		elif nodeName=="UL":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_LIST)
			info["descriptionFunc"]=lambda x: "with %s items"%x.children.length
			info["reportOnEnter"]=True
			info["reportOnExit"]=True
		elif nodeName=="LI":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_LISTITEM)
			info["reportOnEnter"]=True
		elif nodeName=="TEXTAREA":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_TEXT)+" "+_("area")
			info["reportOnEnter"]=True
			info["reportOnExit"]=True
		elif nodeName=="IMG":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_GRAPHIC)
			info["reportOnEnter"]=True
		elif nodeName in ["H1","H2","H3","H4","H5","H6"]:
			info["typeString"]=_("heading")+" %s"%nodeName[1]
			info["reportOnEnter"]=True
		elif nodeName=="BLOCKQUOTE":
			info["typeString"]=_("block quote")
			info["reportOnEnter"]=True
			info["reportOnExit"]=True
		elif nodeName=="INPUT":
			inputType=domNode.getAttribute("type")
			if inputType=="text":
				info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_TEXT)
				info["reportOnEnter"]=True
			if inputType=="password":
				info["typeString"]=_("protected")+" "+MSAAHandler.getRoleName(ROLE_SYSTEM_TEXT)
				info["reportOnEnter"]=True
			elif inputType in ["button","image","reset","submit"]:
				info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_PUSHBUTTON)
				info["reportOnEnter"]=True
			elif inputType=="radio":
				info["stateTextFunc"]=lambda x: x.checked and MSAAHandler.getStateName(STATE_SYSTEM_CHECKED) or _("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)
				info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_RADIOBUTTON)
				info["reportOnEnter"]=True
			elif inputType=="checkbox":
				info["stateTextFunc"]=lambda x: x.checked and MSAAHandler.getStateName(STATE_SYSTEM_CHECKED) or _("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)
				info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_CHECKBUTTON)
				info["reportOnEnter"]=True
		elif nodeName=="SELECT":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_COMBOBOX)
			info["reportOnEnter"]=True
		else:
			info["typeString"]=nodeName
		try:
			if domNode.onclick and (nodeName not in ["INPUT","A"]):
				info["typeString"]=_("clickable")+" "+info["typeString"]
		except:
			pass
		return info
