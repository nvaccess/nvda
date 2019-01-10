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
		empty = (comtypes.automation.VT_EMPTY, 0)
		control = self.control()  # self.control held as a weak ref, ensure it stays alive for the duration of this method
		if control is None:
			return empty

		# Import late to prevent circular import.
		from IAccessibleHandler import accPropServices
		handle, objid, childid = accPropServices.DecomposeHwndIdentityString(pIDString, dwIDStringLen)
		if childid == winUser.CHILDID_SELF:
			return empty

		if idProp == oleacc.PROPID_ACC_ROLE:
			return oleacc.ROLE_SYSTEM_CHECKBUTTON, 1

		if idProp == oleacc.PROPID_ACC_STATE:
			states = oleacc.STATE_SYSTEM_SELECTABLE|oleacc.STATE_SYSTEM_FOCUSABLE
			if control.IsChecked(childid-1):
				states |= oleacc.STATE_SYSTEM_CHECKED
			if control.IsSelected(childid-1):
				# wx doesn't seem to  have a method to check whether a list item is focused.
				# Therefore, assume that a selected item is focused,which is the case in single select list boxes.
				states |= oleacc.STATE_SYSTEM_SELECTED | oleacc.STATE_SYSTEM_FOCUSED
			return states, 1

#: An array with the GUIDs of the properties that an AccPropServer should override for list controls with checkboxes.
#: The role is supposed to be checkbox, rather than list item.
#: The state should be overridden to include the checkable state as well as the checked state if the item is checked.
CHECK_LIST_PROPS = (comtypes.GUID * 2)(*[oleacc.PROPID_ACC_ROLE,oleacc.PROPID_ACC_STATE])

class CustomCheckListBox(wx.CheckListBox):
	"""Custom checkable list to fix a11y bugs in the standard wx checkable list box."""

	def __init__(self, *args, **kwargs):
		super(CustomCheckListBox, self).__init__(*args, **kwargs)
		# Import late to prevent circular import.
		from IAccessibleHandler import accPropServices
		# Register object with COM to fix accessibility bugs in wx.
		server = ListCtrlAccPropServer(self)
		accPropServices.SetHwndPropServer(
			hwnd=self.Handle,
			idObject=winUser.OBJID_CLIENT,
			idChild=0,
			paProps=CHECK_LIST_PROPS,
			cProps=len(CHECK_LIST_PROPS),
			pServer=server,
			AnnoScope=1
		)
		# Register ourself with ourself's selected event, so that we can notify winEvent of the state change.
		self.Bind(wx.EVT_CHECKLISTBOX, self.notifyIAccessible)

	def notifyIAccessible(self, evt):
		# Notify winEvent that something changed.
		# We must do this, so that NVDA receives a stateChange.
		evt.Skip()
		winUser.NotifyWinEvent(winUser.EVENT_OBJECT_STATECHANGE, self.Handle, winUser.OBJID_CLIENT, evt.Selection+1)

class AutoWidthColumnCheckListCtrl(AutoWidthColumnListCtrl, listmix.CheckListCtrlMixin):
	"""
	An L{AutoWidthColumnListCtrl} with accessible checkboxes per item.
	In contrast with L{CustomCheckableListBox}, this class supports multiple columns.
	Also note that this class ignores the L{CheckListCtrlMixin.OnCheckItem} callback.
	If you want to be notified of checked/unchecked events,
	create an event handler for wx.EVT_CHECKLISTBOX.
	This event is only fired when an item is toggled with the mouse or keyboard.
	"""

	def __init__(self, parent, id=wx.ID_ANY, autoSizeColumnIndex="LAST", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
		check_image=None, uncheck_image=None, imgsz=(16, 16)
	):
		AutoWidthColumnListCtrl.__init__(self, parent, id=id, pos=pos, size=size, style=style)
		listmix.CheckListCtrlMixin.__init__(self, check_image, uncheck_image, imgsz)
		# Import late to prevent circular import.
		from IAccessibleHandler import accPropServices
		# Register object with COM to fix accessibility bugs in wx.
		server = ListCtrlAccPropServer(self)
		accPropServices.SetHwndPropServer(
			hwnd=self.GetHandle(),
			idObject=winUser.OBJID_CLIENT,
			idChild=0,
			paProps=CHECK_LIST_PROPS,
			cProps=len(CHECK_LIST_PROPS),
			pServer=server,
			AnnoScope=1
		)
		# Register our hook to check/uncheck items with space.
		# Use wx.EVT_CHAR_HOOK, because EVT_LIST_KEY_DOWN isn't triggered for space.
		self.Bind(wx.EVT_CHAR_HOOK, self.onCharHook)
		# Register an additional event handler to call sendCheckListBoxEvent for mouse clicks if appropriate.
		self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
		# clean up of the accPropServices needs to happen when the control is destroyed. The Destroy method is not called
		# by the wx framework, but we can register to receive the event. https://github.com/wxWidgets/Phoenix/issues/630
		self.Bind(wx.EVT_WINDOW_DESTROY, self._onDestroy, source=self)

	def GetCheckedItems(self):
		return tuple(i for i in xrange(self.ItemCount) if self.IsChecked(i))

	def SetCheckedItems(self, indexes):
		for i in indexes:
			assert 0 <= i < self.ItemCount, "Index (%s) out of range" % i
		for i in xrange(self.ItemCount):
			self.CheckItem(i, i in indexes)

	CheckedItems = property(fget=GetCheckedItems, fset=SetCheckedItems)

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
		self.sendCheckListBoxEvent(index)

	def onLeftDown(self,evt):
		"""Additional event handler for mouse clicks to call L{sendCheckListBoxEvent}."""
		(index, flags) = self.HitTest(evt.GetPosition())
		evt.Skip()
		if flags == wx.LIST_HITTEST_ONITEMICON:
			self.sendCheckListBoxEvent(index)

	def CheckItem(self, index, check=True):
		"""
		Adapted from L{CheckListCtrlMixin} to ignore the OnCheckItem callback and to call L{notifyIAccessible}.
		"""
		img_idx = self.GetItem(index).GetImage()
		if img_idx == 0 and check:
			self.SetItemImage(index, 1)
		elif img_idx == 1 and not check:
			self.SetItemImage(index, 0)
		self.notifyIAccessible(index)

	def notifyIAccessible(self, index):
		# Notify winEvent that something changed.
		# We must do this, so that NVDA receives a stateChange.
		winUser.NotifyWinEvent(winUser.EVENT_OBJECT_STATECHANGE, self.Handle, winUser.OBJID_CLIENT, index+1)

	def sendCheckListBoxEvent(self, index):
		evt = wx.CommandEvent(wx.wxEVT_CHECKLISTBOX,self.Id)
		evt.EventObject = self
		evt.Int = index
		self.ProcessEvent(evt)

	def _onDestroy(self, evt):
		evt.Skip() #  Allow other handlers to process this event.
		self._cleanup()

	def _cleanup(self):
		from IAccessibleHandler import accPropServices
		accPropServices.ClearHwndProps(
			hwnd=self.GetHandle(),
			idObject=winUser.OBJID_CLIENT,
			idChild=0,
			paProps=CHECK_LIST_PROPS,
			cProps=len(CHECK_LIST_PROPS)
		)

