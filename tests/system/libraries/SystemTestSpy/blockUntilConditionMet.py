# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module is not a Robot Framework library itself. Instead it provides utility methods called from
libraries. It is also copied into the (system test specific) NVDA profile directory as part of a global plugin
package. This enables sharing utility methods between the global plugin and other Robot Framework libraries.
"""

from time import (
	perf_counter as _timer,
	sleep as _sleep,
)
from typing import (
	Any,
	Callable,
	Optional,
	Tuple,
)

EvaluatorWasMetT = bool
GetValueResultT = Any

DEFAULT_INTERVAL_BETWEEN_EVAL_SECONDS = 0.1
"""The default interval (in seconds) between calls to the evaluator."""

_MIN_INTERVAL_BETWEEN_EVAL_SECONDS = 0.01
"""The minimum interval (in seconds) between calls to the evaluator.
Small values for the interval can starve NVDA core, preventing it
from being able to process queued events.
"""


def _blockUntilConditionMet(
	getValue: Callable[[], GetValueResultT],
	giveUpAfterSeconds: float,
	shouldStopEvaluator: Callable[[GetValueResultT], bool] = lambda value: bool(value),
	intervalBetweenSeconds: float = DEFAULT_INTERVAL_BETWEEN_EVAL_SECONDS,
	errorMessage: Optional[str] = None,
) -> Tuple[
	EvaluatorWasMetT,  # Was evaluator met?
	Optional[GetValueResultT],  # Value when the evaluator was met, if it was met.
]:
	"""Repeatedly tries to get a value up until a time limit expires.
	Tries are separated by a time interval.
	The call will block until shouldStopEvaluator returns True when given the value,
	the default evaluator just returns the value converted to a boolean.
	@param getValue: Get the value to be tested by shouldStopEvaluator.
	@param giveUpAfterSeconds: The max number of seconds to block for.
	@param shouldStopEvaluator: Given the last value from getValue, is the condition met?
	When True is returned, stop blocking.
	@param intervalBetweenSeconds: The approximate period (seconds) between each test of getValue.
	Small values can starve NVDA core preventing it from being able to process queued events.
	Must be greater than _MIN_INTERVAL_BETWEEN_EVAL_SECONDS, higher is recommended.
	@param errorMessage: Use 'None' to suppress the exception.
	@return: A tuple, (True, value) if evaluator condition is met, otherwise (False, None)
	@raises: AssertionError if the time limit expires and an errorMessage is given.
	"""
	assert callable(getValue)
	assert callable(shouldStopEvaluator)
	assert intervalBetweenSeconds > _MIN_INTERVAL_BETWEEN_EVAL_SECONDS
	lastSleepTime = startTime = _timer()
	while (_timer() - startTime) < giveUpAfterSeconds:
		val = getValue()
		if shouldStopEvaluator(val):
			return True, val
		timeElapsedSinceLastSleep = _timer() - lastSleepTime
		sleepTime = max(
			# attempt to keep a regular period between polling
			intervalBetweenSeconds - timeElapsedSinceLastSleep,
			_MIN_INTERVAL_BETWEEN_EVAL_SECONDS,
		)
		_sleep(sleepTime)
		lastSleepTime = _timer()

	if errorMessage:
		raise AssertionError(errorMessage)
	return False, None
