# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import json

from logHandler import log
from .base import ImageCaptioner


def imageCaptionerFactory(
	configPath: str,
	encoderPath: str | None = None,
	decoderPath: str | None = None,
	monomericModelPath: str | None = None,
) -> ImageCaptioner:
	"""Initialize the image caption generator.

	:param monomericModelPath: Path to a single merged model file.
	:param encoderPath: Path to the encoder model file.
	:param decoderPath: Path to the decoder model file.
	:param configPath: Path to the configuration file.
	:raises ValueError: If neither a single model nor both encoder and decoder are provided.
	:raises FileNotFoundError: If config file not found.
	:raises NotImplementedError: if model architecture is unsupported
	:raises Exception: If config.json fail to load.
	:return: instance of ImageCaptioner
	"""
	if not monomericModelPath and not (encoderPath and decoderPath):
		raise ValueError(
			"You must provide either 'monomericModelPath' or both 'encoderPath' and 'decoderPath'.",
		)

	try:
		with open(configPath, "r", encoding="utf-8") as f:
			config = json.load(f)
	except FileNotFoundError:
		raise FileNotFoundError(
			f"Caption model config file {configPath} not found, "
			"please download models and config file first!",
		)
	except Exception:
		log.exception("config file not found")
		raise

	modelArchitecture = config["architectures"][0]
	if modelArchitecture == "VisionEncoderDecoderModel":
		from .vitGpt2 import VitGpt2ImageCaptioner

		return VitGpt2ImageCaptioner(encoderPath, decoderPath, configPath)
	else:
		raise NotImplementedError("Unsupported model architectures")
