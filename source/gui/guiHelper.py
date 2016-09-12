# -*- coding: UTF-8 -*-
#guiHelper.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2015 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx

# when dialog items are laid out vertically use this much space between them
SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS = 10
# put this much space between buttons, vertical or horizontal
SPACE_BETWEEN_BUTTONS = 7

# put this much space between a label and a control (such as a wx.Choice or wx.TextCtrl) when in a horizontal layout.
SPACE_BETWEEN_LABEL_CONTROL_HORIZONTAL = 10

def addLabelAndControlToHorizontalSizer(wxSizer, wxLabel, wxControl):
	''' Add a label and a control (such as a wx.Choice or wx.TextCtrl) to a horizontal layout sizer, with spacers and 
		alignment set to cater for a horizontal layout.
	'''
	wxSizer.Add(wxLabel,flag=wx.ALIGN_CENTER_VERTICAL)
	wxSizer.AddSpacer(SPACE_BETWEEN_LABEL_CONTROL_HORIZONTAL)
	wxSizer.Add(wxControl)


def addAllContentSizerToMainSizer(wxMainSizer, wxContentSizer):
	''' Add a sizer containing all the content to the main sizer for the dialog. This ensures that the appropriate 
		border is added around the content
	'''
	Content_BorderSpace = 10
	wxMainSizer.Add(wxContentSizer,border=Content_BorderSpace,flag=wx.ALL)

def addButtonsSizerToMainSizer(wxMainSizer, wxButtonsSizer):
	''' Add the given buttons sizer (commonly for OK & Cancel, created with Dialog.CreateButtonSizer) to the main sizer
		for the dialog. This ensures that the appropriate border is added around the content. The Buttons seem to have a
		1px border and 4px spacers inserted before and after each button. 
	'''
	wxMainSizer.Add(wxButtonsSizer, border=5, flag=wx.ALL)

def addItemsToSizer(wxSizer, itemArray, spaceBetween=SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS):
	''' Add the array of items to the sizer putting a spacer between each one.
	'''
	lastIndex = len(itemArray)-1
	for i in xrange(0, lastIndex):
		wxSizer.Add(itemArray[i])
		wxSizer.AddSpacer(spaceBetween)
	# don't add a spacer after the last element
	wxSizer.Add(itemArray[lastIndex])

""" Example usage

class myDialog(class wx.Dialog):

	def __init__(self,parent):
		super(SettingsDialog, self).__init__(parent, wx.ID_ANY, self.title)
		dialog = self

		mainSizer=wx.BoxSizer(wx.VERTICAL)

		sHelper = guiHelper.SizerHelper( wx.VERTICAL)

		filterElement = guiHelper.LabeledControlHelper(dialog, "Filter:", wx.TextCtrl)
		symbols = wx.ListCtrl()
		sHelper.addAutoSpacedItem(guiHelper.associateElement(filterElement, symbols)

		sHelper.addAutoSpacedItem(guiHelper.LabeledControlHelper(dialog, "Choose option", wx.Choice, choices=[1,2,3]))

		button = sHelper.addAutoSpacedItem( wx.Button("Does stuff"))

		# for general items
		checkbox = sHelper.addAutoSpacedItem(wx.CheckBox("always do something"))

		# for groups of buttons
		buttonGroup = guiHelper.ButtonHelper(wx.VERTICAL)
		oneButton = buttonHelper.addButton(wx.Button("one"))
		twoButton = buttonHelper.addButton(wx.Button("one"))
		threeButton = buttonHelper.addButton(wx.Button("three")
		sHelper.addAutoSpacedItem(buttonGroup)

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

class ButtonHelper:
	def __init__(self, orientation):
		self.buttonSizer = wx.BoxSizer(orientation)
		self.space = SPACE_BETWEEN_BUTTONS_HORIZONTAL if orientation is wx.HORIZONTAL else SPACE_BETWEEN_BUTTONS_VERTICALLY

	def addButton(self, *args, **kwargs):
		wxButton = wx.Button(*args, **kwargs)
		if not firstButton:
			self.buttonSizer.AddSpacer(self.space)
		self.buttonSizer.Add(wxButton)
		return wxButton

def associateElements( firstElement, secondElement):
		if isinstance(firstElement, ButtonHelper) or isinstance(secondElement, ButtonHelper):
			raise NotImplemented("AssociateElements has no implementation for buttonHelper elements")

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

		if isinstance(secondElement, (wx.ListCtrl, wx.TextCtrl)):
			sizer = wx.BoxSizer(wx.VERTICAL)
			sizer.Add(firstElement)
			sizer.AddSpacer(SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL)
			sizer.Add(secondElement)

		return sizer

class LabeledControlHelper:
	def __init__(self, dialog, labelText, wxCtrlClass, **kwargs):
		self.label = wx.StaticText(dialog, label=labelText)
		self._ctrl = wxCtrlClass(dialog, **kwargs)
		self.sizer = associateElements(self.label, self._ctrl)

	@property
	def control(self):
		return self._ctrl

class BoxSizerHelper:
	def __init__(self, orientation):
		self.sizer = wx.BoxSizer(orientation)
		self.hasFirstItemBeenAdded = False

	def addAutoSpacedItem(self, item):
		toAdd = item
		keywordArgs = {}
		shouldAddSpacer = self.hasFirstItemBeenAdded

		if isinstance(item, ButtonHelper):
			toAdd = item.sizer
			keywordArgs.update({'border':buttonBorderAmount, 'flags':wx.ALL})
			shouldAddSpacer = False # no need to add a spacer, since the button border has been added.

		if isinstance(item, LabeledControlHelper):
			toAdd = item.sizer

		if shouldAddSpacer:
			self.sizer.AddSpacer(SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		self.sizer.Add(toAdd, **keywordArgs)
		self.hasFirstItemBeenAdded = True
		return item
