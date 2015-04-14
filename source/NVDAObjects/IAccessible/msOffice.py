#NVDAObjects/IAccessible/msOffice.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

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
		if not name and self.role==controlTypes.ROLE_LISTITEM:
			name=self.displayText
		return name

	def _get_positionInfo(self):
		if self.role!=controlTypes.ROLE_LISTITEM:
			return {}
		return super(SDM,self).positionInfo

	def _get_parent(self):
		if self.IAccessibleChildID == 0 and self.role not in (controlTypes.ROLE_DIALOG, controlTypes.ROLE_PROPERTYPAGE, controlTypes.ROLE_WINDOW):
			# SDM child IAccessible objects have a broken accParent.
			# The parent should be the dialog.
			return getNVDAObjectFromEvent(self.windowHandle, winUser.OBJID_CLIENT, 0)
		return super(SDM, self).parent

	def _get_SDMChild(self):
		if controlTypes.STATE_FOCUSED in self.states:
			hwndFocus=winUser.getGUIThreadInfo(0).hwndFocus
			if hwndFocus and hwndFocus!=self.windowHandle and winUser.isDescendantWindow(self.windowHandle,hwndFocus) and not winUser.getClassName(hwndFocus).startswith('bosa_sdm'):
				obj=getNVDAObjectFromEvent(hwndFocus,winUser.OBJID_CLIENT,0)
				if not obj: return None
				if getattr(obj,'parentSDMCanOverrideName',True):
					obj.name=self.name
				return obj
		return None

class MSOUNISTAT(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_STATICTEXT

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
			if not next.keyboardShortcut and next.role==controlTypes.ROLE_STATICTEXT:
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
