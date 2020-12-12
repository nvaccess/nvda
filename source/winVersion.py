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


@functools.total_ordering
class WinVersion(object):
	"""
	Represents a Windows release.
	Includes version major, minor, build, service pack information,
	as well as tools such as checking for specific Windows 10 releases.
	"""

	def __init__(
			self,
			major: int = 0,
			minor: int = 0,
			build: int = 0,
			servicePack: str = "",
			productType: str = ""
	):
		self.major = major
		self.minor = minor
		self.build = build
		self.servicePack = servicePack
		self.productType = productType

	def _windowsVersionToReleaseName(self):
		"""Returns release names for a given Windows version.
		For example, 6.1 will return 'Windows 7'.
		For Windows 10, feature update release name will be included.
		On server systems, client release names will be returned.
		For example, 'Windows 10 1809' will be returned on Server 2019 systems.
		"""
		if (self.major, self.minor) == (6, 1):
			return "Windows 7"
		elif (self.major, self.minor) == (6, 2):
			return "Windows 8"
		elif (self.major, self.minor) == (6, 3):
			return "Windows 8.1"
		elif self.major == 10:
			buildsToReleases = {build: release for release, build in WIN10_RELEASE_NAME_TO_BUILDS.items()}
			if self.build in buildsToReleases:
				return f"Windows 10 {buildsToReleases[self.build]}"
			else:
				# Windows Insider build.
				return "Windows 10 prerelease"
		else:
			raise RuntimeError("Unknown Windows release")

	def __repr__(self):
		winVersionText = [self._windowsVersionToReleaseName()]
		winVersionText.append(f"({self.major}.{self.minor}.{self.build})")
		if self.servicePack != "":
			winVersionText.append(f"service pack {self.servicePack}")
		winVersionText.append(self.productType)
		return " ".join(winVersionText)

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

	@staticmethod
	def fromReleaseName(release: str, servicePack: str = ""):
		"""Returns Windows version information based on release name.
		For example, 6.2.9200 for '8'.
		Versions other than 7 do not come with service packs.
		On Windows 10, pass in either '10' or the string representing a specific Windows 10 release.
		For example, '20H2' will return Windows version 10.0.19042.
		"""
		if release == "7":
			return WIN7 if servicePack == "" else WIN7_SP1
		elif release == "8":
			return WIN8
		elif release == "8.1":
			return WIN81
		elif release in ("10", "1507"):
			return WIN10
		elif release in WIN10_RELEASE_NAME_TO_BUILDS:
			return WinVersion(
				major=10,
				minor=0,
				build=WIN10_RELEASE_NAME_TO_BUILDS[release]
			)
		else:
			raise ValueError(f"Cannot create Windows version information for the specified release: {release}")

	@staticmethod
	def fromVersionText(versionText: str):
		"""Returns a Windows version information based on version string
		of the form major.minor.build.
		"""
		major, minor, build = versionText.split(".")
		# Specifically for Windows 7 service pack 1.
		servicePack = "1" if versionText == "6.1.7601" else ""
		return WinVersion(
			major=int(major),
			minor=int(minor),
			build=int(build),
			servicePack=servicePack
		)


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
	"""Returns a record of current Windows version NVDA is running on.
	"""
	winVer = sys.getwindowsversion()
	return WinVersion(
		major=winVer.major,
		minor=winVer.minor,
		build=winVer.build,
		servicePack=winVer.service_pack,
		productType=("workstation", "domain controller", "server")[winVer.product_type - 1]
	)


def isSupportedOS():
	# NVDA can only run on Windows 7 Service pack 1 and above
	return getWinVer() >= WIN7_SP1

def canRunVc2010Builds():
	return isSupportedOS()

UWP_OCR_DATA_PATH = os.path.expandvars(r"$windir\OCR")
def isUwpOcrAvailable():
	return os.path.isdir(UWP_OCR_DATA_PATH)


WIN10_RELEASE_NAME_TO_BUILDS = {
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


def isFullScreenMagnificationAvailable():
	return getWinVer() >= WIN8
