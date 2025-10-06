import ctypes

from logHandler import log
import wx


lastScreenPosition = [0, 0]


def getScreenSize():
	"""Return screen width and height."""
	screenWidth, screenHeight = (
		ctypes.windll.user32.GetSystemMetrics(0),
		ctypes.windll.user32.GetSystemMetrics(1),
	)
	return screenWidth, screenHeight


def loadMagnifierApi():
	"""Initialize the Magnification API."""
	try:
		# Attempt to access the magnification DLL
		ctypes.windll.magnification
	except (OSError, AttributeError):
		# If the DLL is not available, log this and exit the function
		log.info("Magnification API not available")
		return
	# Try to initialize the magnification API
	# MagInitialize returns 0 if already initialized or on failure
	if ctypes.windll.magnification.MagInitialize() == 0:
		log.info("Magnification API already initialized")
		return
	# If initialization succeeded, log success
	log.info("Magnification API initialized")


def getMagnifierPosition(x, y, zoomLevel):
	"""
	Compute the top-left corner of the magnifier window centered on (x, y).
	Returns (left, top, visibleWidth, visibleHeight).
	"""
	# Get the screen size in pixels
	screenWidth, screenHeight = getScreenSize()

	# Calculate the size of the visible area at the current zoom level
	visibleWidth, visibleHeight = screenWidth / zoomLevel, screenHeight / zoomLevel

	# Compute the top-left corner so that (x, y) is at the center of the visible area
	left, top = int(x - (visibleWidth / 2)), int(y - (visibleHeight / 2))

	# Clamp the top-left corner so the visible area stays within the screen boundaries
	left, top = (
		max(0, min(left, int(screenWidth - visibleWidth))),
		max(0, min(top, int(screenHeight - visibleHeight))),
	)

	return (left, top, visibleWidth, visibleHeight)


class GlobalPanel(wx.Panel):
	"""Unified panel that handles both docked and lens magnification display."""

	def __init__(self, parent, panelType):
		"""
		Initialize the global panel.

		Args:
		    parent: Parent window
		    panelType: Either "docked" or "lens" to determine behavior
		"""
		super().__init__(parent)

		# Store panel configuration
		self.panelType = panelType
		self.SetName(panelType)

		# Content properties
		self.contentImage = None
		self.contentBitmap = None
		self.cursorPos = (0, 0)

		# Drawing settings
		self.crosshairColor = wx.Colour(255, 0, 0)
		self.crosshairWidth = 2
		self.crosshairSize = 10
		self.placeholderText = f"{self.panelType} starting..."

		# Bind paint event
		self.Bind(wx.EVT_PAINT, self.onPaint)

		log.info(f"GlobalPanel initialized - type: {self.panelType}, parent: {parent}")

	def setContent(self, content, cursorPos):
		"""
		Set the magnified content and cursor position.

		Args:
		    content: Either wx.Bitmap (for docked) or wx.Image (for lens)
		    cursorPos: Tuple (x, y) for cursor position
		"""
		log.info(f"Setting {self.panelType} content: content={content is not None}, cursor={cursorPos}")

		# Handle different content types
		if content:
			if isinstance(content, wx.Bitmap):
				self.contentBitmap = content
				self.contentImage = content.ConvertToImage() if content.IsOk() else None
			elif isinstance(content, wx.Image):
				self.contentImage = content
				self.contentBitmap = wx.Bitmap(content) if content.IsOk() else None
			else:
				log.error(f"Unknown content type: {type(content)}")
				return

			if self.contentImage:
				log.info(f"Content details: {self.contentImage.GetWidth()}x{self.contentImage.GetHeight()}")
		else:
			self.contentBitmap = None
			self.contentImage = None

		self.cursorPos = cursorPos
		self.Refresh()
		log.info(f"{self.panelType.capitalize()} panel refreshed")

	def drawCrosshair(self, dc, x, y):
		"""
		Draw crosshair at specified position.

		Args:
		    dc: Drawing context
		    x, y: Position to draw crosshair
		"""
		panelSize = self.GetSize()

		# Only draw if cursor is within panel bounds
		if 0 <= x < panelSize.width and 0 <= y < panelSize.height:
			# Set pen for cursor crosshair
			dc.SetPen(wx.Pen(self.crosshairColor, self.crosshairWidth))

			# Draw horizontal line
			dc.DrawLine(x - self.crosshairSize, y, x + self.crosshairSize, y)

			# Draw vertical line
			dc.DrawLine(x, y - self.crosshairSize, x, y + self.crosshairSize)

	def drawPlaceholder(self, dc):
		"""Draw placeholder content when no image is available."""
		panelSize = self.GetSize()
		width, height = panelSize.width, panelSize.height
		dc.SetTextForeground(wx.Colour(128, 128, 128))
		font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
		dc.SetFont(font)

		# Center the placeholder text
		textSize = dc.GetTextExtent(self.placeholderText)
		text_x = (width - textSize.width) // 2
		text_y = (height - textSize.height) // 2
		dc.DrawText(self.placeholderText, text_x, text_y)

	def onPaint(self, event):
		"""Paint the magnified content and cursor overlay."""
		log.info(f"GlobalPanel ({self.panelType}) onPaint called")

		dc = wx.PaintDC(self)
		panelSize = self.GetSize()
		width, height = panelSize.width, panelSize.height

		log.info(f"Panel size in paint: {width}x{height}")

		# Clear background
		dc.Clear()

		# Draw content if available
		if self.contentImage and self.contentImage.IsOk():
			# Draw the magnified content
			dc.DrawBitmap(self.contentBitmap, 0, 0)

			# Draw crosshair at cursor position
			cursorX, cursorY = self.cursorPos
			self.drawCrosshair(dc, cursorX, cursorY)

		else:
			# Draw placeholder
			self.drawPlaceholder(dc)

		log.info(f"GlobalPanel ({self.panelType}) paint completed")


