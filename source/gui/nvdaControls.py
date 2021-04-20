# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2021 NV Access Limited, Derek Riemer
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import wx
from wx.lib import scrolledpanel
from wx.lib.mixins import listctrl as listmix
from .dpiScalingHelper import DpiScalingHelperMixin
from . import guiHelper
import winUser
import winsound

from collections.abc import Callable


class AutoWidthColumnListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
	"""
	A list control that allows you to specify a column to resize to take up the remaining width of a wx.ListCtrl.
	It also changes L{OnGetItemText} to call an optionally provided callable,
	and adds a l{sendListItemFocusedEvent} method.
	"""

	def __init__(
		self,
		parent,
		id=wx.ID_ANY,
		autoSizeColumn="LAST",
		itemTextCallable=None,
		pos=wx.DefaultPosition,
		size=wx.DefaultSize,
		style=0
	):
		""" initialiser
			Takes the same parameter as a wx.ListCtrl with the following additions:
			@param autoSizeColumn: defaults to "LAST" which results in the last column being resized.
				Pass the column number to be resized, valid values: 1 to N
			@type autoSizeColumn: int
			@param itemTextCallable: A callable to be called to get the item text for a particular item's column in the list.
				It should accept the same parameters as L{OnGetItemText},
			@type itemTextCallable: L{callable}
		"""
		if itemTextCallable is not None:
			if not isinstance(itemTextCallable, Callable):
				raise TypeError("itemTextCallable should be None or a callable")
			self._itemTextCallable = itemTextCallable
		else:
			self._itemTextCallable = self._super_itemTextCallable
		wx.ListCtrl.__init__(self, parent, id=id, pos=pos, size=size, style=style)
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		self.setResizeColumn(autoSizeColumn)
		self.Bind(wx.EVT_WINDOW_DESTROY, source=self, id=self.GetId, handler=self._onDestroy)

	def _onDestroy(self, evt):
		evt.Skip()
		self._itemTextCallable = None

	def _super_itemTextCallable(self, item, column):
		return super(AutoWidthColumnListCtrl, self).OnGetItemText(item, column)

	def OnGetItemText(self, item, column):
		return self._itemTextCallable(item, column)

	def sendListItemFocusedEvent(self, index):
		evt = wx.ListEvent(wx.wxEVT_LIST_ITEM_FOCUSED, self.Id)
		evt.EventObject = self
		evt.Index = index
		self.ProcessEvent(evt)

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


class ListCtrlAccessible(wx.Accessible):
	"""WX Accessible implementation for checkable lists which aren't fully accessible."""

	def GetRole(self, childId):
		if childId == winUser.CHILDID_SELF:
			return super().GetRole(childId)
		return (wx.ACC_OK, wx.ROLE_SYSTEM_CHECKBUTTON)

	def GetState(self, childId):
		if childId == winUser.CHILDID_SELF:
			return super().GetState(childId)
		states = wx.ACC_STATE_SYSTEM_SELECTABLE | wx.ACC_STATE_SYSTEM_FOCUSABLE
		if self.Window.IsChecked(childId - 1):
			states |= wx.ACC_STATE_SYSTEM_CHECKED
		if self.Window.IsSelected(childId - 1):
			# wx doesn't seem to  have a method to check whether a list item is focused.
			# Therefore, assume that a selected item is focused,which is the case in single select list boxes.
			states |= wx.ACC_STATE_SYSTEM_SELECTED | wx.ACC_STATE_SYSTEM_FOCUSED
		return (wx.ACC_OK, states)


