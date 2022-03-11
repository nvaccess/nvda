# virtualBuffers/MSHTML.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2009-2020 NV Access Limited, Babbage B.V., Accessolutions, Julien Cochuyt

from comtypes import COMError
import eventHandler
from . import VirtualBuffer, VirtualBufferTextInfo, VBufStorage_findMatch_word, VBufStorage_findMatch_notEmpty
import controlTypes
from controlTypes import TextPosition
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
import exceptions

FORMATSTATE_INSERTED=1
FORMATSTATE_DELETED=2
FORMATSTATE_MARKED=4
FORMATSTATE_STRONG=8
FORMATSTATE_EMPH=16

class MSHTMLTextInfo(VirtualBufferTextInfo):

	def _getTextPositionAttribute(self, attrs: dict) -> TextPosition:
		textPositionValue = attrs.get('text-position')
		try:
			return TextPosition(textPositionValue)
		except ValueError:
			log.debug(f'textPositionValue={textPositionValue}')
			return TextPosition.BASELINE

	def _normalizeFormatField(self, attrs):
		formatState=attrs.get('formatState',"0")
		formatState=int(formatState)
		if formatState&FORMATSTATE_INSERTED:
			attrs['revision-insertion']=True
		if formatState&FORMATSTATE_DELETED:
			attrs['revision-deletion']=True
		if formatState&FORMATSTATE_STRONG:
			attrs['strong']=True
		if formatState&FORMATSTATE_EMPH:
			attrs['emphasised']=True
		language=attrs.get('language')
		if language:
			attrs['language']=languageHandler.normalizeLanguage(language)
		textPosition = attrs.get('textPosition')
		textPosition = self._getTextPositionAttribute(attrs)
		attrs['text-position'] = textPosition
		return attrs

	def _getIsCurrentAttribute(self, attrs: dict) -> controlTypes.IsCurrent:
		defaultAriaCurrentStringVal = "false"
		ariaCurrentValue = attrs.get('HTMLAttrib::aria-current', defaultAriaCurrentStringVal)
		# key 'HTMLAttrib::aria-current' may be in attrs with a value of None
		ariaCurrentValue = defaultAriaCurrentStringVal if ariaCurrentValue is None else ariaCurrentValue
		try:
			ariaCurrent = controlTypes.IsCurrent(ariaCurrentValue)
		except ValueError:
			log.debugWarning(f"Unknown aria-current value: {ariaCurrentValue}")
			ariaCurrent = controlTypes.IsCurrent.NO
		return ariaCurrent

	# C901 'MSHTMLTextInfo._normalizeControlField' is too complex (42)
	# Look for opportunities to simplify this function.
	def _normalizeControlField(self, attrs: textInfos.ControlField):  # noqa: C901
		level = None

		isCurrent = self._getIsCurrentAttribute(attrs)
		if isCurrent != controlTypes.IsCurrent.NO:
			attrs['current'] = isCurrent

		placeholder = self._getPlaceholderAttribute(attrs, 'HTMLAttrib::aria-placeholder')
		if placeholder:
			attrs['placeholder']=placeholder
		nodeName=attrs.get('IHTMLDOMNode::nodeName',"")
		roleAttrib = attrs.get("HTMLAttrib::role", "")
		ariaRoles = [ar for ar in roleAttrib.split(" ") if ar]
		#choose role
		#Priority is aria role -> HTML tag name -> IAccessible role
		role = next(
			(aria.ariaRolesToNVDARoles[ar] for ar in ariaRoles if ar in aria.ariaRolesToNVDARoles),
			controlTypes.Role.UNKNOWN
		)
		if role == controlTypes.Role.UNKNOWN and nodeName:
			role=NVDAObjects.IAccessible.MSHTML.nodeNamesToNVDARoles.get(nodeName,controlTypes.Role.UNKNOWN)

		if role == controlTypes.Role.UNKNOWN:
			role = IAccessibleHandler.NVDARoleFromAttr(attrs.get('IAccessible::role'))

		roleText=attrs.get('HTMLAttrib::aria-roledescription')
		if roleText:
			attrs['roleText']=roleText

		states = IAccessibleHandler.getStatesSetFromIAccessibleAttrs(attrs)
		role, states = controlTypes.transformRoleStates(role, states)

		if attrs.get('HTMLAttrib::longdesc'):
			states.add(controlTypes.State.HASLONGDESC)
		#IE exposes destination anchors as links, this is wrong
		if nodeName=="A" and role==controlTypes.Role.LINK and controlTypes.State.LINKED not in states:
			role=controlTypes.Role.TEXTFRAME
		if 'IHTMLElement::isContentEditable' in attrs:
			states.add(controlTypes.State.EDITABLE)
		if 'HTMLAttrib::onclick' in attrs or 'HTMLAttrib::onmousedown' in attrs or 'HTMLAttrib::onmouseup' in attrs:
			states.add(controlTypes.State.CLICKABLE)
		if 'HTMLAttrib::required' in attrs or attrs.get('HTMLAttrib::aria-required','false')=='true':
			states.add(controlTypes.State.REQUIRED)
		description=None
		ariaDescribedBy=attrs.get('HTMLAttrib::aria-describedby')
		if ariaDescribedBy:
			ariaDescribedByIds=ariaDescribedBy.split()
			description=""
			for ariaDescribedById in ariaDescribedByIds:
				descNode=None
				try:
					descNode=self.obj.rootNVDAObject.HTMLNode.document.getElementById(ariaDescribedById)
				except (COMError,NameError):
					descNode=None
				if not descNode:
					try:
						descNode=NVDAObjects.IAccessible.MSHTML.locateHTMLElementByID(self.obj.rootNVDAObject.HTMLNode.document,ariaDescribedById)
					except (COMError,NameError):
						descNode=None
				if descNode:
					try:
						description=description+" "+self.obj.makeTextInfo(NVDAObjects.IAccessible.MSHTML.MSHTML(HTMLNode=descNode)).text
					except:
						pass
		ariaSort=attrs.get('HTMLAttrib::aria-sort')
		state=aria.ariaSortValuesToNVDAStates.get(ariaSort)
		if state is not None:
			states.add(state)
		ariaSelected=attrs.get('HTMLAttrib::aria-selected')
		if ariaSelected=="true":
			states.add(controlTypes.State.SELECTED)
		elif ariaSelected=="false":
			states.discard(controlTypes.State.SELECTED)
		ariaExpanded=attrs.get('HTMLAttrib::aria-expanded')
		if ariaExpanded=="true":
			states.add(controlTypes.State.EXPANDED)
		elif ariaExpanded=="false":
			states.add(controlTypes.State.COLLAPSED)
		if attrs.get('HTMLAttrib::aria-invalid','false')=='true':
			states.add(controlTypes.State.INVALID_ENTRY)
		if attrs.get('HTMLAttrib::aria-multiline','false')=='true':
			states.add(controlTypes.State.MULTILINE)
		if attrs.get('HTMLAttrib::aria-dropeffect','none')!='none':
			states.add(controlTypes.State.DROPTARGET)
		ariaGrabbed=attrs.get('HTMLAttrib::aria-grabbed',None)
		if ariaGrabbed=='false':
			states.add(controlTypes.State.DRAGGABLE)
		elif ariaGrabbed=='true':
			states.add(controlTypes.State.DRAGGING)
		if nodeName=="TEXTAREA":
			states.add(controlTypes.State.MULTILINE)
		if "H1"<=nodeName<="H6":
			level=nodeName[1:]
		if nodeName in ("UL","OL","DL"):
			states.add(controlTypes.State.READONLY)
		if role==controlTypes.Role.UNKNOWN:
			role=controlTypes.Role.TEXTFRAME
		if role==controlTypes.Role.GRAPHIC:
			# MSHTML puts the unavailable state on all graphics when the showing of graphics is disabled.
			# This is rather annoying and irrelevant to our users, so discard it.
			states.discard(controlTypes.State.UNAVAILABLE)
		lRole = aria.htmlNodeNameToAriaRoles.get(nodeName.lower())
		if lRole:
			ariaRoles.append(lRole)
		# If the first role is a landmark role, use it.
		landmark = ariaRoles[0] if ariaRoles and ariaRoles[0] in aria.landmarkRoles else None
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
		# Force focus mode for applications, and dialogs with no parent treeInterceptor (E.g. a dialog embedded in an application)  
		if rootNVDAObject.role==controlTypes.Role.APPLICATION or (rootNVDAObject.role==controlTypes.Role.DIALOG and (not rootNVDAObject.parent or not rootNVDAObject.parent.treeInterceptor or rootNVDAObject.parent.treeInterceptor.passThrough)):
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
		if not winUser.isDescendantWindow(self.rootDocHandle,obj.windowHandle) and obj.windowHandle!=self.rootDocHandle:
			return False
		return not self._isNVDAObjectInApplication(obj)

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
		except exceptions.CallCancelled:
			# #1831: If the root object isn't responding, treat the buffer as dead.
			# Otherwise, we'll keep querying it on every focus change and freezing.
			return False
		states=root.states
		if controlTypes.State.EDITABLE in states:
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
				{
					"IAccessible::role": [
						oleacc.ROLE_SYSTEM_CHECKBUTTON,
						oleacc.ROLE_SYSTEM_OUTLINE,
						oleacc.ROLE_SYSTEM_PUSHBUTTON,
						oleacc.ROLE_SYSTEM_PAGETAB,
						oleacc.ROLE_SYSTEM_RADIOBUTTON,
					],
					f"IAccessible::state_{oleacc.STATE_SYSTEM_READONLY}": [None],
				},
				{"IAccessible::role": [oleacc.ROLE_SYSTEM_COMBOBOX]},
				# Focusable edit fields (input type=text, including readonly ones)
				{
					"IAccessible::role": [oleacc.ROLE_SYSTEM_TEXT],
					f"IAccessible::state_{oleacc.STATE_SYSTEM_FOCUSABLE}": [1],
				},
				# Any top-most content editable element (E.g. an editable div for rhich text editing) 
				{
					"IHTMLElement::isContentEditable": [1],
					"parent::IHTMLElement::isContentEditable": [0, None],
				},
				{"IHTMLDOMNode::nodeName": ["SELECT"]},
				{"HTMLAttrib::role": ["listbox"]},
			]
		elif nodeType=="button":
			attrs={"IAccessible::role":[oleacc.ROLE_SYSTEM_PUSHBUTTON]}
		elif nodeType=="edit":
			attrs=[
				# Focusable edit fields (input type=text, including readonly ones)
				{"IAccessible::role":[oleacc.ROLE_SYSTEM_TEXT],"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]},
				# Any top-most content editable element (E.g. an editable div for rhich text editing) 
				{"IHTMLElement::isContentEditable":[1],"parent::IHTMLElement::isContentEditable":[0,None]},
			]
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
		elif nodeType == "annotation":
			attrs = {"IHTMLDOMNode::nodeName": ["INS","DEL"]}
		elif nodeType == "graphic":
			attrs = [{"IHTMLDOMNode::nodeName": ["IMG"]},{"HTMLAttrib::role":["img"]}]
		elif nodeType == "frame":
			attrs = {"IHTMLDOMNode::nodeName": ["FRAME","IFRAME"]}
		elif nodeType=="focusable":
			attrs={"IAccessible::state_%s"%oleacc.STATE_SYSTEM_FOCUSABLE:[1]}
		elif nodeType=="landmark":
			attrs = [
				{"HTMLAttrib::role": [VBufStorage_findMatch_word(lr) for lr in aria.landmarkRoles]},
				{
					"HTMLAttrib::role": [VBufStorage_findMatch_word("region")],
					"name": [VBufStorage_findMatch_notEmpty]
				},
				{"IHTMLDOMNode::nodeName": [
					VBufStorage_findMatch_word(node.upper()) for node, lr in aria.htmlNodeNameToAriaRoles.items()
					if lr in aria.landmarkRoles
				]},
				{
					"IHTMLDOMNode::nodeName": [VBufStorage_findMatch_word("SECTION")],
					"name": [VBufStorage_findMatch_notEmpty]
				},
			]
		elif nodeType == "article":
			attrs = [
				{"HTMLAttrib::role": [VBufStorage_findMatch_word("article")]},
				{"IHTMLDOMNode::nodeName": [VBufStorage_findMatch_word("ARTICLE")]},
			]
		elif nodeType == "grouping":
			attrs = [
				{
					"HTMLAttrib::role": [
						VBufStorage_findMatch_word(r) for r in ("group", "radiogroup")
					],
					"name": [VBufStorage_findMatch_notEmpty]
				},
				{
					"IHTMLDOMNode::nodeName": [VBufStorage_findMatch_word("FIELDSET")],
					"name": [VBufStorage_findMatch_notEmpty]
				},
			]
		elif nodeType == "embeddedObject":
			attrs = [
				{"IHTMLDOMNode::nodeName": ["OBJECT", "EMBED", "APPLET", "AUDIO", "VIDEO", "FIGURE"]},
				{"IAccessible::role": [oleacc.ROLE_SYSTEM_APPLICATION, oleacc.ROLE_SYSTEM_DIALOG]},
			]
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
