import ctypes
from ctypes import wintypes
from enum import Enum
from typing import Callable

from .windowsHandler import DockedFrame, LensFrame

from logHandler import log
import ui
import wx
import api

# Utils


class MouseHandler:
	def __init__(self):
		pass
		self._mousePosition: tuple[int, int] = (0, 0)

	@property
	def mousePosition(self):
		return self.getMousePosition()

	@mousePosition.setter
	def mousePosition(self, pos: tuple[int, int]):
		self._mousePosition = pos

	def getMousePosition(self) -> tuple[int, int]:
		"""
		Get the current mouse position as (x, y).
		"""
		pt = wintypes.POINT()
		ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
		return (pt.x, pt.y)

	def isLeftClickPressed(self) -> bool:
		"""
		Check if the left mouse button is currently pressed.
		"""
		# VK_LBUTTON = 0x01 (Virtual key code for left mouse button)
		# GetKeyState returns negative value if key is pressed
		return ctypes.windll.user32.GetKeyState(0x01) < 0


class ColorFilter(Enum):
	NORMAL = "normal"
	GREYSCALE = "greyscale"
	INVERTED = "inverted"


class FullScreenMode(Enum):
	CENTER = "center"
	BORDER = "border"
	RELATIVE = "relative"


class MagnifierType(Enum):
	FULLSCREEN = "fullscreen"
	DOCKED = "docked"
	LENS = "lens"


class ColorFilterMatrix(Enum):
	NORMAL = (ctypes.c_float * 25)(
		1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
	)

	GREYSCALE = (ctypes.c_float * 25)(
		0.33,
		0.33,
		0.33,
		0.0,
		0.0,
		0.59,
		0.59,
		0.59,
		0.0,
		0.0,
		0.11,
		0.11,
		0.11,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
	)

	INVERTED = (ctypes.c_float * 25)(
		-1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		-1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		-1.0,
		0.0,
		0.0,
		0.0,
		0.0,
		0.0,
		1.0,
		0.0,
		1.0,
		1.0,
		1.0,
		0.0,
		1.0,
	)


# Base Code


