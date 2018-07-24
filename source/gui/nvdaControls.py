# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016-2018 NV Access Limited, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
from wx.lib.mixins import listctrl as listmix
from gui import accPropServer
import oleacc
import winUser
import comtypes
from ctypes import c_int

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
	def __init__(self, parent, id=wx.ID_ANY, value=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.SP_ARROW_KEYS|wx.ALIGN_RIGHT, min=0, max=100, initial=0, name="labelStr"):
		""" initialiser - Takes the same parameters as a wx.SpinCtrl.
		"""
		wx.SpinCtrl.__init__(self, parent, id, value, pos, size, style, min, max, initial, name)
		self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

	def OnSetFocus(self, evt):
		numChars = len(str(self.GetValue()))
		self.SetSelection(0, numChars)
		evt.Skip()

class ListCtrlAccPropServer(accPropServer.IAccPropServer_Impl):
	"""AccPropServer for wx checkable lists which aren't fully accessible."""
	def _getPropValue(self, pIDString, dwIDStringLen, idProp):
		#Import late to prevent circular import.
		from IAccessibleHandler import accPropServices
		handle, objid, childid = accPropServices.DecomposeHwndIdentityString(pIDString, dwIDStringLen)
		if childid != winUser.CHILDID_SELF:
			if idProp == oleacc.PROPID_ACC_ROLE:
				return oleacc.ROLE_SYSTEM_CHECKBUTTON, 1
			if idProp == oleacc.PROPID_ACC_STATE:
				states = oleacc.STATE_SYSTEM_SELECTABLE|oleacc.STATE_SYSTEM_FOCUSABLE
				if self.control.IsChecked(childid-1):
					states |= oleacc.STATE_SYSTEM_CHECKED
				if self.control.IsSelected(childid-1):
					# wx doesn't seem to  have a method to check whether a list item is focused.
					# Therefore, assume that a selected item is focused,which is the case in single select list boxes.
					states |= oleacc.STATE_SYSTEM_SELECTED | oleacc.STATE_SYSTEM_FOCUSED
				return states, 1
		return comtypes.automation.VT_EMPTY, 0

class CustomCheckableListBox(wx.CheckListBox):
	"""Custom checkable list to fix a11y bugs in the standard wx checkable list box."""

	def __init__(self, *args, **kwargs):
		super(CustomCheckableListBox, self).__init__(*args, **kwargs)
		#Import late to prevent circular import.
		from IAccessibleHandler import accPropServices
		#Register object with COM to fix accessibility bugs in wx.
		server = ListCtrlAccPropServer(self)
		accPropServices.SetHwndPropServer(self.Handle, winUser.OBJID_CLIENT, 0, (comtypes.GUID * 2)(*[oleacc.PROPID_ACC_ROLE,oleacc.PROPID_ACC_STATE]), c_int(2), server, 1)
		#Register ourself with ourself's selected event, so that we can notify winEvent of the state change.
		self.Bind(wx.EVT_CHECKLISTBOX, self.notifyIAccessible)

	def notifyIAccessible(self, evt):
		#Notify winEvent that something changed.
		#We must do this, so that NVDA receives a stateChange.
		evt.Skip()
		winUser.NotifyWinEvent(winUser.EVENT_OBJECT_STATECHANGE, self.Handle, winUser.OBJID_CLIENT, evt.Selection+1)

class CheckableAutoWidthColumnListCtrl(AutoWidthColumnListCtrl, listmix.CheckListCtrlMixin):
	"""
	An L{AutoWidthColumnListCtrl} with accessible checkboxes per item.
	In contrast with L{CustomCheckableListBox}, this class supports multiple columns.
	"""

	def __init__(self, parent, id=wx.ID_ANY, autoSizeColumnIndex="LAST", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
		check_image=None, uncheck_image=None, imgsz=(16, 16)
	):
		AutoWidthColumnListCtrl.__init__(self, parent, id=id, pos=pos, size=size, style=style)
		listmix.CheckListCtrlMixin.__init__(self, check_image, uncheck_image, imgsz)
		# A list containing the checked items
		self._checked = []
		#Import late to prevent circular import.
		from IAccessibleHandler import accPropServices
		#Register object with COM to fix accessibility bugs in wx.
		server = ListCtrlAccPropServer(self)
		accPropServices.SetHwndPropServer(self.Handle, winUser.OBJID_CLIENT, 0, (comtypes.GUID * 2)(*[oleacc.PROPID_ACC_ROLE,oleacc.PROPID_ACC_STATE]), c_int(2), server, 1)
		# Register our hook to check/uncheck items with space.
		# Use wx.EVT_CHAR_HOOK, because EVT_LIST_KEY_DOWN isn't triggered for space.
		self.Bind(wx.EVT_CHAR_HOOK, self.onCharHook)

	@property
	def Checked(self):
		return self._checked

	@Checked.setter
	def Checked(self, value):
		for index in xrange(self.ItemCount):
			self.CheckItem(index, index in value)

	def onCharHook(self,evt):
		key = evt.GetKeyCode()
		if key!=wx.WXK_SPACE:
			evt.Skip()
			return
		index = self.FocusedItem
		if index == -1:
			evt.Skip()
			return
		self.ToggleItem(index)

	def OnCheckItem(self, index, flag):
		if flag:
			self._checked.append(index)
		else:
			assert index in self._checked
			self._checked.remove(index)
		#Notify winEvent that something changed.
		#We must do this, so that NVDA receives a stateChange.
		winUser.NotifyWinEvent(winUser.EVENT_OBJECT_STATECHANGE, self.Handle, winUser.OBJID_CLIENT, index+1)
