# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import math
import os
import json
import re
import io
from functools import lru_cache

from PIL import Image

from logHandler import log

from .base import ImageCaptioner
from .winML import _WinML
from ..modelConfig import (
	_EncoderConfig,
	_DecoderConfig,
	_GenerationConfig,
	_ModelConfig,
	_PreprocessorConfig,
	_createConfigFromDict,
)
from .. import modelConfig


class VitGpt2ImageCaptioner(ImageCaptioner):
	"""Lightweight ONNX Runtime image captioning model.

	This class provides image captioning functionality using ONNX models
	without PyTorch dependencies. It uses a Vision Transformer encoder
	and GPT-2 decoder for generating captions.
	"""

	def __init__(
		self,
		encoderPath: str,
		decoderPath: str,
		configPath: str,
		enableProfiling: bool = False,
	) -> None:
		"""Initialize the lightweight ONNX image captioning model.

		:param encoderPath: Path to the ViT encoder ONNX model.
		:param decoderPath: Path to the GPT-2 decoder ONNX model.
		:param configPath: Path to the configuration file (required).
		:param enableProfiling: Whether to enable ONNX Runtime profiling.
		:raises FileNotFoundError: If config file is not found.
		:raises Exception: If model initialization fails.
		"""
		# Import late to avoid importing numpy at initialization
		import onnxruntime as ort
		_WinML().registerExecutionProvidersToOrt()

		# Load configuration file
		try:
			with open(configPath, "r", encoding="utf-8") as f:
				self.config = json.load(f)
		except FileNotFoundError:
			raise FileNotFoundError(
				f"Caption model config file {configPath} not found, "
				"please download models and config file first!",
			)
		except Exception:
			raise

		# Load vocabulary from vocab.json in the same directory as config
		configDir = os.path.dirname(configPath)
		vocabPath = os.path.join(configDir, "vocab.json")
		self.vocab = self._loadVocab(vocabPath)
		self.vocabSize = len(self.vocab)

		preprocessorPath = os.path.join(configDir, "preprocessor_config.json")
		self.preprocessorConfig = self._loadPreprocessorConfig(preprocessorPath)

		# Load all model parameters from configuration
		self._loadModelParams()

		# Configure ONNX Runtime session
		sessionOptions = ort.SessionOptions()
		sessionOptions.set_provider_selection_policy(ort.OrtExecutionProviderDevicePolicy.MAX_EFFICIENCY)
		if enableProfiling:
			sessionOptions.enable_profiling = True

		# Load ONNX models
		try:
			self.encoderSession = ort.InferenceSession(encoderPath, sess_options=sessionOptions)
			self.decoderSession = ort.InferenceSession(decoderPath, sess_options=sessionOptions)
		except (
			ort.capi.onnxruntime_pybind11_state.InvalidProtobuf,
			ort.capi.onnxruntime_pybind11_state.NoSuchFile,
		) as e:
			raise FileNotFoundError(
				"model file incomplete"
				f" Please check whether the file is complete or re-download. Original error: {e}",
			) from e

		log.debug(
			f"Loaded ONNX models - Encoder: {os.path.basename(encoderPath)}, Decoder: {os.path.basename(decoderPath)}",
		)
		log.debug(f"Loaded config : {os.path.basename(configPath)}")
		log.debug(f"Loaded vocabulary : {os.path.basename(vocabPath)}")
		log.debug(
			f"Model config - Image size: {self.encoderConfig.image_size}, Max length: {self.decoderConfig.max_length}",
		)

	def _loadModelParams(self) -> None:
		"""Load all model parameters from configuration file."""
		# Load encoder configuration
		encoder_dict = self.config.get("encoder", {})
		self.encoderConfig = _createConfigFromDict(
			_EncoderConfig,
			encoder_dict,
			modelConfig._DEFAULT_ENCODER_CONFIG,
		)

		# Load decoder configuration
		decoder_dict = self.config.get("decoder", {})
		self.decoderConfig = _createConfigFromDict(
			_DecoderConfig,
			decoder_dict,
			modelConfig._DEFAULT_DECODER_CONFIG,
		)

		# Load generation configuration
		generation_dict = self.config.get("generation", {})
		self.generationConfig = _createConfigFromDict(
			_GenerationConfig,
			generation_dict,
			modelConfig._DEFAULT_GENERATION_CONFIG,
		)

		# Load main model configuration
		self.modelConfig = _createConfigFromDict(_ModelConfig, self.config, modelConfig._DEFAULT_MODEL_CONFIG)

	def _loadVocab(self, vocabPath: str) -> dict[int, str]:
		"""Load vocabulary file.

		:param vocabPath: Path to vocab.json file.
		:return: Dictionary mapping token IDs to tokens.
		"""
		try:
			with open(vocabPath, "r", encoding="utf-8") as f:
				vocabData = json.load(f)

			# Convert to id -> token format
			vocab = {v: k for k, v in vocabData.items()}
			log.debug(f"Successfully loaded vocabulary with {len(vocab)} tokens")
			return vocab

		except FileNotFoundError:
			log.exception(f"vocab.json not found at {vocabPath}")
			raise
		except Exception:
			log.exception(f"Could not load vocabulary from {vocabPath}")
			raise

	def _loadPreprocessorConfig(self, preprocessorPath: str) -> _PreprocessorConfig:
		"""Load preprocessor configuration from preprocessor_config.json."""
		try:
			with open(preprocessorPath, "r", encoding="utf-8") as f:
				preprocessor_dict = json.load(f)
		except FileNotFoundError:
			log.warning("Preprocessor config not found, using defaults")
			return modelConfig._DEFAULT_PREPROCESSOR_CONFIG
		else:
			return _createConfigFromDict(
				_PreprocessorConfig,
				preprocessor_dict,
				modelConfig._DEFAULT_PREPROCESSOR_CONFIG,
			)

	@staticmethod
	def scaleImage(image: Image.Image, scaleFactor: float | int) -> Image.Image:
		def scalePixel(pixelValue: float) -> float:
			return pixelValue * scaleFactor

		return Image.eval(image, scalePixel)

	@staticmethod
	def normalizeImage(image: Image.Image) -> Image.Image:
		# split image into bands
		bands = image.split()
		newBands: list[Image.Image] = []
		for band in bands:
			pixels = list(band.getdata())  # Get all pixel values as a list
			count = len(pixels)
			mean = sum(pixels) / count
			var = sum((p - mean) ** 2 for p in pixels) / count
			stdDev = math.sqrt(var) if var else 1.0

			def scalePixel(pixelValue: float) -> float:
				return (pixelValue - mean) / stdDev

			newBands.append(Image.eval(band, scalePixel))
		return Image.merge("RGB", newBands)

	def _preprocessImage(self, image: str | bytes) -> list[list[list[float]]]:
		"""Preprocess image for model input using external configuration.

		:param image: Image file path or binary data.
		:return: Preprocessed image array ready for model input.
		"""
		# Load image
		if isinstance(image, str) and os.path.isfile(image):
			img = Image.open(image).convert("RGB")
		else:
			img = Image.open(io.BytesIO(image)).convert("RGB")

		# Resize image if configured
		if self.preprocessorConfig.do_resize:
			target_size = (
				self.preprocessorConfig.size["width"],
				self.preprocessorConfig.size["height"],
			)
			# Map resample integer to PIL constant
			resample_map = {
				0: Image.NEAREST,
				1: Image.LANCZOS,
				2: Image.BILINEAR,
				3: Image.BICUBIC,
				4: Image.BOX,
				5: Image.HAMMING,
			}
			resample_method = resample_map.get(self.preprocessorConfig.resample, Image.LANCZOS)
			img = img.resize(target_size, resample_method)

		# Rescale if configured (typically from [0, 255] to [0, 1])
		if self.preprocessorConfig.do_rescale:
			img = self.scaleImage(img, self.preprocessorConfig.rescale_factor)

		# Normalize if configured
		if self.preprocessorConfig.do_normalize:
			img = self.normalizeImage(img)

		# Adjust dimensions: (H, W, C) -> (1, C, H, W)
		pixels = list(img.getdata())
		r: list[float] = [p[0] / 255.0 for p in pixels]
		g: list[float] = [p[1] / 255.0 for p in pixels]
		b: list[float] = [p[2] / 255.0 for p in pixels]
		chw_list = [[[r, g, b]]]  # Adding batch dimension: [1, 3, 224, 224]

		return chw_list

	def _encodeImage(self, image: list[list[list[float]]]) -> list:
		"""Encode image using ViT encoder.

		:param imageArray: Preprocessed image array.
		:return: Encoder hidden states.
		"""
		# Get encoder input name
		inputName = self.encoderSession.get_inputs()[0].name

		# Run encoder inference
		encoderOutputs = self.encoderSession.run(None, {inputName: image})

		# Return last hidden state
		return encoderOutputs[0]

	def _decodeTokens(self, tokenIds: list[int]) -> str:
		"""Decode token IDs to text.

		:param tokenIds: List of token IDs.
		:return: Decoded text string.
		"""
		tokens = []
		for tokenId in tokenIds:
			if tokenId in self.vocab:
				token = self.vocab[tokenId]
				if token not in ["<|endoftext|>", "<|pad|>"]:
					tokens.append(token)

		# Simple text post-processing
		# Ġ (Unicode U+0120) is used by GPT-2 and RoBERTa to indicate space at the beginning of a word in their vocabulary
		text = " ".join(tokens).replace("Ġ", " ")

		# Basic text cleaning
		text = re.sub(r"\s+", " ", text)  # Merge multiple spaces
		text = text.strip()

		return text

	def _getDecoderInputNames(self) -> list[str]:
		"""Get decoder input names for debugging.

		:returns: List of decoder input names.
		"""
		return [inp.name for inp in self.decoderSession.get_inputs()]

	def _getDecoderOutputNames(self) -> list[str]:
		"""Get decoder output names for debugging.

		:return: List of decoder output names.
		"""
		return [out.name for out in self.decoderSession.get_outputs()]

	def _initializePastKeyValues(self, batchSize: int = 1) -> dict[str, list]:
		"""Initialize past_key_values for decoder.

		:param batchSize: Batch size for inference.
		:return: Dictionary of initialized past key values.
		"""
		pastKeyValues = {}

		def zerosNdArray(shape: tuple) -> list:
			if not shape:
				return 0.0
			return [zerosNdArray(shape[1:]) for _ in range(shape[0])]

		# Create key and value for each layer
		for layerIdx in range(self.decoderConfig.n_layer):
			# Key and value shape: (batch_size, num_heads, 0, head_dim)
			# Initial sequence length is 0
			headDim = self.decoderConfig.n_embd // self.decoderConfig.n_head

			keyShape = (batchSize, self.decoderConfig.n_head, 0, headDim)
			valueShape = (batchSize, self.decoderConfig.n_head, 0, headDim)

			pastKeyValues[f"past_key_values.{layerIdx}.key"] = zerosNdArray(keyShape)
			pastKeyValues[f"past_key_values.{layerIdx}.value"] = zerosNdArray(valueShape)

		return pastKeyValues

	def _generateWithGreedy(
		self,
		encoderHiddenStates: list,
		maxLength: int | None = None,
	) -> str:
		"""Generate text using greedy search.


		:param encoderHiddenStates: Encoder hidden states.
		:param maxLength: Maximum generation length.
		:return: Generated text string.
		"""
		if maxLength is None:
			maxLength = self.decoderConfig.max_length

		# Initialize input sequence
		inputIds = [[self.modelConfig.bos_token_id]]
		generatedTokens = []

		# Initialize past_key_values
		pastKeyValues = self._initializePastKeyValues(batchSize=1)

		for step in range(maxLength):
			# Prepare decoder inputs
			decoderInputs = {
				"input_ids": inputIds if step == 0 else [[generatedTokens[-1]]],
				"encoder_hidden_states": encoderHiddenStates,
				"use_cache_branch": [True],
			}

			# Add past_key_values to inputs
			decoderInputs.update(pastKeyValues)

			# Run decoder
			decoderOutputs = self.decoderSession.run(None, decoderInputs)
			logits = decoderOutputs[0]  # Shape: (batch_size, seq_len, vocab_size)

			# Greedy selection of next token
			nextTokenLogits = logits[0, -1, :]  # Logits for last position
			nextTokenId = max(range(len(nextTokenLogits)), key=nextTokenLogits.__getitem__)  # argmax

			# Check if generation should end
			if nextTokenId == self.modelConfig.eos_token_id:
				break

			generatedTokens.append(nextTokenId)

			# Update past_key_values from outputs
			if len(decoderOutputs) > 1:
				for layerIdx in range(self.decoderConfig.n_layer):
					if len(decoderOutputs) > 1 + layerIdx * 2 + 1:
						# [3] -> layer1 key, [4] -> layer1 value
						keyIndex = 1 + layerIdx * 2
						valueIndex = keyIndex + 1
						pastKeyValues[f"past_key_values.{layerIdx}.key"] = decoderOutputs[keyIndex]
						pastKeyValues[f"past_key_values.{layerIdx}.value"] = decoderOutputs[valueIndex]

			# Avoid sequences that are too long
			if len(generatedTokens) >= self.decoderConfig.n_ctx - 1:
				break

		# Decode generated text
		return self._decodeTokens(generatedTokens)

	@lru_cache()
	def generateCaption(
		self,
		image: str | bytes,
		maxLength: int | None = None,
	) -> str:
		"""Generate image caption.

		:param image: Image file path or binary data.
		:param maxLength: Maximum generation length.
		:return: Generated image caption.
		"""
		# Preprocess image
		imageArray = self._preprocessImage(image)

		# Encode image
		encoderHiddenStates = self._encodeImage(imageArray)

		# Generate text
		caption = self._generateWithGreedy(encoderHiddenStates, maxLength)

		return caption
