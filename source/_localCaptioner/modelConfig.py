# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from dataclasses import dataclass, fields
from typing import Any


@dataclass(frozen=True)
class _EncoderConfig:
	"""Configuration for Vision Transformer encoder."""

	image_size: int = 224
	num_channels: int = 3
	patch_size: int = 16
	hidden_size: int = 768
	num_hidden_layers: int = 12
	num_attention_heads: int = 12
	intermediate_size: int = 3072
	hidden_act: str = "gelu"
	hidden_dropout_prob: float = 0.0
	attention_probs_dropout_prob: float = 0.0
	initializer_range: float = 0.02
	layer_norm_eps: float = 1e-12
	encoder_stride: int = 16
	qkv_bias: bool = True
	model_type: str = "vit"
	# Additional fields from HuggingFace config
	add_cross_attention: bool = False
	is_decoder: bool = False
	is_encoder_decoder: bool = False
	chunk_size_feed_forward: int = 0
	cross_attention_hidden_size: int | None = None
	finetuning_task: str | None = None
	output_attentions: bool = False
	output_hidden_states: bool = False
	return_dict: bool = True
	pruned_heads: dict[str, Any] = None
	tie_word_embeddings: bool = True
	torch_dtype: str | None = None
	torchscript: bool = False
	use_bfloat16: bool = False


@dataclass(frozen=True)
class _DecoderConfig:
	"""Configuration for GPT-2 decoder."""

	vocab_size: int = 50257
	n_embd: int = 768
	n_layer: int = 12
	n_head: int = 12
	n_ctx: int = 1024
	n_positions: int = 1024
	n_inner: int | None = None
	activation_function: str = "gelu_new"
	resid_pdrop: float = 0.1
	embd_pdrop: float = 0.1
	attn_pdrop: float = 0.1
	layer_norm_epsilon: float = 1e-05
	initializer_range: float = 0.02
	model_type: str = "gpt2"
	# Generation parameters
	max_length: int = 20
	min_length: int = 0
	do_sample: bool = False
	early_stopping: bool = False
	num_beams: int = 1
	num_beam_groups: int = 1
	diversity_penalty: float = 0.0
	temperature: float = 1.0
	top_k: int = 50
	top_p: float = 1.0
	typical_p: float = 1.0
	repetition_penalty: float = 1.0
	length_penalty: float = 1.0
	no_repeat_ngram_size: int = 0
	encoder_no_repeat_ngram_size: int = 0
	num_return_sequences: int = 1
	# Cross attention
	add_cross_attention: bool = True
	is_decoder: bool = True
	is_encoder_decoder: bool = False
	# Token IDs
	bos_token_id: int = 50256
	eos_token_id: int = 50256
	pad_token_id: int = 50256
	decoder_start_token_id: int = 50256
	# Additional configuration
	chunk_size_feed_forward: int = 0
	cross_attention_hidden_size: int | None = None
	bad_words_ids: list[int] | None = None
	begin_suppress_tokens: list[int] | None = None
	forced_bos_token_id: int | None = None
	forced_eos_token_id: int | None = None
	suppress_tokens: list[int] | None = None
	exponential_decay_length_penalty: float | None = None
	remove_invalid_values: bool = False
	return_dict_in_generate: bool = False
	output_attentions: bool = False
	output_hidden_states: bool = False
	output_scores: bool = False
	use_cache: bool = True
	# Labels
	id2label: dict[str, str] = None
	label2id: dict[str, int] = None
	# Scaling and attention
	reorder_and_upcast_attn: bool = False
	scale_attn_by_inverse_layer_idx: bool = False
	scale_attn_weights: bool = True
	# Summary configuration
	summary_activation: str | None = None
	summary_first_dropout: float = 0.1
	summary_proj_to_labels: bool = True
	summary_type: str = "cls_index"
	summary_use_proj: bool = True
	# Task specific parameters
	task_specific_params: dict[str, Any] | None = None
	# Other configurations
	finetuning_task: str | None = None
	prefix: str | None = None
	problem_type: str | None = None
	pruned_heads: dict[str, Any] = None
	sep_token_id: int | None = None
	tf_legacy_loss: bool = False
	tie_encoder_decoder: bool = False
	tie_word_embeddings: bool = True
	tokenizer_class: str | None = None
	torch_dtype: str | None = None
	torchscript: bool = False
	use_bfloat16: bool = False


