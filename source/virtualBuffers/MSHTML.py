#virtualBuffers/MSHTML.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2009-2012 NV Access Limited

from comtypes import COMError
import eventHandler
from . import VirtualBuffer, VirtualBufferTextInfo, VBufStorage_findMatch_word, VBufStorage_findMatch_notEmpty
import controlTypes
import NVDAObjects.IAccessible.MSHTML
import winUser
import NVDAHelper
import ctypes
import IAccessibleHandler
import languageHandler
import oleacc
from logHandler import log
import textInfos
import api
import aria
import config
import watchdog

FORMATSTATE_INSERTED=1
FORMATSTATE_DELETED=2
FORMATSTATE_MARKED=4
FORMATSTATE_STRONG=8
FORMATSTATE_EMPH=16

class MSHTMLTextInfo(VirtualBufferTextInfo):

	def _normalizeFormatField(self, attrs):
		formatState=attrs.get('formatState',"0")
		formatState=int(formatState)
		if formatState&FORMATSTATE_INSERTED:
			attrs['revision-insertion']=True
		if formatState&FORMATSTATE_DELETED:
			attrs['revision-deletion']=True
		if formatState&FORMATSTATE_MARKED:
			attrs['marked']=True
		if formatState&FORMATSTATE_STRONG:
			attrs['strong']=True
		if formatState&FORMATSTATE_EMPH:
			attrs['emphasised']=True
		language=attrs.get('language')
		if language:
			attrs['language']=languageHandler.normalizeLanguage(language)
		return attrs

	def _normalizeControlField(self,attrs):
		level=None
		accRole=attrs.get('IAccessible::role',0)
		accRole=int(accRole) if isinstance(accRole,basestring) and accRole.isdigit() else accRole
		nodeName=attrs.get('IHTMLDOMNode::nodeName',"")
		ariaRoles=attrs.get("HTMLAttrib::role", "").split(" ")
		#choose role
		#Priority is aria role -> HTML tag name -> IAccessible role
		role=next((aria.ariaRolesToNVDARoles[ar] for ar in ariaRoles if ar in aria.ariaRolesToNVDARoles),controlTypes.ROLE_UNKNOWN)
		if not role and nodeName:
			role=NVDAObjects.IAccessible.MSHTML.nodeNamesToNVDARoles.get(nodeName,controlTypes.ROLE_UNKNOWN)
		if not role:
			role=IAccessibleHandler.IAccessibleRolesToNVDARoles.get(accRole,controlTypes.ROLE_UNKNOWN)
		states=set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in [1<<y for y in xrange(32)] if int(attrs.get('IAccessible::state_%s'%x,0)) and x in IAccessibleHandler.IAccessibleStatesToNVDAStates)
		if attrs.get('HTMLAttrib::longdesc'):
			states.add(controlTypes.STATE_HASLONGDESC)
		#IE exposes destination anchors as links, this is wrong
		if nodeName=="A" and role==controlTypes.ROLE_LINK and controlTypes.STATE_LINKED not in states:
			role=controlTypes.ROLE_TEXTFRAME
		if 'IHTMLElement::isContentEditable' in attrs:
			states.add(controlTypes.STATE_EDITABLE)
		if 'HTMLAttrib::onclick' in attrs or 'HTMLAttrib::onmousedown' in attrs or 'HTMLAttrib::onmouseup' in attrs:
			states.add(controlTypes.STATE_CLICKABLE)
		if attrs.get('HTMLAttrib::aria-required','false')=='true':
			states.add(controlTypes.STATE_REQUIRED)
		description=None
		ariaDescribedBy=attrs.get('HTMLAttrib::aria-describedby')
		if ariaDescribedBy:
			try:
				descNode=self.obj.rootNVDAObject.HTMLNode.document.getElementById(ariaDescribedBy)
			except (COMError,NameError):
				descNode=None
			if descNode:
				try:
					description=self.obj.makeTextInfo(NVDAObjects.IAccessible.MSHTML.MSHTML(HTMLNode=descNode)).text
				except:
					pass
		ariaSort=attrs.get('HTMLAttrib::aria-sort')
		state=aria.ariaSortValuesToNVDAStates.get(ariaSort)
		if state is not None:
			states.add(state)
		ariaSelected=attrs.get('HTMLAttrib::aria-selected')
		if ariaSelected=="true":
			states.add(controlTypes.STATE_SELECTED)
		elif ariaSelected=="false":
			states.discard(controlTypes.STATE_SELECTED)
		ariaExpanded=attrs.get('HTMLAttrib::aria-expanded')
		if ariaExpanded=="true":
			states.add(controlTypes.STATE_EXPANDED)
		elif ariaExpanded=="false":
			states.add(controlTypes.STATE_COLLAPSED)
		if attrs.get('HTMLAttrib::aria-invalid','false')=='true':
			states.add(controlTypes.STATE_INVALID_ENTRY)
		if attrs.get('HTMLAttrib::aria-multiline','false')=='true':
			states.add(controlTypes.STATE_MULTILINE)
		if attrs.get('HTMLAttrib::aria-dropeffect','none')!='none':
			states.add(controlTypes.STATE_DROPTARGET)
		ariaGrabbed=attrs.get('HTMLAttrib::aria-grabbed',None)
		if ariaGrabbed=='false':
			states.add(controlTypes.STATE_DRAGGABLE)
		elif ariaGrabbed=='true':
			states.add(controlTypes.STATE_DRAGGING)
		if nodeName=="TEXTAREA":
			states.add(controlTypes.STATE_MULTILINE)
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
		# Get the first landmark role, if any.
		landmark=next((ar for ar in ariaRoles if ar in aria.landmarkRoles),None)
		ariaLevel=attrs.get('HTMLAttrib::aria-level',None)
		ariaLevel=int(ariaLevel) if ariaLevel is not None else None
		if ariaLevel:
			level=ariaLevel
		if role:
			attrs['role']=role
		attrs['states']=states
		if level:
			attrs["level"] = level
		if landmark:
			attrs["landmark"]=landmark
		if description:
			attrs["description"]=description
		return super(MSHTMLTextInfo,self)._normalizeControlField(attrs)

