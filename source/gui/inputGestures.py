# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import itertools
import re
from typing import Tuple, Union, Dict

import wx
from wx.lib.mixins.treemixin import VirtualTree
import wx.lib.newevent
import gui
from logHandler import log

from typing import List, Optional
import keyboardHandler
from . import guiHelper
try:
	import updateCheck
except RuntimeError:
	updateCheck = None
import inputCore
import keyLabels
from locale import strxfrm
from .settingsDialogs import SettingsDialog


#: Type for structure returned by inputCore
_CommandsModel = Dict[
	str,  # command display name
	inputCore.AllGesturesScriptInfo,
]

#: Type for structure returned by inputCore
_GesturesModel = Dict[
	str,  # category name
	_CommandsModel
]


def _getAllGestureScriptInfo() -> _GesturesModel:
	gestureMappings = inputCore.manager.getAllGestureMappings(
		obj=gui.mainFrame.prevFocus,
		ancestors=gui.mainFrame.prevFocusAncestors
	)
	if inputCore.SCRCAT_KBEMU not in gestureMappings:
		gestureMappings[inputCore.SCRCAT_KBEMU] = {}
	return gestureMappings


def _formatGesture(identifier):
	try:
		source, main = inputCore.getDisplayTextForGestureIdentifier(identifier)
		# Translators: Describes a gesture in the Input Gestures dialog.
		# {main} is replaced with the main part of the gesture; e.g. alt+tab.
		# {source} is replaced with the gesture's source; e.g. laptop keyboard.
		return _("{main} ({source})").format(main=main, source=source)
	except LookupError:
		return identifier


class _GestureVM:
	displayName: str  #: How the gesture should be displayed
	normalizedGestureIdentifier: str  #: As per items in inputCore.AllGesturesScriptInfo.gestures
	canAdd = False  #: adding children is not supported.
	canRemove = True  #: gestures can be removed

	def __init__(self, normalizedGestureIdentifier: str):
		self.normalizedGestureIdentifier = normalizedGestureIdentifier
		self.displayName = _formatGesture(normalizedGestureIdentifier)


class _ScriptVM:
	displayName: str  #: Translated display name for the script
	scriptInfo: inputCore.AllGesturesScriptInfo
	gestures: List[_GestureVM]
	canAdd = True  #: able to add gestures that trigger this script
	canRemove = False  #: Scripts can not be removed
	addedGestures: List[_GestureVM]  #: These will also be in self.gestures
	#: These will not be in self.gestures anymore. Key is the normalized Gesture Identifier.
	removedGestures: Dict[str, _GestureVM]

	def __init__(self, displayName: str, scriptInfo: inputCore.AllGesturesScriptInfo):
		self.displayName = displayName
		self.scriptInfo = scriptInfo
		self.addedGestures = []
		self.removedGestures = {}
		self.gestures = []

		for g in scriptInfo.gestures:
			self.gestures.append(_GestureVM(g))
	# todo: Gestures could be sorted?

	def addGesture(self, normalizedGestureIdentifier: str) -> int:
		gesture = self.removedGestures.pop(normalizedGestureIdentifier, None)
		if not gesture:
			gesture = _GestureVM(normalizedGestureIdentifier)
			for g in self.addedGestures:
				if g.normalizedGestureIdentifier == gesture.normalizedGestureIdentifier:
					raise ValueError("Gesture already added!")
			self.addedGestures.append(gesture)
		self.gestures.append(gesture)
		return self.gestures.index(gesture)

	def removeGesture(self, gestureVM: _GestureVM):
		if gestureVM in self.addedGestures:
			self.addedGestures.remove(gestureVM)
		else:
			self.removedGestures[gestureVM.normalizedGestureIdentifier] = gestureVM
		self.gestures.remove(gestureVM)


class _CategoryVM:
	displayName: str  #: Translated display name for the category
	scripts: List[_ScriptVM]
	canAdd = False  #: not able to add Scripts
	canRemove = False  #: categories can not be removed

	def __init__(self, displayName: str, scripts: _CommandsModel):
		self.displayName = displayName
		self.scripts = []
		for scriptName in sorted(scripts, key=strxfrm):
			scriptInfo = scripts[scriptName]
			self.scripts.append(_ScriptVM(
				displayName=scriptName,
				scriptInfo=scriptInfo
			))


