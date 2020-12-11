# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2020 NV Access Limited, Bill Dengler, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""A module used to record Windows versions.
It is also used to define feature checks such as
making sure NVDA can run on a minimum supported version of Windows.
"""

import sys
import os
import functools
import winUser

winVersion=sys.getwindowsversion()
winVersionText="{v.major}.{v.minor}.{v.build}".format(v=winVersion)
if winVersion.service_pack_major!=0:
	winVersionText+=" service pack %d"%winVersion.service_pack_major
	if winVersion.service_pack_minor!=0:
		winVersionText+=".%d"%winVersion.service_pack_minor
winVersionText+=" %s" % ("workstation","domain controller","server")[winVersion.product_type-1]


@functools.total_ordering
class WinVersion(object):
	"""
	Represents a Windows release.
	Includes version major, minor, build, service pack information,
	as well as tools such as checking for specific Windows 10 releases.
	"""

	def __init__(
			self,
			release: str = None,
			major: int = 0,
			minor: int = 0,
			build: int = 0,
			servicePack: str = ""
	):
		if release in (None, ""):
			self.major = major
			self.minor = minor
			self.build = build
		elif release == "7":
			self.major = 6
			self.minor = 1
			self.build = 7601
		elif release == "8":
			self.major = 6
			self.minor = 2
			self.build = 9200
		elif release == "8.1":
			self.major = 6
			self.minor = 3
			self.build = 9600
		elif release in ("10", "1507"):
			self.major = 10
			self.minor = 0
			self.build = 10240
		elif release in WIN10_VERSIONS_TO_BUILDS:
			self.major = 10
			self.minor = 0
			self.build = WIN10_VERSIONS_TO_BUILDS[release]
		else:
			raise ValueError("Cannot create Windows version information for the specified release")
		self.servicePack = "1" if release == "7" else ""

	def __eq__(self, other):
		return (
			(self.major, self.minor, self.build)
			== (other.major, other.minor, other.build)
		)

	def __ge__(self, other):
		return (
			(self.major, self.minor, self.build)
			>= (other.major, other.minor, other.build)
		)

	def isWin10(self, release: str = "1507", atLeast: bool = True):
		"""
		Returns True if NVDA is running on the supplied release version of Windows 10.
		If no argument is supplied, returns True for all public Windows 10 releases.
		@param release: a release version of Windows 10 (such as 1903).
		@param atLeast: return True if NVDA is running on at least this Windows 10 build
		(i.e. this version or higher).
		"""
		if self.major != 10:
			return False
		# #11795: special cases.
		# Remove this workaround in a future API compatibility (year.1) release.
		# October 2020 Update is 20H2, not 2009.
		if release == "2009":
			release = "20H2"
		if release not in WIN10_VERSIONS_TO_BUILDS:
			raise ValueError(f"Unknown Windows 10 release {release}")
		if atLeast:
			return self.build >= WIN10_VERSIONS_TO_BUILDS[release]
		else:
			return self.build > WIN10_VERSIONS_TO_BUILDS[release]


# Windows releases to WinVersion instances for easing comparisons.
WIN7 = WinVersion(major=6, minor=1, build=7600)
WIN7_SP1 = WinVersion(major=6, minor=1, build=7601, servicePack="1")
WIN8 = WinVersion(major=6, minor=2, build=9200)
WIN81 = WinVersion(major=6, minor=3, build=9600)
WIN10 = WIN10_1507 = WinVersion(major=10, minor=0, build=10240)
WIN10_1511 = WinVersion(major=10, minor=0, build=10586)
WIN10_1607 = WinVersion(major=10, minor=0, build=14393)
WIN10_1703 = WinVersion(major=10, minor=0, build=15063)
WIN10_1709 = WinVersion(major=10, minor=0, build=16299)
WIN10_1803 = WinVersion(major=10, minor=0, build=17134)
WIN10_1809 = WinVersion(major=10, minor=0, build=17763)
WIN10_1903 = WinVersion(major=10, minor=0, build=18362)
WIN10_1909 = WinVersion(major=10, minor=0, build=18363)
WIN10_2004 = WinVersion(major=10, minor=0, build=19041)
WIN10_20H2 = WinVersion(major=10, minor=0, build=19042)


def getWinVer():
	winVer = sys.getwindowsversion()
	return WinVersion(
		major=winVer.major,
		minor=winVer.minor,
		build=winVer.build,
		servicePack=winVer.service_pack
	)


def getWinVerFromVersionText(versionText: str):
	major, minor, build = versionText.split(".")
	return WinVersion(
		major=int(major),
		minor=int(minor),
		build=int(build)
	)

def isSupportedOS():
	# NVDA can only run on Windows 7 Service pack 1 and above
	return (winVersion.major,winVersion.minor,winVersion.service_pack_major) >= (6,1,1)

def canRunVc2010Builds():
	return isSupportedOS()

UWP_OCR_DATA_PATH = os.path.expandvars(r"$windir\OCR")
def isUwpOcrAvailable():
	return os.path.isdir(UWP_OCR_DATA_PATH)


WIN10_VERSIONS_TO_BUILDS = {
	"1507": 10240,
	"1511": 10586,
	"1607": 14393,
	"1703": 15063,
	"1709": 16299,
	"1803": 17134,
	"1809": 17763,
	"1903": 18362,
	"1909": 18363,
	"2004": 19041,
	"20H2": 19042,
}


def isWin10(version: int = 1507, atLeast: bool = True):
	"""
	@deprecated: use getWinVer().isWin10 instead.
	Returns True if NVDA is running on the supplied release version of Windows 10. If no argument is supplied, returns True for all public Windows 10 releases.
	@param version: a release version of Windows 10 (such as 1903).
	@param atLeast: return True if NVDA is running on at least this Windows 10 build (i.e. this version or higher).
	"""
	return getWinVer().isWin10(release=str(version), atLeast=atLeast)

def isFullScreenMagnificationAvailable():
	return (winVersion.major, winVersion.minor) >= (6, 2)
