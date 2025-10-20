import unittest
from unittest.mock import MagicMock, Mock, patch
import wx
import ctypes

from NVDAMagnifier import ColorFilter, ColorFilterMatrix, MagnifierType, FullScreenMagnifier, FullScreenMode


class TestFullScreenMagnifier(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""
		Setup qui s'exécute une fois au début.
		"""
		if not wx.GetApp():
			cls.app = wx.App(False)

	@patch.object(FullScreenMagnifier, "_startMagnifier")
	@patch.object(FullScreenMagnifier, "_applyColorFilter")
	def testFullScreenMagnifierCreation(self, mock_apply_color_filter, mock_start_magnifier):
		"""Test : Creating the fullscreen magnifier."""
		zoomDefault = 2.0
		colorDefault = ColorFilter.NORMAL
		fullscreenModeDefault = FullScreenMode.CENTER

		def testValues(
			magnifier: FullScreenMagnifier,
			zoomPassed: float = zoomDefault,
			colorFilterPassed: ColorFilter = colorDefault,
			fullscreenModePassed: FullScreenMode = fullscreenModeDefault,
		):
			self.assertEqual(magnifier.zoomLevel, zoomPassed)
			self.assertEqual(magnifier.colorFilter, colorFilterPassed)
			self.assertEqual(magnifier.fullscreenMode, fullscreenModePassed)
			self.assertIsInstance(magnifier, FullScreenMagnifier)
			self.assertEqual(magnifier.magnifierType, MagnifierType.FULLSCREEN)
			mock_start_magnifier.assert_called_once()
			mock_apply_color_filter.assert_called_once()

			# reseting instance

			mock_start_magnifier.reset_mock()
			mock_apply_color_filter.reset_mock()

		# Case 1: No parameters

		magnifier = FullScreenMagnifier()
		testValues(magnifier)

		# Case 2: Only zoom
		magnifier = FullScreenMagnifier(zoomLevel=4.0)
		testValues(magnifier, zoomPassed=4.0)

		# Case 3: Only color filter
		magnifier = FullScreenMagnifier(colorFilter=ColorFilter.INVERTED)
		testValues(magnifier, colorFilterPassed=ColorFilter.INVERTED)

		# case 4: all parameters
		magnifier = FullScreenMagnifier(
			zoomLevel=4.0, colorFilter=ColorFilter.GREYSCALE, fullscreenMode=FullScreenMode.BORDER
		)
		testValues(
			magnifier,
			zoomPassed=4.0,
			colorFilterPassed=ColorFilter.GREYSCALE,
			fullscreenModePassed=FullScreenMode.BORDER,
		)

	def testStartFullScreenMagnifier(self):
		"""Test : Activating and deactivating the fullscreen magnifier."""
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

		magnifier._loadMagnifierApi = MagicMock()
		magnifier._startTimer = MagicMock()

		magnifier._startMagnifier()
		magnifier._loadMagnifierApi.assert_called_once()
		magnifier._startTimer.assert_called_once()
		self.assertTrue(magnifier.isActive)

	def testFullScreenDoUpdate(self):
		"""Test : Updating the magnifier"""
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

		def initValues(currentCoordinates: tuple[int, int], mode: FullScreenMode, lastFocusedObject: str):
			magnifier.currentCoordinates = currentCoordinates
			magnifier.lastScreenPosition = (0, 0)
			magnifier.fullscreenMode = mode
			magnifier.lastFocusedObject = lastFocusedObject
			magnifier._borderPos = MagicMock(return_value=(20, 20))
			magnifier._relativePos = MagicMock(return_value=(30, 30))
			magnifier._fullscreenMagnifier = MagicMock()

		def testValues(x, y):
			magnifier._doUpdate()
			if magnifier.fullscreenMode.value == "border" and magnifier.lastFocusedObject == "mouse":
				magnifier._borderPos.assert_called_once()
			elif magnifier.fullscreenMode.value == "relative":
				magnifier._relativePos.assert_called_once()
			self.assertEqual(magnifier.currentCoordinates, (x, y))
			self.assertEqual(magnifier.lastScreenPosition, (x, y))
			magnifier._fullscreenMagnifier.assert_called_once()

		# Case 1: Center mode last focused object: Mouse

		initValues((10, 10), FullScreenMode.CENTER, "mouse")
		testValues(10, 10)

		# Case 2: Center mode last focused object: Nvda

		initValues((10, 10), FullScreenMode.CENTER, "nvda")
		testValues(10, 10)

		# Case 3: Border mode last focused object: Mouse

		initValues((20, 20), FullScreenMode.BORDER, "mouse")
		testValues(20, 20)

		# Case 4: Border mode last focused object: Nvda Should

		initValues((20, 20), FullScreenMode.BORDER, "nvda")
		testValues(20, 20)

		# Case 5: relative mode last focused object: Mouse

		initValues((30, 30), FullScreenMode.RELATIVE, "mouse")
		testValues(30, 30)

		# Case 6: relative mode last focused object: Nvda
		initValues((30, 30), FullScreenMode.RELATIVE, "nvda")
		testValues(30, 30)

	def testStopMagnifier(self):
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

		ctypes.windll.magnification.MagSetFullscreenColorEffect = MagicMock()
		magnifier._getMagnificationApi = MagicMock()
		magnifier._stopMagnifierApi = MagicMock()

		magnifier._stopMagnifier()

		ctypes.windll.magnification.MagSetFullscreenColorEffect.assert_called_once()
		magnifier._getMagnificationApi.assert_called_once()
		magnifier._stopMagnifierApi.assert_called_once()

	def testApplyColorFilter(self):
		magnifier = FullScreenMagnifier()

		def testValues(colorFilter: ColorFilter, colorFilterMatrix: ColorFilterMatrix):
			magnifier.colorFilter = colorFilter
			ctypes.windll.magnification.MagSetFullscreenColorEffect = MagicMock()

			magnifier._applyColorFilter()
			ctypes.windll.magnification.MagSetFullscreenColorEffect.assert_called_once_with(
				colorFilterMatrix.value
			)

		# Case 1: Color filter: Normal
		testValues(ColorFilter.NORMAL, ColorFilterMatrix.NORMAL)

		# Case 2: Color filter: Grayscale
		testValues(ColorFilter.GREYSCALE, ColorFilterMatrix.GREYSCALE)

		# Case 3: Color filter: Inverted
		testValues(ColorFilter.INVERTED, ColorFilterMatrix.INVERTED)

	# Windows dll test todo

	def testLoadMagnifierApi(self):
		pass

	def stopMagnifierApi(self):
		pass

	def testGetMagnifierApi(self):
		pass

	def testFullscreenMagnifierTryExcept(self):
		"""Test : Specific try/except behavior in _fullscreenMagnifier."""
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

		magnifier._SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
		magnifier._SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)
		magnifier._MARGIN_BORDER = 50
		centerX = magnifier._SCREEN_WIDTH // 2
		centerY = magnifier._SCREEN_HEIGHT // 2
		magnifier.lastScreenPosition = (centerX, centerY)
		magnifier.zoomLevel = 2.0

		visibleWidth = int(magnifier._SCREEN_WIDTH / magnifier.zoomLevel)
		visibleHeight = int(magnifier._SCREEN_HEIGHT / magnifier.zoomLevel)
		left = centerX - visibleWidth // 2
		top = centerY - visibleHeight // 2

		with patch.object(
			magnifier, "_getMagnifierPosition", return_value=(left, top, visibleWidth, visibleHeight)
		):
			with patch.object(magnifier, "_getMagnificationApi") as mockGetApi:
				mockApiFunction = Mock(return_value=True)
				mockGetApi.return_value = mockApiFunction

				magnifier._fullscreenMagnifier(centerX, centerY)
				magnifier._getMagnifierPosition.assert_called_once_with(centerX, centerY)

				resultLeft, resultTop, resultVisibleWidth, resultVisibleHeight = (
					left,
					top,
					visibleWidth,
					visibleHeight,
				)
				self.assertEqual(
					(resultLeft, resultTop, resultVisibleWidth, resultVisibleHeight),
					(left, top, visibleWidth, visibleHeight),
				)

				mockGetApi.assert_called_once()
				mockApiFunction.assert_called_once()

				call_args = mockApiFunction.call_args[0]

				self.assertEqual(call_args[0].value, magnifier.zoomLevel)
				self.assertEqual(call_args[1].value, left)
				self.assertEqual(call_args[2].value, top)

	def testBorderPosReal(self):
		"""Test : Border position with realistic screen values."""
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

		magnifier._SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
		magnifier._SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)
		magnifier._MARGIN_BORDER = 50
		centerX = magnifier._SCREEN_WIDTH // 2
		centerY = magnifier._SCREEN_HEIGHT // 2
		magnifier.lastScreenPosition = (centerX, centerY)
		magnifier.zoomLevel = 2.0

		visibleWidth = int(magnifier._SCREEN_WIDTH / magnifier.zoomLevel)
		visibleHeight = int(magnifier._SCREEN_HEIGHT / magnifier.zoomLevel)
		left = centerX - visibleWidth // 2
		top = centerY - visibleHeight // 2

		with patch.object(
			magnifier, "_getMagnifierPosition", return_value=(left, top, visibleWidth, visibleHeight)
		):
			# Case 1: Focus in the Middle
			result = magnifier._borderPos(centerX, centerY)
			self.assertEqual(result, (centerX, centerY))

			# Case 2: Focus near the Left Edge
			edgeFocusX = 100
			edgeFocusY = centerY
			result = magnifier._borderPos(edgeFocusX, edgeFocusY)
			# Should adjust the position
			self.assertNotEqual(result, (centerX, centerY))
			self.assertIsInstance(result, tuple)
			self.assertEqual(len(result), 2)

			# Case 3: Focus near the Right Edge
			edgeFocusX = magnifier._SCREEN_WIDTH - 100
			edgeFocusY = centerY
			result = magnifier._borderPos(edgeFocusX, edgeFocusY)
			# Devrait ajuster la position
			self.assertIsInstance(result, tuple)
			self.assertEqual(len(result), 2)

			# Case 4: Check that results stay within bounds
			testPositions = [
				(100, 100),  # Top-left
				(magnifier._SCREEN_WIDTH - 100, 100),  # Top-right
				(100, magnifier._SCREEN_HEIGHT - 100),  # Bottom-left
				(magnifier._SCREEN_WIDTH - 100, magnifier._SCREEN_HEIGHT - 100),  # Bottom-right
			]

			for pos in testPositions:
				with self.subTest(position=pos):
					result = magnifier._borderPos(pos[0], pos[1])
					self.assertGreaterEqual(result[0], 0)
					self.assertLessEqual(result[0], magnifier._SCREEN_WIDTH)
					self.assertGreaterEqual(result[1], 0)
					self.assertLessEqual(result[1], magnifier._SCREEN_HEIGHT)

	def testRelativePos(self):
		"""Test : Relative position calculation."""
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

		# Utiliser les vraies dimensions d'écran
		magnifier._SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
		magnifier._SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)
		magnifier.zoomLevel = 2.0
		magnifier.spotlightIsActive = False

		# Case 1: Center of the screen
		centerX = magnifier._SCREEN_WIDTH // 2
		centerY = magnifier._SCREEN_HEIGHT // 2

		result = magnifier._relativePos(centerX, centerY)
		self.assertIsInstance(result, tuple)
		self.assertEqual(len(result), 2)
		self.assertEqual(magnifier.lastScreenPosition, result)
		# The center should remain close to the center
		self.assertAlmostEqual(result[0], centerX, delta=100)
		self.assertAlmostEqual(result[1], centerY, delta=100)

		# Case 2: Spotlight mode
		magnifier.spotlightIsActive = True
		magnifier.spotlightZoom = 4.0
		result = magnifier._relativePos(centerX, centerY)
		self.assertIsInstance(result, tuple)
		self.assertEqual(len(result), 2)

		# Case 3: Clamping edges
		magnifier.spotlightIsActive = False
		visible_width = magnifier._SCREEN_WIDTH / magnifier.zoomLevel
		visible_height = magnifier._SCREEN_HEIGHT / magnifier.zoomLevel

		# Near borders
		result = magnifier._relativePos(50, 50)
		self.assertGreaterEqual(result[0], visible_width / 2)
		self.assertGreaterEqual(result[1], visible_height / 2)

		# Near the opposite edge
		result = magnifier._relativePos(magnifier._SCREEN_WIDTH - 50, magnifier._SCREEN_HEIGHT - 50)
		self.assertLessEqual(result[0], magnifier._SCREEN_WIDTH - visible_width / 2)
		self.assertLessEqual(result[1], magnifier._SCREEN_HEIGHT - visible_height / 2)

	def testSpotlight(self):
		"""Test : Spotlight mode activation."""
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

		magnifier._stopTimer = MagicMock()
		magnifier._getFocusCoordinates = MagicMock(return_value=(500, 400))
		magnifier._relativePos = MagicMock(return_value=(600, 500))
		magnifier._borderPos = MagicMock(return_value=(700, 600))
		magnifier._animateZoom = MagicMock()
		magnifier.zoomLevel = 2.0

		test_cases = [
			{
				"name": "Center mode",
				"mode": FullScreenMode.CENTER,
				"expected_pos": (500, 400),  # Coordinates from _getFocusCoordinates
				"should_call_relative": False,
				"should_call_border": False,
			},
			{
				"name": "Relative mode",
				"mode": FullScreenMode.RELATIVE,
				"expected_pos": (600, 500),  # Coordinates from _relativePos
				"should_call_relative": True,
				"should_call_border": False,
			},
			{
				"name": "Border mode",
				"mode": FullScreenMode.BORDER,
				"expected_pos": (700, 600),  # Coordinates from _borderPos
				"should_call_relative": False,
				"should_call_border": True,
			},
		]

		for case in test_cases:
			with self.subTest(mode=case["name"]):
				# Reset mocks
				magnifier._stopTimer.reset_mock()
				magnifier._getFocusCoordinates.reset_mock()
				magnifier._relativePos.reset_mock()
				magnifier._borderPos.reset_mock()
				magnifier._animateZoom.reset_mock()

				# Setup
				magnifier._fullscreenMode = case["mode"]

				# Test
				magnifier._spotlight()

				# Verification
				magnifier._stopTimer.assert_called_once()
				magnifier._getFocusCoordinates.assert_called_once()

				if case["should_call_relative"]:
					magnifier._relativePos.assert_called_once_with(500, 400)
					magnifier._borderPos.assert_not_called()
				elif case["should_call_border"]:
					magnifier._borderPos.assert_called_once_with(500, 400)
					magnifier._relativePos.assert_not_called()
				else:
					magnifier._relativePos.assert_not_called()
					magnifier._borderPos.assert_not_called()

				self.assertTrue(magnifier.spotlightIsActive)
				self.assertEqual(magnifier.spotlightZoom, 2.0)

				magnifier._animateZoom.assert_called_once()
				call_args = magnifier._animateZoom.call_args[0]
				self.assertEqual(call_args[0], 1.0)
				self.assertEqual(call_args[1], case["expected_pos"][0])
				self.assertEqual(call_args[2], case["expected_pos"][1])

	def testAnimateZoom(self):
		"""Test : Zoom animation setup."""
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

			magnifier._stopTimer = MagicMock()
			magnifier._startTimer = MagicMock()
			magnifier.zoomLevel = 2.0

			# Mock callback
			callbackMock = MagicMock()

			# Test animation setup
			magnifier._animateZoom(4.0, 800, 600, callback=callbackMock)

			magnifier._stopTimer.assert_called_once()
			magnifier._startTimer.assert_called_once_with(magnifier._onAnimationStep)
			self.assertEqual(magnifier._animationStep, 0)
			self.assertEqual(magnifier._animationSteps, 40)
			self.assertEqual(magnifier._animationStartZoom, 2.0)
			self.assertEqual(magnifier._animationDelta, (4.0 - 2.0) / 40)
			self.assertEqual(magnifier._animationTargetZoom, 4.0)
			self.assertEqual(magnifier._animationCenterX, 800)
			self.assertEqual(magnifier._animationCenterY, 600)
			self.assertEqual(magnifier._animationCallback, callbackMock)
			self.assertEqual(magnifier._animationInterval, 500 // 40)

	def testOnAnimationStep(self):
		"""Test : Animation step execution."""
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

		# Setup animation state
		magnifier._animationStep = 0
		magnifier._animationSteps = 10
		magnifier._animationStartZoom = 2.0
		magnifier._animationDelta = 0.2  # (4.0 - 2.0) / 10
		magnifier._animationCenterX = 500
		magnifier._animationCenterY = 400
		magnifier._animationInterval = 25

		# Setup mocks
		magnifier._fullscreenMagnifier = MagicMock()
		magnifier.timer = MagicMock()
		magnifier._finishAnimation = MagicMock()

		# Test 1: Animation step (not finished)
		magnifier._onAnimationStep()

		# Verifications
		expected_zoom = 2.2  # 2.0 + 0.2
		self.assertEqual(magnifier.zoomLevel, expected_zoom)
		self.assertEqual(magnifier._animationStep, 1)
		magnifier._fullscreenMagnifier.assert_called_once_with(500, 400)
		magnifier.timer.Start.assert_called_once_with(25, oneShot=True)
		magnifier._finishAnimation.assert_not_called()

		# Reset mocks
		magnifier._fullscreenMagnifier.reset_mock()
		magnifier.timer.reset_mock()

		# Test 2: Animation step finale
		magnifier._animationStep = 10
		magnifier._onAnimationStep()

		# Verifications
		magnifier._fullscreenMagnifier.assert_not_called()
		magnifier.timer.Start.assert_not_called()
		magnifier._finishAnimation.assert_called_once()

	def testOnAnimationStepProgression(self):
		"""Test : Animation progression through multiple steps."""
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

		magnifier._animationStep = 0
		magnifier._animationSteps = 3
		magnifier._animationStartZoom = 1.0
		magnifier._animationDelta = 0.5
		magnifier._animationCenterX = 300
		magnifier._animationCenterY = 200
		magnifier._animationInterval = 20

		magnifier._fullscreenMagnifier = MagicMock()
		magnifier.timer = MagicMock()
		magnifier._finishAnimation = MagicMock()

		for step in range(3):
			with self.subTest(animation_step=step):
				magnifier._onAnimationStep()

				expected_zoom = 1.0 + 0.5 * (step + 1)
				self.assertAlmostEqual(magnifier.zoomLevel, expected_zoom, places=2)
				self.assertEqual(magnifier._animationStep, step + 1)
				magnifier._fullscreenMagnifier.assert_called_with(300, 200)
				magnifier.timer.Start.assert_called_with(20, oneShot=True)
				magnifier._finishAnimation.assert_not_called()

				magnifier._fullscreenMagnifier.reset_mock()
				magnifier.timer.reset_mock()

		magnifier._onAnimationStep()
		magnifier._finishAnimation.assert_called_once()
		magnifier._fullscreenMagnifier.assert_not_called()
		magnifier.timer.Start.assert_not_called()

	def testFinishAnimation(self):
		"""Test : Animation completion."""
		with patch.object(FullScreenMagnifier, "_startMagnifier"):
			with patch.object(FullScreenMagnifier, "_applyColorFilter"):
				magnifier = FullScreenMagnifier()

		magnifier._animationTargetZoom = 3.5
		magnifier._animationCenterX = 600
		magnifier._animationCenterY = 450
		magnifier._fullscreenMagnifier = MagicMock()

		callbackMock = MagicMock()
		magnifier._animationCallback = callbackMock
		magnifier._finishAnimation()

		self.assertEqual(magnifier.zoomLevel, 3.5)
		magnifier._fullscreenMagnifier.assert_called_once_with(600, 450)
		callbackMock.assert_called_once()

		magnifier._fullscreenMagnifier.reset_mock()
		magnifier._animationCallback = None
		magnifier._finishAnimation()

		magnifier._fullscreenMagnifier.assert_called_once_with(600, 450)
