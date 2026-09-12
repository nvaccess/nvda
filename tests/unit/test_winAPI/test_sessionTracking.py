# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import unittest
from unittest import mock

from winAPI import sessionTracking
from winAPI._wtsApi32 import WTS_LockState


class TestIsWindowsLockedCheckViaSessionQuery(unittest.TestCase):
	def test_unknownLockState_isTreatedAsUnlockedAndLoggedOnce(self):
		with (
			mock.patch.object(sessionTracking, "_loggedSessionQueryFailures", set()),
			mock.patch.object(
				sessionTracking,
				"_getSessionLockedValue",
				return_value=WTS_LockState.WTS_SESSIONSTATE_UNKNOWN,
			),
			mock.patch.object(sessionTracking.log, "error") as logError,
		):
			self.assertFalse(sessionTracking._isWindowsLocked_checkViaSessionQuery())
			self.assertFalse(sessionTracking._isWindowsLocked_checkViaSessionQuery())

			logError.assert_called_once_with(
				f"Unable to determine lock state via Session Query. "
				f"Lock state value: {WTS_LockState.WTS_SESSIONSTATE_UNKNOWN!r}",
				exc_info=False,
			)

	def test_queryFailure_isTreatedAsUnlockedAndLoggedOnce(self):
		with (
			mock.patch.object(sessionTracking, "_loggedSessionQueryFailures", set()),
			mock.patch.object(sessionTracking, "WTSQuerySessionInformation", return_value=False),
			mock.patch.object(sessionTracking, "WTSFreeMemory"),
			mock.patch.object(sessionTracking.log, "error") as logError,
		):
			self.assertFalse(sessionTracking._isWindowsLocked_checkViaSessionQuery())
			self.assertFalse(sessionTracking._isWindowsLocked_checkViaSessionQuery())

			logError.assert_called_once_with("Failure querying session locked state", exc_info=True)

	def test_distinctFailuresAreEachLoggedOnce(self):
		with (
			mock.patch.object(sessionTracking, "_loggedSessionQueryFailures", set()),
			mock.patch.object(sessionTracking.log, "error") as logError,
		):
			sessionTracking._logSessionQueryFailureOnce("query failed", excInfo=True)
			sessionTracking._logSessionQueryFailureOnce("unknown state")
			sessionTracking._logSessionQueryFailureOnce("query failed", excInfo=True)

		self.assertEqual(
			[
				mock.call("query failed", exc_info=True),
				mock.call("unknown state", exc_info=False),
			],
			logError.call_args_list,
		)

	def test_queryFailurePreservesSpecificError(self):
		with (
			mock.patch.object(sessionTracking, "WTSQuerySessionInformation", return_value=False),
			mock.patch.object(sessionTracking, "WTSFreeMemory"),
			self.assertRaisesRegex(
				RuntimeError,
				"Failure calling WTSQuerySessionInformationW",
			),
		):
			sessionTracking._getCurrentSessionInfoEx()