@dataclass(frozen=True)
class _GenerationConfig:
	"""Configuration for text generation parameters."""

	do_sample: bool = False
	num_beams: int = 1
	temperature: float = 1.0
	top_k: int = 50
	top_p: float = 1.0
	repetition_penalty: float = 1.0
	length_penalty: float = 1.0
	max_length: int = 20
	min_length: int = 0
	early_stopping: bool = False
	diversity_penalty: float = 0.0
	num_beam_groups: int = 1
	no_repeat_ngram_size: int = 0
	num_return_sequences: int = 1


@dataclass(frozen=True)
class _ModelConfig:
	"""Main model configuration."""

	model_type: str = "vision-encoder-decoder"
	is_encoder_decoder: bool = True
	tie_word_embeddings: bool = False
	bos_token_id: int = 50256
	eos_token_id: int = 50256
	pad_token_id: int = 50256
	decoder_start_token_id: int = 50256
	transformers_version: str = "4.33.0.dev0"
	architectures: list[str] = None


@dataclass(frozen=True)
class _PreprocessorConfig:
	"""Configuration for image preprocessing."""

	do_normalize: bool = True
	do_rescale: bool = True
	do_resize: bool = True
	feature_extractor_type: str = "ViTFeatureExtractor"
	image_processor_type: str = "ViTFeatureExtractor"
	image_mean: list[float] = None
	image_std: list[float] = None
	resample: int = 2  # PIL.Image.LANCZOS
	rescale_factor: float = 0.00392156862745098  # 1/255
	size: dict[str, int] = None

	def __post_init__(self):
		"""Initialize default values for mutable fields."""
		if self.image_mean is None:
			object.__setattr__(self, "image_mean", [0.5, 0.5, 0.5])
		if self.image_std is None:
			object.__setattr__(self, "image_std", [0.5, 0.5, 0.5])
		if self.size is None:
			object.__setattr__(self, "size", {"height": 224, "width": 224})


# Default configuration instances
_DEFAULT_ENCODER_CONFIG: _EncoderConfig | None = None
_DEFAULT_DECODER_CONFIG: _DecoderConfig | None = None
_DEFAULT_GENERATION_CONFIG: _GenerationConfig | None = None
_DEFAULT_MODEL_CONFIG: _ModelConfig | None = None
_DEFAULT_PREPROCESSOR_CONFIG: _PreprocessorConfig | None = None


def initialize():
	global \
		_DEFAULT_ENCODER_CONFIG, \
		_DEFAULT_DECODER_CONFIG, \
		_DEFAULT_GENERATION_CONFIG, \
		_DEFAULT_MODEL_CONFIG, \
		_DEFAULT_PREPROCESSOR_CONFIG
	_DEFAULT_ENCODER_CONFIG = _EncoderConfig()
	_DEFAULT_DECODER_CONFIG = _DecoderConfig()
	_DEFAULT_GENERATION_CONFIG = _GenerationConfig()
	_DEFAULT_MODEL_CONFIG = _ModelConfig()
	_DEFAULT_PREPROCESSOR_CONFIG = _PreprocessorConfig()


def _createConfigFromDict(configClass: Any, configdict: dict[str, Any], defaultConfig):
	"""Create a dataclass instance from a dictionary with automatic field mapping.

	:param configClass: The dataclass type to create
	:param configdict: dictionary containing configuration values
	:param defaultConfig: Default configuration instance
	:return: New dataclass instance with values from configdict or defaults
	"""
	# Get all field names from the dataclass
	field_names = {f.name for f in fields(configClass)}

	# Build kwargs dict with values from configdict or defaults
	kwargs = {}
	for field_name in field_names:
		if field_name in configdict:
			kwargs[field_name] = configdict[field_name]
		else:
			kwargs[field_name] = getattr(defaultConfig, field_name)

	return configClass(**kwargs)


