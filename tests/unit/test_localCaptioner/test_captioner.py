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

from _localCaptioner.captioner import VitGpt2ImageCaptioner
from _localCaptioner import modelConfig
modelConfig.initialize()



class TestVitGpt2ImageCaptioner(unittest.TestCase):
	"""Unit tests for the VitGpt2ImageCaptioner class."""

	def setUp(self):
		"""Set up test environment."""
		# Create temporary directory and test files
		self.test_dir = tempfile.mkdtemp()

		# Create test configuration
		self.config_data = {
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
		self.vocab_data = {
			"<|endoftext|>": 50256,
			"a": 0,
			"the": 1,
			"cat": 2,
			"dog": 3,
			"is": 4,
			"sitting": 5,
		}

		# File paths
		self.configPath = os.path.join(self.test_dir, "config.json")
		self.vocab_path = os.path.join(self.test_dir, "vocab.json")
		self.encoderPath = "mock_encoder.onnx"
		self.decoderPath = "mock_decoder.onnx"

		# Write config and vocab files
		with open(self.configPath, "w", encoding="utf-8") as f:
			json.dump(self.config_data, f)
		with open(self.vocab_path, "w", encoding="utf-8") as f:
			json.dump(self.vocab_data, f)

	def tearDown(self):
		"""Clean up temporary files."""
		import shutil

		shutil.rmtree(self.test_dir)

	@patch("onnxruntime.InferenceSession")
	def test_initSuccess(self, mock_session):
		"""Test successful initialization."""
		mock_encoder = Mock()
		mock_decoder = Mock()
		mock_session.side_effect = [mock_encoder, mock_decoder]

		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)

		self.assertEqual(captioner.decoderConfig.max_length, 20)
		self.assertEqual(captioner.modelConfig.bos_token_id, 50256)
		self.assertEqual(captioner.vocabSize, len(self.vocab_data))
		self.assertEqual(mock_session.call_count, 2)

	def test_initConfigNotFound(self):
		"""Test missing config file raises error."""
		with self.assertRaises(FileNotFoundError) as context:
			VitGpt2ImageCaptioner(
				encoderPath=self.encoderPath,
				decoderPath=self.decoderPath,
				configPath="nonexistent_config.json",
			)
		self.assertIn("config file", str(context.exception))

	@patch("onnxruntime.InferenceSession")
	def test_loadVocabSuccess(self, mock_session):
		"""Test vocabulary loads successfully."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		expected_vocab = {v: k for k, v in self.vocab_data.items()}
		self.assertEqual(captioner.vocab, expected_vocab)

	@patch("onnxruntime.InferenceSession")
	def test_preprocessImageFromPath(self, mock_session):
		"""Test preprocessing image from file path."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		test_image = Image.new("RGB", (100, 100), color="red")
		test_image_path = os.path.join(self.test_dir, "test_image.jpg")
		test_image.save(test_image_path)

		result = captioner._preprocessImage(test_image_path)

		self.assertEqual(result.shape, (1, 3, 224, 224))
		self.assertEqual(result.dtype, np.float32)

	@patch("onnxruntime.InferenceSession")
	def test_preprocessImageFromBytes(self, mock_session):
		"""Test preprocessing image from byte input."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		test_image = Image.new("RGB", (100, 100), color="blue")
		img_bytes = io.BytesIO()
		test_image.save(img_bytes, format="PNG")
		img_bytes = img_bytes.getvalue()

		result = captioner._preprocessImage(img_bytes)

		self.assertEqual(result.shape, (1, 3, 224, 224))
		self.assertEqual(result.dtype, np.float32)

	@patch("onnxruntime.InferenceSession")
	def test_encodeImage(self, mock_session):
		"""Test image encoding using encoder."""
		mock_encoder = Mock()
		mock_decoder = Mock()
		mock_encoder_output = np.random.randn(1, 196, 768).astype(np.float32)
		mock_encoder.run.return_value = [mock_encoder_output]
		mock_encoder.get_inputs.return_value = [Mock(name="pixel_values")]

		mock_session.side_effect = [mock_encoder, mock_decoder]

		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)

		test_input = np.random.randn(1, 3, 224, 224).astype(np.float32)
		result = captioner._encodeImage(test_input)

		np.testing.assert_array_equal(result, mock_encoder_output)
		mock_encoder.run.assert_called_once()

	@patch("onnxruntime.InferenceSession")
	def test_decodeTokens(self, mock_session):
		"""Test decoding tokens to text."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		token_ids = [1, 2, 4, 5]
		result = captioner._decodeTokens(token_ids)
		expected = "the cat is sitting"
		self.assertEqual(result, expected)

	@patch("onnxruntime.InferenceSession")
	def test_decodeTokensWithSpecialTokens(self, mock_session):
		"""Test decoding tokens with special tokens removed."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		token_ids = [50256, 1, 2, 50256]
		result = captioner._decodeTokens(token_ids)
		expected = "the cat"
		self.assertEqual(result, expected)

	@patch("onnxruntime.InferenceSession")
	def test_initializePastKeyValues(self, mock_session):
		"""Test initialization of past key values."""
		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		past_kv = captioner._initializePastKeyValues(batchSize=1)
		expected_count = captioner.decoderConfig.n_layer * 2
		self.assertEqual(len(past_kv), expected_count)

		for layer_idx in range(captioner.decoderConfig.n_layer):
			key_name = f"past_key_values.{layer_idx}.key"
			value_name = f"past_key_values.{layer_idx}.value"
			self.assertIn(key_name, past_kv)
			self.assertIn(value_name, past_kv)
			expected_shape = (
				1,
				captioner.decoderConfig.n_head,
				0,
				captioner.decoderConfig.n_embd // captioner.decoderConfig.n_head,
			)
			self.assertEqual(past_kv[key_name].shape, expected_shape)
			self.assertEqual(past_kv[value_name].shape, expected_shape)

	@patch("onnxruntime.InferenceSession")
	def test_generateWithGreedyMock(self, mock_session):
		"""Test greedy generation with mocked outputs."""
		mock_encoder = Mock()
		mock_decoder = Mock()

		mock_decoder.get_inputs.return_value = [
			Mock(name="input_ids"),
			Mock(name="encoder_hidden_states"),
			Mock(name="use_cache_branch"),
		]

		logits_1 = np.zeros((1, 1, 50257))
		logits_1[0, 0, 2] = 10.0

		logits_2 = np.zeros((1, 1, 50257))
		logits_2[0, 0, 50256] = 10.0

		mock_decoder.run.side_effect = [[logits_1], [logits_2]]
		mock_session.side_effect = [mock_encoder, mock_decoder]

		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)
		encoder_states = np.random.randn(1, 196, 768).astype(np.float32)
		result = captioner._generateWithGreedy(encoder_states, maxLength=5)
		self.assertEqual(result, "cat")

	@patch("onnxruntime.InferenceSession")
	def test_getDecoderInfo(self, mock_session):
		"""Test retrieving decoder input/output names."""
		mock_encoder = Mock()
		mock_decoder = Mock()
		mock_input = Mock()
		mock_input.name = "input_ids"
		mock_output = Mock()
		mock_output.name = "logits"

		mock_decoder.get_inputs.return_value = [mock_input]
		mock_decoder.get_outputs.return_value = [mock_output]
		mock_session.side_effect = [mock_encoder, mock_decoder]

		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)

		input_names = captioner._getDecoderInputNames()
		self.assertEqual(input_names, ["input_ids"])

		output_names = captioner._getDecoderOutputNames()
		self.assertEqual(output_names, ["logits"])

	@patch("onnxruntime.InferenceSession")
	@patch.object(VitGpt2ImageCaptioner, "_preprocessImage")
	@patch.object(VitGpt2ImageCaptioner, "_encodeImage")
	@patch.object(VitGpt2ImageCaptioner, "_generateWithGreedy")
	def test_generateCaptionIntegration(self, mock_greedy, mock_encode, mock_preprocess, mock_session):
		"""Test full caption generation pipeline integration."""
		mock_preprocess.return_value = np.random.randn(1, 3, 224, 224)
		mock_encode.return_value = np.random.randn(1, 196, 768)
		mock_greedy.return_value = "a cat sitting on a table"

		captioner = VitGpt2ImageCaptioner(
			encoderPath=self.encoderPath,
			decoderPath=self.decoderPath,
			configPath=self.configPath,
		)

		result = captioner.generateCaption("test_image.jpg")

		mock_preprocess.assert_called_once_with("test_image.jpg")
		mock_encode.assert_called_once()
		mock_greedy.assert_called_once()
		self.assertEqual(result, "a cat sitting on a table")

	@patch("onnxruntime.InferenceSession")
	def test_configParameterLoading(self, mock_session):
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
