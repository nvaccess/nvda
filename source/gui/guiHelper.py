# -*- coding: UTF-8 -*-
#guiHelper.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2015 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx

""" Example usage

class myDialog(class wx.Dialog):

	def __init__(self,parent):
		super(SettingsDialog, self).__init__(parent, wx.ID_ANY, self.title)
		dialog = self

		mainSizer=wx.BoxSizer(wx.VERTICAL)

		sHelper = guiHelper.SizerHelper( wx.VERTICAL)

		filterElement = guiHelper.LabeledControlHelper(dialog, "Filter:", wx.TextCtrl)
		symbols = wx.ListCtrl()
		sHelper.addItem(guiHelper.associateElement(filterElement, symbols)

		sHelper.addItem(guiHelper.LabeledControlHelper(dialog, "Choose option", wx.Choice, choices=[1,2,3]))

		button = sHelper.addItem( wx.Button("Does stuff"))

		# for general items
		checkbox = sHelper.addItem(wx.CheckBox("always do something"))

		# for groups of buttons
		buttonGroup = guiHelper.ButtonHelper(wx.VERTICAL)
		oneButton = buttonHelper.addButton(wx.Button("one"))
		twoButton = buttonHelper.addButton(wx.Button("one"))
		threeButton = buttonHelper.addButton(wx.Button("three")
		sHelper.addItem(buttonGroup)

		mainSizer.Add(sHelper.sizer, border=10, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
	...
"""
# border space to be used around all controls in dialogs
BORDER_FOR_DIALOGS=10

# when dialog items are laid out vertically use this much space between them
SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS = 10

# put this much space between buttons  next to each other horizontally.
SPACE_BETWEEN_BUTTONS_HORIZONTAL = 7

# put this much space between buttons next to each other vertically
SPACE_BETWEEN_BUTTONS_VERTICALLY = 5

# put this much space between two horizontally associated elements (such as a wx.StaticText and a wx.Choice or wx.TextCtrl)
SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL = 10

# put this much space between two vertically associated elements (such as a wx.StaticText and a wx.Choice or wx.TextCtrl)
SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL = 3

class ButtonHelper(object):
	def __init__(self, orientation):
		object.__init__(self)
		self.firstButton = True
		self.sizer = wx.BoxSizer(orientation)
		self.space = SPACE_BETWEEN_BUTTONS_HORIZONTAL if orientation is wx.HORIZONTAL else SPACE_BETWEEN_BUTTONS_VERTICALLY

	def addButton(self, *args, **kwargs):
		wxButton = wx.Button(*args, **kwargs)
		if not self.firstButton:
			self.sizer.AddSpacer(self.space)
		self.sizer.Add(wxButton)
		self.firstButton = False
		return wxButton

def associateElements( firstElement, secondElement):
		if isinstance(firstElement, ButtonHelper) or isinstance(secondElement, ButtonHelper):
			raise NotImplementedError("AssociateElements has no implementation for buttonHelper elements")

		if isinstance(firstElement, LabeledControlHelper):
			firstElement = firstElement.sizer

		if isinstance(secondElement, (wx.Choice, wx.TextCtrl)):
			sizer = wx.BoxSizer(wx.HORIZONTAL)
			kwargs = {}
			if isinstance(firstElement, wx.StaticText):
				kwargs.update( {'flag':wx.ALIGN_CENTER_VERTICAL} )
			sizer.Add(firstElement, **kwargs)
			sizer.AddSpacer(SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL)
			sizer.Add(secondElement)
		elif isinstance(secondElement, (wx.ListCtrl,wx.ListBox,wx.TreeCtrl)):
			sizer = wx.BoxSizer(wx.VERTICAL)
			sizer.Add(firstElement)
			sizer.AddSpacer(SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL)
			sizer.Add(secondElement)
		elif isinstance(firstElement, wx.Button) and isinstance(secondElement, wx.CheckBox):
			sizer = wx.BoxSizer(wx.HORIZONTAL)
			sizer.Add(firstElement)
			sizer.AddSpacer(SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL)
			sizer.Add(secondElement, flag=wx.ALIGN_CENTER_VERTICAL)
		else:
			raise NotImplementedError("The secondElement argument has no implementation")

		return sizer

class LabeledControlHelper(object):
	def __init__(self, dialog, labelText, wxCtrlClass, **kwargs):
		object.__init__(self)
		self.label = wx.StaticText(dialog, label=labelText)
		self._ctrl = wxCtrlClass(dialog, **kwargs)
		self._sizer = associateElements(self.label, self._ctrl)

	@property
	def control(self):
		return self._ctrl
	@property
	def sizer(self):
		return self._sizer

class BoxSizerHelper(object):
	def __init__(self, parent, orientation=None, sizer=None):
		object.__init__(self)
		self.parent = parent
		self.hasFirstItemBeenAdded = False
		if orientation and sizer:
			raise ValueError("Supply either orientation OR sizer. Not both.")
		if orientation and orientation in (wx.VERTICAL, wx.HORIZONTAL):
			self.sizer = wx.BoxSizer(orientation)
		elif sizer and isinstance(sizer, wx.BoxSizer):
			self.sizer = sizer
		else:
			ValueError("Orientation OR Sizer must be supplied.")

	def addItem(self, item):
		toAdd = item
		keywordArgs = {}
		shouldAddSpacer = self.hasFirstItemBeenAdded

		if isinstance(item, ButtonHelper):
			toAdd = item.sizer
			buttonBorderAmount = 5
			keywordArgs.update({'border':buttonBorderAmount, 'flag':wx.ALL})
			shouldAddSpacer = False # no need to add a spacer, since the button border has been added.

		if isinstance(item, LabeledControlHelper):
			raise NotImplementedError("Use addLabeledControl instead")

		if shouldAddSpacer:
			self.sizer.AddSpacer(SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		self.sizer.Add(toAdd, **keywordArgs)
		self.hasFirstItemBeenAdded = True
		return item

	def addLabeledControl(self, labelText, wxCtrlClass, **kwargs):
		labeledControl = LabeledControlHelper(self.parent, labelText, wxCtrlClass, **kwargs)
		self.addItem(labeledControl.sizer)
		return labeledControl.control

