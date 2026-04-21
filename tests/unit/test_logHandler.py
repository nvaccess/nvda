# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for secret redaction in the logHandler module."""

import logging
import types
import unittest
from unittest import mock

import logHandler


class TestLoggerSecretRedaction(unittest.TestCase):
	def setUp(self):
		self.logger = logHandler.Logger("testLogHandler")
		self.logger.setLevel(logging.NOTSET)
		self.logger.parent = None

	def test_logWithoutRedactionPassesMessageAndArgsThrough(self):
		with (
			mock.patch.object(logging.Logger, "_log") as superLog,
			mock.patch("detect_secrets.core.scan.scan_line") as scanLine,
		):
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

		with (
			mock.patch.object(logging.Logger, "_log") as superLog,
			mock.patch(
				"detect_secrets.core.scan.scan_line",
				return_value=[secret],
			) as scanLine,
		):
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
		with (
			mock.patch.object(logging.Logger, "_log") as superLog,
			mock.patch(
				"detect_secrets.core.scan.scan_line",
				return_value=[],
			) as scanLine,
			mock.patch.object(self.logger, "exception") as logException,
		):
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

	def test_logWithRealDetectSecretsMasksHash(self):
		with mock.patch.object(logging.Logger, "_log") as superLog:
			self.logger._log(
				logging.INFO,
				"Config loaded: %s",
				("{'key': '86851a5bab3f33abc2858eca0922c34c34c38f0a'}",),
				codepath="tests.unit.test_logHandler",
				redactSecrets=True,
			)

		loggedMsg = superLog.call_args.args[1]
		self.assertIn("****", loggedMsg)
		self.assertNotIn("86851a5bab3f33abc2858eca0922c34c34c38f0a", loggedMsg)

	def test_logWithRealDetectSecretsCanRedactMultipleMessages(self):
		with mock.patch.object(logging.Logger, "_log") as superLog:
			self.logger._log(
				logging.INFO,
				"first %s",
				("f7dc081e446d6975e462c6aacc4e84cced45e6e5",),
				codepath="tests.unit.test_logHandler",
				redactSecrets=True,
			)
			self.logger._log(
				logging.INFO,
				"second %s",
				("86851a5bab3f33abc2858eca0922c34c34c38f0a",),
				codepath="tests.unit.test_logHandler",
				redactSecrets=True,
			)

		loggedMessages = [call.args[1] for call in superLog.call_args_list]
		self.assertEqual(len(loggedMessages), 2)
		for loggedMsg in loggedMessages:
			self.assertIn("****", loggedMsg)
			self.assertNotIn("86851a5bab3f33abc2858eca0922c34c34c38f0a", loggedMsg)

	def test_logWithRedactionBypassesMaskingAtSecretsLevel(self):
		secret = types.SimpleNamespace(secret_value="secret-value")
		self.logger.setLevel(logHandler.Logger.SECRETS)

		with (
			mock.patch.object(logging.Logger, "_log") as superLog,
			mock.patch("detect_secrets.core.scan.scan_line", return_value=[secret]) as scanLine,
		):
			self.logger._log(
				logging.INFO,
				"api key %s",
				("secret-value",),
				codepath="tests.unit.test_logHandler",
				redactSecrets=True,
			)

		scanLine.assert_not_called()
		superLog.assert_called_once_with(
			logging.INFO,
			"api key %s",
			("secret-value",),
			None,
			{"codepath": "tests.unit.test_logHandler"},
		)
