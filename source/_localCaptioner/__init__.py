# -*- coding: UTF-8 -*-
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
import sys
from typing import Optional
import base64
import json
import io
import threading

import wx
import gui
from gui import guiHelper
import globalVars
import config
from logHandler import log
from keyboardHandler import KeyboardInputGesture
import scriptHandler
import ui
import globalPluginHandler
import api

from .captioner import ImageCaptioner
from .modelManager import ModelManagerFrame
from .panel import CaptionLocalSettingsPanel

try:
	import addonHandler

	addonHandler.initTranslation()
except:
	pass

# Module-level configuration
_here = os.path.dirname(__file__)
_modelsDir = os.path.join(_here, "..", "..", "models")
_modelsDir = os.path.abspath(_modelsDir)

CONFSPEC = {
	"localModelPath": f"string(default={_modelsDir}/Xenova/vit-gpt2-image-captioning)",
	"loadModelWhenInit": "boolean(default=false)",
}

config.conf.spec["captionLocal"] = CONFSPEC


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
		result = api.copyToClip(text=description, notify=False)
	except Exception as e:
		ui.message(str(e))
		log.error(e)


def disableInSecureMode(decoratedCls):
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls


@disableInSecureMode
# class GlobalPlugin(globalPluginHandler.GlobalPlugin):
class LocalCaptioner:
	"""Global plugin for Caption Local functionality.

	This plugin provides image captioning using local ONNX models.
	It can capture screen regions and generate descriptive captions.
	"""

	def __init__(self) -> None:
		"""Initialize the global plugin."""
		# super().__init__()
		self.isModelLoaded = False
		self.captioner: Optional[ImageCaptioner] = None
		self.managerFrame: Optional[ModelManagerFrame] = None

		loadModelWhenInit = config.conf["captionLocal"]["loadModelWhenInit"]
		# Load model when initializing plugin (may cause high memory usage)
		if loadModelWhenInit:
			threading.Thread(target=self._loadModel, daemon=True).start()

		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(CaptionLocalSettingsPanel)

	def terminate(self) -> None:
		"""Clean up resources when the plugin is terminated."""
		try:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(CaptionLocalSettingsPanel)
		except (ValueError, AttributeError):
			pass

	def runCaption(self, gesture) -> None:
		# def script_runCaption(self) -> None:
		"""Script to run image captioning on the current navigator object.

		Args:
			gesture: The input gesture that triggered this script.
		"""
		imageData = shootImage()

		if not self.isModelLoaded:
			# Translators: Message when loading the model
			ui.message(_("loading model..."))
			self._loadModel()

		imageThread = threading.Thread(target=caption, args=(self.captioner, imageData))
		# Translators: Message when starting image recognition
		ui.message(_("starting recognize"))
		imageThread.start()

	def _loadModel(self) -> None:
		"""Load the ONNX model for image captioning.

		Raises:
			Exception: If the model cannot be loaded.
		"""
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
		except Exception as e:
			self.isModelLoaded = False
			ui.message(str(e))
			raise

	def releaseModel(self, gesture) -> None:
		"""Script to release the loaded model from memory.

		Args:
			gesture: The input gesture that triggered this script.
		"""
		# Translators: Message when releasing the model
		ui.message(_("releasing model..."))
		try:
			if hasattr(self, "captioner") and self.captioner:
				del self.captioner
				self.captioner = None
				# Translators: Message when model is successfully released
				ui.message(_("model released and memory freed"))
				self.isModelLoaded = False
		except Exception as e:
			ui.message(str(e))
			raise

	def openManager(self, gesture) -> None:
		"""Script to open the model manager window.

		Args:
			gesture: The input gesture that triggered this script.
		"""
		# Translators: Message when opening model manager
		ui.message(_("opening model manager..."))
		try:
			self._openModelManager()
		except Exception as e:
			ui.message(str(e))
			raise

	def _openModelManager(self) -> None:
		"""Open the model manager frame window."""

		def showManager() -> None:
			"""Show the model manager window."""
			try:
				# Use existing wx.App if available
				app = wx.GetApp()
				if app is None:
					app = wx.App()

				if not hasattr(self, "managerFrame") or not self.managerFrame:
					self.managerFrame = ModelManagerFrame()

				self.managerFrame.Show()
				self.managerFrame.Raise()

			except Exception as e:
				ui.message(str(e))

		# Ensure execution in main thread
		wx.CallAfter(showManager)


def getLocalCaptionerConfig():
	return config.conf["localcaptioner"]


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
