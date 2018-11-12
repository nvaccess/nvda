#versionInfo.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""
This module contains localizable version information such as description, copyright and About messages etc.
As there are localizable strings at module level, this can only be imported once localization is set up via languageHandler.initialize.
To access version information for programmatic version checks before languageHandler.initialize, use the buildVersion module which contains all the non-localizable version information such as major and minor version, and version string etc.
"""

import os
from buildVersion import *
import re

longName=_("NonVisual Desktop Access")
description=_("A free and open source screen reader for Microsoft Windows")
url="http://www.nvaccess.org/"
copyrightYears="2006-2018"
copyright=_("Copyright (C) {years} NVDA Contributors").format(
	years=copyrightYears)
aboutMessage=_(u"""{longName} ({name})
Version: {version}
URL: {url}
{copyright}

{name} is covered by the GNU General Public License (Version 2). You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it. This applies to both original and modified copies of this software, plus any derivative works.
For further details, you can view the license from the Help menu.
It can also be viewed online at: http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

{name} is developed by NV Access, a non-profit organisation committed to helping and promoting free and open source solutions for blind and vision impaired people.
If you find NVDA useful and want it to continue to improve, please consider donating to NV Access. You can do this by selecting Donate from the NVDA menu.""").format(**globals())

#: Compiled regular expression to match an NVDA version string.
#: Supports year.month versions (e.g. 2018.1) and an additional suffix for bug fix releases (e.g. 2018.1.1).
#: It also matches against strings like 2018.1dev.
#: Resulting match objects expose three groups reflecting release year, release month, and optionally release minor version, respectively.
#: @type: RegexObject
NVDA_VERSION_REGEX = re.compile(r"(\d{4,4})\.(\d)(?:\.(\d))?")

def getNVDAVersionTupleFromString(version):
	"""Converts a string containing an NVDA version to a tuple of the form (versionYear, versionMajor, versionMinor)"""
	match = NVDA_VERSION_REGEX.match(version)
	if not match:
		raise ValueError(version)
	return tuple(int(i) if i is not None else 0 for i in match.groups())
