# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


def replace__new__():
	import enum
	# prevent cyclic references on ValueError during construction
	enum.Enum.__new__ = _replacement__new__


def _replacement__new__(cls, value):
	""" Copied from python standard library enum.py class Enum.
	Prevent cyclic references on ValueError during construction.
	Local variable exc must be deleted, otherwise:
	- ref to exc held by the frame
	- ref to traceback held by exc
	- ref to frame held by traceback
	"""
	# all enum instances are actually created during class construction
	# without calling this method; this method is called by the metaclass'
	# __call__ (i.e. Color(3) ), and by pickle
	if type(value) is cls:
		# For lookups like Color(Color.RED)
		return value
	# by-value search for a matching enum member
	# see if it's in the reverse mapping (for hashable values)
	try:
		return cls._value2member_map_[value]
	except KeyError:
		# Not found, no need to do long O(n) search
		pass
	except TypeError:
		# not there, now do long search -- O(n) behavior
		for member in cls._member_map_.values():
			if member._value_ == value:
				return member
	# still not found -- try _missing_ hook
	try:
		result = cls._missing_(value)
	except Exception as e:
		e.__context__ = ValueError("%r is not a valid %s" % (value, cls.__name__))
		raise e

	if isinstance(result, cls):
		return result

	with ValueError(
		"%r is not a valid %s" % (value, cls.__name__)
	) as ve_exc:
		if result is None:
			raise ve_exc

		te_exc = TypeError(
			'error in %s._missing_: returned %r instead of None or a valid member'
			% (cls.__name__, result)
		)
		te_exc.__context__ = ve_exc
		raise te_exc
