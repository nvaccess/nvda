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
		level=None
		accRole=attrs.get('IAccessible::role',0)
		accRole=int(accRole) if isinstance(accRole,basestring) and accRole.isdigit() else accRole
		role=IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole,controlTypes.ROLE_UNKNOWN)
		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('IAccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)
		nodeName=attrs.get('IHTMLDOMNode::nodeName',"").lower()
		if nodeName=="textarea":
			states.add(controlTypes.STATE_MULTILINE)
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
