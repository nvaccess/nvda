from . import VirtualBuffer, VirtualBufferTextInfo
import virtualBufferHandler
import controlTypes
import NVDAObjects.IAccessible.MSHTML
import winUser
import IAccessibleHandler
from logHandler import log
import textInfos

class MSHTMLTextInfo(VirtualBufferTextInfo):

	nodeNamesToNVDARoles={
		"frame":controlTypes.ROLE_FRAME,
		"iframe":controlTypes.ROLE_FRAME,
		"frameset":controlTypes.ROLE_DOCUMENT,
		"body":controlTypes.ROLE_DOCUMENT,
		"p":controlTypes.ROLE_PARAGRAPH,
		"ul":controlTypes.ROLE_LIST,
		"ol":controlTypes.ROLE_LIST,
		"li":controlTypes.ROLE_LISTITEM,
		"dl":controlTypes.ROLE_LIST,
		"dt":controlTypes.ROLE_LISTITEM,
		"dd":controlTypes.ROLE_LISTITEM,
		"table":controlTypes.ROLE_TABLE,
		"thead":controlTypes.ROLE_TABLEHEADER,
		"th":controlTypes.ROLE_TABLECOLUMNHEADER,
		"tbody":controlTypes.ROLE_TABLEBODY,
		"tr":controlTypes.ROLE_TABLEROW,
		"td":controlTypes.ROLE_TABLECELL,
		"img":controlTypes.ROLE_GRAPHIC,
		"a":controlTypes.ROLE_LINK,
		"div":controlTypes.ROLE_SECTION,
		"label":controlTypes.ROLE_LABEL,
		"form": controlTypes.ROLE_FORM,
	}

	def _normalizeControlField(self,attrs):
		print attrs
		level=None
		accRole=attrs.get('IAccessible::role',0)
		accRole=int(accRole) if isinstance(accRole,basestring) and accRole.isdigit() else accRole
		role=IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole,controlTypes.ROLE_UNKNOWN)
		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('IAccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)
		nodeName=attrs.get('IHTMLDOMNode::nodeName',"").lower()
		if role in (controlTypes.ROLE_UNKNOWN,controlTypes.ROLE_PANE):
			role=self.nodeNamesToNVDARoles.get(nodeName,controlTypes.ROLE_UNKNOWN)
		if role==controlTypes.ROLE_UNKNOWN:
			if "h1"<=nodeName<="h6":
				role=controlTypes.ROLE_HEADING
				level=nodeName[1:]
		if nodeName in ("ul","ol","dl"):
			states.add(controlTypes.STATE_READONLY)
		if role==controlTypes.ROLE_UNKNOWN:
			role=controlTypes.ROLE_TEXTFRAME
		newAttrs=textInfos.ControlField()
		newAttrs.update(attrs)
		if role:
			newAttrs['role']=role
		newAttrs['states']=states
		if level:
			newAttrs["level"] = level
		return newAttrs

class MSHTML(VirtualBuffer):

	TextInfo=MSHTMLTextInfo

	def __init__(self,rootNVDAObject):
		super(MSHTML,self).__init__(rootNVDAObject,backendLibPath=r"lib\VBufBackend_mshtml.dll")

	def isNVDAObjectInVirtualBuffer(self,obj):
		if not isinstance(obj,NVDAObjects.IAccessible.MSHTML.MSHTML) or not obj.IHTMLElement:
			return False
		return bool(obj.windowHandle==self.rootDocHandle)

	def isAlive(self):
		root=self.rootNVDAObject
		if not root:
			return False
		states=root.states
		if not winUser.isWindow(root.windowHandle) or controlTypes.STATE_DEFUNCT in states or controlTypes.STATE_READONLY not in states:
			return False
		return True

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		IHTMLElement=self.rootNVDAObject.IHTMLElement.document.GetElementById('ms__id%d'%ID)
		if not IHTMLElement:
			return self.rootNVDAObject
		while IHTMLElement:
			try:
				pacc=NVDAObjects.IAccessible.MSHTML.IAccessibleFromIHTMLElement(IHTMLElement)
			except NotImplementedError:
				pacc=None
			if pacc:
				return NVDAObjects.IAccessible.IAccessible(IAccessibleObject=pacc,IAccessibleChildID=0)
			IHTMLElement=IHTMLElement.parentElement

	def getIdentifierFromNVDAObject(self,obj):
		docHandle=obj.windowHandle
		ID=obj.IHTMLElement.uniqueNumber
		return docHandle,ID

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType=="link":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_LINKED:[1]}
		elif nodeType=="visitedLink":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_TRAVERSED:[1]}
		elif nodeType=="unvisitedLink":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_LINKED:[1],"IAccessible::state_%d"%IAccessibleHandler.STATE_SYSTEM_TRAVERSED:[None]}
		elif nodeType=="formField":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON,IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON,IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON,IAccessibleHandler.ROLE_SYSTEM_COMBOBOX,IAccessibleHandler.ROLE_SYSTEM_LIST,IAccessibleHandler.ROLE_SYSTEM_OUTLINE,IAccessibleHandler.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_READONLY:[None],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="button":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="edit":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_READONLY:[None],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="radioButton":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_RADIOBUTTON],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="comboBox":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_COMBOBOX],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="checkBox":
			attrs={"IAccessible::role":[IAccessibleHandler.ROLE_SYSTEM_CHECKBUTTON],"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="table":
			attrs={"IHTMLDOMNode::nodeName":["TABLE"]}
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
			attrs={"IAccessible::state_%s"%IAccessibleHandler.STATE_SYSTEM_FOCUSABLE:[1]}
		else:
			return None
		return attrs
