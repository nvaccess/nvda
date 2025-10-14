import ctypes
from ctypes import wintypes
from enum import Enum
from logging import PlaceHolder
from sys import settrace

from .windowsHandler import DockedFrame, LensFrame

from logHandler import log
import ui
import wx
import api

# Utils

def getScreenSize() -> tuple[int, int]:
	"""Return screen width and height."""
	screenWidth, screenHeight = (
		ctypes.windll.user32.GetSystemMetrics(0),
		ctypes.windll.user32.GetSystemMetrics(1),
	)
	return screenWidth, screenHeight

class MouseHandler:
	def __init__(self):
		pass
		# not using this yet
		# self._mousePosition: tuple[int, int] = (0, 0)

	@property
	def mousePosition(self):
		# return self._mousePosition
		return self.getMousePosition()

	# @mousePosition.setter
	# def mousePosition(self, pos: tuple[int, int]):
	# 	self._mousePosition = pos

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
	_SCREEN_WIDTH: int = getScreenSize()[0]
	_SCREEN_HEIGHT: int = getScreenSize()[1]

	def __init__(self, zoomLevel: float, colorFilter: ColorFilter):
		self._isActive: bool = False
		self._zoomLevel: float = zoomLevel
		self._timer: None | wx.Timer = None
		self._lastFocusedObject: str = ""
		self._lastNVDAPosition: tuple[int, int] = (0, 0)
		self._lastMousePosition: tuple[int, int] = (0, 0)
		self._lastScreenPosition: tuple[int, int] = (0, 0)
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
		self._applyColorFilter()

