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

