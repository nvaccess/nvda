# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html
"""
Mock Vision-Encoder-Decoder Model Generator

This module provides a class to generate mock ONNX models and configuration files
for a Vision-Encoder-Decoder model (ViT-GPT2 style) used for image captioning.
The generated files can be used for testing and development purposes.
"""

import os
import json
from pathlib import Path
from typing import Any

import numpy as np
import onnx
from onnx import helper, TensorProto, numpy_helper


class MockVisionEncoderDecoderGenerator:
	"""
	A class to generate mock ONNX models and configuration files for a
	Vision-Encoder-Decoder model architecture.

	This generator creates:
	- onnx/encoder_model_quantized.onnx: Vision Transformer encoder
	- onnx/decoder_model_merged_quantized.onnx: GPT-2 style decoder
	- config.json: Model configuration
	- vocab.json: Vocabulary mapping
	"""

	def __init__(self, randomSeed: int = 8):
		"""
		Initialize the mock model generator.

		:param randomSeed (int): Random seed for reproducible weight generation.Defaults to 8.
		"""
		self.randomSeed = randomSeed
		self._setRandomSeed()

		# Model hyperparameters
		self.vocab_size = 100
		self.hidden_size = 64
		self.n_layers = 12
		self.image_size = 224
		self.patch_size = 16
		self.num_channels = 3

		# Derived parameters
		self.num_patches = (self.image_size // self.patch_size) ** 2

	def _setRandomSeed(self) -> None:
		"""Set random seed for reproducible results."""
		np.random.seed(self.randomSeed)

	def generateAllFiles(self, outputDir: str) -> None:
		"""
		Generate all mock model files in the specified directory.

		:param outputDir (str): Target directory to create the model files. Will create the directory if it doesn't exist.
		"""
		outputPath = Path(outputDir)
		outputPath.mkdir(parents=True, exist_ok=True)

		# Create onnx subdirectory
		onnxDir = outputPath / "onnx"
		onnxDir.mkdir(exist_ok=True)

		# Generate all components
		self._generateEncoderModel(os.path.join(onnxDir, "encoder_model_quantized.onnx"))
		self._generateDecoderModel(os.path.join(onnxDir, "decoder_model_merged_quantized.onnx"))
		self._generateConfigFile(os.path.join(outputPath, "config.json"))
		self._generateVocabFile(os.path.join(outputPath, "vocab.json"))

	def _generateEncoderModel(self, outputPath: Path) -> None:
		"""
		Generate the Vision Transformer encoder ONNX model.

		This creates a simplified ViT encoder that performs patch embedding
		using convolution followed by reshaping operations.

		:param outputPath (Path): Output path for the encoder ONNX file.
		"""
		# Define input and output specifications
		pixelValues = helper.make_tensor_value_info(
			"pixelValues",
			TensorProto.FLOAT,
			["batch", self.num_channels, self.image_size, self.image_size],
		)

		patchEmbeds = helper.make_tensor_value_info(
			"patchEmbeds",
			TensorProto.FLOAT,
			["batch", self.num_patches, self.hidden_size],
		)

		# Generate random but reproducible weights for patch embedding
		convWeights = np.random.randn(
			self.hidden_size,
			self.num_channels,
			self.patch_size,
			self.patch_size,
		).astype(np.float32)

		convBias = np.zeros(self.hidden_size, dtype=np.float32)

		# Create initializers
		weightInit = numpy_helper.from_array(convWeights, "convWeights")
		biasInit = numpy_helper.from_array(convBias, "convBias")

		# Shape constant for reshaping
		targetShape = np.array([0, self.num_patches, self.hidden_size], dtype=np.int64)
		shapeInit = numpy_helper.from_array(targetShape, "targetShape")

		# Define computation nodes
		nodes = [
			# Patch embedding using convolution
			helper.make_node(
				"Conv",
				inputs=["pixelValues", "convWeights", "convBias"],
				outputs=["conv_output"],
				kernel_shape=[self.patch_size, self.patch_size],
				strides=[self.patch_size, self.patch_size],
			),
			# Transpose to get correct dimension order
			# From [batch, hidden_size, patch_h, patch_w] to [batch, patch_h, patch_w, hidden_size]
			helper.make_node(
				"Transpose",
				inputs=["conv_output"],
				outputs=["transposed_output"],
				perm=[0, 2, 3, 1],
			),
			# Reshape to flatten patches
			# From [batch, patch_h, patch_w, hidden_size] to [batch, num_patches, hidden_size]
			helper.make_node(
				"Reshape",
				inputs=["transposed_output", "targetShape"],
				outputs=["patchEmbeds"],
			),
		]

		# Create and save the model
		graph = helper.make_graph(
			nodes=nodes,
			name="VisionTransformerEncoder",
			inputs=[pixelValues],
			outputs=[patchEmbeds],
			initializer=[weightInit, biasInit, shapeInit],
		)

		model = helper.make_model(graph, producer_name="mock-vit-encoder")
		model.opset_import[0].version = 13
		model.ir_version = 10

		onnx.save(model, str(outputPath))

	def _generateDecoderModel(self, outputPath: Path) -> None:
		"""
		Generate the GPT-2 style decoder ONNX model.

		This creates a simplified decoder that accepts multiple inputs including
		token IDs, encoder hidden states, cache flags, and past key-value pairs.

		:param outputPath (Path): Output path for the decoder ONNX file.
		"""
		# Generate fixed random weights for reproducibility
		embeddingWeights = np.random.randn(
			self.vocab_size,
			self.hidden_size,
		).astype(np.float32)

		projectionWeights = np.random.randn(
			self.hidden_size,
			self.vocab_size,
		).astype(np.float32)

		# Create weight initializers
		embInit = numpy_helper.from_array(embeddingWeights, "embeddingWeights")
		projInit = numpy_helper.from_array(projectionWeights, "projectionWeights")

		# Define all input specifications
		inputs = self._createDecoderInputs()

		# Define output specification
		outputs = [
			helper.make_tensor_value_info(
				"logits",
				TensorProto.FLOAT,
				["batch", "seq", self.vocab_size],
			),
		]

		# Create computation nodes
		nodes = self._createDecoderNodes()

		# Create shape and scaling constants
		shapeConstants = self._createDecoderConstants()

		# Combine all initializers
		initializers = [embInit, projInit] + shapeConstants

		# Create and save the model
		graph = helper.make_graph(
			nodes=nodes,
			name="GPT2DecoderWithCache",
			inputs=inputs,
			outputs=outputs,
			initializer=initializers,
		)

		model = helper.make_model(graph, producer_name="mock-gpt2-decoder")
		model.opset_import[0].version = 13
		model.ir_version = 10

		onnx.save(model, str(outputPath))

	def _createDecoderInputs(self) -> list:
		"""
		Create input specifications for the decoder model.

		:return: list: List of tensor value info objects for all decoder inputs.
		"""
		inputs = []

		# Primary inputs
		inputs.extend(
			[
				helper.make_tensor_value_info(
					"input_ids",
					TensorProto.INT64,
					["batch", "seq"],
				),
				helper.make_tensor_value_info(
					"encoder_hidden_states",
					TensorProto.FLOAT,
					["batch", "enc_seq_len", self.hidden_size],
				),
				helper.make_tensor_value_info(
					"use_cache_branch",
					TensorProto.BOOL,
					["batch"],
				),
			],
		)

		# Past key-value cache inputs for each layer
		for layerIdx in range(self.n_layers):
			inputs.extend(
				[
					helper.make_tensor_value_info(
						f"past_key_values.{layerIdx}.key",
						TensorProto.FLOAT,
						["batch", "num_heads", "past_seq_len", self.hidden_size],
					),
					helper.make_tensor_value_info(
						f"past_key_values.{layerIdx}.value",
						TensorProto.FLOAT,
						["batch", "num_heads", "past_seq_len", self.hidden_size],
					),
				],
			)

		return inputs

	def _createDecoderNodes(self) -> list:
		"""
		Create computation nodes for the decoder model.

		:return: list: List of ONNX nodes defining the decoder computation.
		"""
		nodes = []

		# Token embedding lookup
		nodes.append(
			helper.make_node(
				"Gather",
				inputs=["embeddingWeights", "input_ids"],
				outputs=["token_embeddings"],
				axis=0,
			),
		)

		# Process encoder hidden states
		nodes.extend(self._createEncoderProcessingNodes())

		# Process cache branch flag
		nodes.extend(self._createCacheProcessingNodes())

		# Process past key-value pairs
		cacheFeatures = self._createCacheFeatureNodes(nodes)

		# Combine all auxiliary features
		nodes.extend(self._createFeatureCombinationNodes(cacheFeatures))

		# Apply main computation pipeline
		nodes.extend(self._createMainComputationNodes())

		return nodes

	def _createEncoderProcessingNodes(self) -> list:
		"""Create nodes to process encoder hidden states."""
		return [
			# Global average pooling over encoder states
			helper.make_node(
				"ReduceMean",
				inputs=["encoder_hidden_states"],
				outputs=["encoder_pooled"],
				axes=[1, 2],  # Pool over sequence length and hidden dimensions
			),
			# Reshape for broadcasting
			helper.make_node(
				"Reshape",
				inputs=["encoder_pooled", "shapeBatch1"],
				outputs=["encoder_feature"],
			),
		]

	def _createCacheProcessingNodes(self) -> list:
		"""Create nodes to process the cache branch flag."""
		return [
			# Convert boolean to float
			helper.make_node(
				"Cast",
				inputs=["use_cache_branch"],
				outputs=["cache_flag_float"],
				to=TensorProto.FLOAT,
			),
			# Reshape for broadcasting
			helper.make_node(
				"Reshape",
				inputs=["cache_flag_float", "shapeBatch1"],
				outputs=["cache_flag_feature"],
			),
		]

	def _createCacheFeatureNodes(self, nodes: list) -> list:
		"""
		Create nodes to process past key-value cache inputs.

		:param nodes (list): List to append new nodes to.
		:return: list: Names of cache feature tensors.
		"""
		cacheFeatures = []

		for layerIdx in range(self.n_layers):
			# Process key cache
			nodes.extend(
				[
					helper.make_node(
						"ReduceMean",
						inputs=[f"past_key_values.{layerIdx}.key"],
						outputs=[f"cache_key_{layerIdx}_pooled"],
						axes=[1, 2, 3],  # Global pooling, keep only batch dimension
					),
					helper.make_node(
						"Reshape",
						inputs=[f"cache_key_{layerIdx}_pooled", "shapeBatch1"],
						outputs=[f"cache_key_{layerIdx}_feature"],
					),
				],
			)

			# Process value cache
			nodes.extend(
				[
					helper.make_node(
						"ReduceMean",
						inputs=[f"past_key_values.{layerIdx}.value"],
						outputs=[f"cache_value_{layerIdx}_pooled"],
						axes=[1, 2, 3],
					),
					helper.make_node(
						"Reshape",
						inputs=[f"cache_value_{layerIdx}_pooled", "shapeBatch1"],
						outputs=[f"cache_value_{layerIdx}_feature"],
					),
				],
			)

			cacheFeatures.extend(
				[
					f"cache_key_{layerIdx}_feature",
					f"cache_value_{layerIdx}_feature",
				],
			)

		return cacheFeatures

	def _createFeatureCombinationNodes(self, cacheFeatures: list) -> list:
		"""
		Create nodes to combine all auxiliary features.

		:param cacheFeatures (list): List of cache feature tensor names.
		:return: list: Nodes for feature combination.
		"""
		nodes = []
		allFeatures = ["encoder_feature", "cache_flag_feature"] + cacheFeatures

		# Sequentially add all features together
		currentSum = allFeatures[0]
		for i, feature in enumerate(allFeatures[1:], 1):
			nodes.append(
				helper.make_node(
					"Add",
					inputs=[currentSum, feature],
					outputs=[f"combined_features_{i}"],
				),
			)
			currentSum = f"combined_features_{i}"

		return nodes

	def _createMainComputationNodes(self) -> list:
		"""Create the main computation pipeline nodes."""
		finalCombined = f"combined_features_{self.n_layers * 2 + 1}"

		return [
			# Flatten token embeddings
			helper.make_node(
				"Reshape",
				inputs=["token_embeddings", "shape2d"],
				outputs=["embeddings_flat"],
			),
			# Scale embeddings
			helper.make_node(
				"Mul",
				inputs=["embeddings_flat", "featureScale"],
				outputs=["scaled_embeddings"],
			),
			# Add auxiliary features (broadcasting)
			helper.make_node(
				"Add",
				inputs=["scaled_embeddings", finalCombined],
				outputs=["final_features"],
			),
			# Project to vocabulary space
			helper.make_node(
				"MatMul",
				inputs=["final_features", "projectionWeights"],
				outputs=["logits_flat"],
			),
			# Reshape back to 3D
			helper.make_node(
				"Reshape",
				inputs=["logits_flat", "shape3d"],
				outputs=["logits"],
			),
		]

	def _createDecoderConstants(self) -> list:
		"""
		Create constant tensors needed for decoder computation.

		:returns: list: List of constant tensor initializers.
		"""
		constants = []

		# Shape constants for reshaping operations
		shape2d = numpy_helper.from_array(
			np.array([-1, self.hidden_size], dtype=np.int64),
			name="shape2d",
		)

		shape3d = numpy_helper.from_array(
			np.array([0, -1, self.vocab_size], dtype=np.int64),
			name="shape3d",
		)

		shapeBatch1 = numpy_helper.from_array(
			np.array([-1, 1], dtype=np.int64),
			name="shapeBatch1",
		)

		# Feature scaling factor
		featureScale = numpy_helper.from_array(
			np.array([[1.1]], dtype=np.float32),
			name="featureScale",
		)

		constants.extend([shape2d, shape3d, shapeBatch1, featureScale])

		return constants

	def _generateConfigFile(self, outputPath: Path) -> None:
		"""
		Generate the model configuration JSON file.

		:param outputPath (Path): Output path for the config.json file.
		"""
		config = self._getModelConfig()

		with open(outputPath, "w", encoding="utf-8") as f:
			json.dump(config, f, indent=2, ensure_ascii=False)

	def _getModelConfig(self) -> dict[str, Any]:
		"""
		Get the complete model configuration dictionary.

		:return: dict[str, Any]: Complete model configuration.
		"""
		return {
			"_name_or_path": "nlpconnect/vit-gpt2-image-captioning",
			"architectures": ["VisionEncoderDecoderModel"],
			"bos_token_id": 99,
			"decoder": self._getDecoderConfig(),
			"decoder_start_token_id": 99,
			"encoder": self._getEncoderConfig(),
			"eos_token_id": 99,
			"is_encoder_decoder": True,
			"model_type": "vision-encoder-decoder",
			"pad_token_id": 99,
			"tie_word_embeddings": False,
			"transformers_version": "4.33.0.dev0",
		}

	def _getDecoderConfig(self) -> dict[str, Any]:
		"""Get decoder-specific configuration."""
		return {
			"_name_or_path": "",
			"activation_function": "gelu_new",
			"add_cross_attention": True,
			"architectures": ["GPT2LMHeadModel"],
			"attn_pdrop": 0.1,
			"bad_words_ids": None,
			"begin_suppress_tokens": None,
			"bos_token_id": 99,
			"chunk_size_feed_forward": 0,
			"cross_attention_hidden_size": None,
			"decoder_start_token_id": 99,
			"diversity_penalty": 0.0,
			"do_sample": False,
			"early_stopping": False,
			"embd_pdrop": 0.1,
			"encoder_no_repeat_ngram_size": 0,
			"eos_token_id": 99,
			"exponential_decay_length_penalty": None,
			"finetuning_task": None,
			"forced_bos_token_id": None,
			"forced_eos_token_id": None,
			"id2label": {"0": "LABEL_0", "1": "LABEL_1"},
			"initializer_range": 0.02,
			"is_decoder": True,
			"is_encoder_decoder": False,
			"label2id": {"LABEL_0": 0, "LABEL_1": 1},
			"layer_norm_epsilon": 1e-05,
			"length_penalty": 1.0,
			"max_length": 20,
			"min_length": 0,
			"model_type": "gpt2",
			"n_ctx": 1024,
			"n_embd": 768,
			"n_head": 12,
			"n_inner": None,
			"n_layer": 12,
			"n_positions": 1024,
			"no_repeat_ngram_size": 0,
			"num_beam_groups": 1,
			"num_beams": 1,
			"num_return_sequences": 1,
			"output_attentions": False,
			"output_hidden_states": False,
			"output_scores": False,
			"pad_token_id": 99,
			"prefix": None,
			"problem_type": None,
			"pruned_heads": {},
			"remove_invalid_values": False,
			"reorder_and_upcast_attn": False,
			"repetition_penalty": 1.0,
			"resid_pdrop": 0.1,
			"return_dict": True,
			"return_dict_in_generate": False,
			"scale_attn_by_inverse_layer_idx": False,
			"scale_attn_weights": True,
			"sep_token_id": None,
			"summary_activation": None,
			"summary_first_dropout": 0.1,
			"summary_proj_to_labels": True,
			"summary_type": "cls_index",
			"summary_use_proj": True,
			"suppress_tokens": None,
			"task_specific_params": {
				"text-generation": {
					"do_sample": True,
					"max_length": 50,
				},
			},
			"temperature": 1.0,
			"tf_legacy_loss": False,
			"tie_encoder_decoder": False,
			"tie_word_embeddings": True,
			"tokenizer_class": None,
			"top_k": 50,
			"top_p": 1.0,
			"torch_dtype": None,
			"torchscript": False,
			"typical_p": 1.0,
			"use_bfloat16": False,
			"use_cache": True,
			"vocab_size": self.vocab_size,
		}

	def _getEncoderConfig(self) -> dict[str, Any]:
		"""Get encoder-specific configuration."""
		return {
			"_name_or_path": "",
			"add_cross_attention": False,
			"architectures": ["ViTModel"],
			"attention_probs_dropout_prob": 0.0,
			"bad_words_ids": None,
			"begin_suppress_tokens": None,
			"bos_token_id": None,
			"chunk_size_feed_forward": 0,
			"cross_attention_hidden_size": None,
			"decoder_start_token_id": None,
			"diversity_penalty": 0.0,
			"do_sample": False,
			"early_stopping": False,
			"encoder_no_repeat_ngram_size": 0,
			"encoder_stride": 16,
			"eos_token_id": None,
			"exponential_decay_length_penalty": None,
			"finetuning_task": None,
			"forced_bos_token_id": None,
			"forced_eos_token_id": None,
			"hidden_act": "gelu",
			"hidden_dropout_prob": 0.0,
			"hidden_size": 768,
			"id2label": {"0": "LABEL_0", "1": "LABEL_1"},
			"image_size": self.image_size,
			"initializer_range": 0.02,
			"intermediate_size": 3072,
			"is_decoder": False,
			"is_encoder_decoder": False,
			"label2id": {"LABEL_0": 0, "LABEL_1": 1},
			"layer_norm_eps": 1e-12,
			"length_penalty": 1.0,
			"max_length": 20,
			"min_length": 0,
			"model_type": "vit",
			"no_repeat_ngram_size": 0,
			"num_attention_heads": 12,
			"num_beam_groups": 1,
			"num_beams": 1,
			"num_channels": self.num_channels,
			"num_hidden_layers": 12,
			"num_return_sequences": 1,
			"output_attentions": False,
			"output_hidden_states": False,
			"output_scores": False,
			"pad_token_id": None,
			"patch_size": self.patch_size,
			"prefix": None,
			"problem_type": None,
			"pruned_heads": {},
			"qkv_bias": True,
			"remove_invalid_values": False,
			"repetition_penalty": 1.0,
			"return_dict": True,
			"return_dict_in_generate": False,
			"sep_token_id": None,
			"suppress_tokens": None,
			"task_specific_params": None,
			"temperature": 1.0,
			"tf_legacy_loss": False,
			"tie_encoder_decoder": False,
			"tie_word_embeddings": True,
			"tokenizer_class": None,
			"top_k": 50,
			"top_p": 1.0,
			"torch_dtype": None,
			"torchscript": False,
			"typical_p": 1.0,
			"use_bfloat16": False,
		}

	def _generateVocabFile(self, outputPath: Path) -> None:
		"""
		Generate the vocabulary JSON file.

		:param outputPath: Output path for the vocab.json file.
		"""
		vocab = self._getVocabulary()

		with open(outputPath, "w", encoding="utf-8") as f:
			json.dump(vocab, f, indent=2, ensure_ascii=False)

	def _getVocabulary(self) -> dict[str, int]:
		"""
		Get the vocabulary mapping dictionary.

		:returns: dict[str, int]: Token to ID mapping.
		"""
		return {
			"<|endoftext|>": 50256,
			"<|pad|>": 50257,
			"a": 0,
			"an": 1,
			"the": 2,
			"free": 3,
			"or": 4,
			"but": 5,
			"in": 6,
			"on": 7,
			"at": 8,
			"to": 9,
			"and": 10,
			"of": 11,
			"with": 12,
			"by": 13,
			"man": 14,
			"for": 15,
			"desk": 16,
			"people": 17,
			"visual": 18,
			"children": 19,
			"software": 20,
			"girl": 21,
			"dog": 22,
			"desktop": 23,
			"car": 24,
			"truck": 25,
			"bus": 26,
			"bike": 27,
			"non-visual": 28,
			"NVDA": 29,
			"plane": 30,
			"boat": 31,
			"house": 32,
			"access": 33,
			"flower": 35,
			"microsoft": 36,
			"sky": 37,
			"cloud": 38,
			"sun": 39,
			"moon": 40,
			"water": 41,
			"river": 42,
			"ocean": 43,
			"red": 44,
			"blue": 45,
			"reader": 46,
			"yellow": 47,
			"black": 48,
			"white": 49,
			"brown": 50,
			"orange": 51,
			"purple": 52,
			"pink": 53,
			"!": 54,
			"small": 55,
			"tall": 56,
			"short": 57,
			"old": 58,
			"young": 59,
			"beautiful": 61,
			"ugly": 62,
			"good": 63,
			"bad": 64,
			"sitting": 65,
			"standing": 66,
			"walking": 67,
			"running": 68,
			"screen": 69,
			"drinking": 70,
			"playing": 71,
			"working": 72,
			"is": 73,
			"open": 74,
			"was": 75,
			"were": 76,
			"has": 77,
			"Best": 78,
			"helping": 79,
			"will": 80,
			"would": 81,
			"could": 82,
			"should": 83,
			"very": 84,
			"quite": 85,
			"really": 86,
			"too": 87,
			"also": 88,
			"source": 89,
			"only": 90,
			"even": 91,
			"still": 92,
			"already": 93,
			"windows": 96,
		}
