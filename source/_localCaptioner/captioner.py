# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import os
import json
import re
import io
from abc import ABC, abstractmethod


import numpy as np
from PIL import Image

from logHandler import log

from .modelConfig import (
	_EncoderConfig,
	_DecoderConfig,
	_GenerationConfig,
	_ModelConfig,
	_PreprocessorConfig,
	_createConfigFromDict,
)
from . import modelConfig


class ImageCaptioner(ABC):
	"""Abstract interface for image caption generation.

	Supports generate caption for image
	"""

	@abstractmethod
	def generateCaption(self, image: str | bytes, maxLength: int | None = None) -> str:
		"""
		Generate a caption for the given image.

		:param image: Image file path or binary data.
		:param maxLength: Optional maximum length for the generated caption.
		:return: The generated image caption as a string.
		"""
		pass


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
		import onnxruntime as ort
		
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
		if enableProfiling:
			sessionOptions.enable_profiling = True

		# Load ONNX models
		try:
			self.encoderSession = ort.InferenceSession(encoderPath, sess_options=sessionOptions)
			self.decoderSession = ort.InferenceSession(decoderPath, sess_options=sessionOptions)
		except ort.capi.onnxruntime_pybind11_state.InvalidProtobuf as e:
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
			log.info(f"Successfully loaded vocabulary with {len(vocab)} tokens")
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

	def _preprocessImage(self, image: str | bytes) -> np.ndarray:
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

		# Convert to numpy array
		imgArray = np.array(img).astype(np.float32)

		# Rescale if configured (typically from [0, 255] to [0, 1])
		if self.preprocessorConfig.do_rescale:
			imgArray = imgArray * self.preprocessorConfig.rescale_factor

		# Normalize if configured
		if self.preprocessorConfig.do_normalize:
			mean = np.array(self.preprocessorConfig.image_mean, dtype=np.float32)
			std = np.array(self.preprocessorConfig.image_std, dtype=np.float32)
			imgArray = (imgArray - mean) / std

		# Adjust dimensions: (H, W, C) -> (1, C, H, W)
		imgArray = np.transpose(imgArray, (2, 0, 1))
		imgArray = np.expand_dims(imgArray, axis=0)

		return imgArray

	def _encodeImage(self, imageArray: np.ndarray) -> np.ndarray:
		"""Encode image using ViT encoder.

		:param imageArray: Preprocessed image array.
		:return: Encoder hidden states.
		"""
		# Get encoder input name
		inputName = self.encoderSession.get_inputs()[0].name

		# Run encoder inference
		imageArray = imageArray.astype(np.float32)
		encoderOutputs = self.encoderSession.run(None, {inputName: imageArray})

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

	def _initializePastKeyValues(self, batchSize: int = 1) -> dict[str, np.ndarray]:
		"""Initialize past_key_values for decoder.

		:param batchSize: Batch size for inference.
		:return: Dictionary of initialized past key values.
		"""
		pastKeyValues = {}

		# Create key and value for each layer
		for layerIdx in range(self.decoderConfig.n_layer):
			# Key and value shape: (batch_size, num_heads, 0, head_dim)
			# Initial sequence length is 0
			headDim = self.decoderConfig.n_embd // self.decoderConfig.n_head

			keyShape = (batchSize, self.decoderConfig.n_head, 0, headDim)
			valueShape = (batchSize, self.decoderConfig.n_head, 0, headDim)

			pastKeyValues[f"past_key_values.{layerIdx}.key"] = np.zeros(keyShape, dtype=np.float32)
			pastKeyValues[f"past_key_values.{layerIdx}.value"] = np.zeros(valueShape, dtype=np.float32)

		return pastKeyValues

	def _generateWithGreedy(
		self,
		encoderHiddenStates: np.ndarray,
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
		inputIds = np.array([[self.modelConfig.bos_token_id]], dtype=np.int64)
		generatedTokens = []

		# Initialize past_key_values
		pastKeyValues = self._initializePastKeyValues(batchSize=1)

		for step in range(maxLength):
			# Prepare decoder inputs
			decoderInputs = {
				"input_ids": inputIds if step == 0 else np.array([[generatedTokens[-1]]], dtype=np.int64),
				"encoder_hidden_states": encoderHiddenStates,
				"use_cache_branch": np.array([1], dtype=np.bool_),
			}

			# Add past_key_values to inputs
			decoderInputs.update(pastKeyValues)

			# Run decoder
			decoderOutputs = self.decoderSession.run(None, decoderInputs)
			logits = decoderOutputs[0]  # Shape: (batch_size, seq_len, vocab_size)

			# Greedy selection of next token
			nextTokenLogits = logits[0, -1, :]  # Logits for last position
			nextTokenId = int(np.argmax(nextTokenLogits))

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
		return VitGpt2ImageCaptioner(encoderPath, decoderPath, configPath)
	else:
		raise NotImplementedError("Unsupported model architectures")
