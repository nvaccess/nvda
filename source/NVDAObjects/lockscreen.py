# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited


from NVDAObjects import NVDAObject


class LockScreenObject(NVDAObject):
	"""
	Prevent users from object navigating outside of the lock screen.
	While usages of `api.objectBelowLockScreenAndWindowsIsLocked` prevent
	the user from moving to the object, this overlay class prevents reading neighbouring objects.
	"""

	def _get_next(self) -> NVDAObject | None:
		nextObject = super()._get_next()
		if nextObject and nextObject.appModule.appName == self.appModule.appName:
			return nextObject
		return None

	def _get_previous(self) -> NVDAObject | None:
		previousObject = super()._get_previous()
		if previousObject and previousObject.appModule.appName == self.appModule.appName:
			return previousObject
		return None

	def _get_parent(self) -> NVDAObject | None:
		parentObject = super()._get_parent()
		if parentObject and parentObject.appModule.appName == self.appModule.appName:
			return parentObject
		return None
