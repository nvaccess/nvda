#braille.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2008-2014 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
import typing

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
	"Sect": controlTypes.Role.SECTION,
	"Div": controlTypes.Role.SECTION,
	"BlockQuote": controlTypes.Role.BLOCKQUOTE,
	"Caption": controlTypes.Role.CAPTION,
	# Toc? Toci? Index? Nonstruct? Private? 
	# Table, TR, TH, TD covered by IAccessible
	"L": controlTypes.Role.LIST,
	"LI": controlTypes.Role.LISTITEM,
	"Lbl": controlTypes.Role.LABEL,
	# LBody
	"P": controlTypes.Role.PARAGRAPH,
	"H": controlTypes.Role.HEADING,
	# H1 to H6 handled separately
	# Span, Quote, Note, Reference, BibEntry, Code, Figure
	"Formula": controlTypes.Role.MATH,
	# form: a form field - MSAA roles are already much more specific here.
}


def normalizeStdName(stdName: str) -> typing.Tuple[controlTypes.Role, typing.Optional[str]]:
	"""
	@param stdName:
	@return: Tuple with the NVDA role and optionally the level number of the heading as a string, E.G.:
	"H5" produces "5"
	"""
	if stdName and "H1" <= stdName <= "H6":
		return controlTypes.Role.HEADING, stdName[1]

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

		if self.event_objectID is not None and self.event_objectID > 0:
			self.accID = self.event_objectID
		elif self.event_childID is not None and self.event_childID > 0:
			self.accID = self.event_childID
		else:
			try:
				self.accID = serv.QueryService(SID_AccID, IAccID).get_accID()
			except COMError:
				self.accID = None

		# Get the IPDDomNode.
		try:
			self.pdDomNode = serv.QueryService(SID_GetPDDomNode, IGetPDDomNode).get_PDDomNode(self.IAccessibleChildID)
		except COMError:
			self.pdDomNode = None

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
		if role == controlTypes.Role.PANE:
			# Pane doesn't make sense for nodes in a document.
			role = controlTypes.Role.TEXTFRAME
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

	def _getNodeMathMl(self, node):
		tag = node.GetTagName()
		yield "<%s" % tag
		# Output relevant attributes.
		if tag == "mfenced":
			for attr in "open", "close", "separators":
				val = node.GetAttribute(attr, "XML-1.00")
				if val:
					yield ' %s="%s"' % (attr, val)
		yield ">"
		val = node.GetValue()
		if val:
			yield val
		else:
			for childNum in range(node.GetChildCount()):
				try:
					subNode = node.GetChild(childNum).QueryInterface(IPDDomElement)
				except COMError:
					continue
				for sub in self._getNodeMathMl(subNode):
					yield sub
		yield "</%s>" % tag

	def _get_mathMl(self):
		# There could be other stuff before the math element. Ug.
		for childNum in range(self.pdDomNode.GetChildCount()):
			try:
				child = self.pdDomNode.GetChild(childNum).QueryInterface(IPDDomElement)
			except COMError:
				continue
			if child.GetTagName() == "math":
				return "".join(self._getNodeMathMl(child))
		raise LookupError

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

	def initOverlayClass(self):
		if self.name or not self.parent:
			return
		# HACK: There are three client objects, one with a name and two without.
		# The unnamed objects (probably manufactured by Acrobat) have broken next and previous relationships.
		# The unnamed objects' parent/grandparent is the named object, but when descending into the named object, the unnamed objects are skipped.
		# Given the brokenness of the unnamed objects, just skip them completely and use the parent/grandparent when they are encountered.
		try:
			acc = self.IAccessibleObject.accParent
			if not acc.accName(0):
				acc = acc.accParent
		except COMError:
			return
		self.IAccessibleObject = acc
		self.invalidateCache()

class BadFocusStates(AcrobatNode):
	"""An object which reports focus states when it shouldn't.
	"""

	def _get_states(self):
		states = super(BadFocusStates, self).states
		states.difference_update({controlTypes.State.FOCUSABLE, controlTypes.State.FOCUSED})
		return states

def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class(es) for Acrobat objects.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	role = obj.role
	states = obj.states
	if role == controlTypes.Role.DOCUMENT or (role == controlTypes.Role.PAGE and controlTypes.State.READONLY in states):
		clsList.append(Document)
	elif obj.event_childID == 0 and obj.event_objectID == winUser.OBJID_CLIENT:
		# Other root node.
		if role == controlTypes.Role.EDITABLETEXT:
			clsList.append(RootTextNode)
		else:
			clsList.append(RootNode)

	elif role == controlTypes.Role.EDITABLETEXT:
		if {controlTypes.State.READONLY, controlTypes.State.FOCUSABLE, controlTypes.State.LINKED} <= states:
			# HACK: Acrobat sets focus states on text nodes beneath links,
			# making them appear as read only editable text fields.
			clsList.append(BadFocusStates)
		elif controlTypes.State.FOCUSABLE in states:
			clsList.append(EditableTextNode)

	clsList.append(AcrobatNode)
