# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2022 NV Access Limited, Peter Vágner, Mesar Hameed, Joseph Lee,
# Aaron Cannon, Ethan Holliger, Julien Cochuyt, Thomas Stivers, Cyrille Bougot, Aleksey Sadovoy
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from abc import abstractmethod
import wx

import globalVars
import gui
import gui.contextHelp
from logHandler import log
import speechDictHandler

from . import guiHelper
from .settingsDialogs import SettingsDialog


class DictionaryEntryDialog(
		gui.contextHelp.ContextHelpMixin,
		wx.Dialog,  # wxPython does not seem to call base class initializer, put last in MRO
):
	helpId = "SpeechDictionaries"
	
	TYPE_LABELS = {
		# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
		speechDictHandler.ENTRY_TYPE_ANYWHERE: _("&Anywhere"),
		# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
		speechDictHandler.ENTRY_TYPE_WORD: _("Whole &word"),
		# Translators: This is a label for an Entry Type radio button in add dictionary entry dialog.
		speechDictHandler.ENTRY_TYPE_REGEXP: _("Regular &expression")
	}
	TYPE_LABELS_ORDERING = (
		speechDictHandler.ENTRY_TYPE_ANYWHERE,
		speechDictHandler.ENTRY_TYPE_WORD,
		speechDictHandler.ENTRY_TYPE_REGEXP
	)

	# Translators: This is the label for the edit dictionary entry dialog.
	def __init__(self, parent, title=_("Edit Dictionary Entry")):
		super(DictionaryEntryDialog, self).__init__(parent, title=title)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		# Translators: This is a label for an edit field in add dictionary entry dialog.
		patternLabelText = _("&Pattern")
		self.patternTextCtrl = sHelper.addLabeledControl(patternLabelText, wx.TextCtrl)

		# Translators: This is a label for an edit field in add dictionary entry dialog
		# and in punctuation/symbol pronunciation dialog.
		replacementLabelText = _("&Replacement")
		self.replacementTextCtrl = sHelper.addLabeledControl(replacementLabelText, wx.TextCtrl)

		# Translators: This is a label for an edit field in add dictionary entry dialog.
		commentLabelText = _("&Comment")
		self.commentTextCtrl = sHelper.addLabeledControl(commentLabelText, wx.TextCtrl)

		# Translators: This is a label for a checkbox in add dictionary entry dialog.
		caseSensitiveText = _("Case &sensitive")
		self.caseSensitiveCheckBox = sHelper.addItem(wx.CheckBox(self, label=caseSensitiveText))

		# Translators: This is a label for a set of radio buttons in add dictionary entry dialog.
		typeText = _("&Type")
		typeChoices = [DictionaryEntryDialog.TYPE_LABELS[i] for i in DictionaryEntryDialog.TYPE_LABELS_ORDERING]
		self.typeRadioBox = sHelper.addItem(wx.RadioBox(self, label=typeText, choices=typeChoices))

		sHelper.addDialogDismissButtons(wx.OK | wx.CANCEL, separated=True)

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.setType(speechDictHandler.ENTRY_TYPE_ANYWHERE)
		self.patternTextCtrl.SetFocus()
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)

	def getType(self):
		typeRadioValue = self.typeRadioBox.GetSelection()
		if typeRadioValue == wx.NOT_FOUND:
			return speechDictHandler.ENTRY_TYPE_ANYWHERE
		return DictionaryEntryDialog.TYPE_LABELS_ORDERING[typeRadioValue]

	def onOk(self, evt):
		if not self.patternTextCtrl.GetValue():
			gui.messageBox(
				# Translators: This is an error message to let the user know that the pattern field
				# in the dictionary entry is not valid.
				_("A pattern is required."),
				# Translators: The title of an error message raised by the Dictionary Entry dialog
				_("Dictionary Entry Error"),
				wx.OK | wx.ICON_WARNING,
				self
			)
			self.patternTextCtrl.SetFocus()
			return
		try:
			dictEntry = self.dictEntry = speechDictHandler.SpeechDictEntry(
				self.patternTextCtrl.GetValue(),
				self.replacementTextCtrl.GetValue(),
				self.commentTextCtrl.GetValue(),
				bool(self.caseSensitiveCheckBox.GetValue()),
				self.getType()
			)
			dictEntry.sub("test")  # Ensure there are no grouping error (#11407)
		except Exception as e:
			log.debugWarning("Could not add dictionary entry due to (regex error) : %s" % e)
			gui.messageBox(
				# Translators: This is an error message to let the user know that the dictionary entry is not valid.
				_("Regular Expression error: \"%s\".") % e,
				# Translators: The title of an error message raised by the Dictionary Entry dialog
				_("Dictionary Entry Error"),
				wx.OK | wx.ICON_WARNING,
				self
			)
			return
		evt.Skip()

	def setType(self, type):
		self.typeRadioBox.SetSelection(DictionaryEntryDialog.TYPE_LABELS_ORDERING.index(type))


