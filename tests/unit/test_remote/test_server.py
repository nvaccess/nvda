# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the Remote Access relay server's client message handling."""

import unittest
from unittest import mock

from _remoteClient.server import Client


class TestClientMessageSizeLimit(unittest.TestCase):
	def setUp(self) -> None:
		self.server = mock.Mock()
		self.socket = mock.Mock()
		self.client = Client(server=self.server, socket=self.socket)
		self.client.parse = mock.Mock()

	def test_incompleteMessageAtLimitIsBuffered(self) -> None:
		self.client.buffer = b"A" * (self.client._MAX_UNAUTHENTICATED_MESSAGE_SIZE_BYTES - 1)
		self.socket.recv.return_value = b"A"

		self.client.handleData()

		self.assertEqual(len(self.client.buffer), self.client._MAX_UNAUTHENTICATED_MESSAGE_SIZE_BYTES)
		self.socket.close.assert_not_called()
		self.client.parse.assert_not_called()

	def test_incompleteMessageOverLimitDisconnects(self) -> None:
		self.client.buffer = b"A" * self.client._MAX_UNAUTHENTICATED_MESSAGE_SIZE_BYTES
		self.socket.recv.return_value = b"A"

		self.client.handleData()

		self.socket.close.assert_called_once_with()
		self.server.clientDisconnected.assert_called_once_with(self.client)
		self.client.parse.assert_not_called()

	def test_completeMessageAtLimitIsParsed(self) -> None:
		self.client.buffer = b"A" * (self.client._MAX_UNAUTHENTICATED_MESSAGE_SIZE_BYTES - 1)
		self.socket.recv.return_value = b"A\n"

		self.client.handleData()

		self.client.parse.assert_called_once()
		self.assertEqual(
			len(self.client.parse.call_args.args[0]),
			self.client._MAX_UNAUTHENTICATED_MESSAGE_SIZE_BYTES,
		)
		self.assertEqual(self.client.buffer, b"")
		self.socket.close.assert_not_called()

	def test_completeMessageOverLimitDisconnectsWithoutParsing(self) -> None:
		self.client.buffer = b"A" * self.client._MAX_UNAUTHENTICATED_MESSAGE_SIZE_BYTES
		self.socket.recv.return_value = b"A\n"

		self.client.handleData()

		self.socket.close.assert_called_once_with()
		self.server.clientDisconnected.assert_called_once_with(self.client)
		self.client.parse.assert_not_called()

	def test_authenticatedMessageMayExceedUnauthenticatedLimit(self) -> None:
		self.client.authenticated = True
		self.client.buffer = b"A" * self.client._MAX_UNAUTHENTICATED_MESSAGE_SIZE_BYTES
		self.socket.recv.return_value = b"A"

		self.client.handleData()

		self.assertEqual(
			len(self.client.buffer),
			self.client._MAX_UNAUTHENTICATED_MESSAGE_SIZE_BYTES + 1,
		)
		self.socket.close.assert_not_called()
		self.client.parse.assert_not_called()

	def test_authenticatedMessageOverLimitDisconnects(self) -> None:
		self.client.authenticated = True
		self.client.buffer = b"A" * self.client._MAX_MESSAGE_SIZE_BYTES
		self.socket.recv.return_value = b"A"

		self.client.handleData()

		self.socket.close.assert_called_once_with()
		self.server.clientDisconnected.assert_called_once_with(self.client)
		self.client.parse.assert_not_called()

	def test_multipleMessagesAndPartialMessageAreHandled(self) -> None:
		self.socket.recv.return_value = b"first\nsecond\npartial"

		self.client.handleData()

		self.client.parse.assert_has_calls([mock.call(b"first"), mock.call(b"second")])
		self.assertEqual(self.client.buffer, b"partial")
		self.socket.close.assert_not_called()
