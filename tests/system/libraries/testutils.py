from timeit import default_timer as timer

def blockUntilConditionMet(
		getValue,
		giveUpAfterSeconds,
		shouldStopEvaluator=lambda value: bool(value),
		intervalBetweenSeconds=0.1,
		errorMessage=None):
	"""Repeatedly tries to get a value up until a time limit expires. Tries are separated by
	a time interval. The call will block until shouldStopEvaluator returns True when given the value,
	the default evaluator just returns the value converted to a boolean.
	@return A tuple, (True, value) if evaluator condition is met, otherwise (False, None)
	@raises RuntimeError if the time limit expires and an errorMessage is given.
	"""
	startTime = timer()
	lastRunTime = startTime
	firstRun=True  # ensure we start trying immediately
	while (timer() - startTime) < giveUpAfterSeconds:
		if firstRun or (timer() - lastRunTime) > intervalBetweenSeconds:
			firstRun = False
			lastRunTime = timer()
			val = getValue()
			if shouldStopEvaluator(val):
				return True, val
	else:
		if errorMessage:
			raise AssertionError(errorMessage)
		return False, None
