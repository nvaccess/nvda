#versionInfo.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2011 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os

def _updateVersionFromVCS():
	"""Update the version from version control system metadata if possible.
	"""
	global version
	# The root of the bzr working tree will be the parent of this module's directory.
	branchPath = os.path.dirname(os.path.dirname(__file__))
	locationPath = os.path.join(branchPath, ".bzr", "branch", "location")
	try:
		# If this is a lightweight checkout of a local branch, use that branch.
		branchPath = file(locationPath, "r").read().split("file:///", 1)[1]
	except (IOError, IndexError):
		pass

	lastRevPath = os.path.join(branchPath, ".bzr", "branch", "last-revision")
	try:
		# If running from a bzr branch, use version info from that.
		rev = file(lastRevPath, "r").read().split(" ")[0]
		branch = os.path.basename(os.path.abspath(branchPath))
		version = "bzr-%s-%s" % (branch, rev)
	except (IOError, IndexError):
		pass

name="NVDA"
longName=_("NonVisual Desktop Access")
version="2011.2dev"
try:
	from _buildVersion import version
except ImportError:
	_updateVersionFromVCS()
description=_("A free and open source screen reader for Microsoft Windows")
url="http://www.nvda-project.org/"
copyright=_("Copyright (C) 2006-2011 NVDA Contributors")
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
