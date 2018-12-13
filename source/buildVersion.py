#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

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


def formatDevVersionString():
	return "%s.%s.%sdev"%(version_year,version_major,version_minor)

def getCurrentVersionTuple():
	return version_year, version_major, version_minor

# ticket:3763#comment:19: name must be str, not unicode.
# Otherwise, py2exe will break.
name="NVDA"
version_year=2019
version_major=1
version_minor=0
version_build=0
version=formatDevVersionString()
publisher="unknown"
updateVersionType=None
try:
	from _buildVersion import version, publisher, updateVersionType, version_build
except ImportError:
	_updateVersionFromVCS()

# A test version is anything other than a final or rc release.
isTestVersion = not version[0].isdigit() or "alpha" in version or "beta" in version or "dev" in version
