#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2018 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import buildVersion
import re

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
#: Supports year.month.minor versions (e.g. 2018.1.1).
#: Resulting match objects expose three groups reflecting release year, release month, and release minor version,
# respectively.
#: @type: RegexObject
ADDON_API_VERSION_REGEX = re.compile(r"^(\d{4})\.(\d)\.(\d)$")

def getAPIVersionTupleFromString(version):
	"""Converts a string containing an NVDA version to a tuple of the form (versionYear, versionMajor, versionMinor)"""
	match = ADDON_API_VERSION_REGEX.match(version)
	if not match:
		raise ValueError(version)
	return tuple(int(i) if i is not None else 0 for i in match.groups())