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

from .constants import Role
from .visionHandler import VisionHandler, getProviderClass
import pkgutil
import visionEnhancementProviders
import config
from logHandler import log
from typing import List, Tuple


def initialize():
	global handler
	config.addConfigDirsToPythonPackagePath(visionEnhancementProviders)
	handler = VisionHandler()


def pumpAll():
	"""Runs tasks at the end of each core cycle."""
	if handler and handler.extensionPoints:
		handler.extensionPoints.post_coreCycle.notify()


def terminate():
	global handler
	handler.terminate()
	handler = None


def getProviderList(
		onlyStartable: bool = True
) -> List[Tuple[str, str, List[Role]]]:
	"""Gets a list of available vision enhancement names with their descriptions as well as supported roles.
	@param onlyStartable: excludes all providers for which the check method returns C{False}.
	@return: list of tuples with provider names, provider descriptions, and supported roles.
		See L{constants.Role} for the available roles.
	"""
	providerList = []
	for loader, name, isPkg in pkgutil.iter_modules(visionEnhancementProviders.__path__):
		if name.startswith('_'):
			continue
		try:
			provider = getProviderClass(name)
		except Exception:
			# Purposely catch everything.
			# A provider can raise whatever exception it likes,
			# therefore it is unknown what to expect.
			log.error(
				"Error while importing vision enhancement provider %s" % name,
				exc_info=True
			)
			continue
		try:
			if not onlyStartable or provider.canStart():
				providerList.append((
					provider.name,
					provider.description,
					list(provider.supportedRoles)
				))
			else:
				log.debugWarning("Vision enhancement provider %s reports as unable to start, excluding" % provider.name)
		except Exception:
			# Purposely catch everything else as we don't want one failing provider
			# make it impossible to list all the others.
			log.error("", exc_info=True)
	# Sort the providers alphabetically by name.
	providerList.sort(key=lambda d: d[1].lower())
	return providerList


def _isDebug() -> bool:
	return config.conf["debugLog"]["vision"]