class CustomCheckListBox(wx.CheckListBox):
	"""Custom checkable list to fix a11y bugs in the standard wx checkable list box."""

	def __init__(self, *args, **kwargs):
		super(CustomCheckListBox, self).__init__(*args, **kwargs)
		# Register a custom wx.Accessible implementation to fix accessibility incompleties
		self.SetAccessible(ListCtrlAccessible(self))
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

	def __init__(self, parent, id=wx.ID_ANY, autoSizeColumn="LAST", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
		check_image=None, uncheck_image=None, imgsz=(16, 16)
	):
		AutoWidthColumnListCtrl.__init__(self, parent, id=id, pos=pos, size=size, style=style, autoSizeColumn=autoSizeColumn)
		listmix.CheckListCtrlMixin.__init__(self, check_image, uncheck_image, imgsz)
		# Register a custom wx.Accessible implementation to fix accessibility incompleties
		self.SetAccessible(ListCtrlAccessible(self))
		# Register our hook to check/uncheck items with space.
		# Use wx.EVT_CHAR_HOOK, because EVT_LIST_KEY_DOWN isn't triggered for space.
		self.Bind(wx.EVT_CHAR_HOOK, self.onCharHook)
		# Register an additional event handler to call sendCheckListBoxEvent for mouse clicks if appropriate.
		self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)

	def GetCheckedItems(self):
		return tuple(i for i in range(self.ItemCount) if self.IsChecked(i))

	def SetCheckedItems(self, indexes):
		for i in indexes:
			assert 0 <= i < self.ItemCount, "Index (%s) out of range" % i
		for i in range(self.ItemCount):
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

class DPIScaledDialog(wx.Dialog, DpiScalingHelperMixin):
	"""Automatically calls constructors in the right order, passing on arguments, and providing scaling features.
	Until wxWidgets/wxWidgets#334 is resolved, and we have updated to that build of wx.
	"""
	def __init__(self, *args, **kwargs):
		"""Called in place of wx.Dialog __init__ arguments are forwarded on.
		Expected args (from wx docs):
		parent, id, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE, name=wx.DialogNameStr
		where:
		wx.DEFAULT_DIALOG_STYLE = (wxCAPTION | wxSYSTEM_MENU | wxCLOSE_BOX)
		"""
		wx.Dialog.__init__(self, *args, **kwargs)
		DpiScalingHelperMixin.__init__(self, self.GetHandle())


class MessageDialog(DPIScaledDialog):
	"""Provides a more flexible message dialog. Consider overriding _addButtons, to set your own
	buttons and behaviour.
	"""

	# Dialog types currently supported
	DIALOG_TYPE_STANDARD = 1
	DIALOG_TYPE_WARNING = 2
	DIALOG_TYPE_ERROR = 3

	_DIALOG_TYPE_ICON_ID_MAP = {
		# DIALOG_TYPE_STANDARD is not in the map, since we wish to use the default icon provided by wx
		DIALOG_TYPE_ERROR: wx.ART_ERROR,
		DIALOG_TYPE_WARNING: wx.ART_WARNING,
	}

	_DIALOG_TYPE_SOUND_ID_MAP = {
		# DIALOG_TYPE_STANDARD is not in the map, since there should be no sound for a standard dialog.
		DIALOG_TYPE_ERROR: winsound.MB_ICONHAND,
		DIALOG_TYPE_WARNING: winsound.MB_ICONASTERISK,
	}

	def _addButtons(self, buttonHelper):
		"""Adds ok / cancel buttons. Can be overridden to provide alternative functionality.
		"""
		ok = buttonHelper.addButton(
			self,
			id=wx.ID_OK,
			# Translators: An ok button on a message dialog.
			label=_("OK")
		)
		ok.SetDefault()
		ok.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.OK))

		cancel = buttonHelper.addButton(
			self,
			id=wx.ID_CANCEL,
			# Translators: A cancel button on a message dialog.
			label=_("Cancel")
		)
		cancel.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.CANCEL))

	def _addContents(self, contentsSizer: guiHelper.BoxSizerHelper):
		"""Adds additional contents  to the dialog, before the buttons.
		Subclasses may implement this method.
		"""

	def _setIcon(self, type):
		try:
			iconID = self._DIALOG_TYPE_ICON_ID_MAP[type]
		except KeyError:
			# type not found, use default icon.
			return
		icon = wx.ArtProvider.GetIcon(iconID, client=wx.ART_MESSAGE_BOX)
		self.SetIcon(icon)

	def _setSound(self, type):
		try:
			self._soundID = self._DIALOG_TYPE_SOUND_ID_MAP[type]
		except KeyError:
			# type not found, no sound.
			self._soundID = None
			return

	def _playSound(self):
		winsound.MessageBeep(self._soundID)

	def __init__(self, parent, title, message, dialogType=DIALOG_TYPE_STANDARD):
		DPIScaledDialog.__init__(self, parent, title=title)

		self._setIcon(dialogType)
		self._setSound(dialogType)
		self.Bind(wx.EVT_SHOW, self._onShowEvt, source=self)
		self.Bind(wx.EVT_ACTIVATE, self._onDialogActivated, source=self)

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentsSizer = guiHelper.BoxSizerHelper(parent=self, orientation=wx.VERTICAL)

		text = wx.StaticText(self, label=message)
		text.Wrap(self.scaleSize(self.GetSize().Width))
		contentsSizer.addItem(text)
		self._addContents(contentsSizer)

		buttonHelper = guiHelper.ButtonHelper(wx.HORIZONTAL)
		self._addButtons(buttonHelper)
		contentsSizer.addDialogDismissButtons(buttonHelper)

		mainSizer.Add(
			contentsSizer.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL
		)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.CentreOnScreen()

	def _onDialogActivated(self, evt):
		evt.Skip()

	def _onShowEvt(self, evt):
		"""
		:type evt: wx.ShowEvent
		"""
		if evt.IsShown():
			self._playSound()
		evt.Skip()


