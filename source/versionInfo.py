#versionInfo.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from __future__ import with_statement
import os

SVN_ENTRIES_PATH = r".svn\entries"
BZR_LASTREV_PATH = r"..\.bzr\branch\last-revision"

def _updateVersionFromVCS():
	"""Update the version from version control system metadata if possible.
	"""
	global version
	if os.path.isfile(SVN_ENTRIES_PATH):
		# Running from svn checkout.
		try:
			f = file(SVN_ENTRIES_PATH, "r")
			# The revision number is on the fourth line.
			for ln in xrange(4):
				rev = f.readline()
			rev = rev.strip()
			# URL is on the next line.
			branch = f.readline().split("/")[-2]
			version = "%s-r%s" % (branch, rev)
		except (IOError, IndexError):
			pass
	elif os.path.isfile(BZR_LASTREV_PATH):
		# Running from bzr checkout.
		try:
			rev = file(BZR_LASTREV_PATH, "r").read().split(" ")[0]
			branch = os.path.basename(os.path.abspath(".."))
			version = "bzr-%s-%s" % (branch, rev)
		except (IOError, IndexError):
			pass

name="NVDA"
longName=_("NonVisual Desktop Access")
version="unknown"
description=_("A free and open-source screen reader for MS Windows")
url="http://www.nvda-project.org/"
copyright=_("Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>")
copyrightInfo=_("""%(copyright)s
%(name)s is covered by the GNU General Public License (Version 2). You are free to share or change this software in any way you like as long as you distribute the licence along with the software, and make all source code available to anyone who wants it. This applies to both origional and modified copies of the software, plus any software that uses code taken from this software.
For further details, you can view the licence online at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
Or see the file Copying.txt that came with this software.""")%globals()

_updateVersionFromVCS()