class GlobalFrame(wx.Frame):
	"""Base frame class that handles common magnifier functionality."""

	def __init__(self, frameType, title=None, size=None, style=None, position=None):
		"""
		Initialize the global frame.

		Args:
		    frameType: Either "docked" or "lens" to determine behavior
		    title: Window title
		    size: Window size tuple (width, height)
		    style: Window style flags
		    position: Window position tuple (x, y)
		"""
		# Default parameters
		if style is None:
			style = wx.DEFAULT_FRAME_STYLE
		if size is None:
			size = (400, 300)

		super().__init__(None, title=title, size=size, style=style)

		# Store frame configuration
		self.frameType = frameType

		# Common properties
		self.running = False
		self.panel = None

		self.movementThreshold = 2

		# Set initial position if provided
		if position is not None:
			self.SetPosition(position)

		log.info(f"GlobalFrame initialized - type: {frameType}, size: {size}")

	def createPanel(self):
		"""Create the magnifier panel - can be overridden by subclasses."""
		self.panel = GlobalPanel(self, self.frameType)
		return self.panel

	def setupLayout(self):
		"""Setup the window layout with panel."""
		self.createPanel()
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 0)
		self.SetSizer(sizer)
		self.Layout()
		log.info(f"{self.frameType.capitalize()} sizer configured and layout forced")

	def forceRefresh(self):
		"""Force immediate paint events on the panel."""
		if self.panel:
			wx.CallAfter(self.panel.Refresh)
			wx.CallAfter(self.panel.Update)

	def startMagnifying(self):
		"""Start the magnification."""
		self.running = True
		self.setupLayout()
		self.Show()
		self.forceRefresh()
		self.Bind(wx.EVT_CLOSE, self.stopMagnifying)
		self.screenWidth, self.screenHeight = getScreenSize()

		log.info(f"{self.frameType.capitalize()} magnifying started")

	def stopMagnifying(self, event=None):
		"""Stop the magnification."""
		self.running = False
		self.Destroy()
		log.info(f"{self.frameType.capitalize()} magnifying stopped")

	def updateMagnifier(self, focusX, focusY, zoomLevel):
		"""Update magnifier - base implementation with common checks."""
		if not self.running or not self.panel:
			return
		try:
			self.Layout()
			magnifierSize = self.panel.GetSize()

			log.info(f"Magnifier size: {magnifierSize}, zoom: {zoomLevel}")

			captureWidth = magnifierSize.width / zoomLevel
			captureHeight = magnifierSize.height / zoomLevel

			captureX = focusX - captureWidth / 2
			captureY = focusY - captureHeight / 2

			# Ensure capture area stays on screen
			screenWidth, screenHeight = getScreenSize()

			captureX = max(0, min(captureX, screenWidth - captureWidth))
			captureY = max(0, min(captureY, screenHeight - captureHeight))

			log.info(f"Capture area: {captureX},{captureY} size: {captureWidth}x{captureHeight}")

			# Capture screen - convert to int only here where needed
			screen = wx.ScreenDC()
			bitmap = wx.Bitmap(int(captureWidth), int(captureHeight))
			memoryDc = wx.MemoryDC()
			memoryDc.SelectObject(bitmap)
			success = memoryDc.Blit(
				0, 0, int(captureWidth), int(captureHeight), screen, int(captureX), int(captureY)
			)
			memoryDc.SelectObject(wx.NullBitmap)

			log.info(f"Capture success: {success}, bitmap OK: {bitmap.IsOk()}")

			if success and bitmap.IsOk():
				# Convert to image and scale to fill the entire panel
				image = bitmap.ConvertToImage()

				# Get panel size to scale the image to fill it completely
				panelSize = self.panel.GetSize()
				panelWidth, panelHeight = panelSize.width, panelSize.height

				# Scale image to fill the entire panel
				magnifiedImage = image.Scale(panelWidth, panelHeight, wx.IMAGE_QUALITY_BICUBIC)
				magnifiedBitmap = wx.Bitmap(magnifiedImage)

				# Calculate cursor position relative to panel size
				# Map from capture area to panel area
				cursorCaptureX = focusX - captureX
				cursorCaptureY = focusY - captureY

				# Scale cursor position to panel coordinates
				cursorPanelX = (cursorCaptureX / captureWidth) * panelWidth
				cursorPanelY = (cursorCaptureY / captureHeight) * panelHeight

				log.info(f"Panel size: {panelWidth}x{panelHeight}, Cursor pos: {cursorPanelX},{cursorPanelY}")

				wx.CallAfter(
					self.panel.setContent,
					magnifiedBitmap,
					(int(cursorPanelX), int(cursorPanelY)),
				)
			else:
				log.error("Failed to capture screen or bitmap not valid")

		except Exception as e:
			log.error(f"Error in screen capture: {e}")
			import traceback

			log.error(traceback.format_exc())


