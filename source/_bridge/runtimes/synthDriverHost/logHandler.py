# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations
import typing
import logging

if typing.TYPE_CHECKING:
	import extensionPoints


log = logging.getLogger()
log.debugWarning = log.debug


_onErrorSoundRequested: "extensionPoints.Action | None" = None


def getOnErrorSoundRequested() -> "extensionPoints.Action":
	"""Creates _onErrorSoundRequested extension point if needed (i.e. on first use only) and returns it."""

	global _onErrorSoundRequested

	import extensionPoints

	if not _onErrorSoundRequested:
		_onErrorSoundRequested = extensionPoints.Action()
	return _onErrorSoundRequested
