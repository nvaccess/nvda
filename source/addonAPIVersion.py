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
BACK_COMPAT_TO = (2022, 1, 0)
"""
As BACK_COMPAT_TO is incremented, the changed / removed parts / or reasoning should be added below.
These only serve to act as a reminder, the changelog should be consulted for a comprehensive listing.
EG: (x, y, z): Large changes to speech.py
---
(2022, 1, 0): various constants moved to enums, notably a controlTypes refactor.
(2021, 1, 0): wxPython 4.1.1, SayAll / Speech re-arranged, removal of previously deprecated code.
(2019, 3, 0): speech refactor, Python 3
(0, 0, 0): API version zero, used to signify addons released prior to API version checks.
"""

#: Compiled regular expression to match an addon API version string.
#: Supports year.major.minor versions (e.g. 2018.1.1).
# Although year and major are mandatory, minor is optional.
#: Resulting match objects expose three groups reflecting release year, release major, and release minor version,
# respectively.
# As minor is optional, the final group in the resulting match object may be None if minor is not provided in the original string. In this case it should be treated as being 0. 
#: @type: RegexObject
ADDON_API_VERSION_REGEX = re.compile(r"^(0|\d{4})\.(\d)(?:\.(\d))?$")

def getAPIVersionTupleFromString(version):
	"""Converts a string containing an NVDA version to a tuple of the form (versionYear, versionMajor, versionMinor)"""
	match = ADDON_API_VERSION_REGEX.match(version)
	if not match:
		raise ValueError(version)
	return tuple(int(i) if i is not None else 0 for i in match.groups())


def formatForGUI(versionTuple):
	"""Converts a version tuple to a string for displaying in the GUI
	Examples:
	- (2018, 1, 1) becomes "2018.1.1"
	- (2018, 1, 0) becomes "2018.1"
	- (0, 0, 0) becomes "0.0"
	"""
	try:
		year, major, minor = versionTuple
		return buildVersion.formatVersionForGUI(year, major, minor)
	except (
			ValueError,  # Too few/many values to unpack
			TypeError  # versionTuple is None or some other incorrect type
	):
		# This path should never be hit. But the appearance of "unknown" in the GUI is a better outcome
		# than an exception and unusable dialog.
		# Translators: shown when an addon API version string is unknown
		default = _("unknown")
		log.error("Unable to format versionTuple: {}".format(repr(versionTuple)), exc_info=True)
		return default
