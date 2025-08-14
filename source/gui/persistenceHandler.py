# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Custom persistence handlers for use with :mod:`wx.lib.agw.persist`."""

import wx
import wx.lib
from wx.lib.agw.persist.persist_handlers import AbstractHandler
from wx.lib.agw.persist.persistencemanager import PersistentObject


class EnumeratedChoiceHandler(AbstractHandler):
	"""
	Persistence handler which stores and retrieves the persisted window's selected index.

	Supported windows:
	- :class:`wx.Choice`

	In theory, any `wx.Window` subclass that implements integer `GetSelection` and `SetSelection` should work.
	"""

	_KIND = "EnumeratedChoice"
	"""String that uniquely identifies this persistence handler."""

	_NAME = "Selection"
	"""Key for the :attr:`wx.Choice.Selection` when persisted."""

	# Type hints for AbstractHandler
	_pObject: PersistentObject
	"""PersistentObject we're handling read/write for."""

	_window: wx.Choice
	"""Window being persisted."""

	def __init__(self, pObject: PersistentObject):
		"""Initialiser.

		:param pObject: :class:`PersistentObject` for which we're handling saving and restoring.
		:raises TypeError: If ``pObject``'s ``Window`` isn't a :class:`wx.Choice`.
		"""
		if not isinstance(pObject.GetWindow(), wx.Choice):
			raise TypeError("Only wx.Choice controls are supported.")
		super().__init__(pObject)

	def Save(self) -> bool:
		"""Save the control's value to storage.

		:return: ``True`` if successful; ``False`` otherwise.
		"""
		self._pObject.SaveCtrlValue(self._NAME, self._window.GetSelection())
		return True

	def Restore(self) -> bool:
		"""Restore the control's value from storage.

		:return: ``True`` if the control's selection was restored from storage; ``False`` otherwise.
		"""
		value = self._pObject.RestoreCtrlValue(self._NAME)
		if value is not None:
			try:
				value = int(value)
			except ValueError:
				return False
			if (0 <= value < self._window.GetCount()) or value == wx.NOT_FOUND:
				self._window.SetSelection(value)
				return True
		return False

	def GetKind(self) -> str:
		"""Get a string that uniquely identifies the type of persistence handler being used.

		:return: A unique string that identifies this class of persistence handler.
		"""
		return self._KIND