class _EmulatedGestureVM(_ScriptVM):
	displayName: str  #: Display name for the gesture to be emulated
	canAdd = True  #: able to add gestures that trigger this emulation
	scriptInfo: Union[inputCore.AllGesturesScriptInfo, inputCore.KbEmuScriptInfo]

	def __init__(self, displayName: str, emuGestureInfo: inputCore.AllGesturesScriptInfo):
		super(_EmulatedGestureVM, self).__init__(displayName=displayName, scriptInfo=emuGestureInfo)

	@property
	def canRemove(self) -> bool:
		return not bool(self.gestures) and isinstance(self.scriptInfo, inputCore.KbEmuScriptInfo)


class _EmuCategoryVM:
	displayName = inputCore.SCRCAT_KBEMU  #: Translated display name for the gesture emulation category
	scripts: List[_EmulatedGestureVM]
	canAdd = True  #: Can add new emulated gestures
	canRemove = False  #: categories can not be removed
	addedKbEmulation: List[_EmulatedGestureVM]  #: These will also be in self.scripts
	#: These will not be in self.scripts anymore. Key is the display name.
	removedKbEmulation: Dict[str, _EmulatedGestureVM]

	def __init__(self, displayName: str, emuGestures: _CommandsModel):
		assert self.displayName == displayName

		self.addedKbEmulation = []
		self.removedKbEmulation = {}
		self.scripts = []
		for scriptName in sorted(emuGestures, key=strxfrm):
			emuG = emuGestures[scriptName]
			self.scripts.append(_EmulatedGestureVM(
				displayName=scriptName,
				emuGestureInfo=emuG
			))

	def addEmulation(self, gestureDisplayName, scriptInfo: inputCore.AllGesturesScriptInfo) -> int:
		emuGesture = self.removedKbEmulation.pop(gestureDisplayName, None)
		if not emuGesture:
			emuGesture = _EmulatedGestureVM(gestureDisplayName, scriptInfo)
			for a in self.addedKbEmulation:
				if a.displayName == emuGesture.displayName:
					raise ValueError("Already added this emulated gesture!")
			self.addedKbEmulation.append(emuGesture)
		self.scripts.append(emuGesture)
		return self.scripts.index(emuGesture)

	def removeEmulation(self, gestureEmulation: _EmulatedGestureVM):
		if gestureEmulation in self.addedKbEmulation:
			self.addedKbEmulation.remove(gestureEmulation)
		else:
			self.removedKbEmulation[gestureEmulation.displayName] = gestureEmulation
		self.scripts.remove(gestureEmulation)


