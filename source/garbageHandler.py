# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import sys
import gc
import threading
from logHandler import log

""" Watches Python's cyclic garbage collector and reports questionable collections. """


class TrackedObject:
	"""
	An object that notifies garbageHandler when it is destructed,
	so that NVDA can log when important unreachable objects are being deleted
	by Python's cyclic garbage collector.
	"""

	def __del__(self):
		# __del__ may still be called while Python is exiting.
		# And therefore some symbols may be set to None.
		isFinalizing = getattr(sys, 'is_finalizing', lambda: True)()
		if not isFinalizing:
			notifyObjectDeletion(self)


_collectionThreadID = 0
_reportCountDuringCollection = 0


def initialize():
	""" Initializes NVDA's garbage handler. """
	# Instruct Python to keep all unreachable objects for later inspection
	# gc.set_debug(gc.DEBUG_SAVEALL)
	# Register a callback with Python's garbage collector
	# That will notify us of the start and end of each collection run.
	gc.callbacks.append(_collectionCallback)


def _collectionCallback(action, info):
	global _collectionThreadID, _reportCountDuringCollection
	if action == "start":
		_collectionThreadID = threading.currentThread().ident
		_reportCountDuringCollection = 0
	elif action == "stop":
		_collectionThreadID = 0
		if _reportCountDuringCollection > 0:
			log.error(f"Found at least {_reportCountDuringCollection} unreachable objects in run")
	else:
		log.error(f"Unknown action: {action}")


def notifyObjectDeletion(obj):
	"""
	Logs a message about the given object being deleted,
	if it is due to Python's cyclic garbage collector.
	"""
	global _reportCountDuringCollection
	if _collectionThreadID != threading.currentThread().ident:
		return
	_reportCountDuringCollection += 1
	if _reportCountDuringCollection == 1:
		log.warning(
			"Garbage collector has found one or more unreachable objects. See further warnings for specific objects.",
			stack_info=True
		)
	log.warning(f"Deleting unreachable object {obj}")



def terminate():
	""" Terminates NVDA's garbage handler. """
	gc.callbacks.remove(_collectionCallback)
