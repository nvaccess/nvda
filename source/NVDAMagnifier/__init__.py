import ctypes
from ctypes import wintypes
from enum import Enum

from logHandler import log
import ui
import wx
import api

from . import windowsHandler

ZOOM_MIN = 1.0
ZOOM_MAX = 10.0
ZOOM_STEP = 0.5
TIMER_INTERVAL_MS = 15
MARGIN_BORDER = 50


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
		-1.0, 0.0, 0.0, 0.0, 0.0,
		0.0, -1.0, 0.0, 0.0, 0.0,
		0.0, 0.0, -1.0, 0.0, 0.0,
		0.0, 0.0, 0.0, 1.0, 0.0,
		1.0, 1.0, 1.0, 0.0, 1.0
	)

class ColorFilter(Enum):
	NORMAL = "normal"
	GREYSCALE = "greyscale"
	INVERTED = "inverted"

class FullScreenFocusMode(Enum):
	CENTER = "center"
	BORDER = "border"
	RELATIVE = "relative"


class ZoomType(Enum):
	FULLSCREEN = "fullscreen"
	DOCKED = "docked"
	LENS = "lens"


class NVDAMagnifier:
	def __init__(self):
		self.magnifierSettings = MagnifierSettings()
		self.magnifierTimer = MagnifierTimer()
		self.focusManager = FocusManager()
		self.mouseHandler = MouseHandler()
		self.fullscreenMagnifier = FullscreenMagnifier(
			self.magnifierSettings, self.focusManager, self.magnifierTimer, self.mouseHandler
		)
		self.dockedMagnifier = DockedMagnifier(
			self.magnifierSettings, self.focusManager, self.magnifierTimer, self.mouseHandler
		)
		self.lensMagnifier = LensMagnifier(
			self.magnifierSettings, self.focusManager, self.magnifierTimer, self.mouseHandler
		)
		windowsHandler.loadMagnifierApi()

	def _fullscreenModeIsActive(self) -> bool:
		"""Check if magnifier is in fullscreen."""
		return self.magnifierSettings.zoomType == ZoomType.FULLSCREEN

	def _zoom(self, direction: int) -> None:
		"""
		Change the zoom level.
		direction: +1 to zoom in, -1 to zoom out.
		Only works if magnifier centering is enabled.
		"""
		if self.magnifierSettings.isActive():
			currentZoom = self.magnifierSettings.getZoomLevel()
			if direction > 0:
				newZoom = min(currentZoom + ZOOM_STEP, ZOOM_MAX)
			else:
				newZoom = max(currentZoom - ZOOM_STEP, ZOOM_MIN)

			self.magnifierSettings.setZoomLevel(newZoom)
			ui.message(f"Zoom level changed to {newZoom}")
		else:
			ui.message("activate the magnifier with NVDA shift w before zooming")

	def _continueMagnifier(self) -> None:
		"""Start or continue magnifier based on current zoom type."""
		if self.magnifierSettings.isActive():
			if self.magnifierSettings.zoomType == ZoomType.FULLSCREEN:
				self.fullscreenMagnifier.startFullScreenMagnifier()
			elif self.magnifierSettings.zoomType == ZoomType.DOCKED:
				self.dockedMagnifier.startDockedMagnifier()
			elif self.magnifierSettings.zoomType == ZoomType.LENS:
				self.lensMagnifier.startLensMagnifier()
		else:
			self._stopMagnifier()

	def _stopMagnifier(self) -> None:
		"""Stop magnifier based on current zoom type."""
		if self.magnifierSettings.zoomType == ZoomType.FULLSCREEN:
			self.fullscreenMagnifier.stopFullScreenMagnifier()
		elif self.magnifierSettings.zoomType == ZoomType.DOCKED:
			self.dockedMagnifier.stopDockedMagnifier()
		elif self.magnifierSettings.zoomType == ZoomType.LENS:
			self.lensMagnifier.stopLensMagnifier()

	def _setColorEffect(self) -> None:
		"""
		Apply the given color filter (ColorFilter Enum).
		"""
		if self.magnifierSettings.zoomType.value == "fullscreen":
			filter = self.magnifierSettings.currentColorFilter.value
			if filter == "normal":
				matrix = ColorFilterMatrix.NORMAL
			elif filter == "greyscale":
				matrix = ColorFilterMatrix.GREYSCALE
			elif filter == "inverted":
				matrix = ColorFilterMatrix.INVERTED
			ctypes.windll.magnification.MagSetFullscreenColorEffect(matrix.value)
		else:
			pass

