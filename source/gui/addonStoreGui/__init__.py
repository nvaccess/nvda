# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import wx

from utils.schedule import ScheduleThread

from .controls.storeDialog import AddonStoreDialog
from .controls.messageDialogs import UpdatableAddonsDialog

__all__ = [
	"AddonStoreDialog",
	"initialize",
]


def initialize():
	# Ensure the GUI functionality is called from the wx thread from the schedule thread
	ScheduleThread.scheduleDailyJobAtStartUp(
		lambda: wx.CallAfter(UpdatableAddonsDialog._checkForUpdatableAddons)
	)
