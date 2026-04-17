# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for secret redaction in the logHandler module."""

import contextlib
import logging
import types
import unittest
from unittest import mock

import logHandler


class TestLoggerSecretRedaction(unittest.TestCase):
	def setUp(self):
		self.logger = logHandler.Logger("testLogHandler")
		self.logger.secretDetectionSettings = contextlib.nullcontext()

	def test_logWithoutRedactionPassesMessageAndArgsThrough(self):
		with mock.patch.object(logging.Logger, "_log") as superLog, mock.patch.object(logHandler, "scan_line") as scanLine:
			self.logger._log(
				logging.INFO,
				"api key %s",
				("secret-value",),
				codepath="tests.unit.test_logHandler",
			)

		scanLine.assert_not_called()
		superLog.assert_called_once_with(
			logging.INFO,
			"api key %s",
			("secret-value",),
			None,
			{"codepath": "tests.unit.test_logHandler"},
		)

	def test_logWithRedactionMasksDetectedSecrets(self):
		secret = types.SimpleNamespace(secret_value="secret-value")

		with mock.patch.object(logging.Logger, "_log") as superLog, mock.patch.object(
			logHandler,
			"scan_line",
			return_value=[secret],
		) as scanLine:
			self.logger._log(
				logging.INFO,
				"api key %s and again %s",
				("secret-value", "secret-value"),
				codepath="tests.unit.test_logHandler",
				redactSecrets=True,
			)

		scanLine.assert_called_once_with("api key secret-value and again secret-value")
		superLog.assert_called_once_with(
			logging.INFO,
			"api key **** and again ****",
			(),
			None,
			{"codepath": "tests.unit.test_logHandler"},
		)

	def test_logWithRedactionFallsBackWhenFormattingFails(self):
		with mock.patch.object(logging.Logger, "_log") as superLog, mock.patch.object(
			logHandler,
			"scan_line",
			return_value=[],
			) as scanLine, mock.patch.object(self.logger, "exception") as logException:
			self.logger._log(
				logging.INFO,
				"expected int %d",
				("not-an-int",),
				codepath="tests.unit.test_logHandler",
				redactSecrets=True,
			)

		logException.assert_called_once_with(
			"Failed to format log message for secret redaction, logging unredacted exception.",
		)
		scanLine.assert_called_once_with("expected int %d")
		superLog.assert_called_once_with(
			logging.INFO,
			"expected int %d",
			(),
			None,
			{"codepath": "tests.unit.test_logHandler"},
		)
