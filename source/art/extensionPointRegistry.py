# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import Any, Dict

from logHandler import log


def registerExtensionPoints() -> None:
	"""Register all known NVDA extension points with their names for ART integration."""
	try:
		import config
		import inputCore

		extensionPointMappings: Dict[Any, str] = {
			config.post_configProfileSwitch: "config.post_configProfileSwitch",
			config.pre_configProfileSwitch: "config.pre_configProfileSwitch",
			config.configProfileSwitched: "config.configProfileSwitched",
			inputCore.decide_executeGesture: "inputCore.decide_executeGesture",
		}

		for extPoint, name in extensionPointMappings.items():
			if hasattr(extPoint, "_extensionPointName"):
				extPoint._extensionPointName = name
				log.debug(f"Registered extension point: {name}")
			else:
				log.warning(f"Extension point {name} does not support ART integration")

		log.info(f"Registered {len(extensionPointMappings)} extension points for ART integration")

	except Exception:
		log.exception("Error registering extension points for ART")
