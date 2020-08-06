# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2020 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Windows 10 Modern Keyboard aka new touch keyboard panel.
The chief feature is announcing selected emoji when using the keyboard to search for and select one.
Other features include announcing candidates for misspellings if suggestions for hardware keyboard is active,
managing clipboard history, and dictation support.
This is applicable on Windows 10 Fall Creators Update and later."""

import appModuleHandler
import api
import speech
import braille
import ui
import config
import winVersion
import eventHandler
from NVDAObjects.UIA import UIA


class AppModule(appModuleHandler.AppModule):

	# Inform NVDA that modern keyboard interface is active.
	_modernKeyboardInterfaceActive = False
	# Cache the most recently selected item.
	_recentlySelected = None
	# Set when an emoji/kaomoji/symbol group item is selected.
	_symbolsGroupSelected = False
	# Set when emoji/kaomoji/symbol search is in progress, used to prevent unpredictable state announcements.
	_searchInProgress = False

	def event_UIA_elementSelected(self, obj, nextHandler):
		# Wait until modern keyboard is fully displayed on screen.
		# Not seen in Version 1709 as window open event is not fired.
		# Force this flag on if emoji search is in progress.
		if self._searchInProgress:
			self._modernKeyboardInterfaceActive = True
		if winVersion.isWin10(version=1803) and not self._modernKeyboardInterfaceActive:
			return
		# If emoji/kaomoji/symbols group item gets selected,
		# just tell NVDA to treat it as the new navigator object (for presentational purposes) and move on.
		if obj.parent.UIAAutomationId == "TEMPLATE_PART_Groups_ListView":
			if obj.positionInfo["indexInGroup"] == 1:
				self._searchInProgress = True
			else:
				# Symbols group flag must be set if and only if emoji panel is active,
				# because element selected event is fired when opening the panel after a while.
				api.setNavigatorObject(obj)
				self._symbolsGroupSelected = True
			return
		# #7273: in Version 1709 and 1803, first emoji from the newly selected category is not announced.
		# Therefore, move the navigator object to that item if possible.
		# In Version 1809 and later, name change event is also fired.
		# For consistent experience, report the new category first by traversing through controls.
		# #8189: do not announce candidates list itself (not items),
		# as this is repeated each time candidate items are selected.
		if (
			obj.UIAAutomationId == "CandidateList"
			# Also, when changing categories (emoji, kaomoji, symbols) in Version 1903 or later,
			# category items are selected when in fact they have no useful label.
			or obj.parent.UIAAutomationId == "TEMPLATE_PART_Sets_ListView"
			# Suppress skin tone modifiers from being announced after an emoji group was selected.
			or self._symbolsGroupSelected
			# In Version 1709 and 1803, both categories and items raise element selected event when category changes.
			or obj.name == self._recentlySelected and not winVersion.isWin10(version=1809)
		):
			return
		speech.cancelSpeech()
		# Sometimes, due to bad tree traversal or wrong item getting selected,
		# something other than the selected item sees this event.
		# Sometimes clipboard candidates list gets selected, so ask NvDA to descend one more level.
		if obj.UIAAutomationId == "TEMPLATE_PART_ClipboardItemsList":
			obj = obj.firstChild
		# In build 18262, emoji panel may open to People group and skin tone modifier
		# or the list housing them gets selected.
		elif obj.UIAAutomationId == "SkinTonePanelModifier_ListView":
			obj = obj.next
		elif obj.parent.UIAAutomationId == "SkinTonePanelModifier_ListView":
			# But this will point to nothing if emoji search results are not people.
			if obj.parent.next is not None:
				obj = obj.parent.next
			else:
				obj = obj.parent.parent.firstChild
		candidate = obj
		if (
			obj and obj.UIAElement.cachedClassName == "ListViewItem"
			and obj.parent and isinstance(obj.parent, UIA)
			and obj.parent.UIAAutomationId != "TEMPLATE_PART_ClipboardItemsList"
		):
			# The difference between emoji panel and suggestions list is absence of categories/emoji separation.
			# Turns out automation ID for the container is different, observed in
			# build 17666 when opening clipboard copy history.
			candidate = obj.parent.previous
			if candidate is not None:
				# Emoji categories list.
				ui.message(candidate.name)
				obj = candidate.firstChild
		if obj is not None:
			api.setNavigatorObject(obj)
			obj.reportFocus()
			braille.handler.message(braille.getPropertiesBraille(
				name=obj.name,
				role=obj.role,
				positionInfo=obj.positionInfo
			))
			# Cache selected item.
			self._recentlySelected = obj.name
		else:
			# Translators: presented when there is no emoji when searching for one in
			# Windows 10 Fall Creators Update and later.
			ui.message(_("No emoji"))
		nextHandler()

	# Emoji panel for build 16299 and 17134.
	_classicEmojiPanelAutomationID = (
		"TEMPLATE_PART_ExpressiveInputFullViewFuntionBarItemControl",
		"TEMPLATE_PART_ExpressiveInputFullViewFuntionBarCloseButton"
	)

	def event_UIA_window_windowOpen(self, obj, nextHandler):
		# Make sure to announce most recently used emoji first in post-1709 builds.
		# Fake the announcement by locating 'most recently used" category and calling selected event on this.
		# However, in build 17666 and later,
		# child count is the same for both emoji panel and hardware keyboard candidates list.
		# Thankfully first child automation ID's are different for each modern input technology.
		# However this event is raised when the input panel closes.
		inputPanel = obj.firstChild
		if inputPanel is None:
			self._modernKeyboardInterfaceActive = False
			self._recentlySelected = None
			return
		# #9104: different aspects of modern input panel are represented by automation iD's.
		inputPanelAutomationID = inputPanel.UIAAutomationId
		self._modernKeyboardInterfaceActive = True
		self._symbolsGroupSelected = False
		# Emoji panel for build 16299 and 17134.
		# This event is properly raised in build 17134.
		if (
			not winVersion.isWin10(version=1809)
			and inputPanelAutomationID in self._classicEmojiPanelAutomationID
		):
			eventHandler.executeEvent("UIA_elementSelected", obj.lastChild.firstChild)
		# Handle hardware keyboard suggestions.
		# Treat it the same as CJK composition list - don't announce this if candidate announcement setting is off.
		elif (
			inputPanelAutomationID == "CandidateWindowControl"
			and config.conf["inputComposition"]["autoReportAllCandidates"]
		):
			try:
				eventHandler.executeEvent("UIA_elementSelected", inputPanel.firstChild.firstChild)
			except AttributeError:
				# Because this is dictation window.
				pass
		# Emoji panel in Version 1809 (specifically, build 17666) and later.
		elif inputPanelAutomationID == "TEMPLATE_PART_ExpressionGroupedFullView":
			# #10377: on some systems, there is something else besides grouping controls,
			# so another child control must be used.
			emojisList = inputPanel.children[-2]
			if emojisList.UIAAutomationId != "TEMPLATE_PART_Items_GridView":
				emojisList = emojisList.previous
			try:
				eventHandler.executeEvent("UIA_elementSelected", emojisList.firstChild.firstChild)
			except AttributeError:
				# In build 18272's emoji panel, emoji list becomes empty in some situations.
				pass
		# Clipboard history.
		# Move to clipboard list so element selected event can pick it up.
		# #9103: if clipboard is empty, a status message is displayed instead,
		# and luckily it is located where clipboard data items can be found.
		elif inputPanelAutomationID == "TEMPLATE_PART_ClipboardTitleBar":
			# Under some cases, clipboard tip text isn't shown on screen,
			# causing clipboard history title to be announced instead of most recently copied item.
			clipboardHistory = obj.children[-2]
			if clipboardHistory.UIAAutomationId == inputPanelAutomationID:
				clipboardHistory = clipboardHistory.next
			eventHandler.executeEvent("UIA_elementSelected", clipboardHistory)
		nextHandler()

	def event_nameChange(self, obj, nextHandler):
		# On some systems, touch keyboard keys keeps firing name change event.
		# In build 17704, whenever skin tones are selected, name change is fired by emoji entries (GridViewItem).
		if (
			obj.UIAElement.cachedClassName in ("CRootKey", "GridViewItem")
			# Just ignore useless clipboard status.
			# Also top emoji search result must be announced for better user experience.
			or obj.UIAAutomationId in (
				"TEMPLATE_PART_ClipboardItemsList", "TEMPLATE_PART_Search_TextBlock"
			)
			# And no, emoji entries should not be announced here.
			or (self._recentlySelected is not None and self._recentlySelected in obj.name)
		):
			return
		# The word "blank" is kept announced, so suppress this on build 17666 and later.
		if winVersion.isWin10(version=1809):
			# In build 17672 and later, return immediatley
			# when element selected event on clipboard item was fired just prior to this.
			# In some cases, parent will be None, as seen when emoji panel is closed in build 18267.
			try:
				if (
					obj.UIAAutomationId == "TEMPLATE_PART_ClipboardItemIndex"
					or obj.parent.UIAAutomationId == "TEMPLATE_PART_ClipboardItemsList"
				):
					return
			except AttributeError:
				return
			if (
				not self._modernKeyboardInterfaceActive
				or obj.UIAAutomationId != "TEMPLATE_PART_ExpressionGroupedFullView"
			):
				speech.cancelSpeech()
		# Don't forget to add "Microsoft Candidate UI" as something that should be suppressed.
		if obj.UIAAutomationId not in (
			"TEMPLATE_PART_ExpressionFullViewItemsGrid", "TEMPLATE_PART_ClipboardItemIndex", "CandidateWindowControl"
		):
			ui.message(obj.name)
		# Thankfully name change event is the last thing done when selecting items.
		self._symbolsGroupSelected = False
		# In Version 1809, name change event is fired just as emoji panel is being closed (entries are 0).
		if not any(obj.location):
			self._modernKeyboardInterfaceActive = False
			self._recentlySelected = None
			self._searchInProgress = False
		nextHandler()

	def event_stateChange(self, obj, nextHandler):
		# Attempting to retrieve object location fails when emoji panel closes without selecting anything,
		# especially in Version 1903 and later.
		if obj.location is None and winVersion.isWin10(version=1903):
			self._modernKeyboardInterfaceActive = False
			self._recentlySelected = None
		nextHandler()
