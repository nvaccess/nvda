# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
This module provides functions for drawing basic shapes on a TactileGraphicsBuffer.
Implements common shapes like lines and rectangles with bounds checking and optional filling.
"""

from typing import Tuple
from . import TactileGraphicsBuffer


def _isPointInBounds(tgBuf: TactileGraphicsBuffer, x: int, y: int) -> bool:
    """
    Check if a point lies within the buffer boundaries.
    :param tgBuf: The buffer to check against
    :param x: X coordinate to check
    :param y: Y coordinate to check
    :return: True if the point is within bounds, False otherwise
    """
    return 0 <= x < tgBuf.width and 0 <= y < tgBuf.height


def _setDotIfInBounds(tgBuf: TactileGraphicsBuffer, x: int, y: int) -> None:
    """
    Set a dot at the given coordinates if they are within the buffer boundaries.
    :param tgBuf: The buffer to draw on
    :param x: X coordinate
    :param y: Y coordinate
    """
    if _isPointInBounds(tgBuf, x, y):
        tgBuf.setDot(x, y)


def _getLineDirections(x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int, int, int]:
    """
    Calculate direction and delta values for line drawing.
    :param x1: Starting x coordinate
    :param y1: Starting y coordinate
    :param x2: Ending x coordinate
    :param y2: Ending y coordinate
    :return: Tuple of (dx, dy, xDirection, yDirection)
    """
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    xDirection = 1 if x1 < x2 else -1
    yDirection = 1 if y1 < y2 else -1
    return dx, dy, xDirection, yDirection


def drawLine(tgBuf: TactileGraphicsBuffer, x1: int, y1: int, x2: int, y2: int) -> None:
    """
    Draws a line from (x1,y1) to (x2,y2) using Bresenham's line algorithm.
    The algorithm ensures efficient line drawing with evenly spaced dots.
    :param tgBuf: The TactileGraphicsBuffer to draw on
    :param x1: Starting x coordinate
    :param y1: Starting y coordinate
    :param x2: Ending x coordinate
    :param y2: Ending y coordinate
    """
    dx, dy, xDirection, yDirection = _getLineDirections(x1, y1, x2, y2)
    currentX, currentY = x1, y1
    
    # Choose the driving axis based on which has the larger delta
    if dx > dy:
        # X-axis is driving
        error = dx / 2.0
        while currentX != x2:
            _setDotIfInBounds(tgBuf, currentX, currentY)
            error -= dy
            if error < 0:
                currentY += yDirection
                error += dx
            currentX += xDirection
    else:
        # Y-axis is driving
        error = dy / 2.0
        while currentY != y2:
            _setDotIfInBounds(tgBuf, currentX, currentY)
            error -= dx
            if error < 0:
                currentX += xDirection
                error += dy
            currentY += yDirection
    
    # Draw the final point
    _setDotIfInBounds(tgBuf, currentX, currentY)


def drawRectangle(tgBuf: TactileGraphicsBuffer, x: int, y: int, width: int, height: int, fill: bool = False) -> None:
    """
    Draws a rectangle on the buffer.
    :param tgBuf: The TactileGraphicsBuffer to draw on
    :param x: Left coordinate
    :param y: Top coordinate
    :param width: Width of rectangle
    :param height: Height of rectangle
    :param fill: If True, fills the rectangle. If False, only draws the outline
    """
    if fill:
        # Draw filled rectangle by setting all dots within the bounds
        for currentY in range(y, y + height):
            for currentX in range(x, x + width):
                _setDotIfInBounds(tgBuf, currentX, currentY)
    else:
        # Draw outline by drawing four lines
        right = x + width - 1
        bottom = y + height - 1
        
        # Draw horizontal edges
        for currentX in range(x, x + width):
            _setDotIfInBounds(tgBuf, currentX, y)  # Top edge
            _setDotIfInBounds(tgBuf, currentX, bottom)  # Bottom edge
        
        # Draw vertical edges
        for currentY in range(y, y + height):
            _setDotIfInBounds(tgBuf, x, currentY)  # Left edge
            _setDotIfInBounds(tgBuf, right, currentY)  # Right edge
