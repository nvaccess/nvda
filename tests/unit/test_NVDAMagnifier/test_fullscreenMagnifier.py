from numpy import test
import NVDAMagnifier
import unittest
from unittest.mock import MagicMock, Mock, patch
import wx
import ctypes

from NVDAMagnifier import ColorFilter, ColorFilterMatrix, FullScreenMagnifier, FullScreenMode



class TestFullScreenMagnifier(unittest.TestCase):



	@classmethod
	def setUpClass(cls):
		"""
		Setup qui s'exécute une fois au début.
		"""
		if not wx.GetApp():
			cls.app = wx.App(False)


	@patch.object(FullScreenMagnifier, '_startMagnifier')
	@patch.object(FullScreenMagnifier,'_applyColorFilter')
	def testFullScreenMagnifierCreation(self, mock_apply_color_filter, mock_start_magnifier):
		"""Test : Creating the fullscreen magnifier."""
		zoomDefault = 2.0
		colorDefault = ColorFilter.NORMAL
		fullscreenModeDefault = FullScreenMode.CENTER
		
		def testValues(magnifier: FullScreenMagnifier, zoomPassed: float = zoomDefault, colorFilterPassed: ColorFilter = colorDefault, fullscreenModePassed: FullScreenMode = fullscreenModeDefault):
			self.assertEqual(magnifier.zoomLevel, zoomPassed)
			self.assertEqual(magnifier.colorFilter, colorFilterPassed)
			self.assertEqual(magnifier.fullscreenMode, fullscreenModePassed)
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
		magnifier = FullScreenMagnifier(zoomLevel=4.0, colorFilter=ColorFilter.GREYSCALE, fullscreenMode=FullScreenMode.BORDER)
		testValues(magnifier, zoomPassed=4.0, colorFilterPassed=ColorFilter.GREYSCALE, fullscreenModePassed=FullScreenMode.BORDER)



	def testStartFullScreenMagnifier(self):
		"""Test : Activating and deactivating the fullscreen magnifier."""
		with patch.object(FullScreenMagnifier, '_startMagnifier'):
			with patch.object(FullScreenMagnifier, '_applyColorFilter'):
				magnifier = FullScreenMagnifier()
		
		magnifier._loadMagnifierApi = MagicMock()
		magnifier._startTimer = MagicMock()

		magnifier._startMagnifier()
		magnifier._loadMagnifierApi.assert_called_once()
		magnifier._startTimer.assert_called_once()
		self.assertTrue(magnifier.isActive)

	def testFullScreenDoUpdate(self):
		"""Test : Updating the magnifier"""
		with patch.object(FullScreenMagnifier, '_startMagnifier'):
			with patch.object(FullScreenMagnifier, '_applyColorFilter'):
				magnifier = FullScreenMagnifier()

		def initValues(currentCoordinates: tuple[int,int], mode: FullScreenMode, lastFocusedObject: str):
			magnifier.currentCoordinates = currentCoordinates
			magnifier.lastScreenPosition = (0,0)
			magnifier.fullscreenMode = mode
			magnifier.lastFocusedObject = lastFocusedObject
			magnifier._borderPos = MagicMock(return_value=(20, 20))
			magnifier._relativePos = MagicMock(return_value=(30, 30))
			magnifier._fullscreenMagnifier = MagicMock()

		def testValues(x,y):
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
	
		initValues((10,10), FullScreenMode.CENTER, "nvda")
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
		with patch.object(FullScreenMagnifier, '_startMagnifier'):
			with patch.object(FullScreenMagnifier, '_applyColorFilter'):
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
			ctypes.windll.magnification.MagSetFullscreenColorEffect.assert_called_once_with(colorFilterMatrix.value)

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
		with patch.object(FullScreenMagnifier, '_startMagnifier'):
			with patch.object(FullScreenMagnifier, '_applyColorFilter'):
				magnifier = FullScreenMagnifier()

		with patch.object(magnifier, '_getMagnifierPosition', return_value=(10, 20, 100, 200)):
			
			# Test 1: Try block exécuté normalement
			with patch.object(magnifier, '_getMagnificationApi') as mock_get_api:
				with patch('logHandler.log') as mock_log:
					mock_api_func = Mock(return_value=True)
					mock_get_api.return_value = mock_api_func
					
					magnifier._fullscreenMagnifier(100, 200)
					
					# Vérifier que le try block s'exécute
					mock_get_api.assert_called_once()
					mock_api_func.assert_called_once()
					mock_log.info.assert_not_called()  # Pas d'erreur
			
			# Test 2: Except AttributeError déclenché
			with patch.object(magnifier, '_getMagnificationApi', side_effect=AttributeError()):
				with patch('logHandler.log') as mock_log:
					
					magnifier._fullscreenMagnifier(100, 200)
					
					# Vérifier que l'except est exécuté
					mock_log.info.assert_called_once_with("Magnification API not available")

			# Test 3: API retourne False (dans le if not result)
			with patch.object(magnifier, '_getMagnificationApi') as mock_get_api:
				with patch('logHandler.log') as mock_log:
					mock_api_func = Mock(return_value=False)  # Échec
					mock_get_api.return_value = mock_api_func
					
					magnifier._fullscreenMagnifier(100, 200)
					
					# Vérifier que le if not result est exécuté
					mock_log.info.assert_called_once_with("Failed to set fullscreen transform")

	def testBorderPosRealWorld(self):
		"""Test : Border position with realistic screen values."""
		with patch.object(FullScreenMagnifier, '_startMagnifier'):
			with patch.object(FullScreenMagnifier, '_applyColorFilter'):
				magnifier = FullScreenMagnifier()


		magnifier._SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
		magnifier._SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)
		magnifier._MARGIN_BORDER = 50
		magnifier.lastScreenPosition = (960, 540)  # Centre écran
		magnifier.zoomLevel = 2.0
		
		with patch.object(magnifier, '_getMagnifierPosition', return_value=(480, 270, 960, 540)):

			test_cases = [
				{"focus": (960, 540), "expected": (960, 540), "desc": "Perfect center"},
				{"focus": (100, 100), "expected": (480, 270), "desc": "Far top-left corner"},
				{"focus": (1800, 900), "expected": (1420, 730), "desc": "Far bottom-right"},
				{"focus": (580, 540), "expected": (960, 540), "desc": "Exactly on left border"},
				{"focus": (579, 540), "expected": (959, 540), "desc": "Just outside left border"}
			]
			
			for case in test_cases:
				with self.subTest(focus=case["focus"]):
					result = magnifier._borderPos(case["focus"][0], case["focus"][1])
					self.assertEqual(result, case["expected"], case["desc"])

# À ajouter DANS la classe TestFullScreenMagnifier (avec indentation correcte) :

	def testRelativePos(self):
		"""Test : Relative position calculation."""
		with patch.object(FullScreenMagnifier, '_startMagnifier'):
			with patch.object(FullScreenMagnifier, '_applyColorFilter'):
				magnifier = FullScreenMagnifier()

		magnifier._SCREEN_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
		magnifier._SCREEN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)
		magnifier.zoomLevel = 2.0
		magnifier.spotlightIsActive = False
		x = magnifier._SCREEN_WIDTH
		y = magnifier._SCREEN_HEIGHT

		result = magnifier._relativePos(x,y)
		self.assertIsInstance(result, tuple)
		self.assertEqual(len(result), 2)
		self.assertEqual(magnifier.lastScreenPosition, result)

		magnifier.spotlightIsActive = True
		magnifier.spotlightZoom = 4.0
		result = magnifier._relativePos(x,y)
		self.assertIsInstance(result, tuple)

		magnifier.spotlightIsActive = False
		result = magnifier._relativePos(50, 50)
		self.assertGreaterEqual(result[0], 480)  # Minimum possible
		self.assertGreaterEqual(result[1], 270)  # Minimum possible
