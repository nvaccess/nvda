# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2021 NV Access Limited, Bill Dengler, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""A module used to record Windows versions.
It is also used to define feature checks such as
making sure NVDA can run on a minimum supported version of Windows.
"""

import sys
import os
import functools
import winreg


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
			releaseName: str = "",
			servicePack: str = "",
			productType: str = ""
	):
		self.major = major
		self.minor = minor
		self.build = build
		self.releaseName = releaseName
		self.servicePack = servicePack
		self.productType = productType

	def _windowsVersionToReleaseName(self):
		"""Returns release names for a given Windows version if not defined.
		For example, 6.1 will return 'Windows 7'.
		For Windows 10, feature update release name will be included.
		On server systems, unless noted otherwise, client release names will be returned.
		For example, 'Windows 10 1809' will be returned on Server 2019 systems.
		"""
		if self.releaseName:
			return self.releaseName
		if (self.major, self.minor) == (6, 1):
			return "Windows 7"
		elif (self.major, self.minor) == (6, 2):
			return "Windows 8"
		elif (self.major, self.minor) == (6, 3):
			return "Windows 8.1"
		elif self.major == 10:
			# From Version 1511 (build 10586), release Id/display version comes from Windows Registry.
			# Always return "Windows 10 1507" on build 10240.
			if self.build == 10240:
				return "Windows 10 1507"
			with winreg.OpenKey(
				winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion"
			) as currentVersion:
				# Version 20H2 and later where a separate display version string is used.
				# For backward compatibility, release Id will store display version string.
				try:
					releaseId = winreg.QueryValueEx(currentVersion, "DisplayVersion")[0]
				except OSError:
					releaseId = None
				# Version 1511 and later unless display version string is present.
				if not releaseId:
					releaseId = winreg.QueryValueEx(currentVersion, "ReleaseID")[0]
			return f"Windows 10 {releaseId}"
		else:
			raise RuntimeError("Unknown Windows release")

	def __repr__(self):
		winVersionText = [self._windowsVersionToReleaseName()]
		winVersionText.append(f"({self.major}.{self.minor}.{self.build})")
		if self.servicePack != "":
			winVersionText.append(f"service pack {self.servicePack}")
		if self.productType != "":
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


# Windows releases to WinVersion instances for easing comparisons.
WIN7 = WinVersion(major=6, minor=1, build=7600, releaseName="Windows 7")
WIN7_SP1 = WinVersion(major=6, minor=1, build=7601, releaseName="Windows 7", servicePack="1")
WIN8 = WinVersion(major=6, minor=2, build=9200, releaseName="Windows 8")
WIN81 = WinVersion(major=6, minor=3, build=9600, releaseName="Windows 8.1")
WIN10 = WIN10_1507 = WinVersion(major=10, minor=0, build=10240, releaseName="Windows 10 1507")
WIN10_1511 = WinVersion(major=10, minor=0, build=10586, releaseName="Windows 10 1511")
WIN10_1607 = WinVersion(major=10, minor=0, build=14393, releaseName="Windows 10 1607")
WIN10_1703 = WinVersion(major=10, minor=0, build=15063, releaseName="Windows 10 1703")
WIN10_1709 = WinVersion(major=10, minor=0, build=16299, releaseName="Windows 10 1709")
WIN10_1803 = WinVersion(major=10, minor=0, build=17134, releaseName="Windows 10 1803")
WIN10_1809 = WinVersion(major=10, minor=0, build=17763, releaseName="Windows 10 1809")
WIN10_1903 = WinVersion(major=10, minor=0, build=18362, releaseName="Windows 10 1903")
WIN10_1909 = WinVersion(major=10, minor=0, build=18363, releaseName="Windows 10 1909")
WIN10_2004 = WinVersion(major=10, minor=0, build=19041, releaseName="Windows 10 2004")
WIN10_20H2 = WinVersion(major=10, minor=0, build=19042, releaseName="Windows 10 20H2")
WIN10_21H1 = WinVersion(major=10, minor=0, build=19043, releaseName="Windows 10 21H1")


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


UWP_OCR_DATA_PATH = os.path.expandvars(r"$windir\OCR")


def isUwpOcrAvailable():
	return os.path.isdir(UWP_OCR_DATA_PATH)


def isFullScreenMagnificationAvailable():
	return getWinVer() >= WIN8
