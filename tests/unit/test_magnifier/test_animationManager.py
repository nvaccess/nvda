# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from _magnifier.utils.animationManager import AnimationManager
from _magnifier.utils.types import AnimationFrame, Coordinates


def _frame(zoom: float, x: int, y: int) -> AnimationFrame:
	return AnimationFrame(zoom, Coordinates(x, y))


class TestAnimationManager(unittest.TestCase):
	"""Test suite for AnimationManager linear interpolation."""

	def testDefaultTotalSteps(self):
		"""Default number of steps should be 40."""
		manager = AnimationManager()
		self.assertEqual(manager._totalSteps, 40)

	def testCustomTotalSteps(self):
		"""totalSteps parameter should be stored."""
		manager = AnimationManager(totalSteps=20)
		self.assertEqual(manager._totalSteps, 20)

	def testInitiallyComplete(self):
		"""A freshly created manager should report isComplete=True (no animation pending)."""
		manager = AnimationManager()
		self.assertTrue(manager.isComplete)

	def testCurrentFrameIsNoneBeforeStart(self):
		"""currentFrame should be None before start() is called."""
		manager = AnimationManager()
		self.assertIsNone(manager.currentFrame)

	def testStartSetsCurrentFrame(self):
		"""start() should initialise currentFrame to the given frame."""
		manager = AnimationManager()
		initial = _frame(200.0, 500, 400)
		manager.start(initial)
		self.assertEqual(manager.currentFrame, initial)

	def testStartKeepsComplete(self):
		"""start() should leave isComplete=True (no animation running)."""
		manager = AnimationManager()
		manager.start(_frame(200.0, 500, 400))
		self.assertTrue(manager.isComplete)

	def testTickBeforeStartRaisesRuntimeError(self):
		"""tick() without a prior start() should raise RuntimeError."""
		manager = AnimationManager()
		with self.assertRaises(RuntimeError):
			manager.tick()

	def testSetTargetStartsAnimation(self):
		"""setTarget() should mark animation as in progress."""
		manager = AnimationManager(totalSteps=10)
		manager.start(_frame(200.0, 0, 0))
		manager.setTarget(_frame(100.0, 100, 0))
		self.assertFalse(manager.isComplete)

	def testSetTargetStoresTarget(self):
		"""setTarget() should store the target frame."""
		manager = AnimationManager(totalSteps=10)
		manager.start(_frame(200.0, 0, 0))
		target = _frame(100.0, 100, 0)
		manager.setTarget(target)
		self.assertEqual(manager._target, target)

	def testCompletesInExactlyTotalSteps(self):
		"""Animation must complete after exactly totalSteps ticks, no more, no less."""
		steps = 10
		manager = AnimationManager(totalSteps=steps)
		manager.start(_frame(200.0, 0, 0))
		manager.setTarget(_frame(100.0, 100, 0))

		for i in range(steps - 1):
			manager.tick()
			self.assertFalse(manager.isComplete, f"Should not be complete at step {i + 1}")

		manager.tick()  # final step
		self.assertTrue(manager.isComplete)

	def testFinalFrameIsExactlyTarget(self):
		"""The frame returned on the last tick must equal the target exactly."""
		manager = AnimationManager(totalSteps=10)
		target = _frame(100.0, 960, 540)
		manager.start(_frame(200.0, 0, 0))
		manager.setTarget(target)

		for _ in range(10):
			frame = manager.tick()

		self.assertEqual(frame, target)

	def testInterpolationIsLinear(self):
		"""Each step should cover an equal fraction of the total distance."""
		steps = 10
		manager = AnimationManager(totalSteps=steps)
		manager.start(_frame(200.0, 0, 0))
		manager.setTarget(_frame(100.0, 100, 0))

		frames = [manager.tick() for _ in range(steps - 1)]  # exclude snap step

		for i, frame in enumerate(frames):
			expectedZoom = round(200.0 + (100.0 - 200.0) * (i + 1) / steps, 2)
			expectedX = round(0 + (100 - 0) * (i + 1) / steps)
			self.assertAlmostEqual(frame.zoomLevel, expectedZoom, places=1)
			self.assertEqual(frame.coordinates.x, expectedX)

	def testFirstStepIsNotAtTarget(self):
		"""The first tick should produce an intermediate value, not the target."""
		manager = AnimationManager(totalSteps=10)
		manager.start(_frame(200.0, 0, 0))
		manager.setTarget(_frame(100.0, 100, 0))

		frame = manager.tick()
		self.assertNotEqual(frame.zoomLevel, 100.0)

	def testOnCompleteCalledOnFinalStep(self):
		"""onComplete callback should be called exactly once when the animation finishes."""
		manager = AnimationManager(totalSteps=5)
		manager.start(_frame(200.0, 0, 0))

		calls = []
		manager.setTarget(_frame(100.0, 100, 0), onComplete=lambda: calls.append(1))

		for _ in range(5):
			manager.tick()

		self.assertEqual(len(calls), 1)

	def testOnCompleteNotCalledBeforeFinalStep(self):
		"""onComplete must not fire before the last step."""
		manager = AnimationManager(totalSteps=5)
		manager.start(_frame(200.0, 0, 0))

		calls = []
		manager.setTarget(_frame(100.0, 100, 0), onComplete=lambda: calls.append(1))

		for _ in range(4):
			manager.tick()

		self.assertEqual(len(calls), 0)

	def testOnCompleteNotCalledAgainOnExtraTicks(self):
		"""Extra tick() calls after completion must not invoke onComplete again."""
		manager = AnimationManager(totalSteps=5)
		manager.start(_frame(200.0, 0, 0))

		calls = []
		manager.setTarget(_frame(100.0, 100, 0), onComplete=lambda: calls.append(1))

		for _ in range(5):
			manager.tick()

		manager.tick()
		manager.tick()

		self.assertEqual(len(calls), 1)

	def testTickAfterCompleteReturnsTargetFrame(self):
		"""Extra ticks after completion should keep returning the target frame."""
		manager = AnimationManager(totalSteps=5)
		target = _frame(100.0, 100, 0)
		manager.start(_frame(200.0, 0, 0))
		manager.setTarget(target)

		for _ in range(5):
			manager.tick()

		self.assertEqual(manager.tick(), target)

	def testRedirectMidAnimationEndsAtNewTarget(self):
		"""Calling setTarget() mid-animation should redirect and end at the new target."""
		manager = AnimationManager(totalSteps=10)
		manager.start(_frame(200.0, 0, 0))
		manager.setTarget(_frame(100.0, 100, 0))

		# Advance halfway
		for _ in range(5):
			manager.tick()

		# Redirect
		new_target = _frame(150.0, 50, 0)
		manager.setTarget(new_target)
		self.assertFalse(manager.isComplete)

		for _ in range(10):
			frame = manager.tick()

		self.assertEqual(frame, new_target)
		self.assertTrue(manager.isComplete)

	def testRedirectStartsFromCurrentPosition(self):
		"""After a redirect, the first step should depart from the current animated position."""
		manager = AnimationManager(totalSteps=10)
		manager.start(_frame(200.0, 0, 0))
		manager.setTarget(_frame(100.0, 100, 0))

		for _ in range(5):
			mid = manager.tick()

		mid_zoom = mid.zoomLevel

		manager.setTarget(_frame(200.0, 0, 0))
		first = manager.tick()

		# First redirected step must be between mid and the new target, not jump
		self.assertGreater(first.zoomLevel, mid_zoom)
		self.assertLess(first.zoomLevel, 200.0)

	def testSpeedBasedStepsScaleWithDistance(self):
		"""With speedPxPerTick set, totalSteps must equal round(distance / speed)."""
		speed = 10.0
		manager = AnimationManager(speedPxPerTick=speed)
		manager.start(_frame(100.0, 0, 0))

		manager.setTarget(_frame(100.0, 50, 0))  # 50 px → 5 steps
		self.assertEqual(manager._totalSteps, 5)

		manager.start(_frame(100.0, 0, 0))
		manager.setTarget(_frame(100.0, 100, 0))  # 100 px → 10 steps
		self.assertEqual(manager._totalSteps, 10)

	def testSpeedBasedStepsRespectMaxSteps(self):
		"""maxSteps must cap the auto-computed step count."""
		manager = AnimationManager(speedPxPerTick=10.0, maxSteps=5)
		manager.start(_frame(100.0, 0, 0))
		manager.setTarget(_frame(100.0, 1000, 0))  # would be 100 steps without cap

		self.assertEqual(manager._totalSteps, 5)

	def testExplicitTotalStepsOverridesSpeed(self):
		"""An explicit totalSteps argument to setTarget takes precedence over speedPxPerTick."""
		manager = AnimationManager(speedPxPerTick=10.0)
		manager.start(_frame(100.0, 0, 0))
		manager.setTarget(_frame(100.0, 100, 0), totalSteps=3)  # distance would give 10

		self.assertEqual(manager._totalSteps, 3)

	def testReset(self):
		"""reset() must clear animated state while preserving speed configuration."""
		manager = AnimationManager(speedPxPerTick=10.0, maxSteps=20)
		manager.start(_frame(200.0, 0, 0))
		manager.setTarget(_frame(100.0, 50, 0))
		manager.tick()

		manager.reset()

		self.assertIsNone(manager.currentFrame)
		self.assertTrue(manager.isComplete)
		# Speed config must be preserved
		self.assertEqual(manager._speedPxPerTick, 10.0)
		self.assertEqual(manager._maxSteps, 20)

	def testSetTargetBeforeStartRaisesRuntimeError(self):
		"""setTarget() before start() must raise RuntimeError."""
		manager = AnimationManager()
		with self.assertRaises(RuntimeError):
			manager.setTarget(_frame(100.0, 100, 0))

	def testInvalidTotalStepsRaisesValueError(self):
		"""totalSteps=0 in constructor must raise ValueError."""
		with self.assertRaises(ValueError):
			AnimationManager(totalSteps=0)

	def testInvalidSpeedPxPerTickRaisesValueError(self):
		"""speedPxPerTick=0 in constructor must raise ValueError."""
		with self.assertRaises(ValueError):
			AnimationManager(speedPxPerTick=0.0)

	def testInvalidTotalStepsOverrideInSetTargetRaisesValueError(self):
		"""An explicit totalSteps=0 in setTarget must raise ValueError."""
		manager = AnimationManager(totalSteps=10)
		manager.start(_frame(200.0, 0, 0))
		with self.assertRaises(ValueError):
			manager.setTarget(_frame(100.0, 100, 0), totalSteps=0)
