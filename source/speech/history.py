# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Speech history implementation."""

from __future__ import annotations

from .commands import CallbackCommand, _CancellableSpeechCommand
from .types import SpeechSequence
from .priorities import Spri

import typing

if typing.TYPE_CHECKING:
	from characterProcessing import SymbolLevel


speechHistoryBuffer: SpeechHistoryBuffer | None = None


class SpeechHistoryItem:
	def __init__(self, seq: SpeechSequence, symbLevel: "SymbolLevel" | None):
		if not any(isinstance(item, str) for item in seq):
			raise ValueError("The speech sequence does not contain any speech")
		self.seq = [
			item for item in seq if not isinstance(item, (CallbackCommand, _CancellableSpeechCommand))
		]
		self.symbLevel = symbLevel

	@property
	def text(self):
		return "  ".join(i for i in self.seq if isinstance(i, str))


class SpeechHistoryBuffer:
	def __init__(self):
		self.items: list[SpeechHistoryItem] = []
		self.reviewPosition = None

	def lastSpeechItem(self):
		if self.items:
			return self.items[-1]
		return None

	def addSequence(
		self,
		speechSequence: SpeechSequence,
		symbolLevel: "SymbolLevel" | None,
		priority: Spri,
	) -> None:
		import config
		from scriptHandler import getCurrentScript, getLastScriptRepeatCount
		from globalCommands import GlobalCommands

		if (
			getCurrentScript() == GlobalCommands.script_repeatLastSpokenInformation
			and getLastScriptRepeatCount() == 0
		) or getCurrentScript() in [
			GlobalCommands.script_reviewPreviousItemInSpeechHistory,
			GlobalCommands.script_reviewNextItemInSpeechHistory,
			GlobalCommands.script_copyCurrentlyReviewedSpeechHistoryItem,
		]:
			# When calling the scripts to repeat last speech (first call), review it or copy it, we do not store their
			# speech output
			return
		try:
			item = SpeechHistoryItem(speechSequence, symbolLevel)
		except ValueError:
			# Ignore speech sequences that do not contain speech
			return
		if config.conf["coreSpeechHistory"]["enabled"]:
			maxSpeechBufferLength = config.conf["coreSpeechHistory"]["maxSize"]
		else:
			maxSpeechBufferLength = 1
		if len(self.items) >= maxSpeechBufferLength:
			del self.items[0]
		self.items.append(item)
		self.reviewPosition = len(self.items) - 1

	def clearSpeechHistory(self, reportConfirmation=False):
		import ui

		self.items.clear()
		self.reviewPosition = None
		if reportConfirmation:
			# Translators: The message reported when clearing the speech history
			ui.message(_("Speech history cleared"))

	def reviewPrevious(self):
		if self.reviewPosition is None or self.reviewPosition == 0:
			raise LookupError()
		self.reviewPosition -= 1
		return self.currentReviewItem()

	def reviewNext(self):
		if self.reviewPosition is None or self.reviewPosition == len(self.items) - 1:
			raise LookupError()
		self.reviewPosition += 1
		return self.currentReviewItem()

	def currentReviewItem(self):
		if self.reviewPosition is None:
			raise LookupError()
		return self.items[self.reviewPosition]


def initialize():
	global speechHistoryBuffer
	speechHistoryBuffer = SpeechHistoryBuffer()
