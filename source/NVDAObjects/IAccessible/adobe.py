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

	def _get_virtualBufferClass(self):
		if self.role in (controlTypes.ROLE_DOCUMENT,controlTypes.ROLE_PAGE):
			import virtualBuffers.adobeAcrobat
			return virtualBuffers.adobeAcrobat.AdobeAcrobat
		return super(AcrobatNode,self).virtualBufferClass

	def __init__(self, **kwargs):
		super(AcrobatNode, self).__init__(**kwargs)

		try:
			serv = self.IAccessibleObject.QueryInterface(IServiceProvider)
		except COMError:
			log.debugWarning("Could not get IServiceProvider")
			return

		if self.event_objectID is None:
			# This object does not have real event parameters.
			# Get the real child ID using IAccID.
			try:
				self.event_childID = serv.QueryService(SID_AccID, IAccID).get_accID()
			except COMError:
				log.debugWarning("Failed to get ID from IAccID", exc_info=True)

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

	def _get_shouldAllowIAccessibleFocusEvent(self):
		#Acrobat document root objects do not have their focused state set when they have the focus.
		if self.event_childID==0:
			return True
		return super(AcrobatNode,self).shouldAllowIAccessibleFocusEvent

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

	def event_valueChange(self):
		if self.event_childID==0 and self.event_objectID == winUser.OBJID_CLIENT and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			# Acrobat has indicated that a page has died and been replaced by a new one.
			# The new page has the same event params, so we must bypass NVDA's IAccessible caching.
			obj = getNVDAObjectFromEvent(self.windowHandle, -4, 0)
			if not obj:
				return
			eventHandler.queueEvent("gainFocus",obj)

	def scrollIntoView(self):
		try:
			self.pdDomNode.ScrollTo()
		except (AttributeError, COMError):
			log.debugWarning("IPDDomNode::ScrollTo failed", exc_info=True)

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

class AcrobatTextNode(EditableText, AcrobatNode):
	TextInfo = AcrobatTextInfo

class AcrobatSDIWindowClient(IAccessible):

	def __init__(self, **kwargs):
		super(AcrobatSDIWindowClient, self).__init__(**kwargs)
		if not self.name and self.parent:
			# There are two client objects, one with a name and one without.
			# The unnamed object (probably manufactured by Acrobat) has broken next and previous relationships.
			# The unnamed object's parent is the named object, but when descending into the named object, the unnamed object is skipped.
			# Given the brokenness of the unnamed object, just skip it completely and use the parent when it is encountered.
			self.IAccessibleObject = self.IAccessibleObject.accParent