## MAGNIFIER SETTINGS


class MagnifierSettings:
	"""Centralized manager for magnifier settings."""

	def __init__(self):
		"""Initialize magnifier settings with default values."""
		self.zoomLevel = 2.0
		self.magnifierIsOn = False
		self.zoomType = ZoomType.FULLSCREEN
		self.fullscreenFocusMode = FullScreenFocusMode.CENTER
		self.currentColorFilter = ColorFilter.NORMAL

	def getZoomLevel(self) -> float:
		"""Get current zoom level."""
		return self.zoomLevel

	def setZoomLevel(self, level: float) -> None:
		"""Set zoom level within valid range."""
		self.zoomLevel = max(ZOOM_MIN, min(level, ZOOM_MAX))

	def getFullscreenFocusMode(self) -> FullScreenFocusMode:
		"""Get current fullscreen focus mode."""
		return self.fullscreenFocusMode

	def setFullscreenFocusMode(self, mode: FullScreenFocusMode):
		"""Set fullscreen focus mode."""
		self.fullscreenFocusMode = mode

	def getFilter(self) -> ColorFilter:
		"""Get current color filter."""
		return self.currentColorFilter

	def setFilter(self, filter: ColorFilter):
		"""Set color filter."""
		self.currentColorFilter = filter

	def isActive(self) -> bool:
		"""Check if magnifier is currently active."""
		return self.magnifierIsOn

	def setActive(self, active: bool):
		"""Set magnifier active state."""
		self.magnifierIsOn = active

	def reset(self) -> None:
		"""Reset all settings to default values."""
		self.setActive(False)
		self.setZoomLevel(2.0)
		self.zoomType = ZoomType.FULLSCREEN
		self.setFullscreenFocusMode(FullScreenFocusMode.CENTER)
		self.setFilter(ColorFilter.NORMAL)


## FOCUS MANAGER


