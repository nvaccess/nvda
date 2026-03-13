# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Unit tests for on-device OCR result conversion."""

import unittest
from contentRecog.onDeviceOcr.resultConverter import (
	quad_to_rect,
	cluster_into_lines,
	convert_rapidocr_result,
)


class TestQuadToRect(unittest.TestCase):
	"""Test quadrilateral to axis-aligned rectangle conversion."""

	def test_axis_aligned_rectangle(self):
		quad = [[10, 20], [110, 20], [110, 50], [10, 50]]
		result = quad_to_rect(quad)
		self.assertEqual(result, {"x": 10, "y": 20, "width": 100, "height": 30})

	def test_rotated_quad_uses_bounding_box(self):
		# Slightly rotated text
		quad = [[12, 20], [112, 22], [110, 52], [10, 50]]
		result = quad_to_rect(quad)
		self.assertEqual(result["x"], 10)
		self.assertEqual(result["y"], 20)
		self.assertEqual(result["width"], 102)
		self.assertEqual(result["height"], 32)

	def test_degenerate_point_returns_minimum_size(self):
		quad = [[50, 50], [50, 50], [50, 50], [50, 50]]
		result = quad_to_rect(quad)
		self.assertGreaterEqual(result["width"], 1)
		self.assertGreaterEqual(result["height"], 1)

	def test_float_coordinates_truncated_to_int(self):
		quad = [[10.7, 20.3], [60.9, 20.1], [61.2, 40.8], [10.2, 41.1]]
		result = quad_to_rect(quad)
		self.assertIsInstance(result["x"], int)
		self.assertIsInstance(result["y"], int)


class TestClusterIntoLines(unittest.TestCase):
	"""Test grouping OCR results into reading-order lines."""

	def test_single_line_two_words(self):
		items = [
			{"x": 10, "y": 20, "width": 50, "height": 15, "text": "Hello"},
			{"x": 70, "y": 21, "width": 50, "height": 15, "text": "World"},
		]
		lines = cluster_into_lines(items)
		self.assertEqual(len(lines), 1)
		self.assertEqual(len(lines[0]), 2)
		self.assertEqual(lines[0][0]["text"], "Hello")
		self.assertEqual(lines[0][1]["text"], "World")

	def test_two_separate_lines(self):
		items = [
			{"x": 10, "y": 20, "width": 50, "height": 15, "text": "Line1"},
			{"x": 10, "y": 60, "width": 50, "height": 15, "text": "Line2"},
		]
		lines = cluster_into_lines(items)
		self.assertEqual(len(lines), 2)
		self.assertEqual(lines[0][0]["text"], "Line1")
		self.assertEqual(lines[1][0]["text"], "Line2")

	def test_words_sorted_left_to_right_within_line(self):
		items = [
			{"x": 100, "y": 20, "width": 50, "height": 15, "text": "Second"},
			{"x": 10, "y": 20, "width": 50, "height": 15, "text": "First"},
		]
		lines = cluster_into_lines(items)
		self.assertEqual(lines[0][0]["text"], "First")
		self.assertEqual(lines[0][1]["text"], "Second")

	def test_empty_input(self):
		self.assertEqual(cluster_into_lines([]), [])

	def test_single_item(self):
		items = [{"x": 10, "y": 20, "width": 50, "height": 15, "text": "Alone"}]
		lines = cluster_into_lines(items)
		self.assertEqual(len(lines), 1)
		self.assertEqual(len(lines[0]), 1)


class TestConvertRapidOcrResult(unittest.TestCase):
	"""Test full RapidOCR result to NVDA format conversion."""

	def test_none_result(self):
		self.assertEqual(convert_rapidocr_result(None), [])

	def test_empty_result(self):
		self.assertEqual(convert_rapidocr_result([]), [])

	def test_typical_two_line_result(self):
		raw = [
			([[10, 20], [110, 20], [110, 50], [10, 50]], "Hello World", 0.95),
			([[10, 60], [110, 60], [110, 90], [10, 90]], "Second line", 0.92),
		]
		lines = convert_rapidocr_result(raw)
		self.assertEqual(len(lines), 2)
		self.assertEqual(lines[0][0]["text"], "Hello World")
		self.assertEqual(lines[1][0]["text"], "Second line")

	def test_confidence_threshold_filters_low_scores(self):
		raw = [
			([[10, 20], [60, 20], [60, 40], [10, 40]], "Good", 0.9),
			([[10, 60], [60, 60], [60, 80], [10, 80]], "Bad", 0.1),
		]
		lines = convert_rapidocr_result(raw, confidence_threshold=0.5)
		self.assertEqual(len(lines), 1)
		self.assertEqual(lines[0][0]["text"], "Good")

	def test_empty_text_items_excluded(self):
		raw = [
			([[10, 20], [60, 20], [60, 40], [10, 40]], "", 0.9),
			([[10, 60], [60, 60], [60, 80], [10, 80]], "Real text", 0.9),
		]
		lines = convert_rapidocr_result(raw)
		self.assertEqual(len(lines), 1)
		self.assertEqual(lines[0][0]["text"], "Real text")

	def test_result_contains_required_keys(self):
		raw = [
			([[10, 20], [60, 20], [60, 40], [10, 40]], "Word", 0.99),
		]
		lines = convert_rapidocr_result(raw)
		word = lines[0][0]
		for key in ("x", "y", "width", "height", "text"):
			self.assertIn(key, word)


class TestLinesWordsResultIntegration(unittest.TestCase):
	"""Test that converted results integrate correctly with NVDA's LinesWordsResult."""

	def test_converted_result_creates_valid_lineswordsresult(self):
		from contentRecog import RecogImageInfo, LinesWordsResult

		raw = [
			([[10, 20], [60, 20], [60, 40], [10, 40]], "Word1", 0.99),
			([[70, 20], [120, 20], [120, 40], [70, 40]], "Word2", 0.98),
			([[10, 60], [60, 60], [60, 80], [10, 80]], "Word3", 0.97),
		]
		lines_data = convert_rapidocr_result(raw)
		info = RecogImageInfo(0, 0, 200, 100, 1)
		result = LinesWordsResult(lines_data, info)
		self.assertIn("Word1", result.text)
		self.assertIn("Word2", result.text)
		self.assertIn("Word3", result.text)
		# Should have 2 lines
		self.assertEqual(len(result.lines), 2)
