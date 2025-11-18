# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import ui

from .fullscreenMagnifier import FullScreenMagnifier

_nvdaMagnifier: FullScreenMagnifier | None = None
_zoomLevel: float = 2.0


def toggleMagnifier():
	"""Toggle the NVDA magnifier on/off
	"""
	global _nvdaMagnifier
	if _nvdaMagnifier and _nvdaMagnifier.isActive:
		_nvdaMagnifier._stopMagnifier()
		_nvdaMagnifier = None
		ui.message(
			_(
				# Translators: Message announced when starting the NVDA magnifier
				"Stopping NVDA Fullscreen magnifier"
			)
		)
	else:
		_nvdaMagnifier = FullScreenMagnifier(_zoomLevel)
		ui.message(
			_(
				# Translators: Message announced when starting the NVDA magnifier
				"Starting NVDA Fullscreen magnifier"
			)
		)


def zoomIn():
	"""Zoom in the Magnifier
	"""
	global _zoomLevel
	global _nvdaMagnifier
	if _nvdaMagnifier and _nvdaMagnifier.isActive:
		_nvdaMagnifier._zoom(True)
		ui.message(
			_(
				# Translators: Message announced when zooming out with {zoomLevel} being the target zoom level
				"Zooming in with {zoomLevel} level"
			).format(zoomLevel=_nvdaMagnifier.zoomLevel)
		)
		_zoomLevel = _nvdaMagnifier.zoomLevel
	else:
		return


def zoomOut():
	"""Zoom out the Magnifier
	"""
	global _zoomLevel
	global _nvdaMagnifier
	if _nvdaMagnifier and _nvdaMagnifier.isActive:
		_nvdaMagnifier._zoom(False)
		ui.message(
			_(
				# Translators: Message announced when zooming out with {zoomLevel} being the target zoom level
				"Zooming out with {zoomLevel} level"
			).format(zoomLevel=_nvdaMagnifier.zoomLevel)
		)
		_zoomLevel = _nvdaMagnifier.zoomLevel
	else:
		return
