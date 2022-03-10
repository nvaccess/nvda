# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import config
from dataclasses import dataclass
from enum import Enum
from functools import wraps
import globalVars
from typing import Callable
import ui
from gui.message import isModalMessageBoxActive


@dataclass
class _Context:
	blockActionIf: Callable[[], bool]
	translatedMessage: str


class Context(_Context, Enum):
	SECURE_MODE = (
		lambda: globalVars.appArgs.secure,
		# Translators: Reported when an action cannot be performed because NVDA is in a secure screen
		_("Action unavailable in secure context"),
	)
	WINDOWS_STORE_VERSION = (
		lambda: config.isAppX,
		# Translators: Reported when an action cannot be performed because NVDA has been installed
		# from the Windows Store.
		_("Action unavailable in NVDA Windows Store version"),
	)
	MODAL_DIALOG_OPEN = (
		isModalMessageBoxActive,
		# Translators: Reported when an action cannot be performed because NVDA is waiting
		# for a response from a modal dialog
		_("Action unavailable as an open dialog requires a response"),
	)


def when(*contexts: Context):
	"""Returns a function wrapper.
	A function decorated with `when` will exit early if any supplied context in `contexts` is active.

	For example, a function decorated with `@blockAction.when(blockAction.Context.SECURE_MODE)`
	will return without running if secure mode is active.
	"""
	def _wrap(func):
		@wraps(func)
		def funcWrapper(*args, **kwargs):
			for context in contexts:
				if context.blockActionIf():
					ui.message(context.translatedMessage)
					return
			return func(*args, **kwargs)
		return funcWrapper
	return _wrap
