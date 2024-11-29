# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
This module provides functions for drawing basic shapes on a TactileGraphicsBuffer.
"""

from . import TactileGraphicsBuffer


def drawLine(tgBuf: TactileGraphicsBuffer, x1: int, y1: int, x2: int, y2: int):
    """
    Draws a line from (x1,y1) to (x2,y2) using Bresenham's line algorithm.
    :param tgBuf: The TactileGraphicsBuffer to draw on
    :param x1: Starting x coordinate
    :param y1: Starting y coordinate
    :param x2: Ending x coordinate
    :param y2: Ending y coordinate
    """
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            if 0 <= x < tgBuf.width and 0 <= y < tgBuf.height:
                tgBuf.setDot(x, y)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            if 0 <= x < tgBuf.width and 0 <= y < tgBuf.height:
                tgBuf.setDot(x, y)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    if 0 <= x < tgBuf.width and 0 <= y < tgBuf.height:
        tgBuf.setDot(x, y)


def drawRectangle(tgBuf: TactileGraphicsBuffer, x: int, y: int, width: int, height: int, fill: bool = False):
    """
    Draws a rectangle on the buffer.
    :param tgBuf: The TactileGraphicsBuffer to draw on
    :param x: Left coordinate
    :param y: Top coordinate
    :param width: Width of rectangle
    :param height: Height of rectangle
    :param fill: If True, fills the rectangle. If False, only draws the outline.
    """
    if fill:
        for cy in range(y, y + height):
            for cx in range(x, x + width):
                if 0 <= cx < tgBuf.width and 0 <= cy < tgBuf.height:
                    tgBuf.setDot(cx, cy)
    else:
        # Draw horizontal lines
        for cx in range(x, x + width):
            if 0 <= cx < tgBuf.width:
                if 0 <= y < tgBuf.height:
                    tgBuf.setDot(cx, y)
                if 0 <= y + height - 1 < tgBuf.height:
                    tgBuf.setDot(cx, y + height - 1)
        # Draw vertical lines
        for cy in range(y, y + height):
            if 0 <= cy < tgBuf.height:
                if 0 <= x < tgBuf.width:
                    tgBuf.setDot(x, cy)
                if 0 <= x + width - 1 < tgBuf.width:
                    tgBuf.setDot(x + width - 1, cy)
