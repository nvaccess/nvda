# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Runtime components that execute in the ART process."""

import threading

# Global runtime instance - thread-safe singleton pattern
_runtime_instance = None
_runtime_lock = threading.Lock()

def setRuntime(runtimeInstance):
	"""Set the global ART runtime instance. Can only be called once.
	
	@param runtimeInstance: The ARTRuntime instance to register
	@raises RuntimeError: If runtime has already been set
	@raises ValueError: If runtimeInstance is None
	"""
	global _runtime_instance
	with _runtime_lock:
		if _runtime_instance is not None:
			raise RuntimeError("ARTRuntime has already been set.")
		if runtimeInstance is None:
			raise ValueError("runtimeInstance cannot be None.")
		_runtime_instance = runtimeInstance

def getRuntime():
	"""Get the global ART runtime instance.
	
	@return: The registered ARTRuntime instance
	@raises RuntimeError: If runtime has not been initialized yet
	"""
	if _runtime_instance is None:
		raise RuntimeError("ARTRuntime has not been initialized. It must be set before it can be accessed.")
	return _runtime_instance
