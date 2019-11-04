# vision/__init__.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Framework to facilitate changes in how content is displayed on screen.

One or more assistant functions can be implemented in vision enhancement providers.
Add-ons can provide their own provider
using modules in the visionEnhancementProviders package containing a L{VisionEnhancementProvider} class.
"""
from vision.providerInfo import ProviderInfo
from . import visionHandler
from .visionHandler import VisionHandler, getProviderClass
import visionEnhancementProviders
import config
from typing import List, Optional

handler: Optional[VisionHandler] = None


def initialize() -> None:
	global handler
	config.addConfigDirsToPythonPackagePath(visionEnhancementProviders)
	handler = VisionHandler()


def pumpAll() -> None:
	"""Runs tasks at the end of each core cycle."""
	if handler and handler.extensionPoints:
		handler.extensionPoints.post_coreCycle.notify()


def terminate() -> None:
	global handler
	handler.terminate()
	handler = None


def getProviderList(
		onlyStartable: bool = True
) -> List[ProviderInfo]:
	"""Gets a list of available vision enhancement providers
	@param onlyStartable: excludes all providers for which the check method returns C{False}.
	@return: Details of providers available
	"""
	return visionHandler.getProviderList(onlyStartable)


def _isDebug() -> bool:
	return config.conf["debugLog"]["vision"]
