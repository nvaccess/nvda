# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from logHandler import log
import wx

from .types import MagnifierParameters
from winAPI._displayTracking import OrientationState


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
		screenSize: OrientationState = None,
		magnifierParameters: MagnifierParameters = None,
	):
		self.frameType = frameType
		self.screenSize = screenSize
		self.magnifierParameters = magnifierParameters
		super().__init__(
			parent,
			title=title,
			size=(magnifierParameters.magnifierWidth, magnifierParameters.magnifierHeight),
		)
		self.SetWindowStyle(self.magnifierParameters.styles)
		self.SetPosition(self.magnifierParameters.coordinates)
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


class WindowCreator:
	"""A factory class to create magnifier windows."""

	@staticmethod
	def createMagnifierWindow(
		parent: wx.Frame,
		title: str,
		frameType: str,
		screenSize: OrientationState,
		magnifierParameters: MagnifierParameters,
	) -> MagnifierFrame:
		"""
		Create and return a magnifier window.

		:param parent: The parent wx.Frame
		:param title: The title of the window
		:param frameType: The type of the frame (e.g., "magnifier", "spotlight")
		:param screenSize: The size of the screen
		:param magnifierParameters: The parameters for the magnifier

		:return: An instance of MagnifierFrame
		"""
		window = MagnifierFrame(
			parent=parent,
			title=title,
			frameType=frameType,
			screenSize=screenSize,
			magnifierParameters=magnifierParameters,
		)
		window.setupLayout()
		return window


def getContent(magnifierParameters: MagnifierParameters) -> wx.Image:
	"""
	Placeholder function to get the content for the magnifier.
	In a real implementation, this would capture the screen area defined by magnifierParameters.

	:param magnifierParameters: The parameters defining the area to capture

	:return: A wx.Image representing the captured content
	"""
	# Placeholder implementation
	width = magnifierParameters.magnifierWidth
	height = magnifierParameters.magnifierHeight
	x = magnifierParameters.coordinates.x
	y = magnifierParameters.coordinates.y
	image = wx.Image(width, height)
	image.SetRGBRect(wx.Rect(x, y, width, height), 200, 200, 200)
	return image