class EnhancedInputSlider(wx.Slider):

	def __init__(self,*args, **kwargs):
		super(EnhancedInputSlider,self).__init__(*args,**kwargs)
		self.Bind(wx.EVT_CHAR, self.onSliderChar)

	def SetValue(self,i):
		super(EnhancedInputSlider, self).SetValue(i)
		evt = wx.CommandEvent(wx.wxEVT_COMMAND_SLIDER_UPDATED,self.GetId())
		evt.SetInt(i)
		self.ProcessEvent(evt)
		# HACK: Win events don't seem to be sent for certain explicitly set values,
		# so send our own win event.
		# This will cause duplicates in some cases, but NVDA will filter them out.
		winUser.user32.NotifyWinEvent(winUser.EVENT_OBJECT_VALUECHANGE,self.Handle,winUser.OBJID_CLIENT,winUser.CHILDID_SELF)

	def onSliderChar(self, evt):
		key = evt.KeyCode
		if key == wx.WXK_UP:
			newValue = min(self.Value + self.LineSize, self.Max)
		elif key == wx.WXK_DOWN:
			newValue = max(self.Value - self.LineSize, self.Min)
		elif key == wx.WXK_PAGEUP:
			newValue = min(self.Value + self.PageSize, self.Max)
		elif key == wx.WXK_PAGEDOWN:
			newValue = max(self.Value - self.PageSize, self.Min)
		elif key == wx.WXK_HOME:
			newValue = self.Max
		elif key == wx.WXK_END:
			newValue = self.Min
		else:
			evt.Skip()
			return
		self.SetValue(newValue)


class TabbableScrolledPanel(scrolledpanel.ScrolledPanel):
	"""
	This class was created to ensure a ScrolledPanel scrolls to nested children of the panel when navigating
	with tabs (#12224). A PR to wxPython implementing this fix can be tracked on
	https://github.com/wxWidgets/Phoenix/pull/1950
	"""
	def GetChildRectRelativeToSelf(self, child: wx.Window) -> wx.Rect:
		"""
		window.GetRect returns the size of a window, and its position relative to its parent.
		When calculating ScrollChildIntoView, the position relative to its parent is not relevant unless the
		parent is the ScrolledPanel itself. Instead, calculate the position relative to scrolledPanel
		"""
		childRectRelativeToScreen = child.GetScreenRect()
		scrolledPanelScreenPosition = self.GetScreenPosition()
		return wx.Rect(
			childRectRelativeToScreen.x - scrolledPanelScreenPosition.x,
			childRectRelativeToScreen.y - scrolledPanelScreenPosition.y,
			childRectRelativeToScreen.width,
			childRectRelativeToScreen.height
		)

	def ScrollChildIntoView(self, child: wx.Window) -> None:
		"""
		Overrides child.GetRect with `GetChildRectRelativeToSelf` before calling
		`super().ScrollChildIntoView`. `super().ScrollChildIntoView` incorrectly uses child.GetRect to
		navigate scrolling, which is relative to the parent, where it should instead be relative to this
		ScrolledPanel.
		"""
		oldChildGetRectFunction = child.GetRect
		child.GetRect = lambda: self.GetChildRectRelativeToSelf(child)
		try:
			super().ScrollChildIntoView(child)
		finally:
			# ensure child.GetRect is reset properly even if super().ScrollChildIntoView throws an exception
			child.GetRect = oldChildGetRectFunction
