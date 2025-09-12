# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
"""
Unit tests for the VitGpt2ImageCaptioner class.

This test suite includes comprehensive tests for the VitGpt2ImageCaptioner class, including:
- Initialization
- Configuration loading
- Vocabulary loading
- Image preprocessing
- Encoder and decoder execution
- Text generation
- Exception handling
"""

import unittest
import json
import os
import tempfile
import numpy as np
from unittest.mock import Mock, patch
from PIL import Image
import io
import shutil

from _localCaptioner.captioner import VitGpt2ImageCaptioner
from _localCaptioner import modelConfig

modelConfig.initialize()


class TestVitGpt2ImageCaptioner(unittest.TestCase):
	"""Unit tests for the VitGpt2ImageCaptioner class."""

	def setUp(self):
		"""Set up test environment."""
		# Create temporary directory and test files
		self.testDir = tempfile.mkdtemp()

		# Create test configuration
		self.configData = {
			"encoder": {
				"image_size": 224,
				"num_channels": 3,
				"patch_size": 16,
				"hidden_size": 768,
				"num_hidden_layers": 12,
				"num_attention_heads": 12,
				"intermediate_size": 3072,
			},
			"decoder": {
				"max_length": 20,
				"vocab_size": 50257,
				"n_embd": 768,
				"n_layer": 12,
				"n_head": 12,
				"n_ctx": 1024,
				"n_positions": 1024,
			},
			"bos_token_id": 50256,
			"eos_token_id": 50256,
			"pad_token_id": 50256,
			"generation": {
				"do_sample": False,
				"num_beams": 1,
				"temperature": 1.0,
				"top_k": 50,
				"top_p": 1.0,
				"repetition_penalty": 1.0,
				"length_penalty": 1.0,
			},
		}

		# Create test vocabulary
		self.vocabData = {
			"<|endoftext|>": 50256,
			"a": 0,
			"the": 1,
			"cat": 2,
			"dog": 3,
			"is": 4,
			"sitting": 5,
		}

		# File paths
		self.configPath = os.path.join(self.testDir, "config.json")
		self.vocabPath = os.path.join(self.testDir, "vocab.json")
		self.encoderPath = "mockEncoder.onnx"
		self.decoderPath = "mockDecoder.onnx"

		# Write config and vocab files
		with open(self.configPath, "w", encoding="utf-8") as f:
			json.dump(self.configData, f)
		with open(self.vocabPath, "w", encoding="utf-8") as f:
			json.dump(self.vocabData, f)

	def tearDown(self):
		"""Clean up temporary files."""
		shutil.rmtree(self.testDir)

	@patch("onnxruntime.InferenceSession")
	def test_initSuccess(self, mockSession):
		"""Test successful initialization."""
		mockEncoder = Mock()
		mockDecoder = Mock()
		mockSession.side_effect = [mockEncoder, mockDecoder]

		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)

		self.assertEqual(captioner.decoderConfig.max_length, 20)
		self.assertEqual(captioner.modelConfig.bos_token_id, 50256)
		self.assertEqual(captioner.vocabSize, len(self.vocabData))
		self.assertEqual(mockSession.call_count, 2)

	def test_initConfigNotFound(self):
		"""Test missing config file raises error."""
		with self.assertRaises(FileNotFoundError) as context:
			VitGpt2ImageCaptioner(
				encoderPath=self.encoderPath,
				decoderPath=self.decoderPath,
				configPath="nonexistentConfig.json",
			)
		self.assertIn("config file", str(context.exception))

	@patch("onnxruntime.InferenceSession")
	def test_loadVocabSuccess(self, mockSession):
		"""Test vocabulary loads successfully."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		expectedVocab = {v: k for k, v in self.vocabData.items()}
		self.assertEqual(captioner.vocab, expectedVocab)

	@patch("onnxruntime.InferenceSession")
	def test_preprocessImageFromPath(self, mockSession):
		"""Test preprocessing image from file path."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		testImage = Image.new("RGB", (100, 100), color="red")
		testImagePath = os.path.join(self.testDir, "testImage.jpg")
		testImage.save(testImagePath)

		result = captioner._preprocessImage(testImagePath)

		self.assertEqual(result.shape, (1, 3, 224, 224))
		self.assertEqual(result.dtype, np.float32)

	@patch("onnxruntime.InferenceSession")
	def test_preprocessImageFromBytes(self, mockSession):
		"""Test preprocessing image from byte input."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		testImage = Image.new("RGB", (100, 100), color="blue")
		imgBytes = io.BytesIO()
		testImage.save(imgBytes, format="PNG")
		imgBytes = imgBytes.getvalue()

		result = captioner._preprocessImage(imgBytes)

		self.assertEqual(result.shape, (1, 3, 224, 224))
		self.assertEqual(result.dtype, np.float32)

	@patch("onnxruntime.InferenceSession")
	def test_encodeImage(self, mockSession):
		"""Test image encoding using encoder."""
		mockEncoder = Mock()
		mockDecoder = Mock()
		mockEncoderOutput = np.random.randn(1, 196, 768).astype(np.float32)
		mockEncoder.run.return_value = [mockEncoderOutput]
		mockEncoder.get_inputs.return_value = [Mock(name="pixel_values")]

		mockSession.side_effect = [mockEncoder, mockDecoder]

		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)

		testInput = np.random.randn(1, 3, 224, 224).astype(np.float32)
		result = captioner._encodeImage(testInput)

		np.testing.assert_array_equal(result, mockEncoderOutput)
		mockEncoder.run.assert_called_once()

	@patch("onnxruntime.InferenceSession")
	def test_decodeTokens(self, mockSession):
		"""Test decoding tokens to text."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		tokenIds = [1, 2, 4, 5]
		result = captioner._decodeTokens(tokenIds)
		expected = "the cat is sitting"
		self.assertEqual(result, expected)

	@patch("onnxruntime.InferenceSession")
	def test_decodeTokensWithSpecialTokens(self, mockSession):
		"""Test decoding tokens with special tokens removed."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		tokenIds = [50256, 1, 2, 50256]
		result = captioner._decodeTokens(tokenIds)
		expected = "the cat"
		self.assertEqual(result, expected)

	@patch("onnxruntime.InferenceSession")
	def test_initializePastKeyValues(self, mockSession):
		"""Test initialization of past key values."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		pastKv = captioner._initializePastKeyValues(batchSize=1)
		expectedCount = captioner.decoderConfig.n_layer * 2
		self.assertEqual(len(pastKv), expectedCount)

		for layerIdx in range(captioner.decoderConfig.n_layer):
			keyName = f"past_key_values.{layerIdx}.key"
			valueName = f"past_key_values.{layerIdx}.value"
			self.assertIn(keyName, pastKv)
			self.assertIn(valueName, pastKv)
			expectedShape = (
				1,
				captioner.decoderConfig.n_head,
				0,
				captioner.decoderConfig.n_embd // captioner.decoderConfig.n_head,
			)
			self.assertEqual(pastKv[keyName].shape, expectedShape)
			self.assertEqual(pastKv[valueName].shape, expectedShape)

	@patch("onnxruntime.InferenceSession")
	def test_generateWithGreedyMock(self, mockSession):
		"""Test greedy generation with mocked outputs."""
		mockEncoder = Mock()
		mockDecoder = Mock()

		mockDecoder.get_inputs.return_value = [
			Mock(name="input_ids"),
			Mock(name="encoder_hidden_states"),
			Mock(name="use_cache_branch"),
		]

		logits_1 = np.zeros((1, 1, 50257))
		logits_1[0, 0, 2] = 10.0

		logits_2 = np.zeros((1, 1, 50257))
		logits_2[0, 0, 50256] = 10.0

		mockDecoder.run.side_effect = [[logits_1], [logits_2]]
		mockSession.side_effect = [mockEncoder, mockDecoder]

		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		encoderStates = np.random.randn(1, 196, 768).astype(np.float32)
		result = captioner._generateWithGreedy(encoderStates, maxLength=5)
		self.assertEqual(result, "cat")

	@patch("onnxruntime.InferenceSession")
	def test_getDecoderInfo(self, mockSession):
		"""Test retrieving decoder input/output names."""
		mockEncoder = Mock()
		mockDecoder = Mock()
		mockInput = Mock()
		mockInput.name = "input_ids"
		mockOutput = Mock()
		mockOutput.name = "logits"

		mockDecoder.get_inputs.return_value = [mockInput]
		mockDecoder.get_outputs.return_value = [mockOutput]
		mockSession.side_effect = [mockEncoder, mockDecoder]

		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)

		inputNames = captioner._getDecoderInputNames()
		self.assertEqual(inputNames, ["input_ids"])

		outputNames = captioner._getDecoderOutputNames()
		self.assertEqual(outputNames, ["logits"])

	@patch("onnxruntime.InferenceSession")
	@patch.object(VitGpt2ImageCaptioner, "_preprocessImage")
	@patch.object(VitGpt2ImageCaptioner, "_encodeImage")
	@patch.object(VitGpt2ImageCaptioner, "_generateWithGreedy")
	def test_generateCaptionIntegration(self, mockGreedy, mockEncode, mockPreprocess, mockSession):
		"""Test full caption generation pipeline integration."""
		mockPreprocess.return_value = np.random.randn(1, 3, 224, 224)
		mockEncode.return_value = np.random.randn(1, 196, 768)
		mockGreedy.return_value = "a cat sitting on a table"

		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)

		result = captioner.generateCaption("testImage.jpg")

		mockPreprocess.assert_called_once_with("testImage.jpg")
		mockEncode.assert_called_once()
		mockGreedy.assert_called_once()
		self.assertEqual(result, "a cat sitting on a table")

	@patch("onnxruntime.InferenceSession")
	def test_configParameterLoading(self, mockSession):
		"""Test full config parameter parsing."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		self.assertEqual(captioner.encoderConfig.num_channels, 3)
		self.assertEqual(captioner.decoderConfig.max_length, 20)
		self.assertEqual(captioner.decoderConfig.n_embd, 768)
		self.assertEqual(captioner.decoderConfig.n_layer, 12)
		self.assertEqual(captioner.modelConfig.bos_token_id, 50256)
		self.assertEqual(captioner.modelConfig.eos_token_id, 50256)
		self.assertEqual(captioner.modelConfig.pad_token_id, 50256)
