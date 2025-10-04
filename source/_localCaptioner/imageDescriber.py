# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""ImageDescriber module for NVDA.

This module provides local image captioning functionality using ONNX models.
It allows users to capture screen regions and generate captions using local AI models.
"""

import io
import threading
from threading import Thread
import os

import wx
import config
from logHandler import log
import ui
import api
from keyboardHandler import KeyboardInputGesture
from NVDAState import WritePaths
import core

from .captioner import ImageCaptioner
from .captioner import imageCaptionerFactory


# Module-level configuration
_localCaptioner = None


def _screenshotNavigator() -> bytes:
	"""Capture a screenshot of the current navigator object.

	:Return: The captured image data as bytes in JPEG format.
	"""
	# Get the currently focused object on screen
	obj = api.getNavigatorObject()

	# Get the object's position and size information
	x, y, width, height = obj.location

	# Create a bitmap with the same size as the object
	bmp = wx.Bitmap(width, height)

	# Create a memory device context for drawing operations on the bitmap
	mem = wx.MemoryDC(bmp)

	# Copy the specified screen region to the memory bitmap
	mem.Blit(0, 0, width, height, wx.ScreenDC(), x, y)

	# Convert the bitmap to an image object for more flexible operations
	image = bmp.ConvertToImage()

	# Create a byte stream object to save image data as binary data
	body = io.BytesIO()

	# Save the image to the byte stream in JPEG format
	image.SaveFile(body, wx.BITMAP_TYPE_JPEG)

	# Read the binary image data from the byte stream
	imageData = body.getvalue()
	return imageData


def _messageCaption(captioner: ImageCaptioner, imageData: bytes) -> None:
	"""Generate a caption for the given image data.

	:param captioner: The captioner instance to use for generation.
	:param imageData: The image data to caption.
	"""
	try:
		description = captioner.generateCaption(image=imageData)
	except Exception:
		# Translators: error message when an image description cannot be generated
		wx.CallAfter(ui.message, pgettext("imageDesc", "Failed to generate description"))
		log.exception("Failed to generate caption")
	else:
		wx.CallAfter(ui.message, description)


class ImageDescriber:
	"""module for local image caption functionality.

	This module provides image captioning using local ONNX models.
	It can capture screen regions and generate descriptive captions.
	"""

	def __init__(self) -> None:
		self.isModelLoaded = False
		self.captioner: ImageCaptioner | None = None
		self.captionThread: Thread | None = None
		self.loadModelThread: Thread | None = None

		enable = config.conf["automatedImageDescriptions"]["enable"]
		# Load model when initializing (may cause high memory usage)
		if enable:
			core.postNvdaStartup.register(self.loadModelInBackground)

	def terminate(self):
		for t in [self.captionThread, self.loadModelThread]:
			if t is not None and t.is_alive():
				t.join()

		self.captioner = None

	def runCaption(self, gesture: KeyboardInputGesture) -> None:
		"""Script to run image captioning on the current navigator object.

		:param gesture: The input gesture that triggered this script.
		"""
		imageData = _screenshotNavigator()

		if not self.isModelLoaded:
			# Translators: Message when image description is not enabled
			ui.message(pgettext("imageDesc", "image description is not enabled"))
			return

		self.captionThread = threading.Thread(
			target=_messageCaption,
			args=(self.captioner, imageData),
			name="RunCaptionThread",
		)
		# Translators: Message when starting image recognition
		ui.message(pgettext("imageDesc", "getting image description..."))
		self.captionThread.start()

	def _loadModel(self, localModelDirPath: str | None = None) -> None:
		"""Load the ONNX model for image captioning.

		:param localModelDirPath: path of model directory
		"""

		if not localModelDirPath:
			baseModelsDir = WritePaths.modelsDir
			localModelDirPath = os.path.join(
				baseModelsDir,
				config.conf["automatedImageDescriptions"]["defaultModel"],
			)
		encoderPath = f"{localModelDirPath}/onnx/encoder_model_quantized.onnx"
		decoderPath = f"{localModelDirPath}/onnx/decoder_model_merged_quantized.onnx"
		configPath = f"{localModelDirPath}/config.json"

		try:
			self.captioner = imageCaptionerFactory(
				encoderPath=encoderPath,
				decoderPath=decoderPath,
				configPath=configPath,
			)
		except FileNotFoundError:
			self.isModelLoaded = False
			from gui._localCaptioner.messageDialogs import openDownloadDialog

			wx.CallAfter(openDownloadDialog)
		except Exception:
			self.isModelLoaded = False
			# Translators: error message when fail to load model
			wx.CallAfter(ui.message, pgettext("imageDesc", "failed to load image captioner"))
			log.exception("Failed to load image captioner model")
		else:
			self.isModelLoaded = True
			# Translators: Message when successfully load the model
			wx.CallAfter(ui.message, pgettext("imageDesc", "image captioning on"))

	def loadModelInBackground(self, localModelDirPath: str | None = None) -> None:
		"""load model in child thread

		:param localModelDirPath: path of model directory
		"""
		self.loadModelThread = threading.Thread(
			target=self._loadModel,
			args=(localModelDirPath,),
			name="LoadModelThread",
		)
		self.loadModelThread.start()

	def _doReleaseModel(self) -> None:
		if hasattr(self, "captioner") and self.captioner:
			del self.captioner
			self.captioner = None
			# Translators: Message when image captioning terminates
			ui.message(pgettext("imageDesc", "image captioning off"))
			self.isModelLoaded = False

	def toggleSwitch(self) -> None:
		"""do load/unload the model from memory."""
		if self.isModelLoaded:
			self._doReleaseModel()
		else:
			self.loadModelInBackground()

	def toggleImageCaptioning(self, gesture: KeyboardInputGesture) -> None:
		"""do load/unload the model from memory.

		:param gesture: gesture to toggle this function
		"""
		self.toggleSwitch()
