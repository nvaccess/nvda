# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import wx

from .controls.storeDialog import AddonStoreDialog
from .controls.messageDialogs import UpdatableAddonsDialog

__all__ = [
	"AddonStoreDialog",
	"initialize",
]


def initialize():
	from utils.schedule import ScheduleThread
	# Ensure the GUI functionality is called from the wx thread from the schedule thread
	ScheduleThread.scheduleDailyJobAtStartUp(lambda: wx.CallAfter(UpdatableAddonsDialog._checkForUpdatableAddons))
