import eventHandler
from . import VirtualBuffer, VirtualBufferTextInfo, VBufStorage_findMatch_word
import virtualBufferHandler
import controlTypes
import NVDAObjects.IAccessible.MSHTML
import winUser
import IAccessibleHandler
import oleacc
from logHandler import log
import textInfos
import aria
import config

class MSHTMLTextInfo(VirtualBufferTextInfo):

	def _normalizeControlField(self,attrs):
		level=None
		accRole=attrs.get('IAccessible::role',0)
		accRole=int(accRole) if isinstance(accRole,basestring) and accRole.isdigit() else accRole
		role=IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole,controlTypes.ROLE_UNKNOWN)
		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('IAccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)
		if 'HTMLAttrib::onclick' in attrs or 'HTMLAttrib::onmousedown' in attrs or 'HTMLAttrib::onmouseup' in attrs:
			states.add(controlTypes.STATE_CLICKABLE)
		if attrs.get('HTMLAttrib::aria-required','false')=='true':
			states.add(controlTypes.STATE_REQUIRED)
		if attrs.get('HTMLAttrib::aria-invalid','false')=='true':
			states.add(controlTypes.STATE_INVALID)
		if attrs.get('HTMLAttrib::aria-multiline','false')=='true':
			states.add(controlTypes.STATE_MULTILINE)
		if attrs.get('HTMLAttrib::aria-dropeffect','none')!='none':
			states.add(controlTypes.STATE_DROPTARGET)
		ariaGrabbed=attrs.get('HTMLAttrib::aria-grabbed',None)
		if ariaGrabbed=='false':
			states.add(controlTypes.STATE_DRAGGABLE)
		elif ariaGrabbed=='true':
			states.add(controlTypes.STATE_DRAGGING)
		nodeName=attrs.get('IHTMLDOMNode::nodeName',"")
		if nodeName=="TEXTAREA":
			states.add(controlTypes.STATE_MULTILINE)
		if role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_PANE,controlTypes.ROLE_WINDOW):
			role=NVDAObjects.IAccessible.MSHTML.nodeNamesToNVDARoles.get(nodeName,controlTypes.ROLE_UNKNOWN)
		if "H1"<=nodeName<="H6":
			level=nodeName[1:]
		if nodeName in ("UL","OL","DL"):
			states.add(controlTypes.STATE_READONLY)
		if role==controlTypes.ROLE_UNKNOWN:
			role=controlTypes.ROLE_TEXTFRAME
		if role==controlTypes.ROLE_GRAPHIC:
			# MSHTML puts the unavailable state on all graphics when the showing of graphics is disabled.
			# This is rather annoying and irrelevant to our users, so discard it.
			states.discard(controlTypes.STATE_UNAVAILABLE)
		ariaRoles=attrs.get("HTMLAttrib::role", "").split(" ")
		# Get the first landmark role, if any.
		landmark=next((ar for ar in ariaRoles if ar in aria.landmarkRoles),None)

		if role:
			attrs['role']=role
		attrs['states']=states
		if level:
			attrs["level"] = level
		if landmark:
			attrs["landmark"]=landmark
		return super(MSHTMLTextInfo,self)._normalizeControlField(attrs)

