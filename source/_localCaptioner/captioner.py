# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
from __future__ import unicode_literals

import os
import json
import re
import io
import time
from typing import Dict

import numpy as np
from PIL import Image
import onnxruntime as ort

from logHandler import log


class ImageCaptioner:
	"""Lightweight ONNX Runtime image captioning model.

	This class provides image captioning functionality using ONNX models
	without PyTorch dependencies. It uses a Vision Transformer encoder
	and GPT-2 decoder for generating captions.
	"""

	def __init__(
		self,
		encoder_path: str,
		decoder_path: str,
		config_path: str,
		enableProfiling: bool = False,
	) -> None:
		"""Initialize the lightweight ONNX image captioning model.

		Args:
			encoder_path: Path to the ViT encoder ONNX model.
			decoder_path: Path to the GPT-2 decoder ONNX model.
			config_path: Path to the configuration file (required).
			enableProfiling: Whether to enable ONNX Runtime profiling.

		Raises:
			FileNotFoundError: If config file is not found.
			Exception: If model initialization fails.
		"""
		# Load configuration file
		try:
			with open(config_path, "r", encoding="utf-8") as f:
				self.config = json.load(f)
		except FileNotFoundError:
			raise FileNotFoundError(
				f"Caption model config file {config_path} not found, "
				"please download models and config file first!",
			)
		except Exception as e:
			log.error(e)
			raise

		# Load vocabulary from vocab.json in the same directory as config
		configDir = os.path.dirname(config_path)
		vocabPath = os.path.join(configDir, "vocab.json")
		self.vocab = self._loadVocab(vocabPath)
		self.vocabSize = len(self.vocab)

		# Load all model parameters from configuration
		self._loadModelParams()

		# Configure ONNX Runtime session
		sessionOptions = ort.SessionOptions()
		if enableProfiling:
			sessionOptions.enable_profiling = True

		# Load ONNX models
		self.encoderSession = ort.InferenceSession(encoder_path, sess_options=sessionOptions)
		self.decoderSession = ort.InferenceSession(decoder_path, sess_options=sessionOptions)

		log.info(
			f"Loaded ONNX models - Encoder: {os.path.basename(encoder_path)}, Decoder: {os.path.basename(decoder_path)}",
		)
		log.info(f"Loaded config from: {os.path.basename(config_path)}")
		log.info(f"Loaded vocabulary from: {os.path.basename(vocabPath)}")
		log.info(f"Model config - Image size: {self.imageSize}, Max length: {self.maxLength}")

	def _loadModelParams(self) -> None:
		"""Load all model parameters from configuration file."""
		# Encoder parameters
		encoderConfig = self.config.get("encoder", {})
		self.imageSize = encoderConfig.get("image_size", 224)
		self.numChannels = encoderConfig.get("num_channels", 3)
		self.patchSize = encoderConfig.get("patch_size", 16)
		self.encoderHiddenSize = encoderConfig.get("hidden_size", 768)
		self.encoderNumLayers = encoderConfig.get("num_hidden_layers", 12)
		self.encoderNumHeads = encoderConfig.get("num_attention_heads", 12)
		self.encoderIntermediateSize = encoderConfig.get("intermediate_size", 3072)

		# Decoder parameters
		decoderConfig = self.config.get("decoder", {})
		self.maxLength = decoderConfig.get("max_length", 20)
		self.decoderVocabSize = decoderConfig.get("vocab_size", 50257)
		self.nEmbd = decoderConfig.get("n_embd", 768)
		self.nLayer = decoderConfig.get("n_layer", 12)
		self.nHead = decoderConfig.get("n_head", 12)
		self.nCtx = decoderConfig.get("n_ctx", 1024)
		self.nPositions = decoderConfig.get("n_positions", 1024)

		# Special token IDs
		self.bosTokenId = self.config.get("bos_token_id", 50256)
		self.eosTokenId = self.config.get("eos_token_id", 50256)
		self.padTokenId = self.config.get("pad_token_id", 50256)

		# Generation parameters
		generationConfig = self.config.get("generation", {})
		self.doSample = generationConfig.get("do_sample", False)
		self.numBeams = generationConfig.get("num_beams", 1)
		self.temperature = generationConfig.get("temperature", 1.0)
		self.topK = generationConfig.get("top_k", 50)
		self.topP = generationConfig.get("top_p", 1.0)
		self.repetitionPenalty = generationConfig.get("repetition_penalty", 1.0)
		self.lengthPenalty = generationConfig.get("length_penalty", 1.0)

	def _loadVocab(self, vocabPath: str) -> Dict[int, str]:
		"""Load vocabulary file.

		Args:
			vocabPath: Path to vocab.json file.

		Returns:
			Dictionary mapping token IDs to tokens.
		"""
		try:
			with open(vocabPath, "r", encoding="utf-8") as f:
				vocabData = json.load(f)

			# Convert to id -> token format
			vocab = {v: k for k, v in vocabData.items()}
			log.info(f"Successfully loaded vocabulary with {len(vocab)} tokens")
			return vocab

		except FileNotFoundError:
			log.error(f"vocab.json not found at {vocabPath}")
			raise
		except Exception as e:
			log.error(f"Warning: Could not load vocabulary from {vocabPath}: {e}")
			raise

	def preprocessImage(self, image: str | bytes) -> np.ndarray:
		"""Preprocess image for model input.

		Args:
			image: Image file path or binary data.

		Returns:
			Preprocessed image array ready for model input.
		"""
		if isinstance(image, str):
			img = Image.open(image).convert("RGB")
		else:
			img = Image.open(io.BytesIO(image)).convert("RGB")

		# Resize image
		img = img.resize((self.imageSize, self.imageSize), Image.LANCZOS)

		# Convert to numpy array and normalize to [0, 1]
		imgArray = np.array(img).astype(np.float32) / 255.0

		# ImageNet normalization
		mean = np.array([0.485, 0.456, 0.406])
		std = np.array([0.229, 0.224, 0.225])
		imgArray = (imgArray - mean) / std

		# Adjust dimensions: (H, W, C) -> (1, C, H, W)
		imgArray = np.transpose(imgArray, (2, 0, 1))
		imgArray = np.expand_dims(imgArray, axis=0)

		return imgArray

	def encodeImage(self, imageArray: np.ndarray) -> np.ndarray:
		"""Encode image using ViT encoder.

		Args:
			imageArray: Preprocessed image array.

		Returns:
			Encoder hidden states.
		"""
		# Get encoder input name
		inputName = self.encoderSession.get_inputs()[0].name

		# Run encoder inference
		imageArray = imageArray.astype(np.float32)
		encoderOutputs = self.encoderSession.run(None, {inputName: imageArray})

		# Return last hidden state
		return encoderOutputs[0]

	def decodeTokens(self, tokenIds: list[int]) -> str:
		"""Decode token IDs to text.

		Args:
			tokenIds: List of token IDs.

		Returns:
			Decoded text string.
		"""
		tokens = []
		for tokenId in tokenIds:
			if tokenId in self.vocab:
				token = self.vocab[tokenId]
				if token not in ["<|endoftext|>", "<|pad|>"]:
					tokens.append(token)

		# Simple text post-processing
		text = " ".join(tokens).replace("Ġ", " ")

		# Basic text cleaning
		text = re.sub(r"\s+", " ", text)  # Merge multiple spaces
		text = text.strip()

		return text

	def getDecoderInputNames(self) -> list[str]:
		"""Get decoder input names for debugging.

		Returns:
			List of decoder input names.
		"""
		return [inp.name for inp in self.decoderSession.get_inputs()]

	def getDecoderOutputNames(self) -> list[str]:
		"""Get decoder output names for debugging.

		Returns:
			List of decoder output names.
		"""
		return [out.name for out in self.decoderSession.get_outputs()]

	def _initializePastKeyValues(self, batchSize: int = 1) -> Dict[str, np.ndarray]:
		"""Initialize past_key_values for decoder.

		Args:
			batchSize: Batch size for inference.

		Returns:
			Dictionary of initialized past key values.
		"""
		pastKeyValues = {}

		# Create key and value for each layer
		for layerIdx in range(self.nLayer):
			# Key and value shape: (batch_size, num_heads, 0, head_dim)
			# Initial sequence length is 0
			headDim = self.nEmbd // self.nHead

			keyShape = (batchSize, self.nHead, 0, headDim)
			valueShape = (batchSize, self.nHead, 0, headDim)

			pastKeyValues[f"past_key_values.{layerIdx}.key"] = np.zeros(keyShape, dtype=np.float32)
			pastKeyValues[f"past_key_values.{layerIdx}.value"] = np.zeros(valueShape, dtype=np.float32)

		return pastKeyValues

	def generateWithGreedy(
		self,
		encoderHiddenStates: np.ndarray,
		maxLength: int | None = None,
	) -> str:
		"""Generate text using greedy search.

		Args:
			encoderHiddenStates: Encoder hidden states.
			maxLength: Maximum generation length.

		Returns:
			Generated text string.
		"""
		if maxLength is None:
			maxLength = self.maxLength

		# Initialize input sequence
		inputIds = np.array([[self.bosTokenId]], dtype=np.int64)
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
			if nextTokenId == self.eosTokenId:
				break

			generatedTokens.append(nextTokenId)

			# Update past_key_values from outputs
			if len(decoderOutputs) > 1:
				for layerIdx in range(self.nLayer):
					if len(decoderOutputs) > 1 + layerIdx * 2 + 1:
						pastKeyValues[f"past_key_values.{layerIdx}.key"] = decoderOutputs[1 + layerIdx * 2]
						pastKeyValues[f"past_key_values.{layerIdx}.value"] = decoderOutputs[
							1 + layerIdx * 2 + 1
						]

			# Avoid sequences that are too long
			if len(generatedTokens) >= self.nCtx - 1:
				break

		# Decode generated text
		return self.decodeTokens(generatedTokens)

	def generateCaption(
		self,
		image: str | bytes,
		maxLength: int | None = None,
	) -> str:
		"""Generate image caption.

		Args:
			image: Image file path or binary data.
			maxLength: Maximum generation length.

		Returns:
			Generated image caption.
		"""
		# Preprocess image
		imageArray = self.preprocessImage(image)

		# Encode image
		encoderHiddenStates = self.encodeImage(imageArray)

		# Generate text
		caption = self.generateWithGreedy(encoderHiddenStates, maxLength)

		return caption


def benchmarkInference(
	captioner: ImageCaptioner,
	imagePath: str,
	numRuns: int = 5,
) -> None:
	"""Benchmark inference performance.

	Args:
		captioner: Model instance.
		imagePath: Test image path.
		numRuns: Number of runs for benchmarking.
	"""
	log.info(f"Running benchmark with {numRuns} iterations...")

	# Warm up
	captioner.generateCaption(imagePath)

	# Test greedy search
	startTime = time.time()
	for _ in range(numRuns):
		captioner.generateCaption(imagePath)
	greedyTime = (time.time() - startTime) / numRuns

	log.info("Average inference time:")
	log.info(f"  Greedy search: {greedyTime:.3f}s")
