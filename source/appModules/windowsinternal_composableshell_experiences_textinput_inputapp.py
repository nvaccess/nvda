# App module for Composable Shell (CShell) input panel
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017-2018 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Windows 10 Modern Keyboard aka new touch keyboard panel.
The chief feature is allowing NVDA to announce selected emoji when using the keyboard to search for and select one.
Another feature is to announce candidates for misspellings if suggestions for hardware keyboard is selected.
This is applicable on Windows 10 Fall Creators Update and later."""

import appModuleHandler
import api
import speech
import braille
import ui
import config
import winVersion
from NVDAObjects.UIA import UIA

class AppModule(appModuleHandler.AppModule):

	# Cache the most recently selected item.
	_recentlySelected = None

	def event_UIA_elementSelected(self, obj, nextHandler):
		# #7273: When this is fired on categories, the first emoji from the new category is selected but not announced.
		# Therefore, move the navigator object to that item if possible.
		# However, in recent builds, name change event is also fired.
		# For consistent experience, report the new category first by traversing through controls.
		# #8189: do not announce candidates list itself (not items), as this is repeated each time candidate items are selected.
		if obj.UIAElement.cachedAutomationID == "CandidateList": return
		speech.cancelSpeech()
		# Sometimes clipboard candidates list gets selected, so ask NvDA to descend one more level.
		if obj.UIAElement.cachedAutomationID == "TEMPLATE_PART_ClipboardItemsList":
			obj = obj.firstChild
		candidate = obj
		# Sometimes, due to bad tree traversal, something other than the selected item sees this event.
		parent = obj.parent
		if obj.UIAElement.cachedClassName == "ListViewItem" and isinstance(parent, UIA) and parent.UIAElement.cachedAutomationID != "TEMPLATE_PART_ClipboardItemsList":
			# The difference between emoji panel and suggestions list is absence of categories/emoji separation.
			# Turns out automation ID for the container is different, observed in build 17666 when opening clipboard copy history.
			candidate = obj.parent.previous
			if candidate is not None:
				# Emoji categories list.
				ui.message(candidate.name)
				obj = candidate.firstChild
		if obj is not None:
			api.setNavigatorObject(obj)
			obj.reportFocus()
			braille.handler.message(braille.getBrailleTextForProperties(name=obj.name, role=obj.role, positionInfo=obj.positionInfo))
			# Cache selected item.
			self._recentlySelected = obj.name
		else:
			# Translators: presented when there is no emoji when searching for one in Windows 10 Fall Creators Update and later.
			ui.message(_("No emoji"))
		nextHandler()

	def event_UIA_window_windowOpen(self, obj, nextHandler):
		# Make sure to announce most recently used emoji first in post-1709 builds.
		# Fake the announcement by locating 'most recently used" category and calling selected event on this.
		# However, in build 17666 and later, child count is the same for both emoji panel and hardware keyboard candidates list.
		if winVersion.winVersion.build <= 17134 and obj.childCount == 3:
			self.event_UIA_elementSelected(obj.lastChild.firstChild, nextHandler)
		# Handle hardware keyboard suggestions.
		# Treat it the same as CJK composition list - don't announce this if candidate announcement setting is off.
		# This is also the case for emoji panel in build 17666 and later.
		elif obj.childCount == 1:
			childAutomationID = obj.firstChild.UIAElement.cachedAutomationID
			if childAutomationID == "CandidateWindowControl" and config.conf["inputComposition"]["autoReportAllCandidates"]:
				try:
					self.event_UIA_elementSelected(obj.firstChild.firstChild.firstChild, nextHandler)
				except AttributeError:
					# Because this is dictation window.
					pass
			# Emoji panel in build 17666 and later (unless this changes).
			elif childAutomationID == "TEMPLATE_PART_ExpressionGroupedFullView":
				self._emojiPanelJustOpened = True
				self.event_UIA_elementSelected(obj.firstChild.firstChild.next.next.firstChild.firstChild, nextHandler)
		nextHandler()

	# Argh, name change event is fired right after emoji panel opens in build 17666 and later.
	_emojiPanelJustOpened = False

	def event_nameChange(self, obj, nextHandler):
		# #49: reported by a user: on some systems, touch keyboard keys keeps firing name change event.
		# Argh, in build 17704, whenever skin tones are selected, name change is fired by emoji entries (GridViewItem).
		if ((obj.UIAElement.cachedClassName in ("CRootKey", "GridViewItem"))
		or (obj.UIAElement.cachedAutomationID == "TEMPLATE_PART_ClipboardItemsList")
		# And no, emoji entries should not be announced here.
		or (self._recentlySelected is not None and self._recentlySelected in obj.name)):
			return
		# The word "blank" is kept announced, so suppress this on build 17666 and later.
		if winVersion.winVersion.build > 17134:
			# In build 17672 and later, return immediatley when element selected event on clipboard item was fired just prior to this.
			if obj.UIAElement.cachedAutomationID == "TEMPLATE_PART_ClipboardItemIndex" or obj.parent.UIAElement.cachedAutomationID == "TEMPLATE_PART_ClipboardItemsList": return
			if not self._emojiPanelJustOpened or obj.UIAElement.cachedAutomationID != "TEMPLATE_PART_ExpressionGroupedFullView": speech.cancelSpeech()
			self._emojiPanelJustOpened = False
		# Don't forget to add "Microsoft Candidate UI" as something that should be suppressed.
		if obj.UIAElement.cachedAutomationID not in ("TEMPLATE_PART_ExpressionFullViewItemsGrid", "TEMPLATE_PART_ClipboardItemIndex", "CandidateWindowControl"):
			ui.message(obj.name)
		nextHandler()
