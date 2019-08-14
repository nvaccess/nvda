# App module for Composable Shell (CShell) input panel
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017-2018 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Windows 10 Modern Keyboard aka new touch keyboard panel.
The chief feature is allowing NVDA to announce selected emoji when using the keyboard to search for and select one.
Other features include announcing candidates for misspellings if suggestions for hardware keyboard is selected, and managing cloud clipboard paste.
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
		# Sometimes, due to bad tree traversal or wrong item getting selected, something other than the selected item sees this event.
		# Sometimes clipboard candidates list gets selected, so ask NvDA to descend one more level.
		if obj.UIAElement.cachedAutomationID == "TEMPLATE_PART_ClipboardItemsList":
			obj = obj.firstChild
		# In build 18262, emoji panel may open to People group and skin tone modifier or the list housing them gets selected.
		elif obj.UIAElement.cachedAutomationID == "SkinTonePanelModifier_ListView":
			obj = obj.next
		elif obj.parent.UIAElement.cachedAutomationID == "SkinTonePanelModifier_ListView":
			# But this will point to nothing if emoji search results are not people.
			if obj.parent.next is not None: obj = obj.parent.next
			else: obj = obj.parent.parent.firstChild
		candidate = obj
		if obj and obj.UIAElement.cachedClassName == "ListViewItem" and obj.parent and isinstance(obj.parent, UIA) and obj.parent.UIAElement.cachedAutomationID != "TEMPLATE_PART_ClipboardItemsList":
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
		# Thankfully first child automation ID's are different for each modern input technology.
		# However this event is raised when the input panel closes.
		if obj.firstChild is None:
			return
		# #9104: different aspects of modern input panel are represented by automation iD's.
		childAutomationID = obj.firstChild.UIAElement.cachedAutomationID
		# Emoji panel for build 16299 and 17134.
		# This event is properly raised in build 17134.
		if winVersion.winVersion.build <= 17134 and childAutomationID in ("TEMPLATE_PART_ExpressiveInputFullViewFuntionBarItemControl", "TEMPLATE_PART_ExpressiveInputFullViewFuntionBarCloseButton"):
			self.event_UIA_elementSelected(obj.lastChild.firstChild, nextHandler)
		# Handle hardware keyboard suggestions.
		# Treat it the same as CJK composition list - don't announce this if candidate announcement setting is off.
		elif childAutomationID == "CandidateWindowControl" and config.conf["inputComposition"]["autoReportAllCandidates"]:
			try:
				self.event_UIA_elementSelected(obj.firstChild.firstChild.firstChild, nextHandler)
			except AttributeError:
				# Because this is dictation window.
				pass
		# Emoji panel in build 17666 and later (unless this changes).
		elif childAutomationID == "TEMPLATE_PART_ExpressionGroupedFullView":
			self._emojiPanelJustOpened = True
			try:
				self.event_UIA_elementSelected(obj.firstChild.children[-2].firstChild.firstChild, nextHandler)
			except AttributeError:
				# In build 18272's emoji panel, emoji list becomes empty in some situations.
				pass
		# Clipboard history.
		# Move to clipboard list so element selected event can pick it up.
		# #9103: if clipboard is empty, a status message is displayed instead, and luckily it is located where clipboard data items can be found.
		elif childAutomationID == "TEMPLATE_PART_ClipboardTitleBar":
			self.event_UIA_elementSelected(obj.children[-2], nextHandler)
		nextHandler()

	# Argh, name change event is fired right after emoji panel opens in build 17666 and later.
	_emojiPanelJustOpened = False

	def event_nameChange(self, obj, nextHandler):
		# On some systems, touch keyboard keys keeps firing name change event.
		# In build 17704, whenever skin tones are selected, name change is fired by emoji entries (GridViewItem).
		if ((obj.UIAElement.cachedClassName in ("CRootKey", "GridViewItem"))
		# Just ignore useless clipboard status.
		# Also top emoji search result must be announced for better user experience.
		or (obj.UIAElement.cachedAutomationID in ("TEMPLATE_PART_ClipboardItemsList", "TEMPLATE_PART_Search_TextBlock"))
		# And no, emoji entries should not be announced here.
		or (self._recentlySelected is not None and self._recentlySelected in obj.name)):
			return
		# The word "blank" is kept announced, so suppress this on build 17666 and later.
		if winVersion.winVersion.build > 17134:
			# In build 17672 and later, return immediatley when element selected event on clipboard item was fired just prior to this.
			# In some cases, parent will be None, as seen when emoji panel is closed in build 18267.
			try:
				if obj.UIAElement.cachedAutomationID == "TEMPLATE_PART_ClipboardItemIndex" or obj.parent.UIAElement.cachedAutomationID == "TEMPLATE_PART_ClipboardItemsList": return
			except AttributeError:
				return
			if not self._emojiPanelJustOpened or obj.UIAElement.cachedAutomationID != "TEMPLATE_PART_ExpressionGroupedFullView": speech.cancelSpeech()
			self._emojiPanelJustOpened = False
		# Don't forget to add "Microsoft Candidate UI" as something that should be suppressed.
		if obj.UIAElement.cachedAutomationID not in ("TEMPLATE_PART_ExpressionFullViewItemsGrid", "TEMPLATE_PART_ClipboardItemIndex", "CandidateWindowControl"):
			ui.message(obj.name)
		nextHandler()
