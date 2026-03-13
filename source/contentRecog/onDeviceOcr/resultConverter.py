# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Convert RapidOCR/PaddleOCR output to NVDA's LinesWordsResult-compatible format.

RapidOCR returns results as a list of (quad, text, confidence) tuples where quad
is a 4-point polygon [[x1,y1],[x2,y2],[x3,y3],[x4,y4]].
NVDA's LinesWordsResult expects lines of words as dicts: {x, y, width, height, text}.
This module handles that conversion plus reading-order line clustering.
"""

from typing import List, Tuple, Optional


# Type alias: RapidOCR single result item
OcrResultItem = Tuple[List[List[float]], str, float]


def quad_to_rect(quad: List[List[float]]) -> dict:
	"""Convert a 4-point quadrilateral to an axis-aligned bounding rectangle.

	@param quad: Four corner coordinates [[x1,y1],[x2,y2],[x3,y3],[x4,y4]].
	@return: Dict with keys x, y, width, height (all int, width/height >= 1).
	"""
	xs = [p[0] for p in quad]
	ys = [p[1] for p in quad]
	x = int(min(xs))
	y = int(min(ys))
	width = max(int(max(xs)) - x, 1)
	height = max(int(max(ys)) - y, 1)
	return {"x": x, "y": y, "width": width, "height": height}


def cluster_into_lines(
	items: List[dict],
	y_overlap_threshold: float = 0.5,
) -> List[List[dict]]:
	"""Group OCR result items into lines based on vertical position.

	Items whose vertical center is within y_overlap_threshold * item_height
	of each other are considered the same line. Within each line, items
	are sorted left-to-right by x coordinate.

	@param items: List of dicts with keys: x, y, width, height, text.
	@param y_overlap_threshold: Fraction of height used for same-line detection.
	@return: List of lines, each line is a list of word dicts sorted by x.
	"""
	if not items:
		return []

	# Sort by vertical center, then horizontal position
	sorted_items = sorted(items, key=lambda it: (it["y"] + it["height"] / 2, it["x"]))

	lines: List[List[dict]] = []
	current_line = [sorted_items[0]]
	current_center_y = sorted_items[0]["y"] + sorted_items[0]["height"] / 2

	for item in sorted_items[1:]:
		item_center_y = item["y"] + item["height"] / 2
		# Use the average height of current line items as reference
		avg_height = sum(it["height"] for it in current_line) / len(current_line)
		if abs(item_center_y - current_center_y) < avg_height * y_overlap_threshold:
			current_line.append(item)
		else:
			# Sort current line left-to-right and start new line
			current_line.sort(key=lambda it: it["x"])
			lines.append(current_line)
			current_line = [item]
			current_center_y = item_center_y

	# Don't forget the last line
	current_line.sort(key=lambda it: it["x"])
	lines.append(current_line)

	return lines


def convert_rapidocr_result(
	raw_result: Optional[List[OcrResultItem]],
	confidence_threshold: float = 0.0,
) -> List[List[dict]]:
	"""Convert RapidOCR output to NVDA LinesWordsResult-compatible data structure.

	@param raw_result: RapidOCR output list of (quad, text, confidence).
		May be None or empty if no text was detected.
	@param confidence_threshold: Minimum confidence to include a result (0.0-1.0).
	@return: List of lines, each line is a list of word dicts:
		[[{"x": int, "y": int, "width": int, "height": int, "text": str}, ...], ...]
	"""
	if not raw_result:
		return []

	items = []
	for quad, text, confidence in raw_result:
		if confidence < confidence_threshold:
			continue
		if not text or not text.strip():
			continue
		rect = quad_to_rect(quad)
		rect["text"] = text
		items.append(rect)

	if not items:
		return []

	return cluster_into_lines(items)
