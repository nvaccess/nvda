# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os

"""
This module contains non-localizable version information for NVDA such as the version string and major and minor numbers etc.
Any localizable version information should be placed in the versionInfo module, not this one.
This module exists separately so that it can be imported for version checks before localization is initialized.
"""


def _updateVersionFromVCS():
	"""Update the version from version control system metadata if possible."""
	global version
	# The root of the Git working tree will be the parent of this module's directory.
	gitDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".git")
	try:
		with open(os.path.join(gitDir, "HEAD"), "r") as f:
			head = f.read().rstrip()
		if not head.startswith("ref: "):
			# Detached head.
			version = "source-DETACHED-%s" % head[:7]  # noqa: UP031
			return
		# Strip the "ref: " prefix to get the ref.
		ref = head[5:]
		with open(os.path.join(gitDir, ref), "r") as f:
			commit = f.read().rstrip()
		version = f"source-{os.path.basename(ref)}-{commit[:7]}"
	except:  # noqa: E722, S110
		pass


def _formatDevVersionString():
	return f"{version_year}.{version_major}.{version_minor}dev"


def formatBuildVersionString():
	"""Formats a full version string, from the values in the buildVersion module.
	Examples:
	- "2019.1.0.123"
	"""
	return f"{version_year}.{version_major}.{version_minor}.{version_build}"


def formatVersionForGUI(year, major, minor):
	"""Converts three version numbers to a string for displaying in the GUI.
	Examples:
	- (2018, 1, 1) becomes "2018.1.1"
	- (2018, 1, 0) becomes "2018.1"
	- (0, 0, 0) becomes "0.0"
	"""
	if None in (year, major, minor):
		raise ValueError(
			f"Three values must be provided. Got year={year}, major={major}, minor={minor}",
		)
	if minor == 0:
		return f"{year}.{major}"
	return f"{year}.{major}.{minor}"


# Version information for NVDA
name = "NVDA"
version_year = 2027
version_major = 1
version_minor = 0
version_build = 0  # Should not be set manually. Set in 'sconscript'.
version = _formatDevVersionString()
publisher = "unknown"
copyrightYears = "2006-2027"
url = "https://www.nvaccess.org"
updateVersionType = None
try:
	from _buildVersion import version, publisher, updateVersionType, version_build  # type: ignore[reportMissingModuleSource]  # noqa: F401, I001
except ImportError:
	_updateVersionFromVCS()

version_detailed = formatBuildVersionString()
# A test version is anything other than a final or rc release.
isTestVersion = not version[0].isdigit() or "alpha" in version or "beta" in version or "dev" in version