class _InputGesturesViewModel:
	allGestures: List[Union[_CategoryVM, _EmuCategoryVM]]
	filteredGestures: List[Union[_CategoryVM, _EmuCategoryVM]]
	isExpectingNewEmuGesture: Optional[_EmuCategoryVM] = None
	isExpectingNewGesture: Optional[_ScriptVM] = None

	def __init__(self):
		self.reset()

	def reset(self):
		self.allGestures = self.filteredGestures = []
		self._fillAllGestures()

	def getFilteredScriptCount(self):
		scriptCount = 0
		for cat in self.filteredGestures:
			scriptCount += len(cat.scripts)
		return scriptCount

	def _fillAllGestures(self):
		gestureMappings = _getAllGestureScriptInfo()

		# load data into our view model
		for catName in sorted(gestureMappings, key=strxfrm):
			commands = gestureMappings[catName]
			if catName == inputCore.SCRCAT_KBEMU:
				self.allGestures.append(_EmuCategoryVM(
					displayName=catName,
					emuGestures=commands
				))
			else:
				self.allGestures.append(_CategoryVM(
					displayName=catName,
					scripts=commands
				))

	def commitChanges(self):
		gesturesToRemove = [
			(gestureVM, scriptVM.scriptInfo)
			for catVM in self.allGestures
			for scriptVM in catVM.scripts
			for gestureVM in scriptVM.removedGestures.values()
		]

		gesturesForRemovedKbEmu = list([
			(gestureVM, scriptVM.scriptInfo)
			for catVM in self.allGestures if isinstance(catVM, _EmuCategoryVM)
			for scriptVM in catVM.removedKbEmulation.values()
			for gestureVM in scriptVM.removedGestures.values()
		])
		didRemove = False
		for gestureVM, scriptInfo in itertools.chain(gesturesToRemove, gesturesForRemovedKbEmu):
			log.debug(
				f"removing gesture: {gestureVM.normalizedGestureIdentifier} for script: {scriptInfo.scriptName}"
			)
			try:
				inputCore.manager.userGestureMap.remove(
					gestureVM.normalizedGestureIdentifier,
					scriptInfo.moduleName,
					scriptInfo.className,
					scriptInfo.scriptName
				)
			except ValueError:
				# The user wants to unbind a gesture they didn't define.
				inputCore.manager.userGestureMap.add(
					gestureVM.normalizedGestureIdentifier,
					scriptInfo.moduleName,
					scriptInfo.className,
					None  # replace script with None
				)
			didRemove = True

		gesturesToAdd = [
			(gestureVM, scriptVM.scriptInfo)
			for catVm in self.allGestures
			for scriptVM in catVm.scripts
			for gestureVM in scriptVM.addedGestures
		]
		didAdd = False
		for gestureVM, scriptInfo in gesturesToAdd:
			try:
				# The user might have unbound this gesture,
				# so remove this override first.
				inputCore.manager.userGestureMap.remove(
					gestureVM.normalizedGestureIdentifier,
					scriptInfo.moduleName,
					scriptInfo.className,
					None  # replace script with None
				)
			except ValueError:
				pass
			inputCore.manager.userGestureMap.add(
				gestureVM.normalizedGestureIdentifier,
				scriptInfo.moduleName,
				scriptInfo.className,
				scriptInfo.scriptName
			)
			didAdd = True

		if didRemove or didAdd:
			# Only save if there is something to save.
			try:
				inputCore.manager.userGestureMap.save()
			except Exception:
				log.debugWarning("", exc_info=True)
				return False
		return True

	def filter(self, filterText: str):
		if not filterText:
			self.filteredGestures = self.allGestures
			return
		filteredGestures = []
		# This regexp uses a positive lookahead (?=...) for every word in the filter, which just makes sure
		# the word is present in the string to be tested without matching position or order.
		# #5060: Escape the filter text to prevent unexpected matches and regexp errors.
		# Because we're escaping, words must then be split on r"\ ".
		filterText = re.escape(filterText)
		pattern = re.compile(
			r"(?=.*?" + r")(?=.*?".join(filterText.split(r"\ ")) + r")",
			re.U | re.IGNORECASE
		)
		for catVM in self.allGestures:
			filteredScripts = [
				scriptVM
				for scriptVM in catVM.scripts
				if pattern.match(scriptVM.displayName)
			]
			if filteredScripts:
				# clone the catVM, but start empty.
				filteredCat: Union[_CategoryVM, _EmuCategoryVM] = type(catVM)(catVM.displayName, {})
				filteredCat.scripts = filteredScripts
				filteredGestures.append(filteredCat)
		self.filteredGestures = filteredGestures


