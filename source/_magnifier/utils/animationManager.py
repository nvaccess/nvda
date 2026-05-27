# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Linear animation manager for smooth magnifier transitions.
Does not own a timer — callers drive animation by invoking tick() at their own cadence.
"""

import math
from typing import Callable
from .types import AnimationFrame, Coordinates


class AnimationManager:
	"""
	Drives fixed-step linear interpolation between two AnimationFrames.

	Each tick() call advances the animation by exactly 1/totalSteps of the total distance.
	The animation completes after exactly totalSteps ticks, with no asymptotic tail.

	Callers are responsible for the timer: call tick() each interval until isComplete is True.
	A new setTarget() call mid-animation redirects from the current frame in a new totalSteps sequence.

	When speedPxPerTick is provided, setTarget() computes totalSteps from the Euclidean distance
	between the current and target coordinates, capped at maxSteps.  An explicit totalSteps
	argument to setTarget() always takes precedence over the auto-computed value.
	"""

	def __init__(
		self,
		totalSteps: int = 40,
		speedPxPerTick: float | None = None,
		maxSteps: int | None = None,
	) -> None:
		"""
		:param totalSteps: Default number of ticks per animation segment.
		    Used when speedPxPerTick is None, or as the fallback when distance is zero.
		    At 12 ms/tick, 40 steps = 480 ms (matches the original spotlight animation).
		:param speedPxPerTick: Pixels to travel per tick.  When set, setTarget() computes
		    the number of steps from distance ÷ speed so every segment animates at the same
		    visual velocity regardless of distance.
		:param maxSteps: Upper bound on the auto-computed step count.  Has no effect when
		    speedPxPerTick is None.
		"""
		if totalSteps < 1:
			raise ValueError(f"totalSteps must be >= 1, got {totalSteps}")
		if speedPxPerTick is not None and speedPxPerTick <= 0:
			raise ValueError(f"speedPxPerTick must be > 0, got {speedPxPerTick}")
		self._totalSteps = totalSteps
		self._speedPxPerTick = speedPxPerTick
		self._maxSteps = maxSteps
		self._step: int = 0
		self._start: AnimationFrame | None = None
		self._current: AnimationFrame | None = None
		self._target: AnimationFrame | None = None
		self._onComplete: Callable[[], None] | None = None
		self._isComplete: bool = True

	def start(self, initial: AnimationFrame) -> None:
		"""Initialise the animator at a known frame. Must be called before the first tick()."""
		self._start = initial
		self._current = initial
		self._target = initial
		self._isComplete = True
		self._onComplete = None
		self._step = 0

	def reset(self) -> None:
		"""
		Return to uninitialised state without discarding speed/step configuration.
		After reset(), start() must be called before tick() can be used again.
		"""
		self._step = 0
		self._start = None
		self._current = None
		self._target = None
		self._onComplete = None
		self._isComplete = True

	def setTarget(
		self,
		target: AnimationFrame,
		onComplete: Callable[[], None] | None = None,
		totalSteps: int | None = None,
	) -> None:
		"""
		Set a new destination frame, starting a fresh linear sequence from the current position.
		Redirects any in-progress animation from the current frame without jumping.

		Step count resolution (highest priority first):
		  1. The explicit totalSteps argument, if provided.
		  2. Auto-computed from distance when speedPxPerTick was set at construction.
		  3. The totalSteps value from the constructor (unchanged).
		"""
		self._start = self._current
		self._target = target
		self._onComplete = onComplete
		self._isComplete = False
		self._step = 0
		if totalSteps is not None:
			if totalSteps < 1:
				raise ValueError(f"totalSteps must be >= 1, got {totalSteps}")
			self._totalSteps = totalSteps
		elif self._speedPxPerTick is not None and self._start is not None:
			dx = target.coordinates.x - self._start.coordinates.x
			dy = target.coordinates.y - self._start.coordinates.y
			dist = math.hypot(dx, dy)
			steps = round(dist / self._speedPxPerTick)
			if self._maxSteps is not None:
				steps = min(steps, self._maxSteps)
			self._totalSteps = max(1, steps)

	def tick(self) -> AnimationFrame:
		"""
		Advance the animation by one linear step and return the resulting frame.
		Calls onComplete once when totalSteps is reached.
		Raises RuntimeError if start() has not been called yet.
		"""
		if self._current is None:
			raise RuntimeError("AnimationManager not initialised — call start() first")
		if self._isComplete or self._target is None:
			return self._current

		self._step += 1
		t = self._step / self._totalSteps

		zoom = self._start.zoomLevel + (self._target.zoomLevel - self._start.zoomLevel) * t
		x = self._start.coordinates.x + (self._target.coordinates.x - self._start.coordinates.x) * t
		y = self._start.coordinates.y + (self._target.coordinates.y - self._start.coordinates.y) * t

		if self._step >= self._totalSteps:
			self._current = self._target
			self._isComplete = True
			if self._onComplete:
				cb = self._onComplete
				self._onComplete = None
				cb()
		else:
			self._current = AnimationFrame(
				round(zoom, 2),
				Coordinates(round(x), round(y)),
			)

		return self._current

	@property
	def isComplete(self) -> bool:
		return self._isComplete

	@property
	def currentFrame(self) -> AnimationFrame | None:
		return self._current
