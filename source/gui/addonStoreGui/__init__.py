# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import wx

import config
from config.configFlags import AddonsAutomaticUpdate
import gui
from utils.schedule import scheduleThread, ThreadTarget

from .controls.storeDialog import AddonStoreDialog
from .controls.messageDialogs import UpdatableAddonsDialog

__all__ = [
	"AddonStoreDialog",
	"initialize",
]


def initialize():
	scheduleThread.scheduleDailyJobAtStartUp(
		UpdatableAddonsDialog._checkForUpdatableAddons,
		queueToThread=ThreadTarget.GUI,
	)
	scheduleThread.scheduleDailyJobAtStartUp(
		showNewAddons,
		queueToThread=ThreadTarget.GUI,
	)

def showNewAddons():
	if AddonsAutomaticUpdate.NOTIFY == config.conf["addonStore"]["showNewAddons"]:
		wx.CallAfter(gui.mainFrame.onAddonStoreNewAddonsCommand, None)