class _GesturesTree(VirtualTree, wx.TreeCtrl):

	def __init__(self, parent, gesturesVM: _InputGesturesViewModel):
		self.gesturesVM = gesturesVM
		super().__init__(
			parent,
			size=wx.Size(600, 400),
			style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT | wx.TR_LINES_AT_ROOT | wx.TR_SINGLE
		)

	def OnGetChildrenCount(self, index: Tuple[int, ...]) -> int:
		vmfilteredGestures = self.gesturesVM.filteredGestures
		if not index:  # Root node
			return len(vmfilteredGestures)
		catIndex = index[0]
		categoryVM = vmfilteredGestures[catIndex]
		isAddingEmuGestureToThisCategory = categoryVM == self.gesturesVM.isExpectingNewEmuGesture
		if len(index) == 1:  # Get number of children of Category, IE the number of scripts
			scriptCount = len(categoryVM.scripts)
			if isAddingEmuGestureToThisCategory:
				return 1 + scriptCount
			return scriptCount
		scriptsVM = categoryVM.scripts
		if len(index) == 2:  # Get number of children of scripts , IE the number of gestures
			scriptIndex = index[1]
			isIndexInRange = scriptIndex < len(scriptsVM)
			if isIndexInRange:
				scriptVM = scriptsVM[scriptIndex]
				count = len(scriptVM.gestures)
				if self.gesturesVM.isExpectingNewGesture == scriptVM:
					count += 1
				return count

			elif isAddingEmuGestureToThisCategory:
				# the emulated gesture is still being added, it can not have any gestures yet.
				# after it is added, gestures can be assigned.
				return 0
			else:
				log.error(f"unknown situation: {index!r}")
				return 0

		assert len(index) == 3  # Get number of children for gesture, always 0
		return 0  # Gestures have no children

	def OnGetItemText(self, index: Tuple[int, ...], column: int = 0) -> str:
		vmfilteredGestures = self.gesturesVM.filteredGestures

		assert len(index) >= 1
		catIndex = index[0]
		catVM = vmfilteredGestures[catIndex]
		if len(index) == 1:  # Get the display name of a category
			if vmfilteredGestures is self.gesturesVM.allGestures:  # same object, no filtering applied
				return catVM.displayName
			nbResults = len(catVM.scripts)
			if nbResults == 1:
				# Translators: The label for a filtered category in the Input Gestures dialog.
				return _("{category} (1 result)").format(
					category=catVM.displayName
				)
			# Translators: The label for a filtered category in the Input Gestures dialog.
			return _("{category} ({nbResults} results)").format(
				category=catVM.displayName, nbResults=nbResults
			)

		assert len(index) >= 2
		if index[1] >= len(catVM.scripts):
			# Translators: The prompt to enter an emulated gesture in the Input Gestures dialog.
			return _("Enter gesture to emulate:")
		scriptIndex = index[1]
		scriptVm = catVM.scripts[scriptIndex]
		if len(index) == 2:  # Get the display name of a script / emulated gesture
			return scriptVm.displayName

		assert len(index) == 3  # Get the display name of a gesture
		if index[2] >= len(scriptVm.gestures):
			# Translators: The prompt to enter a gesture in the Input Gestures dialog.
			return _("Enter input gesture:")
		gestureIndex = index[2]
		gesture = scriptVm.gestures[gestureIndex]
		return gesture.displayName

	def getData(
		self,
		index: Tuple[int, ...]
	) -> Optional[Union[_GestureVM, _CategoryVM, _EmuCategoryVM, _ScriptVM, _EmulatedGestureVM]]:
		assert 1 <= len(index) <= 3
		catVM = self.gesturesVM.filteredGestures[index[0]]
		if 1 == len(index):
			return catVM
		commandIndex = index[1]
		lastScriptIndex = len(catVM.scripts) - 1
		if commandIndex > lastScriptIndex:
			if commandIndex != 1 + lastScriptIndex:
				log.error(
					"Exceeded expected command bounds, there should only ever be a single pending addition.",
					stack_info=True,
				)
			return None  # Getting data for a command currently being added.
		commandVM = catVM.scripts[commandIndex]
		if 2 == len(index):
			return commandVM
		gestureIndex = index[2]
		lastGestureIndex = len(commandVM.gestures) - 1
		if gestureIndex > lastGestureIndex:
			if gestureIndex != 1 + lastGestureIndex:
				log.error(
					"Exceeded expected gesture bounds, there should only ever be a single pending addition."
					f"Trying to get index {gestureIndex}, current last script index is {lastGestureIndex}",
					stack_info=True,
				)
			return None  # Getting data for a gesture currently being added.
		gestureVM = commandVM.gestures[gestureIndex]
		return gestureVM

	def doRefresh(self, postFilter=False, focus: Optional[Tuple[int, ...]] = None):
		with guiHelper.autoThaw(self):
			self.RefreshItems()
			if postFilter:
				self.CollapseAll()
				if 10 >= self.gesturesVM.getFilteredScriptCount():
					catIndexes = range(len(self.gesturesVM.filteredGestures))
					for index in catIndexes:
						# Expand categories
						self.Expand(self.GetItemByIndex((index,)))
			if focus:
				log.debug(f"focusing: {focus}")
				assert 1 <= len(focus) <= 3
				for i in range(1, len(focus)):
					focusItem = self.GetItemByIndex(focus[:i])
					self.Expand(focusItem)
		if focus:
			# selecting the item must be done after the freeze has completed (thawed) other wise WX calculates
			# the wrong scrolling position and puts the item outside of the virtual window.
			focusItem = self.GetItemByIndex(focus)
			log.debug(f"selecting: {focusItem} at {focus}")
			self.SelectItem(focusItem)
		if not postFilter:
			self.SetFocus()


