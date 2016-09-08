# -*- coding: UTF-8 -*-
#guiHelper.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2015 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx

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

class buttonHelper:
	def __init__(self, orientation):
		self.buttonSizer = wx.BoxSizer(orientation)
		self.space = SPACE_BETWEEN_BUTTONS_HORIZONTAL if orientation is wx.HORIZONTAL else SPACE_BETWEEN_BUTTONS_VERTICALLY

	def AddButton(self, *args, **kwargs):
		wxButton = wx.Button(*args, **kwargs)
		if is not firstButton:
			self.buttonSizer.AddSpacer(self.space)
		self.buttonSizer.Add(wxButton)
		return wxButton

""" Example usage

class myDialog(class wx.Dialog):

	def __init__(self,parent):
		super(SettingsDialog, self).__init__(parent, wx.ID_ANY, self.title)
		mainSizer=wx.BoxSizer(wx.VERTICAL)

		# Use factory method to create a sizer type specific helper
		sHelper = guiHelper.sizerHelper(dialog, wx.BoxSizer(wx.VERTICAL))

		filterElement = guiHelper.labeledControlHelper(dialog, "Filter:", wx.TextCtrl)
		symbols = wx.ListCtrl()
		sHelper.AddAutoSpacedItem(associateElement(filterElement, symbols)

		sHelper.AddAutoSpacedItem(guiHelper.labeledControlHelper(dialog, "Choose option", wx.Choice, choices=[1,2,3]))

		button = sHelper.AddAutoSpacedItem( wx.Button("Does stuff"))

		# for general items
		checkbox = sHelper.AddAutoSpacedItem(wx.CheckBox("always do something"))

		# for groups of buttons
		buttonGroup = guiHelper.buttonHelper(wx.VERTICAL)
		oneButton = buttonHelper.AddButton(wx.Button("one"))
		twoButton = buttonHelper.AddButton(wx.Button("one"))
		threeButton = buttonHelper.AddButton(wx.Button("three")
		sHelper.AddItem(buttonGroup)

		mainSizer.Add(sHelper.sizer, border=10, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
	...
"""

def AssociateElements( firstElement, secondElement):
		# check if horizontal / vertical
		# check type of control
		# handle different combinations eg:
		if isinstance(firstElement, buttonHelper) or isinstance(secondElement, buttonHelper):
			raise NotImplemented("AssociateElements has no implementation for buttonHelper elements")

		if isinstance(firstElement, labeledControlHelper):
			firstElement = firstElement.sizer

		if isinstance(secondElement, [wx.Choice, wx.TextCtrl]):
			sizer = wx.BoxSizer(wx.HORIZONTAL)
			sizer.Add(firstElement)
			sizer.AddSpacer(SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL)
			sizer.Add(secondElement)

		if isinstance(secondElement, [wx.ListCtrl, wx.TextCtrl])
			sizer = wx.BoxSizer(wx.VERTICAL)
			sizer.Add(firstElement)
			sizer.AddSpacer(SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL)
			sizer.Add(secondElement)

		return sizer

class labeledControlHelper:
	def __init__(self, dialog, labelText, wxCtrlClass, **kwargs):
		self.label = wx.StaticText(dialog, labelText)
		self.ctrl = ctlClass(dialog, **kwargs)
		self.sizer = AssociateElements(self.label, self.ctrl)

class sizerHelper:
	def __init__(self, wxSizer):
		self.sizer = wxSizer
		self.hasFirstItemBeenAdded = False

	def AddAutoSpacedItem(item):
		toAdd = item
		if isinstance(item, ButtonHelper):
			self.Sizer.Add(item.sizer, border=buttonBorderAmount, flags=wx.ALL)
			return item # no need to add a spacer, since the button border has been added.

		if self.hasFirstItemBeenAdded:
			self.sizer.AddSpacer(betweenItemsAmount)

		if isinstance(item, labeledControlHelper):
			toAdd = item.sizer

		self.Sizer.Add(toAdd)
		return item
