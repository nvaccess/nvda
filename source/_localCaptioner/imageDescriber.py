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
from tones import beep
from controlTypes import Role, State

from .captioner import ImageCaptioner
from .captioner import imageCaptionerFactory


# Module-level configuration
_localCaptioner = None
_beepInterval = 2  # The unit is 0.1s
_beepHz = 300
_beepLength = 100


def _isNavigatorExpected() -> bool:
	""" Check whether the current navigation object is of the expected type
	
	:return: Whether it is an element of the expected type
	"""
	# Get the currently focused object on screen
	obj = api.getNavigatorObject()

	# todo: Choose whether to recognize elements other than images based on configuration
	if obj.role != Role.GRAPHIC:
		# Translators: message when trying to describe an element that is not an image
		ui.message(pgettext("imageDesc", "This is not an image"))
		return False

	if State.OFFSCREEN in obj.states:
		# Translator: Message when image is off screen
		ui.message(pgettext("imageDesc", "Image off screen"))
		return False

	return True


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
		self.isModelDownloading = False

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
		self._prepareCaption()

	def _prepareCaption(self) -> None:
		"""Preparations for running image captions on the current navigator object."""
		if not _isNavigatorExpected():
			return 
			
		if not self.isModelLoaded:
			# Directly load the model here (session only), it may take a while
			self.loadModelInBackground()

		imageData = _screenshotNavigator()

		# Ensure that only one thread is describing the image
		if self.captionThread is not None and self.captionThread.is_alive():
			return

		if self.isModelDownloading:
			return

		self.captionThread = threading.Thread(
			target=self._pollCaption,
			args=(imageData,),
			name="captionThread",
		)
		beep(_beepHz, _beepLength)
		log.debug("starting caption thread")
		self.captionThread.start()

	def _pollCaption(self, imageData: bytes) -> None:
		"""Poll to load the model and run caption to get the results.

		:param imageData: The image data to caption.
		"""
		# Ensure model is loaded
		i = 0
		while self.loadModelThread is not None and self.loadModelThread.is_alive():
			self.loadModelThread.join(0.1)
			i += 1
			if i % _beepInterval == 0:
				beep(_beepHz, _beepLength)

		# Check if model is successfully loaded
		if self.captioner is None:
			log.debug("Captioner not found.")
			return

		pollThread = threading.Thread(
			target=_messageCaption,
			args=(self.captioner, imageData),
			name="RunCaptionThread",
		)
		pollThread.start()

		while pollThread.is_alive():
			pollThread.join(timeout=0.1)
			i += 1
			if i % _beepInterval == 0:
				beep(_beepHz, _beepLength)

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

		# Mark each time the model is loading
		self.isModelDownloading = False

		try:
			self.captioner = imageCaptionerFactory(
				encoderPath=encoderPath,
				decoderPath=decoderPath,
				configPath=configPath,
			)
		except FileNotFoundError:
			self.isModelLoaded = False
			# Should be set before prepareCaptioner checks
			# If not, the user will hear an extra beep
			# and incur the overhead of starting a thread one more time.
			self.isModelDownloading = True
			from gui._localCaptioner.messageDialogs import ImageDescDownloader

			descDownloader = ImageDescDownloader()
			wx.CallAfter(descDownloader.openDownloadDialog)
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
