#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2018 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import buildVersion
import re
from logHandler import log

"""
This module contains add-on API version information for this build of NVDA. This file provides information on
how the API has changed as well as the range of API versions supported by this build of NVDA
"""

CURRENT = (buildVersion.version_year, buildVersion.version_major, buildVersion.version_minor)
BACK_COMPAT_TO = (0, 0, 0)
"""
As BACK_COMPAT_TO is incremented, the changed / removed parts / or reasoning should be added below.
EG: (x, y, z): Large changes to speech.py
---
(0, 0, 0): API version zero, used to signify addons released prior to API version checks.
"""

#: Compiled regular expression to match an addon API version string.
#: Supports year.major.minor versions (e.g. 2018.1.1).
#: Resulting match objects expose three groups reflecting release year, release major, and release minor version,
# respectively.
#: @type: RegexObject
ADDON_API_VERSION_REGEX = re.compile(r"^(0|\d{4})\.(\d)\.(\d)$")


def getAPIVersionTupleFromString(version):
	"""Converts a string containing an NVDA version to a tuple of the form (versionYear, versionMajor, versionMinor)"""
	match = ADDON_API_VERSION_REGEX.match(version)
	if not match:
		raise ValueError(version)
	return tuple(int(i) if i is not None else 0 for i in match.groups())


def formatAsString(versionTuple):
	"""Converts an API version tuple as a string for displaying in the GUI
	Examples:
	- (2018, 1, 1) becomes "2018.1.1"
	- (2018, 1, 0) becomes "2018.1"
	- (0, 0, 0) becomes "0.0"
	"""
	# Translators: shown when an addon API version string is unknown
	default = _("unknown")
	if not versionTuple:
		return default
	try:
		year, major, minor = versionTuple
		if minor is 0:
			return "{y}.{M}".format(y=year, M=major)
		return "{y}.{M}.{m}".format(y=year, M=major, m=minor)
	except:
		log.debug("Error formatting versionTuple: {}".format(repr(versionTuple)), exc_info=True)
		return default
