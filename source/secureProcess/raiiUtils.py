# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from typing import Callable, TypeVar, cast, Any

class OnDelete[T]:
	"""RAII helper: call a deleter with the stored value when this object is destroyed.

	Example: OnDelete(handle, CloseHandle)
	"""

	def __init__(self, value: T, deleter: Callable[[T], Any]):
		"""Initialize the RAII helper.

		:param value: The resource or value to hold. This will be passed to the
		    deleter when this object is destroyed.
		:param deleter: Callable that releases or cleans up the stored value.
		    It will be invoked with the value as its only argument when the
		    object's destructor runs.
		"""

		self._value = value
		self._deleter = deleter

	def __del__(self):
		self._deleter(self._value)

	@property
	def value(self) -> T:
		return self._value


_makeAutoFreeCache = {}
def makeAutoFree[T](cls: type[T], deleter: Callable[[T], Any], cache: bool = True) -> type[T]:
	"""Create a lightweight RAII-style subclass that auto-frees instances.

	This factory returns a new subclass of ``cls`` whose ``__del__`` method
	invokes ``deleter`` with the instance when it is garbage-collected. The
	created subclass name is prefixed with ``AutoFree`` followed by the base
	class name.

	:param cls: The base class to subclass. Instances of the returned class
		behave like instances of ``cls`` but will call ``deleter`` on
		finalization.
	:param deleter: Callable invoked from the generated ``__del__`` method.
		It will be called with the instance as its sole argument when the
		Python garbage collector finalizes the object.
	:param cache: When true, attempt to reuse a previously created subclass
		for the same (class, deleter) pair. This avoids creating multiple
		identical subclasses.

	:return: A subclass of ``cls`` whose destructor calls ``deleter``.

	Notes
	-----
	The returned class implements ``__del__`` by calling ``deleter(self)``;
	ensure the provided deleter accepts the instance type. Caching is best-effort
	and keyed by the base class and the ``id`` of the deleter callable.
	"""

	key = (cls, id(deleter))
	if cache:
		cachedCls = _makeAutoFreeCache.get(key)
		if cachedCls:
			return cachedCls
	newCls = type(
		f"AutoFree{cls.__name__}",
		(cls,),
		{
			"__del__": lambda self: deleter(self) if self else None
		}
	)
	return cast(type[T], newCls)
