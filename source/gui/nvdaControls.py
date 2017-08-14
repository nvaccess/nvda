# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
from wx.lib.mixins import listctrl as listmix
from gui.accPropServer import *
import oleacc
import winUser
from winUser import EVENT_OBJECT_STATECHANGE
import comtypes
from ctypes import *

class AutoWidthColumnListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
	"""
	A list control that allows you to specify a column to resize to take up the remaining width of a wx.ListCtrl
	"""
	def __init__(self, parent, id=wx.ID_ANY, autoSizeColumnIndex="LAST", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
		""" initialiser
			Takes the same parameter as a wx.ListCtrl with the following additions:
			autoSizeColumnIndex - defaults to "LAST" which results in the last column being resized. Pass the index of 
			the column to be resized.
		"""
		wx.ListCtrl.__init__(self, parent, id, pos, size, style)
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		self.setResizeColumn(autoSizeColumnIndex)

class SelectOnFocusSpinCtrl(wx.SpinCtrl):
	"""
	A spin control that automatically selects the value when the control gains focus.
	This makes editing the values quicker.
	"""
	def __init__(self, parent, id=wx.ID_ANY, value=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.SP_ARROW_KEYS|wx.ALIGN_RIGHT, min=0, max=100, initial=0, name=wx.SpinCtrlNameStr):
		""" initialiser - Takes the same parameters as a wx.SpinCtrl.
		"""
		wx.SpinCtrl.__init__(self, parent, id, value, pos, size, style, min, max, initial, name)
		self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

	def OnSetFocus(self, evt):
		numChars = len(str(self.GetValue()))
		self.SetSelection(0, numChars)
		evt.Skip()

class ListCtrlAccPropServer(IAccPropServer_Impl):
	"""AccPropServer for wx checkable lists which aren't fully accessible."""
	def _getPropValue(self, pIDString, dwIDStringLen, idProp):
		#Import late to prevent circular import.
		from IAccessibleHandler import accPropServices
		handle, objid, childid = accPropServices.DecomposeHwndIdentityString(pIDString, dwIDStringLen)
		if childid != winUser.CHILDID_SELF:
			if idProp == PROPID_ACC_ROLE:
				return oleacc.ROLE_SYSTEM_CHECKBUTTON, 1
			if idProp == PROPID_ACC_STATE:
				if self.control.IsChecked(childid-1):
					return oleacc.STATE_SYSTEM_CHECKED|oleacc.STATE_SYSTEM_SELECTED, 1
				else:
					return oleacc.STATE_SYSTEM_SELECTED, 1
		return comtypes.automation.VT_EMPTY, 0

class CustomCheckableList(wx.CheckListBox):
	"""Custom checkable list to fix a11y bugs in the standard wx checkable list."""

	def __init__(self, *args, **kwargs):
		super(CustomCheckableList, self).__init__(*args, **kwargs)
		#Import late to prevent circular import.
		from IAccessibleHandler import accPropServices
		#Register object with COM to fix accessibility bugs in wx.
		server = ListCtrlAccPropServer(self)
		accPropServices.SetHwndPropServer(self.Handle, winUser.OBJID_CLIENT, 0, (comtypes.GUID * 2)(*[PROPID_ACC_ROLE,PROPID_ACC_STATE]), c_int(2), server, 1)
		#Register ourself with ourself's selected event, so that we can notify winEvent of the state change.
		self.Bind(wx.EVT_CHECKLISTBOX, self.notifyIAccessible)

	def notifyIAccessible(self, evt):
		#Notify winEvent that something changed.
		#We must do this, so that NVDA receives a stateChange.
		evt.Skip()
		winUser.NotifyWinEvent(EVENT_OBJECT_STATECHANGE, self.Handle, winUser.OBJID_CLIENT, evt.Selection+1)
