# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2020 NV Access Limited, Manish Agrawal, Łukasz Golonka
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import oleacc
import IAccessibleHandler
import controlTypes
import winUser
import api
from . import IAccessible, getNVDAObjectFromEvent
import eventHandler
import re

"""Miscellaneous support for Microsoft Office applications.
"""

class SDM(IAccessible):

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# #4199: Some SDM controls can incorrectly firefocus when they are not focused
		# E.g. File recovery pane, clipboard manager pane
		if winUser.getGUIThreadInfo(0).hwndFocus!=self.windowHandle:
			return False
		return super(SDM,self).shouldAllowIAccessibleFocusEvent

	def _get_name(self):
		name=super(SDM,self).name
		if not name and self.role==controlTypes.Role.LISTITEM:
			name=self.displayText
		return name

	def _get_positionInfo(self):
		if self.role!=controlTypes.Role.LISTITEM:
			return {}
		return super(SDM,self).positionInfo

	def _get_parent(self):
		if self.IAccessibleChildID == 0 and self.role not in (controlTypes.Role.DIALOG, controlTypes.Role.PROPERTYPAGE, controlTypes.Role.WINDOW):
			# SDM child IAccessible objects have a broken accParent.
			# The parent should be the dialog.
			return getNVDAObjectFromEvent(self.windowHandle, winUser.OBJID_CLIENT, 0)
		return super(SDM, self).parent

	def _get_presentationType(self):
		t=super(SDM,self).presentationType
		if t==self.presType_content and self.SDMChild:
			t=self.presType_layout
		return t

	def _get_firstChild(self):
		child=super(SDM,self).firstChild
		if not child:
			child=self.SDMChild
		return child

	def _get_lastChild(self):
		child=super(SDM,self).lastChild
		if not child:
			child=self.SDMChild
		return child

	def _get_SDMChild(self):
		if controlTypes.State.FOCUSED in self.states:
			hwndFocus=winUser.getGUIThreadInfo(0).hwndFocus
			if hwndFocus and hwndFocus!=self.windowHandle and winUser.isDescendantWindow(self.windowHandle,hwndFocus) and not winUser.getClassName(hwndFocus).startswith('bosa_sdm'):
				obj=getNVDAObjectFromEvent(hwndFocus,winUser.OBJID_CLIENT,0)
				if not obj: return None
				if getattr(obj,'parentSDMCanOverrideName',True):
					obj.name=self.name
				obj.keyboardShortcut=self.keyboardShortcut
				obj.parent=self
				return obj
		return None

class MSOUNISTAT(IAccessible):

	def _get_role(self):
		return controlTypes.Role.STATICTEXT

class MsoCommandBarToolBar(IAccessible):

	def _get_isPresentableFocusAncestor(self):
		# #4096: Many single controls are  wrapped in their own SmoCommandBar toolbar.
		# Therefore suppress reporting of these toolbars in focus ancestry if they only have one child.
		if self.childCount==1:
			return False
		return super(MsoCommandBarToolBar,self).isPresentableFocusAncestor

	def _get_name(self):
		name=super(MsoCommandBarToolBar,self).name
		# #3407: overly verbose and programmatic toolbar label
		if name and name.startswith('MSO Generic Control Container'):
			name=u""
		return name

	description=None

class BrokenMsoCommandBar(IAccessible):
	"""Work around broken IAccessible implementation for Microsoft Office XP-2003 toolbars.
	For these IAccessibles, accNavigate is rather broken
	and retrieving only the first child with AccessibleChildren causes a crash.
	"""

	@classmethod
	def appliesTo(cls, obj):
		return obj.childCount > 0 and not IAccessibleHandler.accNavigate(obj.IAccessibleObject, obj.IAccessibleChildID, oleacc.NAVDIR_FIRSTCHILD)

	def _get_firstChild(self):
		# accNavigate incorrectly returns nothing for NAVDIR_FIRSTCHILD and requesting one child with AccessibleChildren causes a crash.
		# Therefore, we must use accChild(1).
		child = IAccessibleHandler.accChild(self.IAccessibleObject, 1)
		if not child:
			return None
		return IAccessible(IAccessibleObject=child[0], IAccessibleChildID=child[1])

	# accNavigate incorrectly returns the first child for NAVDIR_NEXT.
	next = None
	# description is redundant.
	description = None

	def _get_name(self):
		name = super(BrokenMsoCommandBar, self).name
		if name == "MSO Generic Control Container":
			return None
		return name

class CommandBarListItem(IAccessible):
	"""A list item in an MSO commandbar, that may be part of a color palet."""

	COMPILED_RE = re.compile(r'RGB\(\d+, \d+, \d+\)',re.I)
	def _get_rgbNameAndMatch(self):
		name = super(CommandBarListItem,self).name
		if self.COMPILED_RE.match(name):
			matchRGB = True
		else:
			matchRGB = False
		return name, matchRGB

	def _get_name(self):
		name, matchRGB = self.rgbNameAndMatch
		if matchRGB:
			import colors
			return colors.RGB.fromString(name).name
		else:
			return name

	def _get_description(self):
		name, matchRGB = self.rgbNameAndMatch
		if matchRGB:
			import colors
			rgb=colors.RGB.fromString(name)
			# Translators: a color, broken down into its RGB red, green, blue parts.
			return _("RGB red {rgb.red}, green {rgb.green}, blue {rgb.blue}").format(rgb=colors.RGB.fromString(name))
		else:
			return super(CommandBarListItem,self).description

class SDMSymbols(SDM):

	def _get_value(self):
		#The value (symbol) is in a static text field somewhere in the direction of next.
		# There can be multiple symbol lists all in a row, and these lists have their own static text labels, yet the active list's value field is always after them all.
		# static text labels for these lists seem to have a keyboardShortcut, therefore we can skip over those.
		next=self.next
		while next:
			if not next.keyboardShortcut and next.role==controlTypes.Role.STATICTEXT:
				return next.name
			next=next.next

	def script_selectGraphic(self, gesture):
		gesture.send()
		eventHandler.queueEvent("valueChange",self)

	__gestures = {
		"kb:downArrow": "selectGraphic",
		"kb:upArrow": "selectGraphic",
		"kb:home": "selectGraphic",
		"kb:end": "selectGraphic",
		"kb:leftArrow": "selectGraphic",
		"kb:rightArrow": "selectGraphic",
	}


class StatusBar (IAccessible):

	def _get_role(self):
		""" #4257: Status bar in Office applications does not  expose proper role via IAccessible.
We cannot acces it via UIA because it does not fire focus events when focused for the first time.
Fortunately accValue contains "status bar" and is not localized.
"""
		accValue = self.IAccessibleObject.accValue(self.IAccessibleChildID)
		if accValue == 'Ribbon Tab':
			return controlTypes.Role.TAB
		if accValue == 'Status Bar':
			return controlTypes.Role.STATUSBAR
		return super()._get_role()

	def _get_description(self):
		return ""

	def _get_isPresentableFocusAncestor(self):
		accValue = self.IAccessibleObject.accValue(self.IAccessibleChildID)
		if accValue == "Ribbon":
			return False
		return super().isPresentableFocusAncestor


class RibbonSection (IAccessible):

	def _get_role(self):
		accValue = self.IAccessibleObject.accValue(self.IAccessibleChildID)
		if accValue == "Group":
			return controlTypes.Role.GROUPING
		return super()._get_role()
