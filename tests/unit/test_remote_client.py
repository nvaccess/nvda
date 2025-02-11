import unittest
from unittest.mock import MagicMock, patch
import remoteClient.client as rc_client
from remoteClient.connectionInfo import ConnectionInfo, ConnectionMode
from remoteClient.protocol import RemoteMessageType


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
			def getURLToConnect(_):
				return self.url

		return FakeConnectionInfo()


class FakeAPI:
	clip_data = "Fake clipboard text"
	copied = None

	@staticmethod
	def getClipData():
		return FakeAPI.clip_data

	@staticmethod
	def copyToClip(text):
		FakeAPI.copied = text


class TestRemoteClient(unittest.TestCase):
	def setUp(self):
		import wx

		if not wx.GetApp():
			self.app = wx.App()
		# Patch gui.mainFrame to a fake object so RemoteMenu can access sysTrayIcon.toolsMenu.
		patcher_mainFrame = patch("remoteClient.client.gui.mainFrame")
		self.addCleanup(patcher_mainFrame.stop)
		mock_mainFrame = patcher_mainFrame.start()
		mock_mainFrame.sysTrayIcon = MagicMock()
		mock_mainFrame.sysTrayIcon.toolsMenu = MagicMock()
		self.client = rc_client.RemoteClient()
		# Override localMachine and menu with fake implementations.
		self.client.localMachine = FakeLocalMachine()
		self.client.menu = FakeMenu()
		# Patch ui.message to capture calls.
		patcher = patch("remoteClient.client.ui.message")
		self.addCleanup(patcher.stop)
		self.ui_message = patcher.start()
		# Patch the API module to use our fake API.
		patcher_api = patch("remoteClient.client.api", new=FakeAPI)
		self.addCleanup(patcher_api.stop)
		patcher_api.start()
		FakeAPI.copied = None
		patcher_nvwave = patch("remoteClient.cues.nvwave.playWaveFile", return_value=None)

		self.addCleanup(patcher_nvwave.stop)
		patcher_nvwave.start()

	def tearDown(self):
		self.client = None

	def test_toggle_mute(self):
		# Initially, local machine should not be muted.
		self.assertFalse(self.client.localMachine.isMuted)
		# Toggle mute: should mute the local machine.
		self.client.toggleMute()
		self.assertTrue(self.client.localMachine.isMuted)
		self.assertTrue(self.client.menu.muteItem.checked)
		self.ui_message.assert_called_once()
		# Now toggle again: should unmute.
		self.ui_message.reset_mock()
		self.client.toggleMute()
		self.assertFalse(self.client.localMachine.isMuted)
		self.assertFalse(self.client.menu.muteItem.checked)
		self.ui_message.assert_called_once()

	def test_push_clipboard_no_connection(self):
		# Without any transport (neither slave nor master), pushClipboard should warn.
		self.client.followerTransport = None
		self.client.leaderTransport = None
		self.client.pushClipboard()
		self.ui_message.assert_called_with("Not connected.")

	def test_push_clipboard_with_transport(self):
		# With a fake transport, pushClipboard should send the clipboard text.
		fake_transport = FakeTransport()
		self.client.leaderTransport = fake_transport
		FakeAPI.clip_data = "TestClipboard"
		self.client.pushClipboard()
		self.assertTrue(len(fake_transport.sent) > 0)
		messageType, kwargs = fake_transport.sent[0]
		self.assertEqual(messageType, RemoteMessageType.SET_CLIPBOARD_TEXT)
		self.assertEqual(kwargs.get("text"), "TestClipboard")

	def test_copy_link_no_session(self):
		# If there is no session, copyLink should warn the user.
		self.client.leaderSession = None
		self.client.followerSession = None
		self.ui_message.reset_mock()
		self.client.copyLink()
		self.ui_message.assert_called_with("Not connected.")

	def test_copy_link_with_session(self):
		# With a fake session, copyLink should call api.copyToClip with the proper URL.
		fake_session = FakeSession("http://fake.url/connect")
		self.client.leaderSession = fake_session
		FakeAPI.copied = None
		self.client.copyLink()
		self.assertEqual(FakeAPI.copied, "http://fake.url/connect")

	def test_send_sas_no_master_transport(self):
		# Without a leaderTransport, sendSAS should log an error.
		self.client.leaderTransport = None
		with patch("remoteClient.client.log.error") as mock_log_error:
			self.client.sendSAS()
			mock_log_error.assert_called_once_with("No master transport to send SAS")

	def test_send_sas_with_master_transport(self):
		# With a fake leaderTransport, sendSAS should forward the SEND_SAS message.
		fake_transport = FakeTransport()
		self.client.leaderTransport = fake_transport
		self.client.sendSAS()
		self.assertTrue(len(fake_transport.sent) > 0)
		messageType, _ = fake_transport.sent[0]
		self.assertEqual(messageType, RemoteMessageType.SEND_SAS)

	def test_connect_dispatch(self):
		# Ensure that connect() dispatches to connectAsMaster or connectAsSlave based on connection mode.
		fake_connect_as_master = MagicMock()
		fake_connect_as_slave = MagicMock()
		self.client.connectAsMaster = fake_connect_as_master
		self.client.connectAsSlave = fake_connect_as_slave
		conn_info_master = ConnectionInfo(
			hostname="localhost",
			mode=ConnectionMode.MASTER,
			key="abc",
			port=1000,
			insecure=False,
		)
		self.client.connect(conn_info_master)
		fake_connect_as_master.assert_called_once_with(conn_info_master)
		fake_connect_as_master.reset_mock()
		conn_info_slave = ConnectionInfo(
			hostname="localhost",
			mode=ConnectionMode.SLAVE,
			key="abc",
			port=1000,
			insecure=False,
		)
		self.client.connect(conn_info_slave)
		fake_connect_as_slave.assert_called_once_with(conn_info_slave)

	def test_disconnect(self):
		# Test disconnect with no active sessions.
		self.client.leaderSession = None
		self.client.followerSession = None
		with patch("remoteClient.client.log.debug") as mock_log_debug:
			self.client.disconnect()
			mock_log_debug.assert_called()
		# Test disconnect with an active localControlServer.
		fake_control = MagicMock()
		self.client.localControlServer = fake_control
		self.client.leaderSession = MagicMock()
		self.client.followerSession = MagicMock()
		self.client.disconnect()
		fake_control.close.assert_called_once()


if __name__ == "__main__":
	unittest.main()