class MSHTML(VirtualBuffer):

	TextInfo=MSHTMLTextInfo

	def __init__(self,rootNVDAObject):
		super(MSHTML,self).__init__(rootNVDAObject,backendName="mshtml")

	def _setInitialCaretPos(self):
		if super(MSHTML,self)._setInitialCaretPos():
			return
		url=getattr(self.rootNVDAObject.HTMLNode.document,'url',"").split('#')
		if not url or len(url)!=2:
			return False
		anchorName=url[-1]
		if not anchorName:
			return False
		obj=self._getNVDAObjectByAnchorName(anchorName)
		self._handleScrollTo(obj)

	def isNVDAObjectInVirtualBuffer(self,obj):
		if not obj.windowClassName.startswith("Internet Explorer_"):
			return False
		#Combo box lists etc are popup windows, so rely on accessibility hierarchi instead of window hierarchi for those.
		#However only helps in IE8.
		if obj.windowStyle&winUser.WS_POPUP:
			parent=obj.parent
			obj.parent=parent
			while parent and parent.windowHandle==obj.windowHandle:
				newParent=parent.parent
				parent.parent=newParent
				parent=newParent
			if parent and parent.windowClassName.startswith('Internet Explorer_'):
				obj=parent
		if obj.windowHandle==self.rootDocHandle:
			return True
		if winUser.isDescendantWindow(self.rootDocHandle,obj.windowHandle):
			return True
		return False


	def isAlive(self):
		root=self.rootNVDAObject
		if not root:
			return False
		states=root.states
		if not winUser.isWindow(root.windowHandle) or controlTypes.STATE_DEFUNCT in states or controlTypes.STATE_READONLY not in states:
			return False
		return True

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		HTMLNode=NVDAObjects.IAccessible.MSHTML.locateHTMLElementByID(self.rootNVDAObject.HTMLNode.document,'ms__id%d'%ID)
		if not HTMLNode:
			return self.rootNVDAObject
		return NVDAObjects.IAccessible.MSHTML.MSHTML(HTMLNode=HTMLNode)

	def getIdentifierFromNVDAObject(self,obj):
		docHandle=obj.windowHandle
		ID=obj.HTMLNode.uniqueNumber
		return docHandle,ID

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType=="link":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_LINKED:[1]}
		elif nodeType=="visitedLink":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_TRAVERSED:[1]}
		elif nodeType=="unvisitedLink":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_LINKED:[1],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_TRAVERSED:[None]}
		elif nodeType=="formField":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON,oleacc.ROLE_SYSTEM_RADIOBUTTON,oleacc.ROLE_SYSTEM_CHECKBUTTON,oleacc.ROLE_SYSTEM_COMBOBOX,oleacc.ROLE_SYSTEM_LIST,oleacc.ROLE_SYSTEM_OUTLINE,oleacc.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_READONLY:[None],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="button":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="edit":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_READONLY:[None],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="radioButton":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_RADIOBUTTON],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="comboBox":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_COMBOBOX],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="checkBox":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_CHECKBUTTON],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="table":
			attrs={"IHTMLDOMNode::nodeName":["TABLE"]}
			if not config.conf["documentFormatting"]["includeLayoutTables"]:
				attrs["table-layout"]=[None]
		elif nodeType.startswith("heading") and nodeType[7:].isdigit():
			attrs = {"IHTMLDOMNode::nodeName": ["H%s" % nodeType[7:]]}
		elif nodeType == "heading":
			attrs = {"IHTMLDOMNode::nodeName": ["H1", "H2", "H3", "H4", "H5", "H6"]}
		elif nodeType == "list":
			attrs = {"IHTMLDOMNode::nodeName": ["UL","OL","DL"]}
		elif nodeType == "listItem":
			attrs = {"IHTMLDOMNode::nodeName": ["LI","DD","DT"]}
		elif nodeType == "blockQuote":
			attrs = {"IHTMLDOMNode::nodeName": ["BLOCKQUOTE"]}
		elif nodeType == "graphic":
			attrs = {"IHTMLDOMNode::nodeName": ["IMG"]}
		elif nodeType == "frame":
			attrs = {"IHTMLDOMNode::nodeName": ["FRAME","IFRAME"]}
		elif nodeType=="focusable":
			attrs={"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="landmark":
			attrs={"HTMLAttrib::role":[VBufStorage_findMatch_word(lr) for lr in aria.landmarkRoles]}
		else:
			return None
		return attrs

	def _activateNVDAObject(self,obj):
		super(MSHTML,self)._activateNVDAObject(obj)
		#If we activated a same-page link, then scroll to its anchor
		if obj.HTMLNodeName=="A":
			anchorName=getattr(obj.HTMLNode,'hash')
			if not anchorName:
				return 
			obj=self._getNVDAObjectByAnchorName(anchorName[1:],HTMLDocument=obj.HTMLNode.document)
			if not obj:
				return
			self._handleScrollTo(obj)

	def _getNVDAObjectByAnchorName(self,name,HTMLDocument=None):
		if not HTMLDocument:
			HTMLDocument=self.rootNVDAObject.HTMLNode.document
		HTMLNode=HTMLDocument.getElementById(name)
		if not HTMLNode:
			raise ValueError("node %s"%name)
		obj=NVDAObjects.IAccessible.MSHTML.MSHTML(HTMLNode=HTMLNode)
		return obj
