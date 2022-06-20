# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2006-2021 NV Access Limited

"""Base classes with common support for browsers exposing IAccessible2.
"""
import typing
from ctypes import c_short
from comtypes import COMError, BSTR

import oleacc
from comInterfaces import IAccessible2Lib as IA2
import controlTypes
from logHandler import log
from documentBase import DocumentWithTableNavigation
from NVDAObjects.behaviors import Dialog, WebDialog 
from . import IAccessible, Groupbox
from .ia2TextMozilla import MozillaCompoundTextInfo
import aria
import api
import speech
import config

class Ia2Web(IAccessible):
	IAccessibleTableUsesTableCellIndexAttrib=True
	caretMovementDetectionUsesEvents = False

	def _get_positionInfo(self):
		info=super(Ia2Web,self).positionInfo
		level=info.get('level',None)
		if not level:
			level=self.IA2Attributes.get('level',None)
			if level:
				info['level']=level
		return info

	def _get_descriptionFrom(self) -> controlTypes.DescriptionFrom:
		ia2attrDescriptionFrom: typing.Optional[str] = self.IA2Attributes.get("description-from")
		try:
			return controlTypes.DescriptionFrom(ia2attrDescriptionFrom)
		except ValueError:
			if ia2attrDescriptionFrom:
				log.debugWarning(f"Unknown 'description-from' IA2Attribute value: {ia2attrDescriptionFrom}")
			return controlTypes.DescriptionFrom.UNKNOWN

	def _get_detailsSummary(self) -> typing.Optional[str]:
		if not self.hasDetails:
			# optimisation that avoids having to fetch details relations which may be a more costly procedure.
			if config.conf["debugLog"]["annotations"]:
				log.debug("no details-roles")
			return None
		detailsRelations = self.detailsRelations
		if not detailsRelations:
			log.error("should be able to fetch detailsRelations")
			return None
		for target in detailsRelations:
			# just take the first for now.
			return target.summarizeInProcess()

	@property
	def hasDetails(self) -> bool:
		return bool(self.IA2Attributes.get("details-roles"))

	def _get_isCurrent(self) -> controlTypes.IsCurrent:
		ia2attrCurrent: str = self.IA2Attributes.get("current", "false")
		try:
			return controlTypes.IsCurrent(ia2attrCurrent)
		except ValueError:
			log.debugWarning(f"Unknown 'current' IA2Attribute value: {ia2attrCurrent}")
			return controlTypes.IsCurrent.NO

	def _get_placeholder(self):
		placeholder = self.IA2Attributes.get('placeholder', None)
		return placeholder

	def _get_isPresentableFocusAncestor(self):
		if self.role==controlTypes.Role.TABLEROW:
			# It is not useful to present IAccessible2 table rows in the focus ancestry as  cells contain row and column information anyway.
			# Also presenting the rows would cause duplication of information
			return False
		return super(Ia2Web,self).isPresentableFocusAncestor

	def _get_roleText(self):
		roleText = self.IA2Attributes.get('roledescription')
		if roleText:
			return roleText
		return super().roleText

	def _get_states(self):
		states=super(Ia2Web,self).states
		# Ensure that ARIA gridcells always get the focusable state, even if the Browser fails to provide it.
		# This is necessary for other code that calculates how selection of cells should be spoken.
		if 'gridcell' in self.IA2Attributes.get('xml-roles','').split(' '):
			states.add(controlTypes.State.FOCUSABLE)
		# Google has a custom ARIA attribute to force a node's editable state off (such as in Google Slides).
		if self.IA2Attributes.get('goog-editable')=="false":
			states.discard(controlTypes.State.EDITABLE)
		return states

	def _get_landmark(self):
		xmlRoles = self.IA2Attributes.get('xml-roles', '').split(' ')
		landmark = next((xr for xr in xmlRoles if xr in aria.landmarkRoles), None)
		if (
			landmark
			and self.IAccessibleRole != IA2.IA2_ROLE_LANDMARK
			and landmark != xmlRoles[0]
		):
			# Ignore the landmark role
			landmark = None
		if landmark:
			return landmark
		return super().landmark

	def event_IA2AttributeChange(self):
		super().event_IA2AttributeChange()
		if self is api.getFocusObject():
			# Report aria-current if it changed.
			speech.speakObjectProperties(
				self,
				current=True,
				reason=controlTypes.OutputReason.CHANGE
			)
		# super calls event_stateChange which updates braille, so no need to
		# update braille here.

	def _get_liveRegionPoliteness(self) -> aria.AriaLivePoliteness:
		politeness = self.IA2Attributes.get('live', "off")
		try:
			return aria.AriaLivePoliteness(politeness.lower())
		except ValueError:
			log.error(f"Unknown live politeness of {politeness}", exc_info=True)
			super().liveRegionPoliteness