class InputGesturesDialog(SettingsDialog):
	# Translators: The title of the Input Gestures dialog where the user can remap input gestures for commands.
	title = _("Input Gestures")

	def __init__(self, parent: "InputGesturesDialog"):
		#: The index in the _GesturesTree of the prompt for entering a new gesture
		super().__init__(parent, resizeable=True)

	def makeSettings(self, settingsSizer):
		filterSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a text field to search for gestures in the Input Gestures dialog.
		filterLabel = wx.StaticText(self, label=pgettext("inputGestures", "&Filter by:"))
		self.filterCtrl = filterCtrl = wx.TextCtrl(self)
		filterSizer.Add(filterLabel, flag=wx.ALIGN_CENTER_VERTICAL)
		filterSizer.AddSpacer(guiHelper.SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL)
		filterSizer.Add(filterCtrl, proportion=1)
		settingsSizer.Add(filterSizer, flag=wx.EXPAND)
		settingsSizer.AddSpacer(5)
		filterCtrl.Bind(wx.EVT_TEXT, self.onFilterChange, filterCtrl)

		self.gesturesVM = _InputGesturesViewModel()
		tree = self.tree = _GesturesTree(self, self.gesturesVM)
		tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.onTreeSelect)
		settingsSizer.Add(tree, proportion=1, flag=wx.EXPAND)

		settingsSizer.AddSpacer(guiHelper.SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL)

		bHelper = guiHelper.ButtonHelper(wx.HORIZONTAL)

		# Translators: The label of a button to add a gesture in the Input Gestures dialog.
		self.addButton = bHelper.addButton(self, label=_("&Add"))
		self.addButton.Bind(wx.EVT_BUTTON, self.onAdd)
		self.addButton.Disable()

		# Translators: The label of a button to remove a gesture in the Input Gestures dialog.
		self.removeButton = bHelper.addButton(self, label=_("&Remove"))
		self.removeButton.Bind(wx.EVT_BUTTON, self.onRemove)
		self.removeButton.Disable()

		bHelper.sizer.AddStretchSpacer()
		# Translators: The label of a button to reset all gestures in the Input Gestures dialog.
		resetButton = wx.Button(self, label=_("Reset to factory &defaults"))
		bHelper.sizer.Add(resetButton, flag=wx.ALIGN_RIGHT)
		resetButton.Bind(wx.EVT_BUTTON, self.onReset)

		settingsSizer.Add(bHelper.sizer, flag=wx.EXPAND)

	def postInit(self):
		self.tree.RefreshItems()
		self.tree.SetFocus()

	def _onWindowDestroy(self, evt):
		super()._onWindowDestroy(evt)

	def onFilterChange(self, evt):
		filterText = evt.GetEventObject().GetValue()
		self.filter(filterText)

	def filter(self, filter: str):
		try:
			self.gesturesVM.filter(filter)
		except Exception:
			log.exception()
			return
		self.tree.doRefresh(postFilter=True)

	def onTreeSelect(self, evt):
		if evt:
			evt.Skip()
		# #7077: Check if the treeview is still alive.
		try:
			index = self.tree.GetIndexOfItem(self.tree.Selection)
		except RuntimeError:
			log.exception()
			return
		item = self.tree.getData(index)
		pendingAdd = self.gesturesVM.isExpectingNewEmuGesture or self.gesturesVM.isExpectingNewGesture
		self.addButton.Enabled = bool(item and item.canAdd and not pendingAdd)
		self.removeButton.Enabled = bool(item and item.canRemove and not pendingAdd)

	def onAdd(self, evt):
		if inputCore.manager._captureFunc:
			# don't add while already in process of adding.
			return

		selIdx = self.tree.GetIndexOfItem(self.tree.Selection)
		if not self.tree.IsExpanded(self.tree.Selection):
			self.tree.Expand(self.tree.Selection)
		log.info(f"selection: {self.tree.getData(selIdx).displayName} index: {selIdx}")

		item = self.tree.getData(selIdx)
		if isinstance(item, _EmuCategoryVM):
			self.tree.gesturesVM.isExpectingNewEmuGesture = item
			newItemIdx = (
				*selIdx,
				len(self.tree.gesturesVM.isExpectingNewEmuGesture.scripts)
			)
			self.tree.doRefresh(focus=newItemIdx)
			self.onTreeSelect(None)

			def addKbEmuGestureCaptor(gesture):
				if not isinstance(gesture, keyboardHandler.KeyboardInputGesture) or gesture.isModifier:
					return False
				inputCore.manager._captureFunc = None
				wx.CallAfter(self._addCapturedKbEmu, gesture, selIdx)
				return False

			inputCore.manager._captureFunc = addKbEmuGestureCaptor
		elif isinstance(item, _ScriptVM):
			self.tree.gesturesVM.isExpectingNewGesture = item
			newItemIdx = (
				*selIdx,
				len(self.tree.gesturesVM.isExpectingNewGesture.gestures)
			)
			self.tree.doRefresh(focus=newItemIdx)
			self.onTreeSelect(None)

			def addGestureCaptor(gesture):
				if gesture.isModifier:
					return False
				if item.scriptInfo.category == inputCore.SCRCAT_KBEMU:
					gesName = keyLabels.getKeyCombinationLabel(gesture.normalizedIdentifiers[-1][3:])
					if gesName == item.scriptInfo.displayName:
						# Disallow assigning an emulated gesture to itself
						return False
				inputCore.manager._captureFunc = None
				wx.CallAfter(self._addCaptured, item, selIdx, gesture)
				return False

			inputCore.manager._captureFunc = addGestureCaptor
		else:
			log.error(f"unable to add for selected item: {item.displayName}")

	def _addCaptured(self, scriptVM: _ScriptVM, addingToIndex: Tuple[int, int], gesture):
		gids = gesture.normalizedIdentifiers
		if len(gids) > 1:
			# Multiple choices. Present them in a pop-up menu.
			menu = wx.Menu()
			for gid in gids:
				gestureVM = _GestureVM(gid)
				item = menu.Append(wx.ID_ANY, gestureVM.displayName)
				self.Bind(
					wx.EVT_MENU,
					lambda evt, gid=gid: self._addChoice(scriptVM, addingToIndex, gid),
					item
				)
			self.PopupMenu(menu)
			if self.tree.gesturesVM.isExpectingNewGesture:
				# No item was selected, so use the first.
				self._addChoice(scriptVM, addingToIndex, gids[0])
			menu.Destroy()
		else:
			self._addChoice(scriptVM, addingToIndex, gids[0])

	def _addChoice(self, scriptVM: _ScriptVM, addingToIndex: Tuple[int, int], gid: str):
		"""
		:param scriptVM: The script to add the gesture to
		:param gid:  Normalized gesture ID to be added.
		:return:
		"""
		newItemIndex = (
			*addingToIndex,
			scriptVM.addGesture(gid)
		)
		log.info(f"newItemIndex = {newItemIndex}")
		self.tree.gesturesVM.isExpectingNewGesture = None
		self.tree.doRefresh(focus=newItemIndex)
		self.onTreeSelect(None)

	def _addCapturedKbEmu(self, gesture, addingToIndex: Tuple[int]):
		# Use the last normalized identifier, which is the most generic one
		gestureToEmulate = gesture.normalizedIdentifiers[-1]
		from globalCommands import GlobalCommands
		scriptInfo = inputCore._AllGestureMappingsRetriever.makeKbEmuScriptInfo(GlobalCommands, gestureToEmulate)
		# Translators: An gesture that will be emulated by some other new gesture. The token {emulateGesture}
		# will be replaced by the gesture that can be triggered by a mapped gesture.
		# E.G. Emulate key press: NVDA+b
		emuGestureDisplayName = _("Emulate key press: {emulateGesture}").format(
			emulateGesture=scriptInfo.displayName
		)
		catVM = self.tree.gesturesVM.isExpectingNewEmuGesture
		assert isinstance(catVM, _EmuCategoryVM)
		newEmuItemIndex = (
			*addingToIndex,
			catVM.addEmulation(emuGestureDisplayName, scriptInfo)
		)
		self.tree.gesturesVM.isExpectingNewEmuGesture = None
		self.tree.doRefresh(focus=newEmuItemIndex)
		self.onTreeSelect(None)

	def onRemove(self, evt):
		selectionId = self.tree.GetIndexOfItem(self.tree.Selection)
		categoryId = selectionId[:1]
		if len(selectionId) == 3:  # removing a gesture
			gestureVM = self.tree.getData(selectionId)
			scriptVM = self.tree.getData(selectionId[:2])
			scriptVM.removeGesture(gestureVM)
		elif len(selectionId) == 2:  # removing a emulated KB gesture
			emuCatVM = self.tree.getData(categoryId)
			if not isinstance(emuCatVM, _EmuCategoryVM):
				log.error(
					f"Trying to remove command, only emulatedGestures can be removed from level of tree."
					f" Trying to remove: {emuCatVM.displayName}"
				)
				return
			emuGesture = self.tree.getData(selectionId)
			emuCatVM.removeEmulation(emuGesture)
		else:
			log.error(f"Unhandled selectionId: {selectionId}, {self.tree.getData(selectionId).displayName}")
			return
		catItem = self.tree.GetItemByIndex(categoryId)
		self.tree.RefreshChildrenRecursively(catItem)
		self.tree.SetFocus()
		self.onTreeSelect(None)

	def onReset(self, evt):
		if gui.messageBox(
			# Translators: A prompt for confirmation to reset all gestures in the Input Gestures dialog.
			_("""Are you sure you want to reset all gestures to their factory defaults?

			All of your user defined gestures, whether previously set or defined during this session, will be lost.
			This cannot be undone."""),
			# Translators: A prompt for confirmation to reset all gestures in the Input Gestures dialog.
			_("Reset gestures"),
			style=wx.YES | wx.NO | wx.NO_DEFAULT
		) != wx.YES:
			return
		inputCore.manager.userGestureMap.clear()
		try:
			inputCore.manager.userGestureMap.save()
		except Exception:
			log.debugWarning("", exc_info=True)
			# Translators: An error displayed when saving user defined input gestures fails.
			gui.messageBox(
				_("Error saving user defined gestures - probably read only file system."),
				caption=_("Error"),
				style=wx.OK | wx.ICON_ERROR
			)
			self.onCancel(None)
			return
		self.gesturesVM.reset()
		self.tree.doRefresh()
		self.tree.SetFocus()

	def onOk(self, evt):
		self.tree.Unbind(wx.EVT_TREE_SEL_CHANGED)
		self.filterCtrl.Unbind(wx.EVT_TEXT)
		if not self.gesturesVM.commitChanges():
			gui.messageBox(
				# Translators: An error displayed when saving user defined input gestures fails.
				_("Error saving user defined gestures - probably read only file system."),
				# Translators: An title for an error displayed when saving user defined input gestures fails.
				_("Error"),
				wx.OK | wx.ICON_ERROR
			)

		super(InputGesturesDialog, self).onOk(evt)

	def onCancel(self, evt: wx.Event):
		self.tree.Unbind(wx.EVT_TREE_SEL_CHANGED)
		self.filterCtrl.Unbind(wx.EVT_TEXT)
		super(InputGesturesDialog, self).onCancel(evt)