class DockedFrame(GlobalFrame):
	"""Docked magnifier window that shows content under mouse cursor."""

	def __init__(self):
		# Get screen dimensions to size the magnifier appropriately
		self.screenWidth, self.screenHeight = getScreenSize()
		magnifierWidth = self.screenWidth
		magnifierHeight = max(150, min(300, self.screenHeight // 4))

		super().__init__(
			frameType="docked",
			title="NVDA Docked Magnifier",
			size=(magnifierWidth, magnifierHeight),
			style=wx.STAY_ON_TOP | wx.CAPTION | wx.RESIZE_BORDER,
			position=(0, 0),
		)

	def startMagnifying(self, lastMousePos):
		"""Start the magnification with docked-specific settings."""
		self.lastMousePos = lastMousePos
		super().startMagnifying()

	def updateMagnifier(self, focusX, focusY, zoomLevel, mousePos):
		"""Implementation of docked magnifier update."""
		mouseX, mouseY = mousePos
		lastMouseX, lastMouseY = self.lastMousePos
		movementMouseDistance = ((mouseX - lastMouseX) ** 2 + (mouseY - lastMouseY) ** 2) ** 0.5

		if movementMouseDistance < self.movementThreshold and self.lastMousePos != (
			0,
			0,
		):
			log.info("No significant movement detected, skipping update")
			return

		super().updateMagnifier(focusX, focusY, zoomLevel)


class LensFrame(GlobalFrame):
	"""Circular lens magnifier that follows the cursor."""

	def __init__(self):
		# Initialize lens properties first
		self.lensSize = 300

		super().__init__(
			frameType="lens",
			title="NVDA Lens Magnifier",
			size=(self.lensSize, self.lensSize),
			style=wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR,
		)

	def startMagnifying(self):
		"""Start the magnification with lens-specific settings."""
		super().startMagnifying()

	def updateMagnifier(self, focusX, focusY, zoomLevel):
		"""Implementation of lens magnifier update."""
		offsetX = 120  # Move lens to the right of mouse
		offsetY = -120  # Move lens above the mouse

		lensX = min(max(0, focusX + offsetX), self.screenWidth - self.lensSize)
		lensY = min(max(0, focusY + offsetY), self.screenHeight - self.lensSize)

		self.SetPosition((lensX, lensY))

		super().updateMagnifier(focusX, focusY, zoomLevel)
