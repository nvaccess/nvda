# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Fix the broken Reshape node in the ViT encoder ONNX model.

The quantized encoder from nlpconnect/vit-gpt2-image-captioning has a Reshape
that incorrectly requests {1,768,14} instead of {1,768,196} after patch embeddings.
This script corrects that Reshape to flatten both spatial dimensions properly.

Usage:
	python fix_encoder_reshape.py <path_to_encoder.onnx> [output_path]
"""

import sys
import os


def fix_encoder_reshape(input_path: str, output_path: str | None = None) -> None:
	"""
	Fix the Reshape node in the ViT encoder ONNX model.

	:param input_path: Path to the broken encoder ONNX file
	:param output_path: Path to save the fixed model (defaults to input_path with _fixed suffix)
	"""
	try:
		import onnx
		from onnx import helper, numpy_helper
	except ImportError:
		print("Error: 'onnx' package is required. Install with: pip install onnx")
		sys.exit(1)

	if not os.path.exists(input_path):
		print(f"Error: Input file not found: {input_path}")
		sys.exit(1)

	print(f"Loading ONNX model from: {input_path}")
	model = onnx.load(input_path)

	# Find the problematic Reshape node
	reshape_node = None
	reshape_node_idx = None

	for idx, node in enumerate(model.graph.node):
		if node.op_type == "Reshape" and "/embeddings/patch_embeddings/Reshape" in node.name:
			reshape_node = node
			reshape_node_idx = idx
			print(f"Found problematic Reshape node: {node.name}")
			break

	if not reshape_node:
		print("Warning: Could not find the specific Reshape node. Searching for Reshape after Conv...")
		# Try to find any Reshape that follows a Conv in embeddings
		for idx, node in enumerate(model.graph.node):
			if node.op_type == "Reshape" and "embeddings" in node.name.lower():
				reshape_node = node
				reshape_node_idx = idx
				print(f"Found candidate Reshape node: {node.name}")
				break

	if not reshape_node:
		print("Error: Could not find a Reshape node to fix in the embeddings section")
		sys.exit(1)

	# Find the shape input (typically the second input to Reshape)
	shape_input_name = reshape_node.input[1] if len(reshape_node.input) > 1 else None

	if not shape_input_name:
		print("Error: Reshape node does not have a shape input")
		sys.exit(1)

	print(f"Shape input name: {shape_input_name}")

	# Find the initializer that defines this shape
	shape_initializer = None
	shape_init_idx = None

	for idx, init in enumerate(model.graph.initializer):
		if init.name == shape_input_name:
			shape_initializer = init
			shape_init_idx = idx
			break

	import numpy as np

	if not shape_initializer:
		print(f"Shape initializer '{shape_input_name}' not found in model.graph.initializer")
		print("Shape likely comes from a Concat or other operation.")
		print("Creating new constant shape initializer and rewiring Reshape...")

		# Create a new unique name for the shape constant
		new_shape_name = f"{reshape_node.name}_fixed_shape"
		new_shape = np.array([1, 768, 196], dtype=np.int64)
		new_shape_tensor = numpy_helper.from_array(new_shape, name=new_shape_name)
		model.graph.initializer.append(new_shape_tensor)

		# Update the Reshape node to use the new shape constant
		reshape_node.input[1] = new_shape_name
		print(f"Created new shape initializer: {new_shape_name} = [1, 768, 196]")
		print(f"Updated Reshape node to use new shape constant")
	else:
		# Get current shape values
		current_shape = numpy_helper.to_array(shape_initializer)
		print(f"Current shape: {current_shape}")

		# Check if this is the problematic {1, 768, 14} shape
		if len(current_shape) == 3 and current_shape[0] == 1 and current_shape[1] == 768 and current_shape[2] == 14:
			print("Confirmed: This is the problematic Reshape expecting {1,768,14}")
			print("Fixing to {1,768,196} (14x14 patches flattened)")

			# Create new shape tensor: [1, 768, 196]
			new_shape = np.array([1, 768, 196], dtype=np.int64)
			new_shape_tensor = numpy_helper.from_array(new_shape, name=shape_input_name)

			# Replace the initializer
			model.graph.initializer[shape_init_idx].CopyFrom(new_shape_tensor)

			print("Shape updated successfully")
		else:
			print(f"Warning: Shape {current_shape} doesn't match expected problematic pattern")
			print("Please verify this is the correct Reshape to modify")
			response = input("Continue anyway? (y/n): ")
			if response.lower() != 'y':
				print("Aborted")
				sys.exit(0)

			# Try to fix it anyway
			new_shape = np.array([1, 768, 196], dtype=np.int64)
			new_shape_tensor = numpy_helper.from_array(new_shape, name=shape_input_name)
			model.graph.initializer[shape_init_idx].CopyFrom(new_shape_tensor)
			print("Shape updated to {1,768,196}")

	# Determine output path
	if output_path is None:
		base, ext = os.path.splitext(input_path)
		output_path = f"{base}_fixed{ext}"

	# Save the corrected model
	print(f"Saving fixed model to: {output_path}")
	onnx.save(model, output_path)

	# Verify the model
	print("Verifying fixed model...")
	try:
		onnx.checker.check_model(model)
		print("✓ Model validation passed")
	except Exception as e:
		print(f"Warning: Model validation failed: {e}")
		print("The model may still work, but please test it")

	print("\nDone! Replace your encoder file with the fixed version:")
	print(f"  {output_path}")


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(__doc__)
		print("\nExample:")
		print("  python fix_encoder_reshape.py encoder_model_quantized.onnx")
		sys.exit(1)

	input_path = sys.argv[1]
	output_path = sys.argv[2] if len(sys.argv) > 2 else None

	fix_encoder_reshape(input_path, output_path)
