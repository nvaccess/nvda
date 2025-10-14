import ctypes
import array

from logHandler import log
import wx


lastScreenPosition = [0, 0]


def getScreenSize() -> tuple[int, int]:
	"""Return screen width and height."""
	screenWidth, screenHeight = (
		ctypes.windll.user32.GetSystemMetrics(0),
		ctypes.windll.user32.GetSystemMetrics(1),
	)
	return screenWidth, screenHeight

class GlobalPanel(wx.Panel):
	"""Unified panel that handles both docked and lens magnification display."""

	def __init__(self, parent: wx.Frame, panelType: str):
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
		self.contentBitmap = None
		self.cursorPos = (0, 0)

		# Drawing settings
		self.crosshairColor = wx.Colour(255, 0, 0)
		self.crosshairWidth = 2
		self.crosshairSize = 10
		self.placeholderText = f"{self.panelType} starting..."

		# Bind paint event
		self.Bind(wx.EVT_PAINT, self.onPaint)

	def setContent(self, content: wx.Bitmap, cursorPos: tuple[int, int]) -> None:
		"""
		Set the magnified content and cursor position.
		"""
		self.contentBitmap = content
		self.cursorPos = cursorPos
		self.Refresh()

	def drawCrosshair(self, dc: wx.PaintDC, x: int, y: int) -> None:
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

	def drawPlaceholder(self, dc: wx.PaintDC) -> None:
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

	def onPaint(self, event) -> None:
		"""Paint the magnified content and cursor overlay."""
		dc = wx.PaintDC(self)
		# Clear background
		dc.Clear()

		# Draw content if available
		if self.contentBitmap:
			# Draw the magnified content
			dc.DrawBitmap(self.contentBitmap, 0, 0)

			# Draw crosshair at cursor position
			cursorX, cursorY = self.cursorPos
			self.drawCrosshair(dc, cursorX, cursorY)

		else:
			# Draw placeholder
			self.drawPlaceholder(dc)


