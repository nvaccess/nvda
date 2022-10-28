# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html


from time import (
	perf_counter as timer,
	sleep,
)
from typing import (
	Any,
	Callable,
	Optional,
	Tuple,
)


def blockUntilConditionMet(
		getValue: Callable[[], Any],
		giveUpAfterSeconds: float,
		shouldStopEvaluator: Callable[[Any], bool] = lambda value: bool(value),
		intervalBetweenSeconds: float = 0.1,
		) -> Tuple[
bool,  # Was evaluator met?
Optional[Any]  # None or the value when the evaluator was met
]:
	"""Repeatedly tries to get a value up until a time limit expires.
	Tries are separated by a time interval.
	The call will block until shouldStopEvaluator returns True when given the value,
	the default evaluator just returns the value converted to a boolean.
	@return: A tuple, (True, value) if evaluator condition is met, otherwise (False, None)
	"""
	minIntervalBetweenSeconds = 0.001
	assert intervalBetweenSeconds > minIntervalBetweenSeconds
	lastSleepTime = startTime = timer()
	while (timer() - startTime) < giveUpAfterSeconds:
		val = getValue()
		if shouldStopEvaluator(val):
			return True, val
		timeElapsedSinceLastSleep = timer() - lastSleepTime
		sleepTime = max(
			# attempt to keep a regular period between polling
			intervalBetweenSeconds - timeElapsedSinceLastSleep,
			minIntervalBetweenSeconds,
		)
		sleep(sleepTime)
		lastSleepTime = timer()

	return False, None
