# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
"""Localcaptioner  module  for NVDA.

This module provides local image captioning functionality using ONNX models.
It allows users to capture screen regions and generate captions using local AI models.
"""

from __future__ import unicode_literals

import os

import io
import threading

import wx
import config
from logHandler import log
import ui
import api

from .captioner import ImageCaptioner


# Module-level configuration
_localCaptioner = None


def shootImage() -> bytes:
	"""Capture a screenshot of the current navigator object.

	Returns:
		The captured image data as bytes in JPEG format.
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


def caption(captioner: ImageCaptioner, imageData: bytes) -> None:
	"""Generate a caption for the given image data.

	Args:
		captioner: The captioner instance to use for generation.
		imageData: The image data to caption.
	"""
	try:
		description = captioner.generate_caption(image=imageData)
		ui.message(description)
	except Exception as e:
		# Translators: error message when fail to generate caption
		ui.message(_("fail to generate caption"))
		log.error(e)

	api.copyToClip(text=description, notify=False)


class LocalCaptioner:
	"""module for local image caption functionality.

	This module provides image captioning using local ONNX models.
	It can capture screen regions and generate descriptive captions.
	"""

	def __init__(self) -> None:
		self.isModelLoaded = False
		self.captioner: ImageCaptioner | None = None

		loadModelWhenInit = config.conf["captionLocal"]["loadModelWhenInit"]
		# Load model when initializing (may cause high memory usage)
		if loadModelWhenInit:
			threading.Thread(target=self._loadModel, daemon=True).start()

	def terminate(self):
		self.captioner = None

	def runCaption(self, gesture) -> None:
		"""Script to run image captioning on the current navigator object.

		Args:
			gesture: The input gesture that triggered this script.
		"""
		imageData = shootImage()

		if not self.isModelLoaded:
			self._loadModel()

		imageThread = threading.Thread(target=caption, args=(self.captioner, imageData))
		# Translators: Message when starting image recognition
		ui.message(_("getting Image description..."))
		imageThread.start()

	def _loadModel(self) -> None:
		"""Load the ONNX model for image captioning.

		Raises:
			Exception: If the model cannot be loaded.
		"""
		# Translators: Message when loading the model
		ui.message(_("loading model..."))

		try:
			localModelDirPath = config.conf["captionLocal"]["localModelPath"]
			encoderPath = f"{localModelDirPath}/onnx/encoder_model_quantized.onnx"
			decoderPath = f"{localModelDirPath}/onnx/decoder_model_merged_quantized.onnx"
			configPath = f"{localModelDirPath}/config.json"

			self.captioner = ImageCaptioner(
				encoder_path=encoderPath,
				decoder_path=decoderPath,
				config_path=configPath,
			)
			self.isModelLoaded = True
			# Translators: Message when successfully load the model
			ui.message(_("image captioning on"))
		except FileNotFoundError as e:
			self.isModelLoaded = False
			# Translators: error Message when fail to load the model
			ui.message(
				_(
					"models And config file not found or incomplete, please download models and config file first!",
				),
			)
			log.error(e)
			raise
		except Exception as e:
			self.isModelLoaded = False
			# Translators: error message when fail to load model
			ui.message(_("fail to load model."))
			log.error(e)
			raise

	def _doReleaseModel(self) -> None:
		# Translators: Message when releasing the model
		ui.message(_("releasing model..."))
		try:
			if hasattr(self, "captioner") and self.captioner:
				del self.captioner
				self.captioner = None
				# Translators: Message when model is successfully released
				ui.message(_("image captioning off"))
				self.isModelLoaded = False
		except Exception as e:
			ui.message(str(e))
			raise

	def toggleImageCaptioning(self, gesture) -> None:
		"""Script to load/unload the model from memory.

		Args:
			gesture: The input gesture that triggered this script.
		"""
		if self.isModelLoaded:
			self._doReleaseModel()
		else:
			self._loadModel()


def initialize():
	"""Initialise the local captioner."""
	global _localCaptioner
	log.debug("Initializing local captioner")
	_localCaptioner = LocalCaptioner()


def terminate():
	"""Terminate the local captioner."""
	global _localCaptioner
	if _localCaptioner is None:
		log.debug("local captioner not running.")
		return
	log.debug("Terminating local captioner")
	_localCaptioner.terminate()
	_localCaptioner = None
