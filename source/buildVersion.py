# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os

"""
This module contains non-localizable version information for NVDA such as the version string and major and minor numbers etc.
Any localizable version information should be placed in the versionInfo module, not this one.
This module exists separately so that it can be imported for version checks before localization is initialized.
"""

def _updateVersionFromVCS():
	"""Update the version from version control system metadata if possible.
	"""
	global version
	# The root of the Git working tree will be the parent of this module's directory.
	gitDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".git")
	try:
		with open(os.path.join(gitDir, "HEAD"), "r") as f:
			head = f.read().rstrip()
		if not head.startswith("ref: "):
			# Detached head.
			version = "source-DETACHED-%s" % head[:7]
			return
		# Strip the "ref: " prefix to get the ref.
		ref = head[5:]
		with open(os.path.join(gitDir, ref), "r") as f:
			commit = f.read().rstrip()
		version = "source-%s-%s" % (
			os.path.basename(ref),
			commit[:7])
	except:
		pass


def _formatDevVersionString():
	return "{y}.{M}.{m}dev".format(y=version_year, M=version_major, m=version_minor)


def formatBuildVersionString():
	"""Formats a full version string, from the values in the buildVersion module.
	Examples:
	- "2019.1.0.123"
	"""
	return "{y}.{M}.{m}.{b}".format(y=version_year, M=version_major, m=version_minor, b=version_build)


def formatVersionForGUI(year, major, minor):
	"""Converts three version numbers to a string for displaying in the GUI.
	Examples:
	- (2018, 1, 1) becomes "2018.1.1"
	- (2018, 1, 0) becomes "2018.1"
	- (0, 0, 0) becomes "0.0"
	"""
	if None in (year, major, minor):
		raise ValueError(
			"Three values must be provided. Got year={}, major={}, minor={}".format(year, major, minor)
		)
	if minor == 0:
		return "{y}.{M}".format(y=year, M=major)
	return "{y}.{M}.{m}".format(y=year, M=major, m=minor)


# Version information for NVDA
name = "NVDA"
version_year = 2022
version_major = 2
version_minor = 0
version_build = 0  # Should not be set manually. Set in 'sconscript' provided by 'appVeyor.yml'
version=_formatDevVersionString()
publisher="unknown"
updateVersionType=None
try:
	from _buildVersion import version, publisher, updateVersionType, version_build
except ImportError:
	_updateVersionFromVCS()

# A test version is anything other than a final or rc release.
isTestVersion = not version[0].isdigit() or "alpha" in version or "beta" in version or "dev" in version
