from . import VirtualBuffer, VirtualBufferTextInfo
import controlTypes
import NVDAObjects.IAccessible
import winUser
import IAccessibleHandler
import oleacc
from logHandler import log
import textInfos

class AdobeAcrobat_TextInfo(VirtualBufferTextInfo):
	stdNamesToRoles = {
		# part? art?
		"sect": controlTypes.ROLE_SECTION,
		"div": controlTypes.ROLE_SECTION,
		"blockquote": controlTypes.ROLE_BLOCKQUOTE,
		"caption": controlTypes.ROLE_CAPTION,
		# toc? toci? index? nonstruct? private? 
		"l": controlTypes.ROLE_LIST,
		"li": controlTypes.ROLE_LISTITEM,
		"lbl": controlTypes.ROLE_LABEL,
		# lbody
		"p": controlTypes.ROLE_PARAGRAPH,
		"h": controlTypes.ROLE_HEADING,
		# h1 to h6 handled separately
		# span, quote, note, reference, bibentry, code, figure, formula
		"form": controlTypes.ROLE_FORM,
	}

	def _normalizeControlField(self,attrs):
		role = None
		level = None

		stdName = attrs.get("acrobat::stdname", "").lower()
		if "h1" <= stdName <= "h6":
			role = controlTypes.ROLE_HEADING
			level = stdName[1]
		if not role:
			try:
				role = self.stdNamesToRoles[stdName]
			except KeyError:
				pass

		if not role:
			accRole=attrs['IAccessible::role']
			if accRole.isdigit():
				accRole=int(accRole)
			else:
				accRole = accRole.lower()
			role=IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole,controlTypes.ROLE_UNKNOWN)

		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('IAccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)

		attrs['role']=role
		attrs['states']=states
		if level:
			attrs["level"] = level
		return super(AdobeAcrobat_TextInfo, self)._normalizeControlField(attrs)

class AdobeAcrobat(VirtualBuffer):
	TextInfo = AdobeAcrobat_TextInfo

	def __init__(self,rootNVDAObject):
		super(AdobeAcrobat,self).__init__(rootNVDAObject,backendName="adobeAcrobat")

	def isNVDAObjectInVirtualBuffer(self,obj):
		if self.rootNVDAObject.windowHandle==obj.windowHandle:
			return True
		return False

	def isAlive(self):
		root=self.rootNVDAObject
		if not root:
			return False
		if not winUser.isWindow(root.windowHandle) or root.role == controlTypes.ROLE_UNKNOWN:
			return False
		return True

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		return NVDAObjects.IAccessible.getNVDAObjectFromEvent(docHandle, winUser.OBJID_CLIENT, ID)

	def getIdentifierFromNVDAObject(self,obj):
		docHandle=obj.windowHandle
		ID=obj.event_childID
		return docHandle,ID

	def event_focusEntered(self,obj,nextHandler):
		if self.passThrough:
			nextHandler()

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType in ("link", "unvisitedLink"):
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK]}
		elif nodeType=="table":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_TABLE]}
		elif nodeType.startswith("heading") and nodeType[7:].isdigit():
			attrs = {"acrobat::stdname": ["H%s" % nodeType[7:]]}
		elif nodeType == "heading":
			attrs = {"acrobat::stdname": ["H1", "H2", "H3", "H4", "H5", "H6"]}
		elif nodeType == "formField":
			attrs = {"IAccessible::role": [oleacc.ROLE_SYSTEM_PUSHBUTTON, oleacc.ROLE_SYSTEM_RADIOBUTTON, oleacc.ROLE_SYSTEM_CHECKBUTTON, oleacc.ROLE_SYSTEM_COMBOBOX, oleacc.ROLE_SYSTEM_LIST, oleacc.ROLE_SYSTEM_OUTLINE, oleacc.ROLE_SYSTEM_TEXT], "IAccessible::state_%s" % oleacc.STATE_SYSTEM_READONLY: [None]}
		elif nodeType == "list":
			attrs = {"acrobat::stdname": ["L"]}
		elif nodeType == "listItem":
			attrs = {"acrobat::stdname": ["LI"]}
		elif nodeType=="button":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON]}
		elif nodeType=="edit":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_READONLY:[None]}
		elif nodeType=="radioButton":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_RADIOBUTTON]}
		elif nodeType=="checkBox":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_CHECKBUTTON]}
		elif nodeType == "blockQuote":
			attrs = {"acrobat::stdname": ["BlockQuote"]}
		elif nodeType=="focusable":
			attrs={"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		else:
			return None
		return attrs

	def event_valueChange(self, obj, nextHandler):
		if obj.event_childID == 0:
			return nextHandler()
		if not self._handleScrollTo(obj):
			return nextHandler()
