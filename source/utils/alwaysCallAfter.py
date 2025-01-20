"""Thread-safe GUI updates for wxPython.

Provides a decorator that ensures functions execute in the main GUI thread
using wx.CallAfter, required for safe interface updates from background threads.
"""

from functools import wraps

import wx


def alwaysCallAfter(func):
	"""Makes GUI updates thread-safe by running in the main thread.

	Example:
	    @alwaysCallAfter
	    def update_label(text):
	        label.SetLabel(text)  # Safe GUI update from any thread
	"""

	@wraps(func)
	def wrapper(*args, **kwargs):
		wx.CallAfter(func, *args, **kwargs)

	return wrapper