class NVDAMagnifier:
	_ZOOM_MIN: float = 1.0
	_ZOOM_MAX: float = 10.0
	_ZOOM_STEP: float = 0.5
	_TIMER_INTERVAL_MS: int = 20
	_MARGIN_BORDER: int = 50
	_SCREEN_WIDTH: int = ctypes.windll.user32.GetSystemMetrics(0)
	_SCREEN_HEIGHT: int = ctypes.windll.user32.GetSystemMetrics(1)

	def __init__(self, zoomLevel: float, colorFilter: ColorFilter):
		self._isActive: bool = False
		self._zoomLevel: float = zoomLevel
		self._timer: None | wx.Timer = None
		self._lastFocusedObject: str = ""
		self._lastNVDAPosition: tuple[int, int] = (0, 0)
		self._lastMousePosition: tuple[int, int] = (0, 0)
		self._lastScreenPosition: tuple[int, int] = (0, 0)
		self._currentCoordinates: tuple[int, int] = (0, 0)
		self._colorFilter: ColorFilter = colorFilter
		self._mouseHandler: MouseHandler = MouseHandler()

	# Properties

	@property
	def isActive(self) -> bool:
		return self._isActive

	@isActive.setter
	def isActive(self, value: bool) -> None:
		self._isActive = value

	@property
	def zoomLevel(self) -> float:
		return self._zoomLevel

	@zoomLevel.setter
	def zoomLevel(self, value: float) -> None:
		if self._ZOOM_MIN <= value <= self._ZOOM_MAX:
			self._zoomLevel = value

	@property
	def lastFocusedObject(self) -> str:
		return self._lastFocusedObject

	@lastFocusedObject.setter
	def lastFocusedObject(self, value: str) -> None:
		self._lastFocusedObject = value

	@property
	def lastNVDAPosition(self) -> tuple[int, int]:
		return self._lastNVDAPosition

	@lastNVDAPosition.setter
	def lastNVDAPosition(self, value: tuple[int, int]) -> None:
		self._lastNVDAPosition = value

	@property
	def lastMousePosition(self) -> tuple[int, int]:
		return self._lastMousePosition

	@lastMousePosition.setter
	def lastMousePosition(self, value: tuple[int, int]) -> None:
		self._lastMousePosition = value

	@property
	def lastScreenPosition(self) -> tuple[int, int]:
		return self._lastScreenPosition

	@lastScreenPosition.setter
	def lastScreenPosition(self, value: tuple[int, int]) -> None:
		self._lastScreenPosition = value

	@property
	def currentCoordinates(self) -> tuple[int, int]:
		return self._currentCoordinates

	@currentCoordinates.setter
	def currentCoordinates(self, value: tuple[int, int]) -> None:
		self._currentCoordinates = value

	@property
	def magnifierType(self) -> MagnifierType:
		return self._magnifierType

	@magnifierType.setter
	def magnifierType(self, value: MagnifierType) -> None:
		self._magnifierType = value

	@property
	def timer(self) -> wx.Timer | None:
		return self._timer

	@timer.setter
	def timer(self, value: wx.Timer | None) -> None:
		self._timer = value

	@property
	def colorFilter(self) -> ColorFilter:
		return self._colorFilter

	@colorFilter.setter
	def colorFilter(self, value: ColorFilter) -> None:
		self._colorFilter = value

	# Functions

	def _startMagnifier(self) -> None:
		"""Start the magnifier."""
		if self.isActive:
			return  # Already active
		self.isActive = True
		self.currentCoordinates = self._getFocusCoordinates()

	def _updateMagnifier(self) -> None:
		"""Update the magnifier position and content."""
		if not self.isActive:
			return
		self.currentCoordinates = self._getFocusCoordinates()
		self._doUpdate()
		self._startTimer(self._updateMagnifier)

	def _doUpdate(self) -> None:
		"""Perform the actual update of the magnifier."""
		raise NotImplementedError("Subclasses must implement this method.")

	def _stopMagnifier(self) -> None:
		"""Stop the magnifier."""
		if not self.isActive:
			return
		self._stopTimer()
		self.isActive = False

	def _zoom(self, direction: bool) -> None:
		"""Adjust the zoom level of the magnifier.

		:param direction: True to zoom in, False to zoom out.
		"""
		if direction:
			self.zoomLevel += self._ZOOM_STEP
			ui.message(
				_(
					# Translators: Message announced when zooming in with {mode} being the target zoom level
					"Zooming in with {mode} level"
				).format(mode=self.zoomLevel)
			)
		else:
			self.zoomLevel -= self._ZOOM_STEP
			ui.message(
				_(
					# Translators: Message announced when zooming out with {mode} being the target zoom level
					"Zooming out with {mode} level"
				).format(mode=self.zoomLevel)
			)

	def _startTimer(self, callback: Callable[[], None] = None) -> None:
		"""Start the timer with a callback function.

		:param callback: The function to call when the timer expires.
		"""
		self._stopTimer()
		self.timer = wx.Timer()
		self.timer.Bind(wx.EVT_TIMER, lambda evt: callback())
		self.timer.Start(self._TIMER_INTERVAL_MS, oneShot=True)

	def _stopTimer(self) -> None:
		"""Stop timer execution."""
		if self.timer:
			if self.timer.IsRunning():
				self.timer.Stop()
			self.timer = None
		else:
			log.info("no timer to stop")

	def _getMagnifierPosition(self, x: int, y: int) -> tuple[int, int, int, int]:
		"""
		Compute the top-left corner of the magnifier window centered on (x, y).

		Args:
			x, y: Focus coordinates
			targetWidth, targetHeight: Target size (defaults to screen size for fullscreen)
		Returns:
			left, top, visibleWidth, visibleHeight: The position and size of the magnifier window.
		"""

		# Calculate the size of the capture area at the current zoom level
		visibleWidth = self._SCREEN_WIDTH / self.zoomLevel
		visibleHeight = self._SCREEN_HEIGHT / self.zoomLevel

		# Compute the top-left corner so that (x, y) is at the center
		left = int(x - (visibleWidth / 2))
		top = int(y - (visibleHeight / 2))

		# Clamp to screen boundaries
		left = max(0, min(left, int(self._SCREEN_WIDTH - visibleWidth)))
		top = max(0, min(top, int(self._SCREEN_HEIGHT - visibleHeight)))

		return (left, top, int(visibleWidth), int(visibleHeight))

	def _getNvdaPosition(self) -> tuple[int, int]:
		"""
		Get the current review position as (x, y), falling back to navigator object if needed.
		Tries to get the review position from NVDA's API, or the center of the navigator object.
		This part is taken from NVDA+shift+m gesture.

		Returns:
			tuple[int, int]: The (x, y) coordinates of the NVDA position.
		"""
		# Try to get the current review position object from NVDA's API
		reviewPosition = api.getReviewPosition()
		if reviewPosition:
			try:
				# Try to get the point at the start of the review position
				point = reviewPosition.pointAtStart
				return point.x, point.y
			except (NotImplementedError, LookupError, AttributeError):
				# If that fails, fall through to try navigator object
				pass

		# Fallback: try to use the navigator object location
		navigatorObject = api.getNavigatorObject()
		try:
			# Try to get the bounding rectangle of the navigator object
			left, top, width, height = navigatorObject.location
			# Calculate the center point of the rectangle
			x = left + (width // 2)
			y = top + (height // 2)
			return x, y
		except Exception:
			# If no location is found, log this and return (0, 0)
			return 0, 0

	def _getFocusCoordinates(self) -> tuple[int, int]:
		"""
		Return position (x,y) of current focus element.

		Returns:
			tuple[int, int]: The (x, y) coordinates of the focus element.
		"""
		nvdaPosition = self._getNvdaPosition()
		mousePosition = self._mouseHandler.mousePosition
		# Check if left mouse button is pressed
		isClickPressed = self._mouseHandler.isLeftClickPressed()

		# Always update positions in background (keep them synchronized)
		nvdaChanged = self.lastNVDAPosition != nvdaPosition
		mouseChanged = self.lastMousePosition != mousePosition

		if nvdaChanged:
			self.lastNVDAPosition = nvdaPosition
		if mouseChanged:
			self.lastMousePosition = mousePosition

		# During drag & drop, force focus on mouse
		if isClickPressed:
			self.lastFocusedObject = "mouse"
			return mousePosition

		# Check mouse first (mouse has priority) - when not dragging
		if mouseChanged:
			self.lastFocusedObject = "mouse"
			return mousePosition

		# Then check NVDA (only change focus if mouse didn't move)
		if nvdaChanged:
			self.lastFocusedObject = "nvda"
			return nvdaPosition

		# Return current position of the focused object (no changes detected)
		if self.lastFocusedObject == "nvda":
			return nvdaPosition
		elif self.lastFocusedObject == "mouse":
			return mousePosition
		else:
			return mousePosition


class FullScreenMagnifier(NVDAMagnifier):
	def __init__(
		self,
		zoomLevel: float = 2.0,
		colorFilter: ColorFilter = ColorFilter.NORMAL,
		fullscreenMode: FullScreenMode = FullScreenMode.CENTER,
	):
		super().__init__(zoomLevel=zoomLevel, colorFilter=colorFilter)
		self._magnifierType = MagnifierType.FULLSCREEN
		self._fullscreenMode = fullscreenMode
		self._currentCoordinates: tuple[int, int] = (0, 0)
		self._startMagnifier()
		self._applyColorFilter()

	@property
	def fullscreenMode(self) -> FullScreenMode:
		return self._fullscreenMode

	@fullscreenMode.setter
	def fullscreenMode(self, value: FullScreenMode) -> None:
		self._fullscreenMode = value

	@property
	def currentCoordinates(self) -> tuple[int, int]:
		return self._currentCoordinates

	@currentCoordinates.setter
	def currentCoordinates(self, value: tuple[int, int]) -> None:
		self._currentCoordinates = value

	def _startMagnifier(self) -> None:
		"""Start the Fullscreen magnifier using windows DLL."""
		super()._startMagnifier()
		self._loadMagnifierApi()
		self._startTimer(self._updateMagnifier)

	def _doUpdate(self):
		"""Perform the actual update of the magnifier."""
		# Calculate new position based on focus mode
		x, y = self._getCoordinatesForMode(self.currentCoordinates)
		# Always save screen position for mode continuity
		self.lastScreenPosition = (x, y)
		# Apply transformation
		self._fullscreenMagnifier(x, y)

	def _stopMagnifier(self) -> None:
		"""Stop the Fullscreen magnifier using windows DLL."""
		super()._stopMagnifier()
		# reset color filter of fullscreen to normal
		ctypes.windll.magnification.MagSetFullscreenColorEffect(ColorFilterMatrix.NORMAL.value)
		try:
			# Get MagSetFullscreenTransform function from magnification API
			MagSetFullscreenTransform = self._getMagnificationApi()
			# Reset fullscreen magnifier: 1.0 zoom, 0,0 position
			MagSetFullscreenTransform(ctypes.c_float(1.0), ctypes.c_int(0), ctypes.c_int(0))
		except AttributeError:
			log.info("Magnification API not available")
		self._stopMagnifierApi()

	def _applyColorFilter(self) -> None:
		"""Apply the current color filter to the fullscreen magnifier."""
		if self.colorFilter == ColorFilter.NORMAL:
			ctypes.windll.magnification.MagSetFullscreenColorEffect(ColorFilterMatrix.NORMAL.value)
		elif self.colorFilter == ColorFilter.GREYSCALE:
			ctypes.windll.magnification.MagSetFullscreenColorEffect(ColorFilterMatrix.GREYSCALE.value)
		elif self.colorFilter == ColorFilter.INVERTED:
			ctypes.windll.magnification.MagSetFullscreenColorEffect(ColorFilterMatrix.INVERTED.value)
		else:
			log.info(f"Unknown color filter: {self.colorFilter}")

	def _loadMagnifierApi(self) -> None:
		"""Initialize the Magnification API."""
		try:
			# Attempt to access the magnification DLL
			ctypes.windll.magnification
		except Exception as e:
			# If the DLL is not available, log this and exit the function
			log.error(f"Magnification API not available with error {e}")
			return
		# Try to initialize the magnification API
		# MagInitialize returns 0 if already initialized or on failure
		if ctypes.windll.magnification.MagInitialize() == 0:
			log.info("Magnification API already initialized")
			return
		# If initialization succeeded, log success
		log.info("Magnification API initialized")

	def _stopMagnifierApi(self) -> None:
		"""Stop the Magnification API."""
		try:
			ctypes.windll.magnification
		except Exception as e:
			log.error(f"Magnification API not available with error {e}")
			return
		if ctypes.windll.magnification.MagUninitialize() == 0:
			log.info("Magnification API already uninitialized")
			return
		log.info("Magnification API uninitialized")

	def _getMagnificationApi(self):
		"""Get Windows Magnification API function."""
		MagSetFullscreenTransform = ctypes.windll.magnification.MagSetFullscreenTransform
		MagSetFullscreenTransform.restype = wintypes.BOOL
		MagSetFullscreenTransform.argtypes = [ctypes.c_float, ctypes.c_int, ctypes.c_int]
		return MagSetFullscreenTransform

	def _fullscreenMagnifier(self, x: int, y: int) -> None:
		"""Apply fullscreen magnification at given coordinates.

		:param x: The x-coordinate for the magnifier.
		:param y: The y-coordinate for the magnifier.
		"""
		left, top, visibleWidth, visibleHeight = self._getMagnifierPosition(x, y)
		try:
			MagSetFullscreenTransform = self._getMagnificationApi()
			result = MagSetFullscreenTransform(
				ctypes.c_float(self.zoomLevel), ctypes.c_int(left), ctypes.c_int(top)
			)
			if not result:
				log.info("Failed to set fullscreen transform")
		except AttributeError:
			log.info("Magnification API not available")

	def _getCoordinatesForMode(self, coordinates: tuple[int, int]) -> tuple[int, int]:
		"""Get coordinates adjusted for the current fullscreen mode.

		Args:
			coordinates: Raw coordinates (x, y)

		Returns:
			Adjusted coordinates according to fullscreen mode
		"""
		x, y = coordinates

		if self._fullscreenMode == FullScreenMode.RELATIVE:
			return self._relativePos(x, y)
		elif self._fullscreenMode == FullScreenMode.BORDER:
			# For border mode, use the current position as reference
			return self._borderPos(x, y)
		else:  # CENTER mode
			return coordinates

	def _borderPos(self, focusX: int, focusY: int) -> tuple[int, int]:
		"""
		Check if focus is near magnifier border and adjust position accordingly.
		Returns adjusted position to keep focus within margin limits.

		Args:
			focusX (int): The x-coordinate of the focus point.
			focusY (int): The y-coordinate of the focus point.

		Returns:
			lastScreenPosition (tuple[int, int]): The adjusted position (x, y) of the focus point.
		"""

		lastLeft, lastTop, visibleWidth, visibleHeight = self._getMagnifierPosition(
			self.lastScreenPosition[0], self.lastScreenPosition[1]
		)

		minX = lastLeft + self._MARGIN_BORDER
		maxX = lastLeft + visibleWidth - self._MARGIN_BORDER
		minY = lastTop + self._MARGIN_BORDER
		maxY = lastTop + visibleHeight - self._MARGIN_BORDER

		dx = 0
		dy = 0

		if focusX < minX:
			dx = focusX - minX
		elif focusX > maxX:
			dx = focusX - maxX

		if focusY < minY:
			dy = focusY - minY
		elif focusY > maxY:
			dy = focusY - maxY

		if dx != 0 or dy != 0:
			return self.lastScreenPosition[0] + dx, self.lastScreenPosition[1] + dy
		else:
			return self.lastScreenPosition

	def _relativePos(self, mouseX: int, mouseY: int) -> tuple[int, int]:
		"""
		Calculate magnifier center maintaining mouse relative position.
		Handles screen edges to prevent going off-screen.

		Args:
			mouseX (int): The x-coordinate of the mouse pointer.
			mouseY (int): The y-coordinate of the mouse pointer.

		Returns:
			tuple[int, int]: The (x, y) coordinates of the magnifier center.
		"""
		if (
			hasattr(self, "_spotlightManager")
			and self._spotlightManager
			and self._spotlightManager._spotlightIsActive
		):
			zoom = self._spotlightManager._originalZoomLevel
		else:
			zoom = self.zoomLevel

		screenWidth = self._SCREEN_WIDTH
		screenHeight = self._SCREEN_HEIGHT
		visibleWidth = screenWidth / zoom
		visibleHeight = screenHeight / zoom
		margin = int(zoom * 10)

		# Calculate left/top maintaining mouse relative position
		left = mouseX - (mouseX / screenWidth) * (visibleWidth - margin)
		top = mouseY - (mouseY / screenHeight) * (visibleHeight - margin)

		# Clamp to screen boundaries
		left = max(0, min(left, screenWidth - visibleWidth))
		top = max(0, min(top, screenHeight - visibleHeight))

		# Return center of zoom window
		centerX = int(left + visibleWidth / 2)
		centerY = int(top + visibleHeight / 2)
		self.lastScreenPosition = (centerX, centerY)
		return self.lastScreenPosition

	def _startSpotlight(self) -> None:
		if (
			hasattr(self, "_spotlightManager")
			and self._spotlightManager
			and self._spotlightManager._spotlightIsActive
		):
			ui.message(
				_(
					# Translators: Message announced when trying to start spotlight mode while it's already active
					"Spotlight mode is already active"
				)
			)
			return
		self._stopTimer()
		self._spotlightManager = SpotlightManager(self)
		self._spotlightManager._startSpotlight()

	def _stopSpotlight(self) -> None:
		self._spotlightManager = None
		self._startTimer(self._updateMagnifier)


class SpotlightManager:
	def __init__(self, fullscreenMagnifier: FullScreenMagnifier):
		self._fullscreenMagnifier: FullScreenMagnifier = fullscreenMagnifier
		self._spotlightIsActive: bool = False
		self._lastMousePosition: tuple[int, int] = (0, 0)
		self._timer: wx.CallLater | None = None
		self._animationSteps: int = 40
		self._currentCoordinates: tuple[int, int] = fullscreenMagnifier._getFocusCoordinates()
		self._originalZoomLevel: float = fullscreenMagnifier.zoomLevel
		self._currentZoomLevel: float = fullscreenMagnifier.zoomLevel

	def _startSpotlight(self) -> None:
		"""Start the spotlight."""
		log.info("start spotlight")
		ui.message(
			_(
				# Translators: Message announced when starting the magnifier spotlight
				"Magnifier spotlight started"
			)
		)

		self._spotlightIsActive = True

		startCoords = self._fullscreenMagnifier._getFocusCoordinates()
		startCoords = self._fullscreenMagnifier._getCoordinatesForMode(startCoords)
		centerScreen = (
			self._fullscreenMagnifier._SCREEN_WIDTH // 2,
			self._fullscreenMagnifier._SCREEN_HEIGHT // 2,
		)

		self._currentCoordinates = startCoords
		self._animateZoom(1.0, centerScreen, self._startMouseMonitoring)

	def _stopSpotlight(self) -> None:
		"""Stop the spotlight."""
		log.info("stop spotlight")
		ui.message(
			_(
				# Translators: Message announced when stopping the magnifier spotlight
				"Magnifier spotlight stopped"
			)
		)
		if self._timer:
			self._timer.Stop()
			self._timer = None

		self._spotlightIsActive = False
		self._fullscreenMagnifier._stopSpotlight()

	def _animateZoom(
		self, targetZoom: float, targetCoordinates: tuple[int, int], callback: Callable[[], None]
	) -> None:
		"""Animate the zoom level change."""
		self._animationStepsList = self._computeAnimationSteps(
			self._currentZoomLevel, targetZoom, self._currentCoordinates, targetCoordinates
		)

		self._executeStep(0, callback)

	def _executeStep(self, stepIndex: int, callback: Callable[[], None]) -> None:
		"""Execute one animation step."""

		if stepIndex < len(self._animationStepsList):
			zoomLevel, (x, y) = self._animationStepsList[stepIndex]
			self._fullscreenMagnifier.zoomLevel = zoomLevel
			self._fullscreenMagnifier._fullscreenMagnifier(x, y)
			self._currentZoomLevel = zoomLevel
			self._currentCoordinates = (x, y)
			wx.CallLater(12, lambda: self._executeStep(stepIndex + 1, callback))
		else:
			if callback:
				callback()

	def _startMouseMonitoring(self) -> None:
		self._lastMousePosition = wx.GetMousePosition()
		self._timer = wx.CallLater(2000, self._checkMouseIdle)

	def _checkMouseIdle(self) -> None:
		currentMousePosition = wx.GetMousePosition()
		if currentMousePosition == self._lastMousePosition:
			self._currentCoordinates = (
				self._fullscreenMagnifier._SCREEN_WIDTH // 2,
				self._fullscreenMagnifier._SCREEN_HEIGHT // 2,
			)
			endCoordinates = self._fullscreenMagnifier._getCoordinatesForMode(self._lastMousePosition)

			self._animateZoom(self._originalZoomLevel, endCoordinates, self._stopSpotlight)
		else:
			self._lastMousePosition = currentMousePosition
			self._timer = wx.CallLater(1500, self._checkMouseIdle)

	def _computeAnimationSteps(
		self,
		zoomStart: float,
		zoomEnd: float,
		coordinateStart: tuple[int, int],
		coordinateEnd: tuple[int, int],
	) -> list[tuple[float, tuple[int, int]]]:
		"""Compute all intermediate animation steps with zoom levels and coordinates.

		Args:
			zoomStart: Starting zoom level
			zoomEnd: Ending zoom level
			coordinateStart: Starting coordinates (x, y)
			coordinateEnd: Ending coordinates (x, y)

		Returns:
			List of animation steps as [zoomLevel, (x, y)] for each animation step
		"""
		startX, startY = coordinateStart
		endX, endY = coordinateEnd
		animationSteps = []

		zoomDelta = (zoomEnd - zoomStart) / self._animationSteps
		coordDeltaX = (endX - startX) / self._animationSteps
		coordDeltaY = (endY - startY) / self._animationSteps

		for step in range(1, self._animationSteps + 1):
			currentZoom = zoomStart + zoomDelta * step

			currentX = startX + coordDeltaX * step
			currentY = startY + coordDeltaY * step

			animationSteps.append((round(currentZoom, 2), (int(round(currentX)), int(round(currentY)))))
		return animationSteps


class DockedMagnifier(NVDAMagnifier):
	def __init__(self, zoomLevel: float = 2.0, colorFilter: ColorFilter = ColorFilter.NORMAL):
		super().__init__(zoomLevel=zoomLevel, colorFilter=colorFilter)
		self._magnifierType: MagnifierType = MagnifierType.DOCKED
		self._dockedFrame: DockedFrame = DockedFrame()
		self._startMagnifier()

	def _startMagnifier(self):
		super()._startMagnifier()
		self._dockedFrame.Show()
		self._dockedFrame.startMagnifying(self._mouseHandler.getMousePosition(), self.colorFilter.value)
		self._startTimer(self._updateMagnifier)

	def _doUpdate(self):
		x, y = self.currentCoordinates
		mouseCoordinates = self._mouseHandler.getMousePosition()
		self._dockedFrame.updateMagnifier(x, y, self.zoomLevel, mouseCoordinates, self.colorFilter.value)

	def _stopMagnifier(self):
		super()._stopMagnifier()
		self._dockedFrame.stopMagnifying()


class LensMagnifier(NVDAMagnifier):
	def __init__(self, zoomLevel: float = 2.0, colorFilter: ColorFilter = ColorFilter.NORMAL):
		super().__init__(zoomLevel=zoomLevel, colorFilter=colorFilter)
		self._magnifierType: MagnifierType = MagnifierType.LENS
		self._lensFrame: LensFrame = LensFrame()
		self._startMagnifier()

	def _startMagnifier(self):
		super()._startMagnifier()
		self._lensFrame.Show()
		self._lensFrame.startMagnifying(self.colorFilter.value)
		self._startTimer(self._updateMagnifier)

	def _doUpdate(self):
		x, y = self._mouseHandler.getMousePosition()
		self._lensFrame.updateMagnifier(x, y, self.zoomLevel, self.colorFilter.value)

	def _stopMagnifier(self):
		super()._stopMagnifier()
		self._lensFrame.stopMagnifying()
