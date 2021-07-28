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
import inputCore
import keyLabels
from locale import strxfrm
from .settingsDialogs import SettingsDialog


#: Type for structure returned by inputCore
_ScriptsModel = Dict[
	str,  # script display name
	Union[inputCore.AllGesturesScriptInfo, inputCore.KbEmuScriptInfo],
]

#: Type for structure returned by inputCore
_GesturesModel = Dict[
	str,  # category name
	_ScriptsModel
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

	def __repr__(self):
		return f"Gesture: {self.normalizedGestureIdentifier}"


class _PendingGesture:
	# Translators: The prompt to enter a gesture in the Input Gestures dialog.
	displayName = _("Enter input gesture:")
	canAdd = False
	canRemove = False

	def __repr__(self):
		return f"Pending Gesture"


class _ScriptVM:
	displayName: str  #: Translated display name for the script
	scriptInfo: inputCore.AllGesturesScriptInfo
	gestures: List[Union[_GestureVM, _PendingGesture]]
	canAdd = True  #: able to add gestures that trigger this script
	canRemove = False  #: Scripts can not be removed
	addedGestures: List[_GestureVM]  #: These will also be in self.gestures
	#: These will not be in self.gestures anymore. Key is the normalized Gesture Identifier.
	removedGestures: Dict[str, _GestureVM]

	def __init__(self, displayName: str, scriptInfo: inputCore.AllGesturesScriptInfo):
		self.displayName = displayName
		self.scriptInfo = scriptInfo
		self.pending: Optional[_PendingGesture] = None
		self.addedGestures = []
		self.removedGestures = {}
		self.gestures = []

		for g in scriptInfo.gestures:
			self.gestures.append(_GestureVM(g))
	# todo: Gestures could be sorted?

	def __repr__(self):
		return f"Script: {self.scriptInfo.scriptName}"

	def createPendingGesture(self) -> _PendingGesture:
		self.pending = _PendingGesture()
		self.gestures.append(self.pending)
		return self.pending

	def finalisePending(self, normalizedGestureIdentifier: str) -> _GestureVM:
		assert self.pending is not None
		self.gestures.remove(self.pending)
		return self._addGesture(normalizedGestureIdentifier)

	def _addGesture(self, normalizedGestureIdentifier: str) -> _GestureVM:
		gesture = self.removedGestures.pop(normalizedGestureIdentifier, None)
		if not gesture:
			gesture = _GestureVM(normalizedGestureIdentifier)
			for g in self.addedGestures:
				if g.normalizedGestureIdentifier == gesture.normalizedGestureIdentifier:
					raise ValueError("Gesture already added!")
			self.addedGestures.append(gesture)
		self.gestures.append(gesture)
		return gesture

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

	def __init__(self, displayName: str, scripts: _ScriptsModel):
		self.displayName = displayName
		self.scripts = []
		for scriptName in sorted(scripts, key=strxfrm):
			scriptInfo = scripts[scriptName]
			self.scripts.append(_ScriptVM(
				displayName=scriptName,
				scriptInfo=scriptInfo
			))

	def __repr__(self):
		return f"Category: {self.displayName}"


class _EmulatedGestureVM(_ScriptVM):
	displayName: str  #: Display name for the gesture to be emulated
	canAdd = True  #: able to add gestures that trigger this emulation
	scriptInfo: Union[inputCore.AllGesturesScriptInfo, inputCore.KbEmuScriptInfo]

	def __init__(self, emuGestureInfo: inputCore.AllGesturesScriptInfo):
		if not isinstance(emuGestureInfo, inputCore.KbEmuScriptInfo):
			raise ValueError(f"Unexpected script type.")
		# Translators: An gesture that will be emulated by some other new gesture. The token {emulateGesture}
		# will be replaced by the gesture that can be triggered by a mapped gesture.
		# E.G. Emulate key press: NVDA+b
		emuGestureDisplayName = _("Emulate key press: {emulateGesture}").format(
			emulateGesture=emuGestureInfo.displayName
		)
		super(_EmulatedGestureVM, self).__init__(displayName=emuGestureDisplayName, scriptInfo=emuGestureInfo)

	@property
	def canRemove(self) -> bool:
		return not bool(self.gestures)

	def __repr__(self):
		return f"KB emulated gesture: {self.scriptInfo.scriptName}"


class _PendingEmulatedGestureVM:
	# Translators: The prompt to enter an emulated gesture in the Input Gestures dialog.
	displayName = _("Enter gesture to emulate:")
	canAdd = False
	canRemove = False

	def __repr__(self):
		return "PendingEmulatedGesture"


class _EmuCategoryVM:
	displayName = inputCore.SCRCAT_KBEMU  #: Translated display name for the gesture emulation category
	scripts: List[Union[_ScriptVM, _EmulatedGestureVM, _PendingEmulatedGestureVM]]
	canAdd = True  #: Can add new emulated gestures
	canRemove = False  #: categories can not be removed
	addedKbEmulation: List[_EmulatedGestureVM]  #: These will also be in self.scripts
	#: These will not be in self.scripts anymore. Key is the scriptInfo display name.
	removedKbEmulation: Dict[str, _EmulatedGestureVM]

	def __repr__(self):
		return "KB emulation category"

	def __init__(self, displayName: str, emuGestures: _ScriptsModel):
		assert self.displayName == displayName

		self.addedKbEmulation = []
		self.removedKbEmulation = {}
		self.scripts = []
		self.pending: Optional[_PendingEmulatedGestureVM] = None
		for scriptName in sorted(emuGestures, key=strxfrm):
			emuG = emuGestures[scriptName]
			if isinstance(emuG, inputCore.KbEmuScriptInfo):
				self.scripts.append(_EmulatedGestureVM(
					emuGestureInfo=emuG
				))
			elif isinstance(emuG, inputCore.AllGesturesScriptInfo):
				self.scripts.append(_ScriptVM(scriptName, emuG))
			else:
				log.error(f"Unknown script type: {emuG}")

	def createPendingEmuGesture(self) -> _PendingEmulatedGestureVM:
		self.pending = _PendingEmulatedGestureVM()
		self.scripts.append(self.pending)
		return self.pending

	def finalisePending(
			self,
			scriptInfo: inputCore.AllGesturesScriptInfo
	) -> _EmulatedGestureVM:
		assert self.pending is not None
		self.scripts.remove(self.pending)
		return self._addEmulation(scriptInfo)

	def _addEmulation(
			self,
			scriptInfo: inputCore.AllGesturesScriptInfo
	) -> _EmulatedGestureVM:
		emuGesture = self.removedKbEmulation.pop(scriptInfo.displayName, None)
		if not emuGesture:
			emuGesture = _EmulatedGestureVM(scriptInfo)
			for a in self.addedKbEmulation:
				if a.displayName == emuGesture.displayName:
					raise ValueError("Already added this emulated gesture!")
			self.addedKbEmulation.append(emuGesture)
		self.scripts.append(emuGesture)
		return emuGesture

	def removeEmulation(self, gestureEmulation: _EmulatedGestureVM):
		if gestureEmulation in self.addedKbEmulation:
			self.addedKbEmulation.remove(gestureEmulation)
		else:
			self.removedKbEmulation[gestureEmulation.scriptInfo.displayName] = gestureEmulation
		self.scripts.remove(gestureEmulation)


# convenience types.
_CategoryVMTypes = Union[_CategoryVM, _EmuCategoryVM]
_ScriptVMTypes = Union[_ScriptVM, _EmulatedGestureVM, _PendingEmulatedGestureVM]
_GestureVMTypes = Union[_GestureVM, _PendingGesture]

_VmSelection = Tuple[
	_CategoryVMTypes,
	Optional[_ScriptVMTypes],
	Optional[_GestureVMTypes]
]


class _InputGesturesViewModel:
	allGestures: List[_CategoryVMTypes]
	filteredGestures: List[_CategoryVMTypes]
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

	def getIndexInTree(self, vmSelection: _VmSelection):
		catVM, scriptVM, gestureVM = vmSelection
		catIndex = self.filteredGestures.index(catVM)
		if gestureVM is not None:
			return (
				catIndex,
				catVM.scripts.index(scriptVM),
				scriptVM.gestures.index(gestureVM)
			)
		if scriptVM is not None:
			return (
				catIndex,
				catVM.scripts.index(scriptVM),
			)
		return (
			catIndex,
		)

	def _fillAllGestures(self):
		gestureMappings = _getAllGestureScriptInfo()

		# load data into our view model
		for catName in sorted(gestureMappings, key=strxfrm):
			scripts = gestureMappings[catName]
			if catName == inputCore.SCRCAT_KBEMU:
				self.allGestures.append(_EmuCategoryVM(
					displayName=catName,
					emuGestures=scripts
				))
			else:
				self.allGestures.append(_CategoryVM(
					displayName=catName,
					scripts=scripts
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
		filteredGesturesVM = self.gesturesVM.filteredGestures
		if not index or not len(filteredGesturesVM):  # An empty index indicates the root node is requested
			return len(filteredGesturesVM)
		catIndex = index[0]
		categoryVM = filteredGesturesVM[catIndex]
		scriptsVM: List[_ScriptVMTypes] = categoryVM.scripts
		if len(index) == 1:  # Get number of children of Category, IE the number of scripts
			scriptCount = len(scriptsVM)
			return scriptCount
		if len(index) == 2:  # Get number of children of scripts , IE the number of gestures
			scriptIndex = index[1]
			scriptVM: Union[_ScriptVM, _EmulatedGestureVM, _PendingEmulatedGestureVM] = scriptsVM[scriptIndex]
			gestures = [] if isinstance(scriptVM, _PendingEmulatedGestureVM) else scriptVM.gestures
			return len(gestures)

		assert len(index) == 3  # Get number of children for gesture, always 0
		return 0  # Gestures have no children

	def OnGetItemText(self, index: Tuple[int, ...], column: int = 0) -> str:
		filteredGesturesVM = self.gesturesVM.filteredGestures

		assert len(index) >= 1 and len(filteredGesturesVM) >= 1
		catIndex = index[0]
		catVM = filteredGesturesVM[catIndex]
		if len(index) == 1:  # Get the display name of a category
			if filteredGesturesVM is self.gesturesVM.allGestures:  # same object, no filtering applied
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
		scriptIndex = index[1]
		scriptVm = catVM.scripts[scriptIndex]
		if len(index) == 2:  # Get the display name of a script / emulated gesture
			return scriptVm.displayName

		assert len(index) == 3  # Get the display name of a gesture
		gestureIndex = index[2]
		gesture = scriptVm.gestures[gestureIndex]
		return gesture.displayName

	def getSelectedItemData(self) -> Optional[_VmSelection]:
		selection = self.GetSelection()
		try:
			selIdx: Tuple[int, ...] = self.GetIndexOfItem(selection)
		except AssertionError:
			# If item.IsOK() fails on this item or any parents indexed, an assertion error is thrown. (#12673)
			log.debugWarning(
				"",
				exc_info=True,
			)
			return None
		# ensure that the length of tuple is 3, missing elements replaced with None
		nonesForMissingElements = ((None, ) * (3 - len(selIdx)))
		selIdx: Tuple[int, Optional[int], Optional[int]] = selIdx + nonesForMissingElements
		return self.getData(selIdx)

	def getData(
			self,
			index: Tuple[int, Optional[int], Optional[int]]
	) -> Optional[_VmSelection]:
		assert 3 == len(index) and index[0] is not None
		if len(self.gesturesVM.filteredGestures) == 0:
			log.debug("No filtered gestures available.")
			return None
		catIndex, scriptIndex, gestureIndex = index
		log.debug(f"Getting data for item indexes {index}")
		try:
			catVM: _CategoryVMTypes = self.gesturesVM.filteredGestures[catIndex]
		except IndexError:
			log.error(
				f"Exceeded expected categories bounds,"
				f" trying to access category with index {catIndex},"
				f" but only {len(self.gesturesVM.filteredGestures)} exist.",
				stack_info=True,
			)
			raise
		if scriptIndex is None:
			return (catVM, None, None)
		try:
			scriptVM: Optional[_ScriptVMTypes] = catVM.scripts[scriptIndex]
		except IndexError:
			log.error(
				"Exceeded expected script bounds, use _PendingEmulatedGestureVM as a placeholder."
				f" Trying to get index {scriptIndex}, number of gestures for script: {len(catVM.scripts)}",
				stack_info=True,
			)
			raise
		if gestureIndex is None:
			return (catVM, scriptVM, None)
		try:
			gestureVM: _GestureVMTypes = scriptVM.gestures[gestureIndex]
		except IndexError:
			log.error(
				"Exceeded expected gesture bounds, use _PendingGestureVM as a placeholder."
				f" Trying to get index {gestureIndex}, number of gestures for script: {len(scriptVM.gestures)}",
				stack_info=True,
			)
			raise
		except AttributeError:
			if not isinstance(scriptVM, _PendingEmulatedGestureVM):
				log.error(
					"Pending emulated gestures can not have gestures yet. This indicates a logic error."
					f" Trying to get index {gestureIndex} of pending emulation."
				)
			raise
		return (catVM, scriptVM, gestureVM)

	def doRefresh(self, postFilter=False, focus: Optional[_VmSelection] = None):
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
				log.debug(f"expanding: {focus}")
				catVM, scriptVM, gestureVM = focus
				catIndex = self.gesturesVM.filteredGestures.index(catVM)
				self.Expand(self.GetItemByIndex((catIndex, )))
				if scriptVM is not None:
					scriptIndex = catVM.scripts.index(scriptVM)
					self.Expand(self.GetItemByIndex((catIndex, scriptIndex, )))
		if focus:
			# selecting the item must be done after the freeze has completed (thawed) other wise WX calculates
			# the wrong scrolling position and puts the item outside of the virtual window.
			focusIndex = self.gesturesVM.getIndexInTree(focus)
			focusItem = self.GetItemByIndex(focusIndex)
			log.debug(f"selecting: {focus} at {focusIndex}")
			self.SelectItem(focusItem)
		if not postFilter:
			self.SetFocus()


class InputGesturesDialog(SettingsDialog):
	# Translators: The title of the Input Gestures dialog where the user can remap input gestures for scripts.
	title = _("Input Gestures")
	helpId = "InputGestures"

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
		bHelper.sizer.Add(resetButton)
		resetButton.Bind(wx.EVT_BUTTON, self.onReset)

		settingsSizer.Add(bHelper.sizer, flag=wx.EXPAND)
		self.tree.Bind(wx.EVT_WINDOW_DESTROY, self._onDestroyTree)

	def postInit(self):
		self.tree.RefreshItems()
		self.tree.SetFocus()

	def _onWindowDestroy(self, evt):
		super()._onWindowDestroy(evt)

	def onFilterChange(self, evt):
		filterText = evt.GetEventObject().GetValue()
		self.filter(filterText)

	def filter(self, filterText: str):
		try:
			self.gesturesVM.filter(filterText)
		except Exception:
			log.exception()
			return
		self.tree.doRefresh(postFilter=True)

	def onTreeSelect(self, evt):
		if evt:
			evt.Skip()
		self._refreshButtonState()

	def _refreshButtonState(self):
		selectedItems = self.tree.getSelectedItemData()
		if selectedItems is None:
			item = None
		else:
			# get the leaf of the selection
			item = next((item for item in reversed(selectedItems) if item is not None), None)
		pendingAdd = self.gesturesVM.isExpectingNewEmuGesture or self.gesturesVM.isExpectingNewGesture
		self.addButton.Enabled = bool(item and item.canAdd and not pendingAdd)
		self.removeButton.Enabled = bool(item and item.canRemove and not pendingAdd)

	def onAdd(self, evt):
		if inputCore.manager._captureFunc:
			# don't add while already in process of adding.
			return

		selectedItems = self.tree.getSelectedItemData()
		assert selectedItems is not None
		catVM, scriptVM, gestureVM = selectedItems
		log.debug(f"selection: {catVM}, {scriptVM}, {gestureVM}")

		if scriptVM is None and isinstance(catVM, _EmuCategoryVM):
			self.gesturesVM.isExpectingNewEmuGesture = catVM
			pending = catVM.createPendingEmuGesture()
			self.tree.doRefresh(focus=(catVM, pending, None))
			self._refreshButtonState()

			def addKbEmuGestureCaptor(gesture: inputCore.InputGesture):
				if not isinstance(gesture, keyboardHandler.KeyboardInputGesture) or gesture.isModifier:
					return False
				inputCore.manager._captureFunc = None
				wx.CallAfter(self._addCapturedKbEmu, gesture, catVM)
				return False

			inputCore.manager._captureFunc = addKbEmuGestureCaptor
		elif gestureVM is None and isinstance(scriptVM, _ScriptVM):
			self.gesturesVM.isExpectingNewGesture = scriptVM
			pendingGesture = scriptVM.createPendingGesture()
			self.tree.doRefresh(focus=(catVM, scriptVM, pendingGesture))
			self._refreshButtonState()

			def addGestureCaptor(gesture: inputCore.InputGesture):
				if gesture.isModifier:
					return False
				if isinstance(catVM, _EmuCategoryVM):
					gesName = keyLabels.getKeyCombinationLabel(gesture.normalizedIdentifiers[-1][3:])
					if gesName == scriptVM.scriptInfo.displayName:
						# Disallow assigning an emulated gesture to itself
						return False
				inputCore.manager._captureFunc = None
				wx.CallAfter(self._addCaptured, catVM, scriptVM, gesture)
				return False

			inputCore.manager._captureFunc = addGestureCaptor
		else:
			log.error(f"unable to do 'add' action for selected item")

	def _addCaptured(self, catVM: _CategoryVMTypes, scriptVM: _ScriptVMTypes, gesture):
		gids = gesture.normalizedIdentifiers
		if len(gids) > 1:
			# Multiple choices. Present them in a pop-up menu.
			menu = wx.Menu()
			for gid in gids:
				gestureVM = _GestureVM(gid)
				item = menu.Append(wx.ID_ANY, gestureVM.displayName)
				self.Bind(
					wx.EVT_MENU,
					lambda evt, gid=gid: self._addChoice(catVM, scriptVM, gid),
					item
				)
			self.PopupMenu(menu)
			if self.gesturesVM.isExpectingNewGesture:
				# No item was selected, so use the first.
				self._addChoice(catVM, scriptVM, gids[0])
			menu.Destroy()
		else:
			self._addChoice(catVM, scriptVM, gids[0])

	def _addChoice(self, catVM: _CategoryVMTypes, scriptVM: _ScriptVMTypes, gid: str):
		"""
		:param scriptVM: The script to add the gesture to
		:param gid:  Normalized gesture ID to be added.
		:return:
		"""
		newItem = scriptVM.finalisePending(gid)
		log.debug(f"New: {catVM}, {scriptVM}, {newItem}")
		self.gesturesVM.isExpectingNewGesture = None
		self.tree.doRefresh(focus=(catVM, scriptVM, newItem))
		self._refreshButtonState()

	def _addCapturedKbEmu(self, gesture: inputCore.InputGesture, catVM: _EmulatedGestureVM):
		assert isinstance(catVM, _EmuCategoryVM)
		# Use the last identifier, which is the most generic one
		gestureToEmulate = gesture.identifiers[-1]
		from globalCommands import GlobalCommands
		scriptInfo = inputCore._AllGestureMappingsRetriever.makeKbEmuScriptInfo(
			GlobalCommands,
			kbGestureIdentifier=gestureToEmulate
		)

		catVM = self.gesturesVM.isExpectingNewEmuGesture
		newScript = catVM.finalisePending(scriptInfo)
		self.gesturesVM.isExpectingNewEmuGesture = None
		self.tree.doRefresh(focus=(catVM, newScript, None,))
		self._refreshButtonState()

	def onRemove(self, evt):
		selectedItems = self.tree.getSelectedItemData()
		assert selectedItems is not None
		catVM, scriptVM, gestureVM = selectedItems
		if gestureVM is not None:  # removing a gesture
			scriptVM.removeGesture(gestureVM)
		elif isinstance(scriptVM, _EmulatedGestureVM):  # removing a emulated KB gesture
			if not isinstance(catVM, _EmuCategoryVM):
				log.error(
					f"Trying to remove script, only emulatedGestures can be removed from level of tree."
					f" Trying to remove: {catVM.displayName}"
				)
				return
			catVM.removeEmulation(scriptVM)
		else:
			log.error(f"Unhandled selectionId: {catVM}, {scriptVM}")
			return
		self.tree.doRefresh()
		self._refreshButtonState()

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

	def onOk(self, evt):
		if not self.gesturesVM.commitChanges():
			gui.messageBox(
				# Translators: An error displayed when saving user defined input gestures fails.
				_("Error saving user defined gestures - probably read only file system."),
				# Translators: An title for an error displayed when saving user defined input gestures fails.
				_("Error"),
				wx.OK | wx.ICON_ERROR
			)

		super(InputGesturesDialog, self).onOk(evt)

	def _onDestroyTree(self, evt: wx.WindowDestroyEvent):
		# #7077: Remove the binding when the tree is destroyed so that it can not be called during destruction
		# of the dialog.
		self.tree.Unbind(wx.EVT_TREE_SEL_CHANGED)