class GlobalFrame(wx.Frame):
	"""Base frame class that handles common magnifier functionality."""

	def __init__(
		self, frameType: str, title=None, size=None, style=None, position=None, colorFilter="normal"
	):
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
		self.filter = colorFilter

		# Common properties
		self.running = False
		self.panel = None

		self.movementThreshold = 2

		# Set initial position if provided
		if position is not None:
			self.SetPosition(position)

	def createPanel(self) -> GlobalPanel:
		"""Create the magnifier panel - can be overridden by subclasses."""
		self.panel = GlobalPanel(self, self.frameType)
		return self.panel

	def setupLayout(self) -> None:
		"""Setup the window layout with panel."""
		self.createPanel()
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 0)
		self.SetSizer(sizer)
		self.Layout()

	def setColorFilter(self, colorFilter: str) -> None:
		self.colorFilter = colorFilter

	def applyColorFilter(self, image: wx.Image) -> wx.Image:
		"""Apply color filter with early exit optimization."""
		# width, height = image.GetWidth(), image.GetHeight()
		# if self.colorFilter == "normal":
		# 	return image
		# elif self.colorFilter == "greyscale":
		# 	for y in range(height):
		# 		for x in range(width):
		# 			r, g, b = image.GetRed(x, y), image.GetGreen(x, y), image.GetBlue(x, y)
		# 			gray = int(0.299 * r + 0.587 * g + 0.114 * b)
		# 			gray = max(0, min(255, gray))
		# 			image.SetRGB(x, y, gray, gray, gray)
		# elif self.colorFilter == "inverted":
		# 	for y in range(height):
		# 		for x in range(width):
		# 			r, g, b = image.GetRed(x, y), image.GetGreen(x, y), image.GetBlue(x, y)
		# 			image.SetRGB(x, y, 255 - r, 255 - g, 255 - b)
		# return image

		if self.colorFilter == "normal" or not image or not image.IsOk():
			return image

		try:
			# Get raw image data as bytes
			width, height = image.GetWidth(), image.GetHeight()
			data = image.GetData()  # Returns RGB data as bytes

			# Convert to array for faster manipulation
			rgb_array = array.array("B", data)  # 'B' = unsigned char (0-255)

			if self.colorFilter == "greyscale":
				# Process 3 bytes at a time (R, G, B)
				for i in range(0, len(rgb_array), 3):
					r, g, b = rgb_array[i], rgb_array[i + 1], rgb_array[i + 2]
					# Standard grayscale formula
					gray = int(0.299 * r + 0.587 * g + 0.114 * b)
					rgb_array[i] = rgb_array[i + 1] = rgb_array[i + 2] = gray

			elif self.colorFilter == "inverted":
				# Invert all values
				for i in range(len(rgb_array)):
					rgb_array[i] = 255 - rgb_array[i]

			# Create new image with modified data
			new_image = wx.Image(width, height)
			new_image.SetData(rgb_array.tobytes())
			return new_image

		except Exception as e:
			log.error(f"Error in optimized color filter: {e}")
			return image

	def forceRefresh(self) -> None:
		"""Force immediate paint events on the panel."""
		if self.panel:
			wx.CallAfter(self.panel.Refresh)
			wx.CallAfter(self.panel.Update)

	def startMagnifying(self) -> None:
		"""Start the magnification."""
		self.running = True
		self.setupLayout()
		self.Show()
		self.forceRefresh()
		self.Bind(wx.EVT_CLOSE, self.stopMagnifying)
		self.screenWidth, self.screenHeight = getScreenSize()

	def stopMagnifying(self) -> None:
		"""Stop the magnification."""
		self.running = False
		self.Destroy()

	def updateMagnifier(self, focusX: int, focusY: int, zoomLevel: float) -> None:
		"""Update magnifier - base implementation with common checks."""
		if not self.running or not self.panel:
			return
		try:
			self.Layout()
			magnifierSize = self.panel.GetSize()
			captureWidth = magnifierSize.width / zoomLevel
			captureHeight = magnifierSize.height / zoomLevel

			captureX = focusX - captureWidth / 2
			captureY = focusY - captureHeight / 2

			# Ensure capture area stays on screen
			screenWidth, screenHeight = getScreenSize()

			captureX = max(0, min(captureX, screenWidth - captureWidth))
			captureY = max(0, min(captureY, screenHeight - captureHeight))

			# Capture screen - convert to int only here where needed
			screen = wx.ScreenDC()
			bitmap = wx.Bitmap(int(captureWidth), int(captureHeight))
			memoryDc = wx.MemoryDC()
			memoryDc.SelectObject(bitmap)
			success = memoryDc.Blit(
				0, 0, int(captureWidth), int(captureHeight), screen, int(captureX), int(captureY)
			)
			memoryDc.SelectObject(wx.NullBitmap)

			if success and bitmap.IsOk():
				# Convert to image and scale to fill the entire panel
				image = bitmap.ConvertToImage()

				# Apply color filter
				image = self.applyColorFilter(image)

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

	def startMagnifying(self, lastMousePos: tuple[int, int], colorFilter: str) -> None:
		"""Start the magnification with docked-specific settings."""
		self.lastMousePos = lastMousePos
		self.setColorFilter(colorFilter)
		super().startMagnifying()

	def updateMagnifier(
		self, focusX: int, focusY: int, zoomLevel: float, mousePos: tuple[int, int], colorFilter: str
	) -> None:
		"""Implementation of docked magnifier update."""
		mouseX, mouseY = mousePos
		lastMouseX, lastMouseY = self.lastMousePos
		movementMouseDistance = ((mouseX - lastMouseX) ** 2 + (mouseY - lastMouseY) ** 2) ** 0.5

		if movementMouseDistance < self.movementThreshold and self.lastMousePos != (
			0,
			0,
		):
			# return if mouse didn't move to prevent infinite zoom on crosshair
			return
		if colorFilter != self.colorFilter:
			self.setColorFilter(colorFilter)
		super().updateMagnifier(focusX, focusY, zoomLevel)


class LensFrame(GlobalFrame):
	"""Circular lens magnifier that follows the cursor."""

	def __init__(self):
		self.lensSize = 300

		super().__init__(
			frameType="lens",
			title="NVDA Lens Magnifier",
			size=(self.lensSize, self.lensSize),
			style=wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR,
		)

	def startMagnifying(self, colorFilter: str) -> None:
		"""Start the magnification with lens-specific settings."""
		self.setColorFilter(colorFilter)
		super().startMagnifying()

	def updateMagnifier(self, focusX: int, focusY: int, zoomLevel: float, colorFilter: str) -> None:
		"""Implementation of lens magnifier update."""
		offsetX = 125  # Move lens to the right of mouse
		offsetY = -125  # Move lens above the mouse

		lensX = min(max(0, focusX + offsetX), self.screenWidth - self.lensSize)
		lensY = min(max(0, focusY + offsetY), self.screenHeight - self.lensSize)

		self.SetPosition((lensX, lensY))
		if colorFilter != self.colorFilter:
			self.setColorFilter(colorFilter)
		super().updateMagnifier(focusX, focusY, zoomLevel)
