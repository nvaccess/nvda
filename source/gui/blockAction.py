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
import queueHandler


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
		_("Action unavailable while a dialog requires a response"),
	)


def when(*contexts: Context):
	"""Returns a function wrapper.
	A function decorated with `when` will exit early if any supplied context in `contexts` is active.
	The first supplied context to block will be reported as a message.
	Consider supplying permanent conditions first.

	For example, to block a function when a modal dialog is open (a temporary condition)
	and in the Windows Store version (per installation), decorate it with
	`@blockAction.when(blockAction.Context.WINDOWS_STORE_VERSION, blockAction.Context.MODAL_DIALOG_OPEN)`.
	"""
	def _wrap(func):
		@wraps(func)
		def funcWrapper(*args, **kwargs):
			for context in contexts:
				if context.blockActionIf():
					queueHandler.queueFunction(queueHandler.eventQueue, ui.message, context.translatedMessage)
					return
			return func(*args, **kwargs)
		return funcWrapper
	return _wrap
