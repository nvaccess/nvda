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


def _blockUntilConditionMet(
		getValue: Callable[[], Any],
		giveUpAfterSeconds: float,
		shouldStopEvaluator=lambda value: bool(value),
		intervalBetweenSeconds: float = 0.1,
		errorMessage: Optional[str] = None
		) -> Tuple[
bool,  # Was evaluator met?
Optional[Any]  # None or the value when the evaluator was met
]:
	"""Repeatedly tries to get a value up until a time limit expires. Tries are separated by
	a time interval. The call will block until shouldStopEvaluator returns True when given the value,
	the default evaluator just returns the value converted to a boolean.
	@param errorMessage Use 'None' to suppress the exception.
	@return A tuple, (True, value) if evaluator condition is met, otherwise (False, None)
	@raises RuntimeError if the time limit expires and an errorMessage is given.
	"""
	assert callable(getValue)
	assert callable(shouldStopEvaluator)
	assert intervalBetweenSeconds > 0.001
	SLEEP_TIME = intervalBetweenSeconds * 0.5
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
