#versionInfo.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2015 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os

def _updateVersionFromVCS():
	"""Update the version from version control system metadata if possible.
	"""
	global version
	# The root of the Git working tree will be the parent of this module's directory.
	gitDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".git")
	try:
		head = file(os.path.join(gitDir, "HEAD"), "r").read().rstrip()
		if not head.startswith("ref: "):
			# Detached head.
			version = "source-DETACHED-%s" % head[:7]
			return
		# Strip the "ref: " prefix to get the ref.
		ref = head[5:]
		commit = file(os.path.join(gitDir, ref), "r").read().rstrip()
		version = "source-%s-%s" % (
			os.path.basename(ref),
			commit[:7])
	except:
		pass

# ticket:3763#comment:19: name must be str, not unicode.
# Otherwise, py2exe will break.
name="NVDA"
longName=_("NonVisual Desktop Access")
version="2016.1dev"
publisher="unknown"
updateVersionType=None
try:
	from _buildVersion import version, publisher, updateVersionType
except ImportError:
	_updateVersionFromVCS()
description=_("A free and open source screen reader for Microsoft Windows")
url="http://www.nvaccess.org/"
copyrightYears="2006-2015"
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

# A test version is anything other than a final or rc release.
isTestVersion = not version[0].isdigit() or "alpha" in version or "beta" in version or "dev" in version
