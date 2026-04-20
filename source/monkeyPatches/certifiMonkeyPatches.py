# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
import sys


def _getBundledCaCertPath() -> str:
	return os.path.join(os.path.dirname(sys.executable), "cacert.pem")


def apply() -> None:
	"""Make certifi use the bundled CA bundle in frozen builds."""
	if getattr(sys, "frozen", None) is None:
		return
	bundledCaCertPath = _getBundledCaCertPath()
	if not os.path.isfile(bundledCaCertPath):
		return

	import certifi
	import certifi.core

	def where() -> str:
		return bundledCaCertPath

	def contents() -> str:
		with open(bundledCaCertPath, "r", encoding="ascii") as certFile:
			return certFile.read()

	certifi.where = where
	certifi.contents = contents
	certifi.core.where = where
	certifi.core.contents = contents
