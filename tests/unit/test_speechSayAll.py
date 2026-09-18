# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Unit tests for say all."""

import unittest
from unittest.mock import Mock, patch

from speech import sayAll


class TestReader(unittest.TestCase):
	@patch("speech.sayAll.systemUtils.preventSystemIdle")
	@patch.object(sayAll._CaretTextReader, "getInitialTextInfo", side_effect=NotImplementedError)
	def test_failedConstructionDoesNotPreventSystemIdle(
		self,
		getInitialTextInfo: Mock,
		preventSystemIdle: Mock,
	) -> None:
		with self.assertRaises(NotImplementedError):
			sayAll._CaretTextReader(Mock())

		preventSystemIdle.assert_not_called()