# Functions

	def _startMagnifier(self) -> None:
		"""Start the magnifier.
		"""
		if self.isActive:
			return # Already active
		self.isActive = True
		self.currentCoordinates = self._getFocusCoordinates()

	def _updateMagnifier(self) -> None:
		"""Update the magnifier position and content."""
		if not self.isActive: 
			return
		self.currentCoordinates = self._getFocusCoordinates()
		
	def _stopMagnifier(self) -> None:
		"""Stop the magnifier.
		"""
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
		else:
			self.zoomLevel -= self._ZOOM_STEP

	def _startTimer(self, callback: None) -> None:
		"""Start the timer with a callback function.

		:param callback: The function to call when the timer expires.
		"""
		self._stopTimer()
		self.timer = wx.Timer()
		self.timer.Bind(wx.EVT_TIMER, lambda evt: callback())
		self.timer.Start(self._TIMER_INTERVAL_MS, oneShot=True)

	def _continueTimer(self, callback: None) -> None:
		"""Continue timer execution with a new callback.

		:param callback: The function to call when the timer expires.
		"""
		if self.timer and self.timer.IsRunning():
			self.timer.Stop()
		self.timer = wx.Timer()
		self.timer.Bind(wx.EVT_TIMER, lambda evt: callback())
		self.timer.Start(self._TIMER_INTERVAL_MS, oneShot=True)

	def _stopTimer(self) -> None:
		"""Stop timer execution.
		"""
		if self.timer and self.timer.IsRunning():
			self.timer.Stop()
			self.timer = None

	def _getMagnifierPosition(self,
		x: int, 
		y: int
	) -> tuple[int, int, int, int]:
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
		mousePosition = self._mouseHandler.getMousePosition()

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
	def __init__(self, zoomLevel: float, colorFilter: ColorFilter, fullscreenMode: FullScreenMode):
		super().__init__(zoomLevel=zoomLevel, colorFilter=colorFilter)
		self._magnifierType = MagnifierType.FULLSCREEN
		self._fullscreenMode = fullscreenMode
		self._currentCoordinates: tuple[int,int] = (0, 0)
		self._spotlightIsActive = False
		self._spotlightLastMousePosition: tuple[int, int] = (0, 0)
		self._spotlightZoom: float = 1.0
		self._spotlightTimer: wx.Timer | None = None
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

	@property
	def spotlightIsActive(self) -> bool:
		return self._spotlightIsActive

	@spotlightIsActive.setter
	def spotlightIsActive(self, value: bool) -> None:
		self._spotlightIsActive = value

	@property
	def spotlightLastMousePosition(self) -> tuple[int, int]:
		return self._spotlightLastMousePosition

	@spotlightLastMousePosition.setter
	def spotlightLastMousePosition(self, value: tuple[int, int]) -> None:
		self._spotlightLastMousePosition = value

	@property
	def spotlightZoom(self) -> float:
		return self._spotlightZoom

	@spotlightZoom.setter
	def spotlightZoom(self, value: float) -> None:
		self._spotlightZoom = value

	@property
	def spotlightTimer(self) -> wx.Timer | None:
		return self._spotlightTimer

	@spotlightTimer.setter
	def spotlightTimer(self, value: wx.Timer | None) -> None:
		self._spotlightTimer = value

	def _startMagnifier(self) -> None:
		"""Start the Fullscreen magnifier using windows DLL.
		"""
		super()._startMagnifier()
		self._loadMagnifierApi()
		self._startTimer(self._updateMagnifier)

	def _updateMagnifier(self) -> None:
		
		super()._updateMagnifier()
		# Calculate new position based on focus mode
		if self.fullscreenMode == FullScreenMode.CENTER:
			x, y = self.currentCoordinates
		elif self.fullscreenMode == FullScreenMode.BORDER:
			if self.lastFocusedObject == "nvda":
				x, y = self.currentCoordinates
			else:
				x, y = self._borderPos(self.currentCoordinates[0], self.currentCoordinates[1])
		elif self.fullscreenMode == FullScreenMode.RELATIVE:
			x, y = self._relativePos(self.currentCoordinates[0], self.currentCoordinates[1])
		else:
			x, y = self.currentCoordinates

		# Always save screen position for mode continuity
		self.lastScreenPosition = (x, y)
		# Apply transformation
		self._fullscreenMagnifier(x, y)

		# Continue loop
		self._continueTimer(self._updateMagnifier)

	def _stopMagnifier(self) -> None:
		"""Stop the Fullscreen magnifier using windows DLL.
		"""
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
		if self.spotlightIsActive:
			zoom = self.spotlightZoom
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
	
	def _spotlight(self) -> None:
		"""Activate spotlight mode for the magnifier.
		"""
		self._stopTimer()

		centerX, centerY = self._getFocusCoordinates()

		if self._fullscreenMode == FullScreenMode.RELATIVE:
			centerX, centerY = self._relativePos(centerX, centerY)
		elif self._fullscreenMode == FullScreenMode.BORDER:
			centerX, centerY = self._borderPos(centerX, centerY)

		self.spotlightIsActive = True
		self.spotlightZoom = self.zoomLevel

		def checkMouseIdle() -> None:
			"""Check if the mouse is moving to keep spotlight active."""
			currentPos = self.lastMousePosition
			if currentPos != self.spotlightLastMousePosition:
				self.spotlightLastMousePosition = currentPos
				self.lastMousePosition = currentPos
				self.spotlightTimer = wx.CallLater(1000, checkMouseIdle)
			else:
				restoreZoom()

		def restoreZoom() -> None:
			"""Restore zoom level and position after spotlight."""
			if self.spotlightTimer and self.spotlightTimer.IsRunning():
				self.spotlightTimer.Stop()
				self.spotlightTimer = None

			x, y = self._mouseHandler.getMousePosition()
			if self._fullscreenMode == FullScreenMode.RELATIVE:
				x, y = self._relativePos(x, y)
			else:
				self.lastScreenPosition = (x, y)
			self.spotlightIsActive = False

			def restartAfterAnimation() -> None:
				# Restart fullscreen timer
				self._startTimer(self._updateMagnifier)

			self._animateZoom(self.spotlightZoom, x, y, callback=restartAfterAnimation)

		self._animateZoom(1.0, centerX, centerY, callback=lambda: wx.CallLater(2000, checkMouseIdle))

	def _animateZoom(self, targetZoom: float, centerX: int, centerY: int, callback=None) -> None:
		"""Animate zoom smoothly using magnifierTimer.

		:param targetZoom: The target zoom level.
		:param centerX: The x-coordinate of the zoom center.
		:param centerY: The y-coordinate of the zoom center.
		:param callback: Callback function to call when animation is finished, defaults to None
		"""
		# Animation constants
		animationSteps = 40
		animationDuration = 500
		interval = animationDuration // animationSteps

		# Animation state variables
		self._animationStep = 0
		self._animationSteps = animationSteps
		self._animationStartZoom = self.zoomLevel
		self._animationDelta = (targetZoom - self._animationStartZoom) / animationSteps
		self._animationTargetZoom = targetZoom
		self._animationCenterX = centerX
		self._animationCenterY = centerY
		self._animationCallback = callback
		self._animationInterval = interval

		# Stop normal loop and start animation
		self._stopTimer()
		self._startTimer(self._onAnimationStep)

	def _onAnimationStep(self) -> None:
		"""Animation step called by magnifierTimer."""
		if self._animationStep < self._animationSteps:
			# Calculate and apply current zoom
			currentZoom = self._animationStartZoom + self._animationDelta * (self._animationStep + 1)
			# Temporarily modify zoom in settings (restored at animation end)
			self.zoomLevel = currentZoom
			self._fullscreenMagnifier(self._animationCenterX, self._animationCenterY)
			self._animationStep += 1

			# Continue animation with appropriate interval
			self.timer.Start(self._animationInterval, oneShot=True)
		else:
			# Animation finished
			self._finishAnimation()

	def _finishAnimation(self) -> None:
		"""Finish animation and execute callback."""
		self.zoomLevel = self._animationTargetZoom
		self._fullscreenMagnifier(self._animationCenterX, self._animationCenterY)

		if self._animationCallback:
			self._animationCallback()

