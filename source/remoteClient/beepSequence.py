import collections.abc
import threading
import time
from typing import Tuple, Union

import tones

local_beep = tones.beep

BeepElement = Union[int, Tuple[int, int]]  # Either delay_ms or (frequency_hz, duration_ms)
BeepSequence = collections.abc.Iterable[BeepElement]


def beepSequence(*sequence: BeepElement) -> None:
	"""Play a simple synchronous monophonic beep sequence
	A beep sequence is an iterable containing one of two kinds of elements.
	An element consisting of a tuple of two items is interpreted as a frequency and duration. Note, this function plays beeps synchronously, unlike tones.beep
	A single integer is assumed to be a delay in ms.
	"""
	for element in sequence:
		if not isinstance(element, collections.abc.Sequence):
			time.sleep(float(element) / 1000)
		else:
			tone, duration = element
			time.sleep(float(duration) / 1000)
			local_beep(tone, duration)


def beepSequenceAsync(*sequence: BeepElement) -> threading.Thread:
	"""Play an asynchronous beep sequence.
	This is the same as `beepSequence`, except it runs in a thread."""
	thread = threading.Thread(target=beepSequence, args=sequence)
	thread.daemon = True
	thread.start()
	return thread