class FocusManager:
	"""Centralized manager for determining focus (mouse/NVDA)."""

	def __init__(self):
		"""Initialize focus manager."""
		self.lastFocusedObject = ""
		self.lastNvdaPos = (0, 0)
		self.mouseHandler = MouseHandler()

	def reset(self) -> None:
		"""Reset focus manager to initial state."""
		self.lastFocusedObject = ""

	def getLastFocusedObject(self) -> str:
		"""Return the last focused object."""
		return self.lastFocusedObject

	def _setLastNvdaPos(self, pos:tuple[int, int]):
		self.lastNvdaPos = pos

	def _getLastNvdaPos(self) -> tuple[int, int]:
		return self.lastNvdaPos

	def _getNvdaPos(self) -> tuple[int, int]:
		"""
		Get the current review position as (x, y), falling back to navigator object if needed.
		Tries to get the review position from NVDA's API, or the center of the navigator object.
		This part is taken from NVDA+shift+m gesture.
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

	def getFocusCoordinates(self) -> tuple[int, int]:
		"""Return position (x,y) of current focus element."""
		nvdaPos = self._getNvdaPos()
		mousePos = self.mouseHandler.getMousePosition()

		# Check if left mouse button is pressed
		isClickPressed = self.mouseHandler.isLeftClickPressed()

		# Always update positions in background (keep them synchronized)
		nvdaChanged = self._getLastNvdaPos() != nvdaPos
		mouseChanged = self.mouseHandler.getLastMousePosition() != mousePos

		if nvdaChanged:
			self._setLastNvdaPos(nvdaPos)
		if mouseChanged:
			self.mouseHandler.setLastMousePosition(mousePos)

		# During drag & drop, force focus on mouse
		if isClickPressed:
			self.lastFocusedObject = "mouse"
			return mousePos

		# Check mouse first (mouse has priority) - when not dragging
		if mouseChanged:
			self.lastFocusedObject = "mouse"
			return mousePos

		# Then check NVDA (only change focus if mouse didn't move)
		if nvdaChanged:
			self.lastFocusedObject = "nvda"
			return nvdaPos

		# Return current position of the focused object (no changes detected)
		if self.lastFocusedObject == "nvda":
			return nvdaPos
		elif self.lastFocusedObject == "mouse":
			return mousePos
		else:
			return mousePos


# MOUSE HANDLER


class MouseHandler:
	def __init__(self):
		self.lastMousePos = (0, 0)

	def setLastMousePosition(self, pos: tuple[int, int]):
		self.lastMousePos = pos

	def getLastMousePosition(self) -> tuple[int, int]:
		return self.lastMousePos

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


## MAGNIFIER TIMER


class MagnifierTimer:
	"""Timer manager for magnifier updates."""

	def __init__(self):
		"""Initialize timer."""
		self.timer = None

	def startTimer(self, callback) -> None:
		"""Start timer with callback function."""
		self.stopTimer()
		self.timer = wx.Timer()
		self.timer.Bind(wx.EVT_TIMER, lambda evt: callback())
		self.timer.Start(TIMER_INTERVAL_MS, oneShot=True)

	def continueTimer(self, callback) -> None:
		"""Continue timer execution with callback."""
		if self.timer and self.timer.IsRunning():
			self.timer.Stop()
		self.timer = wx.Timer()
		self.timer.Bind(wx.EVT_TIMER, lambda evt: callback())
		self.timer.Start(TIMER_INTERVAL_MS, oneShot=True)

	def stopTimer(self) -> None:
		"""Stop timer execution."""
		if self.timer and self.timer.IsRunning():
			self.timer.Stop()
			self.timer = None


## MAGNIFIERS


class FullscreenMagnifier:
	"""Fullscreen magnifier implementation."""

	def __init__(self, magnifierSettings: MagnifierSettings, focusManager: FocusManager, magnifierTimer: MagnifierTimer, mouseHandler: MouseHandler):
		"""Initialize fullscreen magnifier with settings and focus manager."""
		self.isActive = False
		self.currentX = 0
		self.currentY = 0
		self.spotlightIsActive = False
		self._spotlightLastMousePos = 0, 0
		self.spotlightZoom = 0.0
		self.spotlightTimer = None
		self.magnifierTimer = magnifierTimer
		self.magnifierSettings = magnifierSettings
		self.focusManager = focusManager
		self.mouseHandler = mouseHandler

	def getMagSetFullscreenTransform(self):
		"""Get Windows Magnification API function."""
		MagSetFullscreenTransform = ctypes.windll.magnification.MagSetFullscreenTransform
		MagSetFullscreenTransform.restype = wintypes.BOOL
		MagSetFullscreenTransform.argtypes = [ctypes.c_float, ctypes.c_int, ctypes.c_int]
		return MagSetFullscreenTransform

	def fullscreenMagnifier(self, x: int, y: int):
		"""Apply fullscreen magnification at given coordinates."""
		zoomLevel = self.magnifierSettings.getZoomLevel()
		left, top, visibleWidth, visibleHeight = windowsHandler.getMagnifierPosition(x, y, zoomLevel)
		try:
			MagSetFullscreenTransform = self.getMagSetFullscreenTransform()
			result = MagSetFullscreenTransform(
				ctypes.c_float(zoomLevel), ctypes.c_int(left), ctypes.c_int(top)
			)
			if not result:
				log.info("Failed to set fullscreen transform")
		except AttributeError:
			log.info("Magnification API not available")

	def _updateMagnifier(self) -> None:
		"""Timer callback to update magnifier position."""
		if not self.isActive or self.spotlightIsActive:
			return

		# Get focus coordinates from FocusManager
		self.currentX, self.currentY = self.focusManager.getFocusCoordinates()

		# Get current focus mode from settings
		focusMode = self.magnifierSettings.getFullscreenFocusMode()

		# Reset mode flags if mode changed
		if not hasattr(self, "_currentFocusMode") or self._currentFocusMode != focusMode:
			self._currentFocusMode = focusMode

		# Calculate new position based on focus mode
		if focusMode == FullScreenFocusMode.CENTER:
			x, y = self.currentX, self.currentY
		elif focusMode == FullScreenFocusMode.BORDER:
			if self.focusManager.getLastFocusedObject() == "nvda":
				x, y = self.currentX, self.currentY
			else:
				x, y = self._borderPos(self.currentX, self.currentY)
		elif focusMode == FullScreenFocusMode.RELATIVE:
			x, y = self._relativePos(self.currentX, self.currentY)
		else:
			x, y = self.currentX, self.currentY

		# Always save screen position for mode continuity
		windowsHandler.lastScreenPosition[0] = x
		windowsHandler.lastScreenPosition[1] = y

		# Apply transformation
		self.fullscreenMagnifier(x, y)

		# Continue loop
		self.magnifierTimer.continueTimer(self._updateMagnifier)

	def startFullScreenMagnifier(self) -> None:
		"""Start fullscreen magnifier with update loop."""
		self.currentX, self.currentY = self.focusManager.getFocusCoordinates()
		self.isActive = True
		if self.magnifierSettings.currentColorFilter.value == "greyscale":
			ctypes.windll.magnification.MagSetFullscreenColorEffect(ColorFilterMatrix.GREYSCALE.value)
		elif self.magnifierSettings.currentColorFilter.value == "inverted":
			ctypes.windll.magnification.MagSetFullscreenColorEffect(ColorFilterMatrix.INVERTED.value)
		self.magnifierTimer.startTimer(self._updateMagnifier)

	def stopFullScreenMagnifier(self) -> None:
		"""Reset magnifier to default (1x zoom) and stop update loop."""
		# reset color filter of fullscreen to normal 
		ctypes.windll.magnification.MagSetFullscreenColorEffect(ColorFilterMatrix.NORMAL.value)
		try:
			# Get MagSetFullscreenTransform function from magnification API
			MagSetFullscreenTransform = self.getMagSetFullscreenTransform()
			# Reset fullscreen magnifier: 1.0 zoom, 0,0 position
			MagSetFullscreenTransform(ctypes.c_float(1.0), ctypes.c_int(0), ctypes.c_int(0))
		except AttributeError:
			log.info("Magnification API not available")

		self.isActive = False
		self.magnifierTimer.stopTimer()	

	def _borderPos(self, focusX: int, focusY: int) -> tuple[int, int]:
		"""
		Check if focus is near magnifier border and adjust position accordingly.
		Returns adjusted position to keep focus within margin limits.
		"""

		zoomLevel = self.magnifierSettings.getZoomLevel()

		lastLeft, lastTop, visibleWidth, visibleHeight = windowsHandler.getMagnifierPosition(
			windowsHandler.lastScreenPosition[0], windowsHandler.lastScreenPosition[1], zoomLevel
		)

		minX = lastLeft + MARGIN_BORDER
		maxX = lastLeft + visibleWidth - MARGIN_BORDER
		minY = lastTop + MARGIN_BORDER
		maxY = lastTop + visibleHeight - MARGIN_BORDER

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
			return windowsHandler.lastScreenPosition[0] + dx, windowsHandler.lastScreenPosition[1] + dy
		else:
			return windowsHandler.lastScreenPosition

	def _relativePos(self, mouseX: int, mouseY: int) -> tuple[int, int]:
		"""
		Calculate magnifier center maintaining mouse relative position.
		Handles screen edges to prevent going off-screen.
		"""
		if self.spotlightIsActive:
			zoom = self.spotlightZoom
		else:
			zoom = self.magnifierSettings.getZoomLevel()
		screenWidth = ctypes.windll.user32.GetSystemMetrics(0)
		screenHeight = ctypes.windll.user32.GetSystemMetrics(1)
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
		windowsHandler.lastScreenPosition[0] = int(left + visibleWidth / 2)
		windowsHandler.lastScreenPosition[1] = int(top + visibleHeight / 2)
		return windowsHandler.lastScreenPosition

	def spotlight(self, onFinish=None):
		"""Show magnifier overview by temporarily zooming out."""
		# Stop fullscreen timer immediately
		self.magnifierTimer.stopTimer()

		centerX, centerY = self.focusManager.getFocusCoordinates()
		focusMode = self.magnifierSettings.getFullscreenFocusMode()
		passedZoom = self.magnifierSettings.getZoomLevel()

		if focusMode == FullScreenFocusMode.RELATIVE:
			centerX, centerY = self._relativePos(centerX, centerY)
		elif focusMode == FullScreenFocusMode.BORDER:
			centerX, centerY = self._borderPos(centerX, centerY)

		self.spotlightIsActive = True
		self.spotlightZoom = passedZoom

		def checkMouseIdle() -> None:
			"""Check if the mouse is moving to keep spotlight active."""
			currentPos = self.mouseHandler.getMousePosition()
			if currentPos != self._spotlightLastMousePos:
				self._spotlightLastMousePos = currentPos
				self.mouseHandler.setLastMousePosition(currentPos)
				self.spotlightTimer = wx.CallLater(1000, checkMouseIdle)
			else:
				restoreZoom()

		def restoreZoom() -> None:
			"""Restore zoom level and position after spotlight."""
			if self.spotlightTimer and self.spotlightTimer.IsRunning():
				self.spotlightTimer.Stop()
				self.spotlightTimer = None

			x, y = self.mouseHandler.getMousePosition()
			if focusMode == FullScreenFocusMode.RELATIVE:
				x, y = self._relativePos(x, y)
			else:
				windowsHandler.lastScreenPosition[0], windowsHandler.lastScreenPosition[1] = x, y
			self.spotlightIsActive = False

			# Update position for normal operation
			self.currentX = x
			self.currentY = y

			def restartAfterAnimation() -> None:
				# Restart fullscreen timer
				self.magnifierTimer.startTimer(self._updateMagnifier)
				if onFinish:
					onFinish()

			self._animateZoom(self.spotlightZoom, x, y, callback=restartAfterAnimation)

		self._animateZoom(1.0, centerX, centerY, callback=lambda: wx.CallLater(2000, checkMouseIdle))

	def _animateZoom(self, targetZoom: float, centerX: int, centerY: int, callback=None) -> None:
		"""Animate zoom smoothly using magnifierTimer."""
		# Animation constants
		animationSteps = 40
		animationDuration = 500
		interval = animationDuration // animationSteps

		# Animation state variables
		self._animationStep = 0
		self._animationSteps = animationSteps
		self._animationStartZoom = self.magnifierSettings.getZoomLevel()
		self._animationDelta = (targetZoom - self._animationStartZoom) / animationSteps
		self._animationTargetZoom = targetZoom
		self._animationCenterX = centerX
		self._animationCenterY = centerY
		self._animationCallback = callback
		self._animationInterval = interval

		# Stop normal loop and start animation
		self.magnifierTimer.stopTimer()
		self.magnifierTimer.startTimer(self._onAnimationStep)

	def _onAnimationStep(self) -> None:
		"""Animation step called by magnifierTimer."""
		if self._animationStep < self._animationSteps:
			# Calculate and apply current zoom
			currentZoom = self._animationStartZoom + self._animationDelta * (self._animationStep + 1)
			# Temporarily modify zoom in settings (restored at animation end)
			self.magnifierSettings.setZoomLevel(currentZoom)
			self.fullscreenMagnifier(self._animationCenterX, self._animationCenterY)
			self._animationStep += 1

			# Continue animation with appropriate interval
			self.magnifierTimer.timer.Start(self._animationInterval, oneShot=True)
		else:
			# Animation finished
			self._finishAnimation()

	def _finishAnimation(self):
		"""Finish animation and execute callback."""
		self.magnifierSettings.setZoomLevel(self._animationTargetZoom)
		self.fullscreenMagnifier(self._animationCenterX, self._animationCenterY)

		if self._animationCallback:
			self._animationCallback()


class DockedMagnifier:
	"""Simple docked magnifier management."""

	def __init__(self, magnifierSettings: MagnifierSettings, focusManager: FocusManager, magnifierTimer: MagnifierTimer, mouseHandler: MouseHandler):
		self.magnifierTimer = magnifierTimer
		self.magnifierSettings = magnifierSettings
		self.focusManager = focusManager
		self.mouseHandler = mouseHandler
		self.dockedFrame = None

	def startDockedMagnifier(self) -> None: 
		"""Start docked magnifier."""
		try:
			# Close existing frame if any
			if self.dockedFrame:
				try:
					self.dockedFrame.stopMagnifying()
				except Exception as e:
					log.error(f"Failed to stop docked magnifier with error: {e}")
				self.dockedFrame = None

			# Create new magnifier frame
			self.dockedFrame = windowsHandler.DockedFrame()
			self.dockedFrame.Show()
			self.dockedFrame.startMagnifying(self.mouseHandler.getMousePosition(), self.magnifierSettings.getFilter().value)
			self.magnifierTimer.startTimer(self._updateMagnifier)
		except Exception as e:
			log.error(f"Error starting docked magnifier: {e}")

	def stopDockedMagnifier(self) -> None:
		"""Stop docked magnifier."""
		try:
			if self.dockedFrame:
				try:
					self.dockedFrame.stopMagnifying()
				except Exception as e:
					log.error(f"Failed to stop docked magnifier with error: {e}")
				self.dockedFrame = None
				ui.message("Docked magnifier stopped")
		except Exception as e:
			log.error(f"Error stopping docked magnifier: {e}")

	def _updateMagnifier(self) -> None:
		"""Update magnifier position"""
		if self.dockedFrame:
			if self.focusManager:
				x, y = self.focusManager.getFocusCoordinates()
				self.dockedFrame.updateMagnifier(
					x, y, self.magnifierSettings.getZoomLevel(), self.mouseHandler.getMousePosition(), self.magnifierSettings.getFilter().value
				)
			self.magnifierTimer.continueTimer(self._updateMagnifier)


class LensMagnifier:
	"""Simple lens magnifier management."""

	def __init__(self, magnifierSettings: MagnifierSettings, focusManager: FocusManager, magnifierTimer: MagnifierTimer, mouseHandler: MouseHandler):
		self.magnifierTimer = magnifierTimer
		self.magnifierSettings = magnifierSettings
		self.focusManager = focusManager
		self.mouseHandler = mouseHandler
		self.lensFrame = None

	def startLensMagnifier(self) -> None:
		"""Start lens magnifier."""
		try:
			# Close existing lens if any
			if self.lensFrame:
				try:
					self.lensFrame.stopMagnifying()
				except Exception as e:
					log.error(f"Failed to stop lens magnifier with error: {e}")
				self.lensFrame = None

			# Create new lens window
			self.lensFrame = windowsHandler.LensFrame()
			self.lensFrame.Show()
			self.lensFrame.startMagnifying(self.magnifierSettings.getFilter().value)
			self.magnifierTimer.startTimer(self._updateMagnifier)

		except Exception as e:
			log.error(f"Error starting lens magnifier: {e}")

	def stopLensMagnifier(self) -> None:
		"""Stop lens magnifier."""
		try:
			if self.lensFrame:
				try:
					self.lensFrame.stopMagnifying()
				except Exception as e:
					log.error(f"Failed to stop lens magnifier with error: {e}")
				self.lensFrame = None
		except Exception as e:
			log.error(f"Error stopping lens magnifier: {e}")

	def _updateMagnifier(self) -> None:
		"""Update lens magnifier position."""
		if self.lensFrame:
			if self.focusManager:
				x, y = self.mouseHandler.getMousePosition()
				# Always center lens on mouse position
				self.lensFrame.updateMagnifier(x, y, self.magnifierSettings.getZoomLevel(), self.magnifierSettings.getFilter().value)
			self.magnifierTimer.continueTimer(self._updateMagnifier)
