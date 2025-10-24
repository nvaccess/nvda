import unittest
from unittest.mock import MagicMock, patch
import wx

from NVDAMagnifier import ColorFilter, windowsHandler


class TestGlobalPanel(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Setup wx App once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Setup before each test."""
		self.parent = wx.Frame(None)

	def tearDown(self):
		"""Cleanup after each test."""
		if self.parent:
			self.parent.Destroy()

	def testGlobalPanelInit(self):
		"""Test : GlobalPanel __init__ method."""
		panelDocked = windowsHandler.GlobalPanel(self.parent, "docked")

		self.assertEqual(panelDocked.panelType, "docked")
		self.assertEqual(panelDocked.GetName(), "docked")
		self.assertIsNone(panelDocked.contentBitmap)
		self.assertEqual(panelDocked.cursorPos, (0, 0))
		self.assertEqual(panelDocked.crosshairColor, wx.Colour(255, 0, 0))
		self.assertEqual(panelDocked.crosshairWidth, 2)
		self.assertEqual(panelDocked.crosshairSize, 10)
		self.assertEqual(panelDocked.placeholderText, "docked starting...")

		panelDocked.Destroy()

		panelLens = windowsHandler.GlobalPanel(self.parent, "lens")

		self.assertEqual(panelLens.panelType, "lens")
		self.assertEqual(panelLens.GetName(), "lens")
		self.assertEqual(panelLens.placeholderText, "lens starting...")

		panelLens.Destroy()

	def testSetContent(self):
		"""Test : GlobalPanel setContent method."""
		content = wx.Bitmap(100, 100)
		cursorPos = (0, 0)

		panelDocked = windowsHandler.GlobalPanel(self.parent, "docked")
		panelDocked.Refresh = MagicMock()

		panelDocked.setContent(content, cursorPos)
		self.assertEqual(panelDocked.contentBitmap, content)
		self.assertEqual(panelDocked.cursorPos, cursorPos)
		panelDocked.Refresh.assert_called_once()

		panelDocked.Destroy()

		panelLens = windowsHandler.GlobalPanel(self.parent, "lens")
		panelLens.Refresh = MagicMock()

		panelLens.setContent(content, cursorPos)
		self.assertEqual(panelLens.contentBitmap, content)
		self.assertEqual(panelLens.cursorPos, cursorPos)
		panelLens.Refresh.assert_called_once()

		panelLens.Destroy()

	def testDrawCrosshair(self):
		"""Test : GlobalPanel drawCrosshair method."""
		panel = windowsHandler.GlobalPanel(self.parent, "docked")
		dcMock = MagicMock()
		panel.GetSize = MagicMock(return_value=wx.Size(100, 100))

		panel.drawCrosshair(dcMock, 50, 50)

		panel.GetSize.assert_called_once()
		dcMock.SetPen.assert_called_once()
		dcMock.DrawLine.assert_called()

		panel.Destroy()

	def testDrawPlaceholder(self):
		"""Test : GlobalPanel drawPlaceholder method."""
		panel = windowsHandler.GlobalPanel(self.parent, "docked")
		dcMock = MagicMock()
		panel.GetSize = MagicMock(return_value=wx.Size(100, 100))

		panel.drawPlaceholder(dcMock)

		panel.GetSize.assert_called_once()
		dcMock.SetTextForeground.assert_called_once_with(wx.Colour(128, 128, 128))
		dcMock.SetFont.assert_called_once()
		dcMock.GetTextExtent.assert_called_once_with(panel.placeholderText)
		dcMock.DrawText.assert_called_once()

		panel.Destroy()

	@patch("wx.PaintDC")
	def testPaint(self, mock_paint_dc_class):
		"""Test : GlobalPanel onPaint method."""
		panel = windowsHandler.GlobalPanel(self.parent, "docked")

		dcMock = MagicMock()
		mock_paint_dc_class.return_value = dcMock

		panel.drawCrosshair = MagicMock()
		panel.drawPlaceholder = MagicMock()

		panel.contentBitmap = wx.Bitmap(100, 100)
		panel.cursorPos = (50, 50)
		event = MagicMock()

		panel.onPaint(event)

		mock_paint_dc_class.assert_called_once_with(panel)
		dcMock.Clear.assert_called_once()
		dcMock.DrawBitmap.assert_called_once_with(panel.contentBitmap, 0, 0)
		panel.drawCrosshair.assert_called_once_with(dcMock, 50, 50)

		dcMock.reset_mock()
		mock_paint_dc_class.reset_mock()
		panel.drawCrosshair.reset_mock()

		panel.contentBitmap = None
		panel.onPaint(event)

		mock_paint_dc_class.assert_called_once_with(panel)
		dcMock.Clear.assert_called_once()
		panel.drawPlaceholder.assert_called_once_with(dcMock)
		dcMock.DrawBitmap.assert_not_called()

		panel.Destroy()


class TestGlobalFrame(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Setup wx App once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		self.parent = wx.Frame(None)

	def tearDown(self):
		self.parent.Destroy()

	def testGlobalFrameInit(self):
		"""Test : GlobalFrame initialization."""
		cases = [
			("docked", "", None, None, None, None),
			("lens", "", None, None, None, None),
			("docked", "Docked", None, None, None, "inverted"),
			("lens", "", None, None, None, "greyscale"),
			("docked", "Docked", (100, 100), None, None, None),
			("lens", "Lens", None, wx.DEFAULT_FRAME_STYLE, None, None),
			("docked", "Docked", None, None, (200, 200), None),
		]

		for frameType, title, size, style, position, colorFilter in cases:
			with patch.object(windowsHandler.GlobalFrame, "SetPosition") as mockSetPosition:
				frame = windowsHandler.GlobalFrame(
					frameType=frameType,
					title=title,
					size=size,
					style=style,
					position=position,
					colorFilter=colorFilter,
				)
				self.assertIsInstance(frame, windowsHandler.GlobalFrame)
				self.assertEqual(frame.frameType, frameType)
				self.assertEqual(frame.colorFilter, colorFilter)
				self.assertIsNotNone(frame.GetTitle())
				self.assertIsNotNone(frame.GetSize())
				self.assertIsNot(frame.running, True)
				self.assertIsNone(frame.panel)
				self.assertEqual(frame.movementThreshold, 2)
				if position is not None:
					mockSetPosition.assert_called_once_with(position)
				else:
					mockSetPosition.assert_not_called()

	def testCreatePanel(self):
		"""Test : GlobalFrame createPanel method."""
		frame = windowsHandler.GlobalFrame(frameType="docked")
		panel = frame.createPanel()
		self.assertIsInstance(panel, windowsHandler.GlobalPanel)

	def testSetupLayout(self):
		"""Test : GlobalFrame setupLayout method."""
		frame = windowsHandler.GlobalFrame(frameType="docked")
		panel = windowsHandler.GlobalPanel(frame, frame.frameType)
		frame.createPanel = MagicMock(return_value=panel)
		frame.SetSizer = MagicMock()
		frame.Layout = MagicMock()

		with patch("NVDAMagnifier.windowsHandler.wx.BoxSizer") as MockBoxSizer:
			mockSizer = MagicMock()
			MockBoxSizer.return_value = mockSizer

			frame.setupLayout()

			frame.createPanel.assert_called_once()
			MockBoxSizer.assert_called_once_with(wx.VERTICAL)
			mockSizer.Add.assert_called_once_with(frame.panel, 1, wx.EXPAND | wx.ALL, 0)
			frame.SetSizer.assert_called_once_with(mockSizer)
			frame.Layout.assert_called_once()

		frame.Destroy()
		panel.Destroy()

	def testSetColorFilter(self):
		"""Test : GlobalFrame setColorFilter method."""
		frame = windowsHandler.GlobalFrame(frameType="docked")
		frame.setColorFilter("inverted")
		self.assertEqual(frame.colorFilter, "inverted")

	def testApplyColorFilter(self):
		"""Test : GlobalFrame applyColorFilter method."""
		frame = windowsHandler.GlobalFrame(frameType="docked")

		testImage = wx.Image(2, 2)

		testImage.SetRGB(0, 0, 255, 0, 0)  # top left red
		testImage.SetRGB(1, 0, 0, 255, 0)  # top right green
		testImage.SetRGB(0, 1, 0, 0, 255)  # bottom left blue
		testImage.SetRGB(1, 1, 255, 255, 255)  # bottom right white

		# Case 1: Normal filter
		frame.colorFilter = "normal"
		result = frame.applyColorFilter(testImage.Copy())

		self.assertEqual(result.GetRed(0, 0), 255)
		self.assertEqual(result.GetGreen(0, 0), 0)
		self.assertEqual(result.GetBlue(0, 0), 0)

		# Case 2: Greyscale filter
		frame.colorFilter = "greyscale"
		result = frame.applyColorFilter(testImage.Copy())

		def greyColor(value):
			return int(0.299 * value[0] + 0.587 * value[1] + 0.114 * value[2])

		expectedRedGrey = greyColor((255, 0, 0))
		self.assertEqual(result.GetRed(0, 0), expectedRedGrey)
		self.assertEqual(result.GetGreen(0, 0), expectedRedGrey)
		self.assertEqual(result.GetBlue(0, 0), expectedRedGrey)

		expectedGreenGrey = greyColor((0, 255, 0))
		self.assertEqual(result.GetRed(1, 0), expectedGreenGrey)
		self.assertEqual(result.GetGreen(1, 0), expectedGreenGrey)
		self.assertEqual(result.GetBlue(1, 0), expectedGreenGrey)

		expectedBlueGrey = greyColor((0, 0, 255))
		self.assertEqual(result.GetRed(0, 1), expectedBlueGrey)
		self.assertEqual(result.GetGreen(0, 1), expectedBlueGrey)
		self.assertEqual(result.GetBlue(0, 1), expectedBlueGrey)

		expectedWhiteGrey = greyColor((255, 255, 255))
		self.assertEqual(result.GetRed(1, 1), expectedWhiteGrey)
		self.assertEqual(result.GetGreen(1, 1), expectedWhiteGrey)
		self.assertEqual(result.GetBlue(1, 1), expectedWhiteGrey)

		# Case 3: Inverted filter
		frame.colorFilter = "inverted"
		result = frame.applyColorFilter(testImage.Copy())

		# Red (255,0,0) -> (0,255,255) = Cyan
		self.assertEqual(result.GetRed(0, 0), 0)
		self.assertEqual(result.GetGreen(0, 0), 255)
		self.assertEqual(result.GetBlue(0, 0), 255)

		# Green (0,255,0) -> (255,0,255) = Magenta
		self.assertEqual(result.GetRed(1, 0), 255)
		self.assertEqual(result.GetGreen(1, 0), 0)
		self.assertEqual(result.GetBlue(1, 0), 255)

		# Blue (0,0,255) -> (255,255,0) = Yellow
		self.assertEqual(result.GetRed(0, 1), 255)
		self.assertEqual(result.GetGreen(0, 1), 255)
		self.assertEqual(result.GetBlue(0, 1), 0)

		# White (255,255,255) -> (0,0,0) = Black
		self.assertEqual(result.GetRed(1, 1), 0)
		self.assertEqual(result.GetGreen(1, 1), 0)
		self.assertEqual(result.GetBlue(1, 1), 0)

		# Error Cases

		# Case 1: image None
		result = frame.applyColorFilter(None)
		self.assertIsNone(result)

		# Case: 2 invalid Image
		invalid_image = wx.Image()
		frame.colorFilter = "greyscale"
		result = frame.applyColorFilter(invalid_image)
		self.assertEqual(result, invalid_image)

	def testForceRefresh(self):
		"""Test : GlobalFrame forceRefresh method."""
		frame = windowsHandler.GlobalFrame(frameType="docked")
		frame.createPanel()
		wx.CallAfter = MagicMock()
		frame.forceRefresh()

		if frame.panel:
			wx.CallAfter.assert_called()

	def testStartMagnifying(self):
		"""Test : GlobalFrame startMagnifying method."""
		frame = windowsHandler.GlobalFrame(frameType="docked")
		frame.createPanel()

		frame.setupLayout = MagicMock()
		frame.Show = MagicMock()
		frame.forceRefresh = MagicMock()
		frame.Bind = MagicMock()
		screenWidth, screenHeight = wx.GetDisplaySize()

		frame.startMagnifying()
		self.assertTrue(frame.running)
		frame.forceRefresh.assert_called()
		frame.Bind.assert_called()
		frame.Show.assert_called()
		frame.setupLayout.assert_called()
		self.assertEqual((frame.screenWidth, frame.screenHeight), (screenWidth, screenHeight))

	def testStopMagnifying(self):
		"""Test : GlobalFrame stopMagnifying method."""
		frame = windowsHandler.GlobalFrame(frameType="docked")
		frame.createPanel()

		frame.Destroy = MagicMock()

		frame.stopMagnifying()

		self.assertFalse(frame.running)
		frame.Destroy.assert_called()

	def testUpdateMagnifier(self):
		"""Test : GlobalFrame updateMagnifier method."""
		frame = windowsHandler.GlobalFrame(frameType="docked")
		frame.createPanel()
		frame.running = True

		# Mock of Function
		frame.Layout = MagicMock()
		frame.panel.GetSize = MagicMock(return_value=wx.Size(400, 300))
		frame.applyColorFilter = MagicMock()

		# Mock of Wx
		mockScreenDc = MagicMock()
		mockBitmap = MagicMock()
		mockMemoryDc = MagicMock()
		mockImage = MagicMock()
		mockScaledImage = MagicMock()
		mockFinalBitmap = MagicMock()

		# Mock configurations
		mockBitmap.IsOk.return_value = True
		mockBitmap.ConvertToImage.return_value = mockImage
		mockImage.Scale.return_value = mockScaledImage
		mockMemoryDc.Blit.return_value = True
		frame.applyColorFilter.return_value = mockImage

		with (
			patch("NVDAMagnifier.windowsHandler.wx.GetDisplaySize", return_value=(1920, 1080)),
			patch("wx.ScreenDC", return_value=mockScreenDc),
			patch("wx.Bitmap", return_value=mockBitmap),
			patch("wx.MemoryDC", return_value=mockMemoryDc),
			patch("wx.CallAfter") as mock_call_after,
		):
			with patch.object(mockScaledImage, "__class__", wx.Image):
				with patch("wx.Bitmap", side_effect=[mockBitmap, mockFinalBitmap]):
					frame.updateMagnifier(500, 400, 2.0)

					frame.Layout.assert_called_once()
					frame.panel.GetSize.assert_called()
					mockMemoryDc.SelectObject.assert_any_call(mockBitmap)
					mockMemoryDc.Blit.assert_called_once_with(0, 0, 200, 150, mockScreenDc, 400, 325)
					mockBitmap.ConvertToImage.assert_called_once()
					frame.applyColorFilter.assert_called_once_with(mockImage)
					mockImage.Scale.assert_called_once_with(400, 300, wx.IMAGE_QUALITY_BICUBIC)
					mock_call_after.assert_called_once()
					call_args = mock_call_after.call_args
					self.assertEqual(call_args[0][0], frame.panel.setContent)
					cursor_pos = call_args[0][2]
					self.assertEqual(cursor_pos, (200, 150))

		frame.Destroy()


class TestDockedFrame(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Setup wx App once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Setup before each test."""
		self.screenWidth, self.screenHeight = wx.GetDisplaySize()
		self.magnifierWidth = self.screenWidth
		self.magnifierHeight = max(150, min(300, self.screenHeight // 4))

		self.dockedFrame = windowsHandler.DockedFrame()

	def tearDown(self):
		"""Clean up after each test."""
		if hasattr(self, "dockedFrame") and self.dockedFrame:
			self.dockedFrame.Destroy()

	def testDockedFrameInit(self):
		"""Test : DockedFrame initialization."""
		self.assertEqual(self.dockedFrame.frameType, "docked")
		self.assertEqual(self.dockedFrame.Title, "NVDA Docked Magnifier")
		self.assertEqual(self.dockedFrame.Size, (self.magnifierWidth, self.magnifierHeight))
		self.assertEqual(self.dockedFrame.GetWindowStyle(), wx.STAY_ON_TOP | wx.CAPTION | wx.RESIZE_BORDER)
		self.assertEqual(self.dockedFrame.Position, (0, 0))

	def testStartDockedFrame(self):
		"""Test : DockedFrame startMagnifying method."""
		with patch.object(windowsHandler.GlobalFrame, "startMagnifying") as mock_super_magnifying:
			self.dockedFrame.setColorFilter = MagicMock()
			mouseX, mouseY = 0, 0

			self.dockedFrame.startMagnifying((mouseX, mouseY), ColorFilter.NORMAL)
			self.dockedFrame.setColorFilter.assert_called_once_with(ColorFilter.NORMAL)
			self.assertEqual(self.dockedFrame.lastMousePos, (mouseX, mouseY))
			mock_super_magnifying.assert_called_once()

	def testUpdateDockedFrame(self):
		"""Test : DockedFrame updateMagnifier method."""
		self.dockedFrame.lastMousePos = (10, 10)

		with patch.object(windowsHandler.GlobalFrame, "updateMagnifier") as mock_super_update:
			self.dockedFrame.setColorFilter = MagicMock()

			lastMouseX, lastMouseY = self.dockedFrame.lastMousePos

			# Case 1: Nothing moved
			self.dockedFrame.updateMagnifier(10, 10, 2.0, (lastMouseX, lastMouseY), ColorFilter.NORMAL.value)

			self.dockedFrame.setColorFilter.assert_not_called()
			mock_super_update.assert_not_called()

			# Case 2: Mouse moved
			self.dockedFrame.setColorFilter.reset_mock()
			mock_super_update.reset_mock()

			self.dockedFrame.updateMagnifier(
				10, 10, 2.0, (lastMouseX + 100, lastMouseY + 100), ColorFilter.NORMAL.value
			)

			self.dockedFrame.setColorFilter.assert_not_called()
			mock_super_update.assert_called_once_with(10, 10, 2.0)

			# Case 3: Color changed
			self.dockedFrame.setColorFilter.reset_mock()
			mock_super_update.reset_mock()
			lastMouseX, lastMouseY = self.dockedFrame.lastMousePos

			self.dockedFrame.updateMagnifier(
				10, 10, 3.0, (lastMouseX + 100, lastMouseY + 100), ColorFilter.INVERTED.value
			)

			self.dockedFrame.setColorFilter.assert_called_once_with(ColorFilter.INVERTED.value)
			mock_super_update.assert_called_once_with(10, 10, 3.0)


class TestLensFrame(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Setup wx App once for all tests."""
		if not wx.GetApp():
			cls.app = wx.App(False)

	def setUp(self):
		"""Setup before each test."""
		self.lensFrame = windowsHandler.LensFrame()
		self.lensFrame.screenWidth, self.lensFrame.screenHeight = wx.GetDisplaySize()

	def tearDown(self):
		"""Clean up after each test."""
		if hasattr(self, "lensFrame") and self.lensFrame:
			self.lensFrame.Destroy()

	def testLensFrameInit(self):
		"""Test : LensFrame initialization."""
		self.assertEqual(self.lensFrame.frameType, "lens")
		self.assertEqual(self.lensFrame.Title, "NVDA Lens Magnifier")
		self.assertEqual(self.lensFrame.Size, (300, 300))
		self.assertEqual(self.lensFrame.GetWindowStyle(), wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)

	def testStartLensFrame(self):
		"""Test : LensFrame startMagnifying method."""
		with patch.object(windowsHandler.GlobalFrame, "startMagnifying") as mock_super_magnifying:
			self.lensFrame.setColorFilter = MagicMock()

			self.lensFrame.startMagnifying(ColorFilter.NORMAL)
			self.lensFrame.setColorFilter.assert_called_once_with(ColorFilter.NORMAL)
			mock_super_magnifying.assert_called_once()

	def testUpdateLensFrame(self):
		"""Test : LensFrame updateMagnifier method."""

		with patch.object(windowsHandler.GlobalFrame, "updateMagnifier") as mock_super_update:
			self.lensFrame.setColorFilter = MagicMock()
			self.lensFrame.SetPosition = MagicMock()

			# Case 1: No colorChanges
			self.lensFrame.updateMagnifier(10, 10, 2.0, ColorFilter.NORMAL.value)

			self.lensFrame.SetPosition.assert_called_once()
			self.lensFrame.setColorFilter.assert_not_called()
			mock_super_update.assert_called_once_with(10, 10, 2.0)

			# Reset mocks

			self.lensFrame.setColorFilter.reset_mock()
			self.lensFrame.SetPosition.reset_mock()
			mock_super_update.reset_mock()

			# Case 2: Color changed

			self.lensFrame.updateMagnifier(10, 10, 3.0, ColorFilter.INVERTED.value)

			self.lensFrame.SetPosition.assert_called_once()
			self.lensFrame.setColorFilter.assert_called_once_with(ColorFilter.INVERTED.value)
			mock_super_update.assert_called_once_with(10, 10, 3.0)
