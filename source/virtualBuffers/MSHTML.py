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
from config import conf
import NVDAObjects
from baseType import *

class virtualBuffer_MSHTML(virtualBuffer):

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

		def onscroll(self,arg,event):
			audio.speakMessage("scroll")

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
		virtualBuffer.__init__(self,NVDAObject)
		#Set up events for the document, plus any sub frames
		self.domEventsObject=self.domEventsType(self)
		comtypesClient.GetEvents(self.dom,self.domEventsObject,interface=self.MSHTMLLib.HTMLDocumentEvents2)
		if self.isDocumentComplete():
			self.loadDocument()

	def event_MSAA_gainFocus(self,hwnd,objectID,childID):
		try:
			nodeName=self.dom.activeElement.nodeName
		except:
			return False
		if (self.dom.body.isContentEditable is False) and (nodeName not in ["INPUT","SELECT","TEXTAREA"]) and api.isVirtualBufferPassThrough():
			api.toggleVirtualBufferPassThrough()
		if not self._allowCaretMovement:
			return False
		domNode=self.dom.activeElement
		ID=self.getDomNodeID(domNode)
		r=self.getRangeFromID(ID)
		if (r is not None) and (len(r)==2) and ((self.caretPosition<r[0]) or (self.caretPosition>=r[1])):
			self.caretPosition=r[0]
			obj=NVDAObjects.MSAA.getNVDAObjectFromEvent(hwnd,objectID,childID)
			if obj and conf["virtualBuffers"]["reportVirtualPresentationOnFocusChanges"]:
				self.reportCaretIDMessages()
				audio.speakText(self.getTextRange(r[0],r[1]))
				api.setFocusObject(obj)
				api.setNavigatorObject(obj)
				return True
		return False

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
			if not api.isVirtualBufferPassThrough():
				api.toggleVirtualBufferPassThrough()
			domNode.focus()
		elif nodeName =="INPUT":
			inputType=domNode.getAttribute('type')
			if inputType in ["checkbox","radio"]:
				domNode.click()
				audio.speakMessage("%s"%(MSAAHandler.getStateName(STATE_SYSTEM_CHECKED) if domNode.checked else _("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)))
			elif inputType in ["file","text","password"]:
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
			audio.speakMessage(_("done"))
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
				return data
		elif isinstance(domNode,self.MSHTMLLib.DispHTMLDocument):
			return domNode.title+"\n "
		elif nodeName=="IMG":
			label=domNode.getAttribute('alt')
			if not label:
				label=domNode.getAttribute('title')
			if not label:
				label=domNode.getAttribute('name')
			if not label:
				label=domNode.getAttribute('src').split('/')[-1]
			return label
		elif nodeName=="SELECT":
			itemText=comtypesClient.wrap(domNode.item(domNode.selectedIndex)).text
			return itemText
		elif (nodeName=="TEXTAREA") and (domNode.children.length==0):
			return " "
		elif nodeName=="INPUT":
			inputType=domNode.getAttribute('type')
			if inputType in ["text","file"]:
				return domNode.getAttribute('value')+" "
			if inputType=="password":
				return "*"*len(domNode.getAttribute('value'))+" "
			elif inputType in ["button","image","reset","submit"]:
				return domNode.getAttribute('value')
			elif inputType in ["checkbox","radio"]:
				return " "

	def getDomNodeInfo(self,domNode):
		info=fieldInfo.copy()
		info["node"]=domNode
		if not domNode:
			return info
		nodeName=domNode.nodeName
		if isinstance(domNode,self.MSHTMLLib.DispHTMLFrameElement):
			info["fieldType"]=fieldType_frame
			info["typeString"]=fieldNames[fieldType_frame]
		elif isinstance(domNode,self.MSHTMLLib.DispHTMLDocument):
			info["fieldType"]=fieldType_document
			info["typeString"]=fieldNames[fieldType_document]
		elif nodeName=="A":
			info["fieldType"]=fieldType_link
			info["typeString"]=fieldNames[fieldType_link]
		elif nodeName=="TABLE":
			info["fieldType"]=fieldType_table
			info["typeString"]=fieldNames[fieldType_table]
		elif nodeName=="P":
			info["fieldType"]=fieldType_paragraph
			info["typeString"]=fieldNames[fieldType_paragraph]
		elif nodeName=="UL":
			info["fieldType"]=fieldType_list
			info["typeString"]=fieldNames[fieldType_list]
			info["descriptionFunc"]=lambda x: "with %s items"%x.children.length
		elif nodeName=="OL":
			info["fieldType"]=fieldType_list
			info["typeString"]=_("ordered")+" "+fieldNames[fieldType_list]
			info["descriptionFunc"]=lambda x: "with %s items"%x.children.length
		elif nodeName=="LI":
			info["fieldType"]=fieldType_listItem
			info["typeString"]=_("bullit item")
		elif nodeName=="DL":
			info["fieldType"]=fieldType_list
			info["typeString"]=_("definition")+" "+fieldNames[fieldType_list]
			info["descriptionFunc"]=lambda x: "with %s items"%x.children.length
		elif nodeName=="DT":
			info["fieldType"]=fieldType_listItem
			info["typeString"]=_("bullit item")
		elif nodeName=="DD":
			info["fieldType"]=fieldType_listItem
			info["typeString"]=_("definition")
		elif nodeName=="TEXTAREA":
			info["fieldType"]=fieldType_editArea
			info["typeString"]=fieldNames[fieldType_editArea]
		elif nodeName=="IMG":
			info["fieldType"]=fieldType_graphic
			info["typeString"]=fieldNames[fieldType_graphic]
		elif nodeName in ["H1","H2","H3","H4","H5","H6"]:
			info["fieldType"]=fieldType_heading
			info["typeString"]=fieldNames[fieldType_heading]+" %s"%nodeName[1]
		elif nodeName=="BLOCKQUOTE":
			info["fieldType"]=fieldType_blockQuote
			info["typeString"]=fieldNames[fieldType_blockQuote]
		elif nodeName=="INPUT":
			inputType=domNode.getAttribute("type")
			if inputType=="text":
				info["fieldType"]=fieldType_edit
				info["typeString"]=fieldNames[fieldType_edit]
			elif inputType=="file":
				info["fieldType"]=fieldType_edit
				info["typeString"]=_("file updload")+" "+fieldNames[fieldType_edit]
			elif inputType=="password":
				info["fieldType"]=fieldType_edit
				info["typeString"]=_("protected")+" "+fieldNames[fieldType_edit]
			elif inputType in ["button","image","reset","submit"]:
				info["fieldType"]=fieldType_button
				info["typeString"]=fieldNames[fieldType_button]
			elif inputType=="radio":
				info["fieldType"]=fieldType_radioButton
				info["typeString"]=fieldNames[fieldType_radioButton]
				info["stateTextFunc"]=lambda x: MSAAHandler.getStateName(STATE_SYSTEM_CHECKED) if x.checked else _("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)
			elif inputType=="checkbox":
				info["fieldType"]=fieldType_checkBox
				info["typeString"]=fieldNames[fieldType_checkBox]
				info["stateTextFunc"]=lambda x: MSAAHandler.getStateName(STATE_SYSTEM_CHECKED) if x.checked else _("not")+" "+MSAAHandler.getStateName(STATE_SYSTEM_CHECKED)
		elif nodeName=="SELECT":
			info["fieldType"]=fieldType_comboBox
			info["typeString"]=fieldNames[fieldType_comboBox]
		else:
			info["typeString"]=nodeName
		try:
			accessKey=domNode.accessKey
			if accessKey:
				info["accessKey"]="alt+%s"%accessKey
		except:
			pass
		try:
			if domNode.onclick and (nodeName not in ["INPUT","A"]):
				info["typeString"]=_("clickable")+" "+info["typeString"]
		except:
			pass
		return info
