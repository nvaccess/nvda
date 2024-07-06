# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

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
