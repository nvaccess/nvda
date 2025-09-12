# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from logHandler import log

from .imageDescriber import ImageDescriber
from . import modelConfig

_localCaptioner: ImageDescriber | None = None


def initialize():
	"""Initialise the local captioner."""
	global _localCaptioner
	log.debug("Initializing local captioner")
	modelConfig.initialize()
	_localCaptioner = ImageDescriber()


def terminate():
	"""Terminate the local captioner."""
	global _localCaptioner
	if _localCaptioner is None:
		log.error("local captioner not running")
		return
	log.debug("Terminating local captioner")
	_localCaptioner.terminate()
	_localCaptioner = None


def isModelLoaded() -> bool:
	"""return if model is loaded"""
	if _localCaptioner is not None:
		return _localCaptioner.isModelLoaded
	else:
		return False


def toggleImageCaptioning() -> None:
	"""do load/unload the model from memory."""
	if _localCaptioner is not None:
		_localCaptioner.toggleSwitch()