class DictionaryDialog(
		SettingsDialog,
		metaclass=guiHelper.SIPABCMeta,
):
	"""A dictionary dialog.
	A dictionary dialog is a setting dialog containing a list of dictionary entries and buttons to manage them.
	
	To use this dialog, override L{__init__} calling super().__init__.
	"""
	
	TYPE_LABELS = {t: l.replace("&", "") for t, l in DictionaryEntryDialog.TYPE_LABELS.items()}
	helpId = "SpeechDictionaries"

	@abstractmethod
	def __init__(self, parent, title, speechDict):
		self.title = title
		self.speechDict = speechDict
		self.tempSpeechDict = speechDictHandler.SpeechDict()
		self.tempSpeechDict.extend(self.speechDict)
		globalVars.speechDictionaryProcessing = False
		super().__init__(parent, resizeable=True)
		# Historical initial size, result of L{self.dictList} being (550,350) as of #6287.
		# Setting an initial size on L{self.dictList} by passing a L{size} argument when
		# creating the control would also set its minimum size and thus block the dialog from being shrunk.
		self.SetSize(576, 502)
		self.CentreOnScreen()

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: The label for the list box of dictionary entries in speech dictionary dialog.
		entriesLabelText = _("&Dictionary entries")
		self.dictList = sHelper.addLabeledControl(
			entriesLabelText,
			wx.ListCtrl, style=wx.LC_REPORT | wx.LC_SINGLE_SEL
		)
		# Translators: The label for a column in dictionary entries list used to identify comments for the entry.
		self.dictList.InsertColumn(0, _("Comment"), width=150)
		# Translators: The label for a column in dictionary entries list used to identify pattern
		# (original word or a pattern).
		self.dictList.InsertColumn(1, _("Pattern"), width=150)
		# Translators: The label for a column in dictionary entries list and in a list of symbols
		# from symbol pronunciation dialog used to identify replacement for a pattern or a symbol
		self.dictList.InsertColumn(2, _("Replacement"), width=150)
		# Translators: The label for a column in dictionary entries list used to identify
		# whether the entry is case sensitive or not.
		self.dictList.InsertColumn(3, _("case"), width=50)
		# Translators: The label for a column in dictionary entries list used to identify
		# whether the entry is a regular expression, matches whole words, or matches anywhere.
		self.dictList.InsertColumn(4, _("Type"), width=50)
		self.offOn = (_("off"), _("on"))
		for entry in self.tempSpeechDict:
			self.dictList.Append((
				entry.comment,
				entry.pattern,
				entry.replacement,
				self.offOn[int(entry.caseSensitive)],
				DictionaryDialog.TYPE_LABELS[entry.type]
			))
		self.editingIndex = -1

		bHelper = guiHelper.ButtonHelper(orientation=wx.HORIZONTAL)
		bHelper.addButton(
			parent=self,
			# Translators: The label for a button in speech dictionaries dialog to add new entries.
			label=_("&Add")
		).Bind(wx.EVT_BUTTON, self.onAddClick)

		bHelper.addButton(
			parent=self,
			# Translators: The label for a button in speech dictionaries dialog to edit existing entries.
			label=_("&Edit")
		).Bind(wx.EVT_BUTTON, self.onEditClick)

		bHelper.addButton(
			parent=self,
			# Translators: The label for a button in speech dictionaries dialog to remove existing entries.
			label=_("&Remove")
		).Bind(wx.EVT_BUTTON, self.onRemoveClick)

		bHelper.sizer.AddStretchSpacer()

		bHelper.addButton(
			parent=self,
			# Translators: The label for a button on the Speech Dictionary dialog.
			label=_("Remove all")
		).Bind(wx.EVT_BUTTON, self.onRemoveAll)

		sHelper.addItem(bHelper, flag=wx.EXPAND)

	def postInit(self):
		self.dictList.SetFocus()

	def onCancel(self, evt):
		globalVars.speechDictionaryProcessing = True
		super(DictionaryDialog, self).onCancel(evt)

	def onOk(self, evt):
		globalVars.speechDictionaryProcessing = True
		if self.tempSpeechDict != self.speechDict:
			del self.speechDict[:]
			self.speechDict.extend(self.tempSpeechDict)
			self.speechDict.save()
		super(DictionaryDialog, self).onOk(evt)

	def onAddClick(self, evt):
		# Translators: This is the label for the add dictionary entry dialog.
		entryDialog = DictionaryEntryDialog(self, title=_("Add Dictionary Entry"))
		if entryDialog.ShowModal() == wx.ID_OK:
			self.tempSpeechDict.append(entryDialog.dictEntry)
			self.dictList.Append((
				entryDialog.commentTextCtrl.GetValue(),
				entryDialog.patternTextCtrl.GetValue(),
				entryDialog.replacementTextCtrl.GetValue(),
				self.offOn[int(entryDialog.caseSensitiveCheckBox.GetValue())],
				DictionaryDialog.TYPE_LABELS[entryDialog.getType()]
			))
			index = self.dictList.GetFirstSelected()
			while index >= 0:
				self.dictList.Select(index, on=0)
				index = self.dictList.GetNextSelected(index)
			addedIndex = self.dictList.GetItemCount() - 1
			self.dictList.Select(addedIndex)
			self.dictList.Focus(addedIndex)
			self.dictList.SetFocus()
		entryDialog.Destroy()

	def onEditClick(self, evt):
		if self.dictList.GetSelectedItemCount() != 1:
			return
		editIndex = self.dictList.GetFirstSelected()
		if editIndex < 0:
			return
		entryDialog = DictionaryEntryDialog(self)
		entryDialog.patternTextCtrl.SetValue(self.tempSpeechDict[editIndex].pattern)
		entryDialog.replacementTextCtrl.SetValue(self.tempSpeechDict[editIndex].replacement)
		entryDialog.commentTextCtrl.SetValue(self.tempSpeechDict[editIndex].comment)
		entryDialog.caseSensitiveCheckBox.SetValue(self.tempSpeechDict[editIndex].caseSensitive)
		entryDialog.setType(self.tempSpeechDict[editIndex].type)
		if entryDialog.ShowModal() == wx.ID_OK:
			self.tempSpeechDict[editIndex] = entryDialog.dictEntry
			self.dictList.SetItem(editIndex, 0, entryDialog.commentTextCtrl.GetValue())
			self.dictList.SetItem(editIndex, 1, entryDialog.patternTextCtrl.GetValue())
			self.dictList.SetItem(editIndex, 2, entryDialog.replacementTextCtrl.GetValue())
			self.dictList.SetItem(editIndex, 3, self.offOn[int(entryDialog.caseSensitiveCheckBox.GetValue())])
			self.dictList.SetItem(editIndex, 4, DictionaryDialog.TYPE_LABELS[entryDialog.getType()])
			self.dictList.SetFocus()
		entryDialog.Destroy()

	def onRemoveClick(self, evt):
		index = self.dictList.GetFirstSelected()
		while index >= 0:
			self.dictList.DeleteItem(index)
			del self.tempSpeechDict[index]
			index = self.dictList.GetNextSelected(index)
		self.dictList.SetFocus()

	def onRemoveAll(self, evt):
		if gui.messageBox(
			# Translators: A prompt for confirmation on the Speech Dictionary dialog.
			_("Are you sure you want to remove all the entries in this dictionary?"),
			# Translators: The title on a prompt for confirmation on the Speech Dictionary dialog.
			_("Remove all"),
			style=wx.YES | wx.NO | wx.NO_DEFAULT
		) != wx.YES:
			return
		# Looping instead of clearing here in order to avoid recreation of the columns
		# eventually loosing their manually changed widths.
		while self.tempSpeechDict:
			self.dictList.DeleteItem(0)
			del self.tempSpeechDict[0]
		self.dictList.SetFocus()


class DefaultDictionaryDialog(DictionaryDialog):
	def __init__(self, parent):
		super().__init__(
			parent,
			# Translators: Title for default speech dictionary dialog.
			title=_("Default dictionary"),
			speechDict=speechDictHandler.dictionaries["default"],
		)


class VoiceDictionaryDialog(DictionaryDialog):
	def __init__(self, parent):
		super().__init__(
			parent,
			# Translators: Title for voice dictionary for the current voice such as current eSpeak variant.
			title=_("Voice dictionary (%s)") % speechDictHandler.dictionaries["voice"].fileName,
			speechDict=speechDictHandler.dictionaries["voice"],
		)


class TemporaryDictionaryDialog(DictionaryDialog):
	def __init__(self, parent):
		super().__init__(
			parent,
			# Translators: Title for temporary speech dictionary dialog (the voice dictionary that is active as long
			# as NvDA is running).
			title=_("Temporary dictionary"),
			speechDict=speechDictHandler.dictionaries["temp"],
		)
