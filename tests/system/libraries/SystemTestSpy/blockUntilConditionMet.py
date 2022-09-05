# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module is not a Robot Framework library itself. Instead it provides utility methods called from
libraries. It is also copied into the (system test specific) NVDA profile directory as part of a global plugin
package. This enables sharing utility methods between the global plugin and other Robot Framework libraries.
"""

from time import sleep as _sleep
from time import perf_counter as _timer
from typing import Any, Callable, Optional, Tuple

EvaluatorWasMetT = bool
GetValueResultT = Any

def _blockUntilConditionMet(
		getValue: Callable[[], GetValueResultT],
		giveUpAfterSeconds: float,
		shouldStopEvaluator=lambda value: bool(value),
		intervalBetweenSeconds: float = 0.3,
		errorMessage: Optional[str] = None
		) -> Tuple[
EvaluatorWasMetT,  # Was evaluator met?
Optional[GetValueResultT]  # Value when the evaluator was met, if it was met.
]:
	"""Repeatedly tries to get a value up until a time limit expires. Tries are separated by
	a time interval. The call will block until shouldStopEvaluator returns True when given the value,
	the default evaluator just returns the value converted to a boolean.
	@param getValue: Get the value to be tested by shouldStropEvaluator.
	@param giveUpAfterSeconds: The max number of seconds to block for.
	@param shouldStopEvaluator: Given the last value from getValue, is the condition met?
	When True is returned, stop blocking.
	@param intervalBetweenSeconds: The approximate period (seconds) between each test of getValue.
	Small values can starve NVDA core preventing it from being able to process queued events.
	Must be greater than 0.1, higher is recommended.
	@param errorMessage: Use 'None' to suppress the exception.
	@raises RuntimeError if the time limit expires and an errorMessage is given.
	"""
	assert callable(getValue)
	assert callable(shouldStopEvaluator)
	assert intervalBetweenSeconds > 0.1

	SLEEP_TIME = max(intervalBetweenSeconds, 0.1)

	startTime = _timer()
	lastRunTime = startTime
	firstRun = True  # ensure we start immediately
	while (_timer() - startTime) < giveUpAfterSeconds:
		if firstRun or (_timer() - lastRunTime) > intervalBetweenSeconds:
			firstRun = False
			lastRunTime = _timer()
			val = getValue()
			if shouldStopEvaluator(val):
				return True, val
			_sleep(SLEEP_TIME)

	else:
		if errorMessage:
			raise AssertionError(errorMessage)
		return False, None
