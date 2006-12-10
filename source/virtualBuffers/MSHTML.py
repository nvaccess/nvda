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
			if domNode.tagName not in ["INPUT","SELECT","TEXTAREA"]:
				return
			ID=self.virtualBufferObject.getDomNodeID(domNode)
			IDs=self.virtualBufferObject.getIDsFromID(ID)
			(start,end)=self.virtualBufferObject.getRangeFromID(ID)
			self.virtualBufferObject.removeID(ID)
			self.virtualBufferObject.fillBuffer(domNode,IDs,position=start)


		def onreadystatechange(self,arg,event):
			if self.virtualBufferObject.isDocumentComplete():
				self.virtualBufferObject.loadDocument()

		def oncontextmenu(self,arg,event):
			if not api.isVirtualBufferPassThroughMode():
				api.toggleVirtualBufferPassThroughMode()

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
		try:
			tagName=self.dom.activeElement.tagName
		except:
			tagName=None
		if (self.dom.body.isContentEditable is False) and (tagName not in ["INPUT","SELECT","TEXTAREA"]) and api.isVirtualBufferPassThrough():
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
		try:
			tagName=domNode.tagName
		except:
			tagName=None
		if (tagName in ["INPUT","SELECT","TEXTAREA"]):
			if domNode.uniqueID!=self.dom.activeElement.uniqueID:
				domNode.focus()
			if not api.isVirtualBufferPassThrough() and not ((tagName=="INPUT") and (domNode.getAttribute('type') in["checkbox","radio"])): 
				api.toggleVirtualBufferPassThrough()
		elif tagName=="A":
			domNode.click()
			domNode.focus()

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
		if isinstance(domNode,ctypes.POINTER(self.MSHTMLLib.DispHTMLCommentElement)):
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
				position=self.fillBuffer(child,IDAncestors,position=position)
				child=child.nextSibling
		return position

	def getDomNodeID(self,domNode):
		#We don't want certain inline nodes like span, font etc to have their own IDs
		while domNode:
			try:
				tagName=domNode.tagName
			except:
				tagName=None
			if tagName not in ["B","CENTER","EM","FONT","I","SPAN","STRONG","SUP","U"]:
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
		try:
			data=domNode.data
			parentNode=domNode.parentNode
			parentTagName=parentNode.tagName
			parentUniqueID=self.getDomNodeID(parentNode)
		except:
			data=None
			parentNode=None
			parentTagName=None
			parentUniqueID=None
		try:
			tagName=domNode.tagName
			uniqueID=self.getDomNodeID(domNode)
		except:
			tagName=None
			uniqueID=None
		if data and not data.isspace() and parentNode and (parentTagName not in ["OPTION"]):
			return data
		elif isinstance(domNode,self.MSHTMLLib.DispHTMLDocument):
			return domNode.title+"\n "
		elif tagName=="IMG":
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

	def getDomNodeInfo(self,domNode):
		info={"node":domNode,"typeString":"","stateTextFunc":None,"descriptionFunc":None,"reportOnEnter":False,"reportOnExit":False}
		if not domNode:
			return info
		try:
			tagName=domNode.tagName
		except:
			tagName=None
		if isinstance(domNode,self.MSHTMLLib.DispHTMLFrameElement):
			info["typeString"]=_("frame")
			info["reportOnEnter"]=True
			info["reportOnExit"]=True
		elif isinstance(domNode,self.MSHTMLLib.DispHTMLDocument):
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_DOCUMENT)
		elif tagName=="A":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_LINK)
			info["reportOnEnter"]=True
		elif tagName=="UL":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_LIST)
			info["descriptionFunc"]=lambda x: "with %s items"%x.children.length
			info["reportOnEnter"]=True
			info["reportOnExit"]=True
		elif tagName=="LI":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_LISTITEM)
			info["reportOnEnter"]=True
		elif tagName=="TEXTAREA":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_TEXT)
			info["reportOnEnter"]=True
			info["reportOnExit"]=True
		elif tagName=="IMG":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_GRAPHIC)
			info["reportOnEnter"]=True
		elif tagName in ["H1","H2","H3","H4","H5","H6"]:
			info["typeString"]=_("heading")+" %s"%tagName[1]
			info["reportOnEnter"]=True
		elif tagName=="BLOCKQUOTE":
			info["typeString"]=_("block quote")
			info["reportOnEnter"]=True
			info["reportOnExit"]=True
		elif tagName=="INPUT":
			inputType=domNode.getAttribute("type")
			if inputType=="text":
				info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_TEXT)
				info["reportOnEnter"]=True
			elif inputType in ["button","reset","submit"]:
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
		elif tagName=="SELECT":
			info["typeString"]=MSAAHandler.getRoleName(ROLE_SYSTEM_COMBOBOX)
			info["reportOnEnter"]=True
		else:
			info["typeString"]=tagName
		return info