class Document(Ia2Web):
	value = None

	def _get_shouldCreateTreeInterceptor(self):
		return controlTypes.State.READONLY in self.states

class Application(Document):
	shouldCreateTreeInterceptor = False

class BlockQuote(Ia2Web):
	role = controlTypes.Role.BLOCKQUOTE


class Treegrid(Ia2Web):
	role = controlTypes.Role.TABLE


class Article(Ia2Web):
	role = controlTypes.Role.ARTICLE


class Region(Ia2Web):
	role = controlTypes.Role.REGION


class Figure(Ia2Web):
	role = controlTypes.Role.FIGURE


class Editor(Ia2Web, DocumentWithTableNavigation):
	TextInfo = MozillaCompoundTextInfo

	def _getTableCellAt(self,tableID,startPos,destRow,destCol):
		# Locate the table in the object ancestry of the given document position. 
		obj=startPos.NVDAObjectAtStart
		while not obj.table and obj!=self:
			obj=obj.parent
		if not obj.table:
			# No table could be found
			raise LookupError
		table = obj.table
		try:
			# We support either IAccessibleTable or IAccessibleTable2 interfaces for locating table cells. 
			# We will be able to get at least one of these.  
			try:
				cell = table.IAccessibleTable2Object.cellAt(destRow - 1, destCol - 1).QueryInterface(IA2.IAccessible2)
			except AttributeError:
				# No IAccessibleTable2, try IAccessibleTable instead.
				cell = table.IAccessibleTableObject.accessibleAt(
					destRow - 1, destCol - 1
				).QueryInterface(IA2.IAccessible2)
			cell = IAccessible(IAccessibleObject=cell, IAccessibleChildID=0)
			# If the cell we fetched is marked as hidden, raise LookupError which will instruct calling code to try an adjacent cell instead.
			if cell.IA2Attributes.get('hidden'):
				raise LookupError("Found hidden cell") 
			# Return the position of the found cell
			return self.makeTextInfo(cell)
		except (COMError, RuntimeError):
			# Any of the above calls could throw a COMError, and sometimes a RuntimeError.
			# Treet this as the cell not existing.
			raise LookupError

	def event_loseFocus(self):
		# MozillaCompoundTextInfo caches the deepest object with the caret.
		# But this can create a reference cycle if not removed.
		# As we no longer need it once this object loses focus, we can delete it here.
		self._lastCaretObj = None
		super().event_loseFocus()


class EditorChunk(Ia2Web):
	beTransparentToMouse = True

class Math(Ia2Web):

	def _get_mathMl(self):
		from comtypes.gen.ISimpleDOM import ISimpleDOMNode
		try:
			node = self.IAccessibleObject.QueryInterface(ISimpleDOMNode)
			# Try the data-mathml attribute.
			attrNames = (BSTR * 1)("data-mathml")
			namespaceIds = (c_short * 1)(0)
			attr = node.attributesForNames(1, attrNames, namespaceIds)
			if attr:
				import mathPres
				if not mathPres.getLanguageFromMath(attr) and self.language:
					attr = mathPres.insertLanguageIntoMath(attr, self.language)
				return attr
			if self.IA2Attributes.get("tag") != "math":
				# This isn't MathML.
				raise LookupError
			if self.language:
				attrs = ' xml:lang="%s"' % self.language
			else:
				attrs = ""
			return "<math%s>%s</math>" % (attrs, node.innerHTML)
		except COMError:
			log.debugWarning("Error retrieving math. "
				"Not supported in this browser or ISimpleDOM COM proxy not registered.", exc_info=True)
			raise LookupError


