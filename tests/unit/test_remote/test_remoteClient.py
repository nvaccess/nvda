# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import unittest
from unittest.mock import MagicMock, patch
import _remoteClient.client as rcClient
from _remoteClient.connectionInfo import ConnectionInfo, ConnectionMode
from _remoteClient.protocol import RemoteMessageType


# Fake implementations for testing
class FakeLocalMachine:
	def __init__(self):
		self.isMuted = False

	def terminate(self):
		pass


class FakeMenu:
	def __init__(self):
		self.muteItem = self.FakeMuteItem()

	class FakeMuteItem:
		def __init__(self):
			self.checked = None

		def Check(self, value):
			self.checked = value


class FakeTransport:
	def __init__(self):
		self.sent = []

	@property
	def connected(self):
		return True

	def send(self, messageType, **kwargs):
		self.sent.append((messageType, kwargs))


class FakeSession:
	def __init__(self, url):
		self.url = url

	def getConnectionInfo(self):
		class FakeConnectionInfo:
			def getURLToConnect(_):  # type: ignore
				return self.url

		return FakeConnectionInfo()


class FakeAPI:
	clipData = "Fake clipboard text"
	copied = None

	@staticmethod
	def getClipData():
		return FakeAPI.clipData

	@staticmethod
	def copyToClip(text):
		FakeAPI.copied = text


class TestRemoteClient(unittest.TestCase):
	def setUp(self):
		import wx

		if not wx.GetApp():
			self.app = wx.App()
		# Patch gui.mainFrame to a fake object so RemoteMenu can access sysTrayIcon.toolsMenu.
		patcherMainFrame = patch("_remoteClient.client.gui.mainFrame")
		self.addCleanup(patcherMainFrame.stop)
		mockMainFrame = patcherMainFrame.start()
		mockMainFrame.sysTrayIcon = MagicMock()
		mockMainFrame.sysTrayIcon.toolsMenu = MagicMock()
		self.client = rcClient.RemoteClient()
		# Override localMachine and menu with fake implementations.
		self.client.localMachine = FakeLocalMachine()
		self.client.menu = FakeMenu()
		# Patch ui.message to capture calls.
		patcher = patch("_remoteClient.client.ui.message")
		self.addCleanup(patcher.stop)
		self.uiMessage = patcher.start()
		# Patch the API module to use our fake API.
		patcherAPI = patch("_remoteClient.client.api", new=FakeAPI)
		self.addCleanup(patcherAPI.stop)
		patcherAPI.start()
		FakeAPI.copied = None
		patcherNvwave = patch("_remoteClient.cues.nvwave.playWaveFile", return_value=None)

		self.addCleanup(patcherNvwave.stop)
		patcherNvwave.start()

	def tearDown(self):
		self.client = None

	@patch.object(rcClient.RemoteClient, "isConnected", lambda self: True)
	def test_toggleMute(self):
		# Initially, local machine should not be muted.
		self.assertFalse(self.client.localMachine.isMuted)
		# Toggle mute: should mute the local machine.
		self.client.toggleMute()
		self.assertTrue(self.client.localMachine.isMuted)
		self.assertTrue(self.client.menu.muteItem.checked)
		self.uiMessage.assert_called_once()
		# Now toggle again: should unmute.
		self.uiMessage.reset_mock()
		self.client.toggleMute()
		self.assertFalse(self.client.localMachine.isMuted)
		self.assertFalse(self.client.menu.muteItem.checked)
		self.uiMessage.assert_called_once()

	def test_pushClipboardNoConnection(self):
		# Without any transport (neither follower nor leader), pushClipboard should warn.
		self.client.followerTransport = None
		self.client.leaderTransport = None
		self.client.pushClipboard()
		self.uiMessage.assert_called_with("Not connected")

	def test_pushClipboardWithTransport(self):
		# With a fake transport, pushClipboard should send the clipboard text.
		fakeTransport = FakeTransport()
		fakeSession = FakeSession("")
		fakeSession.connectedClientsCount = 1
		self.client.leaderTransport = fakeTransport
		self.client.leaderSession = fakeSession
		FakeAPI.clipData = "TestClipboard"
		self.client.pushClipboard()
		self.assertTrue(len(fakeTransport.sent) > 0)
		messageType, kwargs = fakeTransport.sent[0]
		self.assertEqual(messageType, RemoteMessageType.SET_CLIPBOARD_TEXT)
		self.assertEqual(kwargs.get("text"), "TestClipboard")

	def test_copyLinkNoSession(self):
		# If there is no session, copyLink should warn the user.
		self.client.leaderSession = None
		self.client.followerSession = None
		self.uiMessage.reset_mock()
		self.client.copyLink()
		self.uiMessage.assert_called_with("Not connected")

	def test_copyLinkWithSession(self):
		# With a fake session, copyLink should call api.copyToClip with the proper URL.
		fakeSession = FakeSession("http://fake.url/connect")
		self.client.leaderSession = fakeSession
		FakeAPI.copied = None
		self.client.copyLink()
		self.assertEqual(FakeAPI.copied, "http://fake.url/connect")

	def test_sendSasNoLeaderTransport(self):
		# Without a leaderTransport, sendSAS should log an error.
		self.client.leaderTransport = None
		with patch("_remoteClient.client.log.error") as mockLogError:
			self.client.sendSAS()
			mockLogError.assert_called_once_with("No leader transport to send SAS")

	def test_sendSasWithLeaderTransport(self):
		# With a fake leaderTransport, sendSAS should forward the SEND_SAS message.
		fakeTransport = FakeTransport()
		self.client.leaderTransport = fakeTransport
		self.client.sendSAS()
		self.assertTrue(len(fakeTransport.sent) > 0)
		messageType, _ = fakeTransport.sent[0]
		self.assertEqual(messageType, RemoteMessageType.SEND_SAS)

	def test_connectDispatch(self):
		# Ensure that connect() dispatches to connectAsLeader or connectAsFollower based on connection mode.
		fakeConnectAsLeader = MagicMock()
		fakeConnectAsFollower = MagicMock()
		self.client.connectAsLeader = fakeConnectAsLeader
		self.client.connectAsFollower = fakeConnectAsFollower
		connInfoLeader = ConnectionInfo(
			hostname="localhost",
			mode=ConnectionMode.LEADER,
			key="abc",
			port=1000,
			insecure=False,
		)
		self.client.connect(connInfoLeader)
		fakeConnectAsLeader.assert_called_once_with(connInfoLeader)
		fakeConnectAsLeader.reset_mock()
		connInfoFollower = ConnectionInfo(
			hostname="localhost",
			mode=ConnectionMode.FOLLOWER,
			key="abc",
			port=1000,
			insecure=False,
		)
		self.client.connect(connInfoFollower)
		fakeConnectAsFollower.assert_called_once_with(connInfoFollower)

	def test_disconnect(self):
		# Test disconnect with no active sessions.
		self.client.leaderSession = None
		self.client.followerSession = None
		with patch("_remoteClient.client.log.debug") as mockLogDebug:
			self.client.disconnect()
			mockLogDebug.assert_called()
		# Test disconnect with an active localControlServer.
		fakeControl = MagicMock()
		self.client.localControlServer = fakeControl
		self.client.leaderSession = MagicMock()
		self.client.followerSession = MagicMock()
		self.client.disconnect()
		fakeControl.close.assert_called_once()


if __name__ == "__main__":
	unittest.main()