class DockedMagnifier(NVDAMagnifier):
	
	def __init__(self, zoomLevel: float, colorFilter: ColorFilter):
		super().__init__(zoomLevel=zoomLevel, colorFilter=colorFilter)
		self._magnifierType: MagnifierType = MagnifierType.DOCKED
		self._dockedFrame: DockedFrame = DockedFrame()
		self._startMagnifier()

	def _startMagnifier(self):
		super()._startMagnifier()
		self._dockedFrame.Show()
		self._dockedFrame.startMagnifying(self._mouseHandler.getMousePosition(), self.colorFilter.value)
		self._startTimer(self._updateMagnifier)

	def _updateMagnifier(self):

		super()._updateMagnifier()
		x, y = self.currentCoordinates
		mouseCoordinates = self._mouseHandler.getMousePosition()
		self._dockedFrame.updateMagnifier(x, y, self.zoomLevel, mouseCoordinates, self.colorFilter.value)
		self._continueTimer(self._updateMagnifier)

	def _stopMagnifier(self):
		super()._stopMagnifier()
		self._dockedFrame.stopMagnifying()

class LensMagnifier(NVDAMagnifier):

	def __init__(self, zoomLevel: float, colorFilter: ColorFilter):
		super().__init__(zoomLevel=zoomLevel, colorFilter=colorFilter)
		self._magnifierType: MagnifierType = MagnifierType.LENS
		self._lensFrame: LensFrame = LensFrame()
		self._startMagnifier()

	def _startMagnifier(self):
		super()._startMagnifier()
		self._lensFrame.Show()
		self._lensFrame.startMagnifying(self.colorFilter.value)
		self._startTimer(self._updateMagnifier)

	def _updateMagnifier(self):
		super()._updateMagnifier()
		x, y = self._mouseHandler.getMousePosition()
		self._lensFrame.updateMagnifier(x, y, self.zoomLevel, self.colorFilter.value)
		self._continueTimer(self._updateMagnifier)

	def _stopMagnifier(self):
		super()._stopMagnifier()
		self._lensFrame.stopMagnifying()

	