class MSHTML(VirtualBuffer):

	TextInfo=MSHTMLTextInfo

	def __init__(self,rootNVDAObject):
		super(MSHTML,self).__init__(rootNVDAObject,backendName="mshtml")
		# As virtualBuffers must be created at all times for MSHTML to support live regions,
		# Force focus mode for anything other than a document (e.g. dialog, application)
		if rootNVDAObject.role!=controlTypes.ROLE_DOCUMENT:
			self.disableAutoPassThrough=True
			self.passThrough=True

	def _getInitialCaretPos(self):
		initialPos = super(MSHTML,self)._getInitialCaretPos()
		if initialPos:
			return initialPos
		try:
			url=getattr(self.rootNVDAObject.HTMLNode.document,'url',"").split('#')
		except COMError as e:
			log.debugWarning("Error getting URL from document: %s" % e)
			return None
		if not url or len(url)!=2:
			return None
		anchorName=url[-1]
		if not anchorName:
			return None
		return self._getNVDAObjectByAnchorName(anchorName)

	def __contains__(self,obj):
		if not obj.windowClassName.startswith("Internet Explorer_"):
			return False
		#'select' tag lists have MSAA list items which do not relate to real HTML nodes.
		#Go up one parent for these and use it instead
		if isinstance(obj,NVDAObjects.IAccessible.IAccessible) and not isinstance(obj,NVDAObjects.IAccessible.MSHTML.MSHTML) and obj.role==controlTypes.ROLE_LISTITEM:
			parent=obj.parent
			if parent and isinstance(parent,NVDAObjects.IAccessible.MSHTML.MSHTML):
				obj=parent
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
		if not winUser.isDescendantWindow(self.rootDocHandle,obj.windowHandle) and obj.windowHandle!=self.rootDocHandle:
			return False
		newObj=obj
		while  isinstance(newObj,NVDAObjects.IAccessible.MSHTML.MSHTML):
			if newObj==self.rootNVDAObject:
				return True
			if newObj.role in (controlTypes.ROLE_APPLICATION,controlTypes.ROLE_DIALOG):
				break
			newObj=newObj.parent 
		return False

	def _get_isAlive(self):
		if self.isLoading:
			return True
		root=self.rootNVDAObject
		if not root:
			return False
		if not winUser.isWindow(root.windowHandle):
			return False
		if root.appModule.appName.startswith('wwahost') and not winUser.isDescendantWindow(winUser.getForegroundWindow(),root.windowHandle):
			# #4572: When a wwahost hosted app is in the background it gets suspended and all COM calls freeze.
			# Therefore we don't have enough info to say whether its dead or not. We assume it is alive until we can get a better answer.
			return True
		try:
			if not root.IAccessibleRole:
				# The root object is dead.
				return False
		except watchdog.CallCancelled:
			# #1831: If the root object isn't responding, treat the buffer as dead.
			# Otherwise, we'll keep querying it on every focus change and freezing.
			return False
		states=root.states
		if controlTypes.STATE_EDITABLE in states:
			return False
		return True

	def getNVDAObjectFromIdentifier(self, docHandle, ID):
		HTMLNode=NVDAObjects.IAccessible.MSHTML.locateHTMLElementByID(self.rootNVDAObject.HTMLNode.document,'ms__id%d'%ID)
		if not HTMLNode:
			return self.rootNVDAObject
		return NVDAObjects.IAccessible.MSHTML.MSHTML(HTMLNode=HTMLNode)

	def getIdentifierFromNVDAObject(self,obj):
		if not isinstance(obj,NVDAObjects.IAccessible.MSHTML.MSHTML):
			raise LookupError
		docHandle=obj.windowHandle
		ID=obj.HTMLNodeUniqueNumber
		return docHandle,ID

	def _searchableAttribsForNodeType(self,nodeType):
		if nodeType=="link":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_LINKED:[1]}
		elif nodeType=="visitedLink":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_TRAVERSED:[1]}
		elif nodeType=="unvisitedLink":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_LINK],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_LINKED:[1],"IAccessible::state_%d"%oleacc.STATE_SYSTEM_TRAVERSED:[None]}
		elif nodeType=="formField":
			attrs=[
				{"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON,oleacc.ROLE_SYSTEM_RADIOBUTTON,oleacc.ROLE_SYSTEM_CHECKBUTTON,oleacc.ROLE_SYSTEM_COMBOBOX,oleacc.ROLE_SYSTEM_OUTLINE,oleacc.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_READONLY:[None]},
				{"IHTMLDOMNode::nodeName":["SELECT"]},
				{"HTMLAttrib::role":["listbox"]},
			]
		elif nodeType=="button":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON]}
		elif nodeType=="edit":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_TEXT,oleacc.ROLE_SYSTEM_COMBOBOX],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_READONLY:[None],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1],"IHTMLElement::%s"%"isContentEditable":[1]}
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
			attrs = [
				# the correct heading level tag, with no overriding aria-level.
				{"IHTMLDOMNode::nodeName": ["H%s" % nodeType[7:]],"HTMLAttrib::aria-level":['0',None]},
				# any tag with a role of heading, and the correct aria-level
				{"HTMLAttrib::role":["heading"],"HTMLAttrib::aria-level":[nodeType[7:]]},
				# Any heading level tag, with a correct overriding aria-level
				{"IHTMLDOMNode::nodeName": ["H1", "H2", "H3", "H4", "H5", "H6"],"HTMLAttrib::aria-level":[nodeType[7:]]},
			]
		elif nodeType == "heading":
			attrs = [{"IHTMLDOMNode::nodeName": ["H1", "H2", "H3", "H4", "H5", "H6"]},{"HTMLAttrib::role":["heading"]}]
		elif nodeType == "list":
			attrs = {"IHTMLDOMNode::nodeName": ["UL","OL","DL"]}
		elif nodeType == "listItem":
			attrs = {"IHTMLDOMNode::nodeName": ["LI","DD","DT"]}
		elif nodeType == "blockQuote":
			attrs = {"IHTMLDOMNode::nodeName": ["BLOCKQUOTE"]}
		elif nodeType == "graphic":
			attrs = [{"IHTMLDOMNode::nodeName": ["IMG"]},{"HTMLAttrib::role":["img"]}]
		elif nodeType == "frame":
			attrs = {"IHTMLDOMNode::nodeName": ["FRAME","IFRAME"]}
		elif nodeType=="focusable":
			attrs={"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="landmark":
			attrs = [
				{"HTMLAttrib::role": [VBufStorage_findMatch_word(lr) for lr in aria.landmarkRoles if lr != "region"]},
				{"HTMLAttrib::role": [VBufStorage_findMatch_word("region")],
					"name": [VBufStorage_findMatch_notEmpty]}
				]
		elif nodeType == "embeddedObject":
			attrs = {"IHTMLDOMNode::nodeName": ["OBJECT","EMBED","APPLET"]}
		elif nodeType == "separator":
			attrs = {"IHTMLDOMNode::nodeName": ["HR"]}
		else:
			return None
		return attrs

	def _activateLongDesc(self,controlField):
		longDesc=controlField['HTMLAttrib::longdesc']
		self.rootNVDAObject.HTMLNode.document.parentWindow.open(longDesc,'_blank','location=no, menubar=no, toolbar=no')


	def _activateNVDAObject(self,obj):
		super(MSHTML,self)._activateNVDAObject(obj)
		#If we activated a same-page link, then scroll to its anchor
		count=0
		# #4134: The link may not always be the deepest node
		while obj and count<3 and isinstance(obj,NVDAObjects.IAccessible.MSHTML.MSHTML):
			if obj.HTMLNodeName=="A":
				anchorName=getattr(obj.HTMLNode,'hash')
				if not anchorName:
					return 
				obj=self._getNVDAObjectByAnchorName(anchorName[1:],HTMLDocument=obj.HTMLNode.document)
				if not obj:
					return
				self._handleScrollTo(obj)
				return
			obj=obj.parent
			count+=1


	def _getNVDAObjectByAnchorName(self,name,HTMLDocument=None):
		if not HTMLDocument:
			HTMLDocument=self.rootNVDAObject.HTMLNode.document
		# #4134: could be name or ID, document.all.item supports both
		HTMLNode=HTMLDocument.all.item(name)
		if not HTMLNode:
			log.debugWarning("GetElementById can't find node with ID %s"%name)
			return None
		obj=NVDAObjects.IAccessible.MSHTML.MSHTML(HTMLNode=HTMLNode)
		return obj

	def _get_documentConstantIdentifier(self):
		try:
			return self.rootNVDAObject.HTMLNode.document.url
		except COMError:
			return None

	def shouldPassThrough(self, obj, reason=None):
		try:
			if not reason and not self.passThrough and obj.HTMLNodeName == "INPUT" and obj.HTMLNode.type == "file":
				# #1720: The user is activating a file input control in browse mode.
				# The NVDAObject for this is an editable text field,
				# but we want to activate the browse button instead of editing the field.
				return False
		except COMError:
			pass
		return super(MSHTML, self).shouldPassThrough(obj, reason)
