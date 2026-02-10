# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from logHandler import log
import wx
import array

from .types import MagnifierParameters, WindowMagnifierParameters, Size, Filter


class MagnifierPanel(wx.Panel):
	"""A simple panel for the magnifier."""

	def __init__(self, parent: wx.Frame, panelType: str):
		super().__init__(parent)

		self.panelType = panelType
		self.SetName(panelType)

		self.contentImage = None
		self.contentBitmap = None

		self.Bind(wx.EVT_PAINT, self.onPaint)

	def setContent(self, content):
		"""Set the content image to be displayed in the magnifier panel."""
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

			self.Refresh()
			log.info(f"{self.panelType.capitalize()} panel refreshed")

	def onPaint(self, event):
		"""Handle the paint event to draw the magnified content."""
		dc = wx.PaintDC(self)
		# Clear background
		dc.Clear()

		# Draw content if available
		if self.contentImage and self.contentImage.IsOk():
			# Draw the magnified content
			dc.DrawBitmap(self.contentBitmap, 0, 0)


class MagnifierFrame(wx.Frame):
	"""A simple window frame for the magnifier."""

	def __init__(
		self,
		parent=None,
		title: str = "Magnifier Window",
		frameType: str = "magnifier",
		screenSize: Size = None,
		windowMagnifierParameters: WindowMagnifierParameters = None,
	):
		self.frameType = frameType
		self.screenSize = screenSize
		self.windowMagnifierParameters = windowMagnifierParameters
		super().__init__(
			parent,
			title=title,
			size=(windowMagnifierParameters.windowSize.width, windowMagnifierParameters.windowSize.height),
		)
		self.SetWindowStyle(self.windowMagnifierParameters.styles)
		self.SetPosition(self.windowMagnifierParameters.windowPosition)
		self.panel = self.createPanel()
		self.Show()

	def createPanel(self) -> MagnifierPanel:
		"""Create and return a magnifier panel."""
		return MagnifierPanel(self, self.frameType)

	def setupLayout(self) -> None:
		"""Set up the layout of the magnifier frame."""
		self.createPanel()
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.panel, 1, wx.EXPAND)
		self.SetSizer(sizer)
		self.Layout()

	def updateFrameContent(self, content) -> None:
		"""Update the content displayed in the magnifier frame."""
		if self.panel:
			self.panel.setContent(content)


class WindowedMagnifier:
	"""
	Base class for magnifiers that use a separate window to display magnified content.
	Provides common functionality for creating and managing the magnifier window and panel.
	"""

	def __init__(self, windowMagnifierParameters: WindowMagnifierParameters):
		self.windowMagnifierParameters = windowMagnifierParameters
		self._frame: None | MagnifierFrame = None
		self._panel: None | MagnifierPanel = None
		self._setupWindow()

	def _setupWindow(self):
		"""
		Create the magnifier window and panel based on the provided parameters.
		"""
		self._frame = MagnifierFrame(
			title=self.windowMagnifierParameters.title,
			frameType="magnifier",
			screenSize=self.windowMagnifierParameters.windowSize,
			windowMagnifierParameters=self.windowMagnifierParameters,
		)
		self._panel = self._frame.panel

	def _applyColorFilter(self, image: wx.Image, filterType: Filter) -> wx.Image:
		"""
		Apply color filter with array optimization for better performance.

		:param image: The image to apply the filter to
		:param filterType: The filter type to apply (NORMAL, GRAYSCALE, INVERTED)
		:return: The filtered image
		"""
		if filterType == Filter.NORMAL or not image or not image.IsOk():
			return image

		try:
			# Get raw image data as bytes
			width, height = image.GetWidth(), image.GetHeight()
			data = image.GetData()  # Returns RGB data as bytes

			# Convert to array for faster manipulation
			rgb_array = array.array("B", data)  # 'B' = unsigned char (0-255)

			if filterType == Filter.GRAYSCALE:
				# Process 3 bytes at a time (R, G, B)
				for i in range(0, len(rgb_array), 3):
					r, g, b = rgb_array[i], rgb_array[i + 1], rgb_array[i + 2]
					# Standard grayscale formula
					gray = int(0.299 * r + 0.587 * g + 0.114 * b)
					rgb_array[i] = rgb_array[i + 1] = rgb_array[i + 2] = gray

			elif filterType == Filter.INVERTED:
				# Invert all values
				for i in range(len(rgb_array)):
					rgb_array[i] = 255 - rgb_array[i]

			# Create new image with modified data
			new_image = wx.Image(width, height)
			new_image.SetData(rgb_array.tobytes())
			return new_image

		except Exception as e:
			log.error(f"Error applying color filter: {e}")
			return image

	def _setContent(self, magnifierParameters: MagnifierParameters, zoomLevel: float):
		content = self._getContent(magnifierParameters, zoomLevel)
		if self._panel:
			self._panel.setContent(content)
		else:
			log.debug("No panel available to set content")

	def _destroyWindow(self):
		if self._frame:
			self._frame.Destroy()
			self._frame = None
			self._panel = None

	def _getContent(self, magnifierParameters: MagnifierParameters, zoomLevel: float) -> wx.Bitmap | None:
		"""
		Capture the screen area defined by magnifierParameters and return it as a scaled bitmap.

		:param magnifierParameters: The parameters defining the area to capture
		:param zoomLevel: The zoom level to apply to the captured content
		:return: A wx.Bitmap scaled to fill the panel, or None if capture fails
		"""
		if not self._panel:
			log.warning("No panel available for capture")
			return None

		panelSize = self._panel.GetSize()
		panelWidth, panelHeight = panelSize.width, panelSize.height

		# Calculate the size of the area to capture based on zoom level
		captureWidth = panelWidth / zoomLevel
		captureHeight = panelHeight / zoomLevel
		captureLeft = int(magnifierParameters.coordinates.x)
		captureTop = int(magnifierParameters.coordinates.y)

		# Capture screen
		screen = wx.ScreenDC()
		bitmap = wx.Bitmap(int(captureWidth), int(captureHeight))
		memoryDc = wx.MemoryDC()
		memoryDc.SelectObject(bitmap)
		success = memoryDc.Blit(0, 0, int(captureWidth), int(captureHeight), screen, captureLeft, captureTop)
		memoryDc.SelectObject(wx.NullBitmap)

		log.info(
			f"Capture at ({captureLeft}, {captureTop}) "
			f"size {int(captureWidth)}x{int(captureHeight)} "
			f"zoom {zoomLevel}x -> panel {panelWidth}x{panelHeight}",
		)

		if success and bitmap.IsOk():
			# Convert to image
			image = bitmap.ConvertToImage()

			# Apply color filter if we have access to filterType
			if hasattr(self, "_filterType"):
				image = self._applyColorFilter(image, magnifierParameters.filter)

			# Scale image to fill the entire panel (this applies the zoom magnification)
			magnifiedImage = image.Scale(panelWidth, panelHeight, wx.IMAGE_QUALITY_BICUBIC)
			magnifiedBitmap = wx.Bitmap(magnifiedImage)
			return magnifiedBitmap
		else:
			log.error(
				f"Screen capture failed at ({captureLeft}, {captureTop}) size {int(captureWidth)}x{int(captureHeight)}",
			)
			return None