class Switch(Ia2Web):
	# role="switch" gets mapped to IA2_ROLE_TOGGLE_BUTTON, but it uses the
	# checked state instead of pressed. The simplest way to deal with this
	# identity crisis is to map it to a check box.
	role = controlTypes.Role.CHECKBOX

	def _get_states(self):
		states = super().states
		states.discard(controlTypes.State.PRESSED)
		return states


def findExtraOverlayClasses(obj, clsList, baseClass=Ia2Web, documentClass=None):
	"""Determine the most appropriate class if this is an IA2 web object.
	This should be called after finding any classes for the specific web implementation.
	@param baseClass: The base class for all web objects.
	@param documentClass: The class to use for document roots, including ARIA applications.
	"""
	if not documentClass:
		raise ValueError("documentClass cannot be None")
	if not isinstance(obj.IAccessibleObject, IA2.IAccessible2):
		return

	iaRole = obj.IAccessibleRole
	xmlRoles = obj.IA2Attributes.get("xml-roles", "").split(" ")
	if iaRole == IA2.IA2_ROLE_SECTION and obj.IA2Attributes.get("tag", None) == "blockquote":
		clsList.append(BlockQuote)
	elif iaRole == oleacc.ROLE_SYSTEM_OUTLINE and "treegrid" in xmlRoles:
		clsList.append(Treegrid)
	elif iaRole == oleacc.ROLE_SYSTEM_DOCUMENT and xmlRoles[0] == "article":
		clsList.append(Article)
	elif xmlRoles[0] == "region" and obj.name:
		clsList.append(Region)
	elif xmlRoles[0] == "figure":
		clsList.append(Figure)
	elif iaRole == oleacc.ROLE_SYSTEM_ALERT:
		clsList.append(Dialog)
	elif iaRole == oleacc.ROLE_SYSTEM_EQUATION:
		clsList.append(Math)
	elif xmlRoles[0] == "switch":
		clsList.append(Switch)
	elif iaRole == oleacc.ROLE_SYSTEM_GROUPING:
		try:
			# The Groupbox class uses sibling text as the description. This is
			# inappropriate for IA2 web browsers.
			clsList.remove(Groupbox)
		except ValueError:
			pass

	if iaRole==oleacc.ROLE_SYSTEM_APPLICATION:
		clsList.append(Application)
	if iaRole == oleacc.ROLE_SYSTEM_DIALOG:
		clsList.append(WebDialog)
	if (
		iaRole in (oleacc.ROLE_SYSTEM_APPLICATION, oleacc.ROLE_SYSTEM_DIALOG)
		or (iaRole == oleacc.ROLE_SYSTEM_DOCUMENT and Article not in clsList)
	):
		clsList.append(documentClass)

	if obj.IA2States & IA2.IA2_STATE_EDITABLE:
		if obj.IAccessibleStates & oleacc.STATE_SYSTEM_FOCUSABLE:
			clsList.append(Editor)
		else:
			clsList.append(EditorChunk)

	if iaRole in (oleacc.ROLE_SYSTEM_DIALOG,oleacc.ROLE_SYSTEM_PROPERTYPAGE):
		if "dialog" in xmlRoles or "tabpanel" in xmlRoles:
			# #2390: Don't try to calculate text for ARIA dialogs.
			# #4638: Don't try to calculate text for ARIA tab panels.
			try:
				clsList.remove(Dialog)
			except ValueError:
				pass

	clsList.append(baseClass)
