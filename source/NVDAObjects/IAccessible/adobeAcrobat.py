import api
import controlTypes
import eventHandler
import winUser
from . import IAccessible, getNVDAObjectFromEvent
from NVDAObjects import NVDAObjectTextInfo
from NVDAObjects.behaviors import EditableText
from comtypes import GUID, COMError, IServiceProvider
from comtypes.gen.AcrobatAccessLib import IAccID, IGetPDDomNode, IPDDomElement
from logHandler import log

SID_AccID = GUID("{449D454B-1F46-497e-B2B6-3357AED9912B}")
SID_GetPDDomNode = GUID("{C0A1D5E9-1142-4cf3-B607-82FC3B96A4DF}")

stdNamesToRoles = {
	# Part? Art?
	"Sect": controlTypes.ROLE_SECTION,
	"Div": controlTypes.ROLE_SECTION,
	"BlockQuote": controlTypes.ROLE_BLOCKQUOTE,
	"Caption": controlTypes.ROLE_CAPTION,
	# Toc? Toci? Index? Nonstruct? Private? 
	# Table, TR, TH, TD covered by IAccessible
	"L": controlTypes.ROLE_LIST,
	"LI": controlTypes.ROLE_LISTITEM,
	"Lbl": controlTypes.ROLE_LABEL,
	# LBody
	"P": controlTypes.ROLE_PARAGRAPH,
	"H": controlTypes.ROLE_HEADING,
	# H1 to H6 handled separately
	# Span, Quote, Note, Reference, BibEntry, Code, Figure, Formula
	"Form": controlTypes.ROLE_FORM,
}

def normalizeStdName(stdName):
	if "H1" <= stdName <= "H6":
		return controlTypes.ROLE_HEADING, stdName[1]

	try:
		return stdNamesToRoles[stdName], None
	except KeyError:
		pass

	raise LookupError

class AcrobatNode(IAccessible):

	def initOverlayClass(self):
		try:
			serv = self.IAccessibleObject.QueryInterface(IServiceProvider)
		except COMError:
			log.debugWarning("Could not get IServiceProvider")
			return

		if self.event_objectID > 0:
			self.accID = self.event_objectID
		elif self.event_childID > 0:
			self.accID = self.event_childID
		else:
			try:
				self.accID = serv.QueryService(SID_AccID, IAccID).get_accID()
			except COMError:
				log.debugWarning("Failed to get ID from IAccID", exc_info=True)
				self.accID = None

		# Get the IPDDomNode.
		try:
			self.pdDomNode = serv.QueryService(SID_GetPDDomNode, IGetPDDomNode).get_PDDomNode(self.IAccessibleChildID)
		except COMError:
			self.pdDomNode = None
			log.debugWarning("Error getting IPDDomNode")

		if self.pdDomNode:
			# If this node has IPDDomElement, query to that.
			try:
				self.pdDomNode = self.pdDomNode.QueryInterface(IPDDomElement)
			except COMError:
				pass

	def _get_role(self):
		try:
			return normalizeStdName(self.pdDomNode.GetStdName())[0]
		except (AttributeError, LookupError, COMError):
			pass

		role = super(AcrobatNode, self).role
		if role == controlTypes.ROLE_PANE:
			# Pane doesn't make sense for nodes in a document.
			role = controlTypes.ROLE_TEXTFRAME
		return role

	def scrollIntoView(self):
		try:
			self.pdDomNode.ScrollTo()
		except (AttributeError, COMError):
			log.debugWarning("IPDDomNode::ScrollTo failed", exc_info=True)

	def _isEqual(self, other):
		if self.windowHandle == other.windowHandle and self.accID and other.accID:
			return self.accID == other.accID
		return super(AcrobatNode, self)._isEqual(other)

class RootNode(AcrobatNode):
	shouldAllowIAccessibleFocusEvent = True

	def event_valueChange(self):
		# Acrobat has indicated that a page has died and been replaced by a new one.
		if not self.isInForeground:
			# If this isn't in the foreground, it doesn't matter,
			# as focus will be fired on the correct object when it is in the foreground again.
			return
		# The new page has the same event params, so we must bypass NVDA's IAccessible caching.
		obj = getNVDAObjectFromEvent(self.windowHandle, winUser.OBJID_CLIENT, 0)
		if not obj:
			return
		eventHandler.queueEvent("gainFocus",obj)

class Document(RootNode):

	def _get_treeInterceptorClass(self):
		import virtualBuffers.adobeAcrobat
		return virtualBuffers.adobeAcrobat.AdobeAcrobat

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# HACK: #1659: When moving the focus, Acrobat sometimes fires focus on the document before firing it on the real focus;
		# e.g. when tabbing through a multi-page form.
		# This causes extraneous verbosity.
		# Therefore, if already focused inside this document, only allow focus on the document if it has no active descendant.
		if api.getFocusObject().windowHandle == self.windowHandle:
			try:
				return self.IAccessibleObject.accFocus in (None, 0)
			except COMError:
				pass
		return super(Document, self).shouldAllowIAccessibleFocusEvent

class RootTextNode(RootNode):
	"""The message text node that appears instead of the document when the document is not available.
	"""

	def _get_parent(self):
		#hack: This code should be taken out once the crash is fixed in Adobe Reader X.
		#If going parent on a root text node after saying ok to the accessibility options (untagged) and before the processing document dialog appears, Reader X will crash.
		return api.getDesktopObject()

class AcrobatTextInfo(NVDAObjectTextInfo):

	def _getStoryText(self):
		return self.obj.value or ""

	def _getCaretOffset(self):
		caret = getNVDAObjectFromEvent(self.obj.windowHandle, winUser.OBJID_CARET, 0)
		if not caret:
			raise RuntimeError("No caret")
		try:
			return int(caret.description)
		except (ValueError, TypeError):
			raise RuntimeError("Bad caret index")

class EditableTextNode(EditableText, AcrobatNode):
	TextInfo = AcrobatTextInfo

	def event_valueChange(self):
		pass

class AcrobatSDIWindowClient(IAccessible):

	def __init__(self, **kwargs):
		super(AcrobatSDIWindowClient, self).__init__(**kwargs)
		if not self.name and self.parent:
			# There are two client objects, one with a name and one without.
			# The unnamed object (probably manufactured by Acrobat) has broken next and previous relationships.
			# The unnamed object's parent is the named object, but when descending into the named object, the unnamed object is skipped.
			# Given the brokenness of the unnamed object, just skip it completely and use the parent when it is encountered.
			self.IAccessibleObject = self.IAccessibleObject.accParent

def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class(es) for Acrobat objects.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	role = obj.role
	if obj.event_childID == 0 and obj.event_objectID == winUser.OBJID_CLIENT:
		# Root node.
		if role in (controlTypes.ROLE_DOCUMENT,controlTypes.ROLE_PAGE):
			clsList.append(Document)
		elif role == controlTypes.ROLE_EDITABLETEXT:
			clsList.append(RootTextNode)
		else:
			clsList.append(RootNode)

	elif role == controlTypes.ROLE_EDITABLETEXT and controlTypes.STATE_FOCUSABLE in obj.states:
		clsList.append(EditableTextNode)

	clsList.append(AcrobatNode)
