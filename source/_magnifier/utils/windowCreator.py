# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from logHandler import log
import wx

from .types import MagnifierParameters, WindowMagnifierParameters, Size, Filter


class MagnifierPanel(wx.Panel):
	"""A simple panel for the magnifier."""

	def __init__(self, parent: wx.Frame, panelType: str):
		"""
		Initialize the magnifier panel.

		:param parent: The parent frame that will contain this panel
		:param panelType: The type/name identifier for this panel
		"""
		super().__init__(parent)

		self.panelType = panelType
		self.SetName(panelType)

		self.contentBitmap = None

		self.Bind(wx.EVT_PAINT, self.onPaint)

	def setContent(self, content: wx.Bitmap | wx.Image | None) -> None:
		"""
		Set the content image to be displayed in the magnifier panel.

		:param content: The content to display - can be a wx.Bitmap, wx.Image, or None to clear
		"""
		if not content:
			self.contentBitmap = None
			return

		if isinstance(content, wx.Bitmap):
			if content.IsOk():
				self.contentBitmap = content
				log.debug(f"Bitmap content set: {content.GetWidth()}x{content.GetHeight()}")
			else:
				self.contentBitmap = None
				log.debug("Invalid bitmap content")
		elif isinstance(content, wx.Image):
			if content.IsOk():
				self.contentBitmap = wx.Bitmap(content)
				log.debug(f"Image content set: {content.GetWidth()}x{content.GetHeight()}")
			else:
				self.contentBitmap = None
				log.debug("Invalid image content")

		self.Refresh()
		log.debug(f"{self.panelType.capitalize()} panel refreshed")

	def onPaint(self, event: wx.PaintEvent) -> None:
		"""Handle the paint event to draw the magnified content."""
		dc = wx.PaintDC(self)
		dc.Clear()

		if self.contentBitmap and self.contentBitmap.IsOk():
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
		"""
		Initialize the magnifier frame window.

		:param parent: Optional parent window
		:param title: The window title
		:param frameType: The type identifier for the frame
		:param screenSize: The screen size (optional, for reference)
		:param windowMagnifierParameters: Parameters defining window size, position, and styles
		"""
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
		# Setup sizer for proper layout
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.panel, 1, wx.EXPAND)
		self.SetSizer(sizer)
		self.Layout()
		self.Show()

	def createPanel(self) -> MagnifierPanel:
		"""Create and return a magnifier panel."""
		return MagnifierPanel(self, self.frameType)

	def updateFrameContent(self, content: wx.Bitmap | wx.Image | None) -> None:
		"""Update the content displayed in the magnifier frame."""
		if self.panel:
			self.panel.setContent(content)


class WindowedMagnifier:
	"""
	Base class for magnifiers that use a separate window to display magnified content.
	Provides common functionality for creating and managing the magnifier window and panel.
	"""

	def __init__(self, windowMagnifierParameters: WindowMagnifierParameters):
		"""
		Initialize the windowed magnifier.

		:param windowMagnifierParameters: Parameters defining the magnifier window configuration
		"""
		self.windowMagnifierParameters = windowMagnifierParameters
		self._frame = MagnifierFrame(
			title=self.windowMagnifierParameters.title,
			frameType="magnifier",
			screenSize=self.windowMagnifierParameters.windowSize,
			windowMagnifierParameters=self.windowMagnifierParameters,
		)
		self._panel = self._frame.panel

	def _applyColorFilter(self, image: wx.Image, filterType: Filter) -> wx.Image:
		"""
		Apply color filter directly on bytes for optimal performance.

		:param image: The image to apply the filter to
		:param filterType: The filter type to apply (NORMAL, GRAYSCALE, INVERTED)
		:return: The filtered image
		"""
		if filterType == Filter.NORMAL or not image or not image.IsOk():
			return image

		width, height = image.GetWidth(), image.GetHeight()
		data = image.GetData()  # Returns RGB data as bytes

		# Use bytearray for direct manipulation (faster than array.array)
		rgb_data = bytearray(data)

		if filterType == Filter.GRAYSCALE:
			# Process 3 bytes at a time (R, G, B)
			for i in range(0, len(rgb_data), 3):
				r, g, b = rgb_data[i], rgb_data[i + 1], rgb_data[i + 2]
				# Standard grayscale formula (ITU-R BT.601)
				gray = int(0.299 * r + 0.587 * g + 0.114 * b)
				rgb_data[i] = rgb_data[i + 1] = rgb_data[i + 2] = gray

		elif filterType == Filter.INVERTED:
			# Invert all values in place
			for i in range(len(rgb_data)):
				rgb_data[i] = 255 - rgb_data[i]

		# Create new image with modified data
		new_image = wx.Image(width, height)
		new_image.SetData(bytes(rgb_data))
		return new_image

	def _setContent(self, magnifierParameters: MagnifierParameters, zoomLevel: float) -> None:
		"""
		Update the magnifier panel with captured and processed content.

		:param magnifierParameters: Parameters defining what and how to capture
		:param zoomLevel: The zoom magnification level to apply
		"""
		content = self._getContent(magnifierParameters, zoomLevel)
		if self._panel:
			self._panel.setContent(content)
		else:
			log.debug("No panel available to set content")

	def _destroyWindow(self) -> None:
		"""Destroy the magnifier window and clean up resources."""
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
		captureWidth = int(panelWidth / zoomLevel)
		captureHeight = int(panelHeight / zoomLevel)
		captureLeft = int(magnifierParameters.coordinates.x)
		captureTop = int(magnifierParameters.coordinates.y)

		# Capture screen
		screen = wx.ScreenDC()
		bitmap = wx.Bitmap(captureWidth, captureHeight)
		memoryDc = wx.MemoryDC()
		memoryDc.SelectObject(bitmap)
		success = memoryDc.Blit(0, 0, captureWidth, captureHeight, screen, captureLeft, captureTop)
		memoryDc.SelectObject(wx.NullBitmap)

		log.debug(
			f"Capture at ({captureLeft}, {captureTop}) "
			f"size {captureWidth}x{captureHeight} "
			f"zoom {zoomLevel}x -> panel {panelWidth}x{panelHeight}",
		)

		if success and bitmap.IsOk():
			# Convert to image
			image = bitmap.ConvertToImage()

			image = self._applyColorFilter(image, magnifierParameters.filter)

			# Scale image to fill the entire panel (this applies the zoom magnification)
			magnifiedImage = image.Scale(panelWidth, panelHeight, wx.IMAGE_QUALITY_BICUBIC)
			magnifiedBitmap = wx.Bitmap(magnifiedImage)
			return magnifiedBitmap
		else:
			log.error(
				f"Screen capture failed at ({captureLeft}, {captureTop}) size {captureWidth}x{captureHeight}",
			)
			return None
