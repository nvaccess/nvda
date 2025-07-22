# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter

"""Utilities to annotate ctypes dll exports."""

import ctypes
import inspect
from dataclasses import dataclass
from functools import wraps
import types
from typing import Annotated, Any, get_origin, Type, Protocol, runtime_checkable
from enum import IntEnum

from logHandler import log


class ParamDirectionFlag(IntEnum):
	IN = 1
	"""Specifies an input parameter to the function."""
	OUT = 2
	"""Output parameter. The foreign function fills in a value."""
	IN_ZERO = 4
	"""Input parameter which defaults to the integer zero."""


@runtime_checkable
class _SupportsFromParam(Protocol):
	"""Protocol for types that can be used as input parameters to ctypes functions."""

	@classmethod
	def from_param(cls, value: Any) -> Any: ...


@dataclass(frozen=True)
class OutParam:
	"""Annotation for output parameters in function signatures."""

	type: ctypes._Pointer
	"""The type of the output parameter. This should be a pointer type."""
	name: str
	"""The name of the output parameter."""
	position: int
	"""The position of the output parameter in argtypes."""


@dataclass
class FuncSpec:
	"""Specification of a ctypes function."""

	restype: Type[_SupportsFromParam]
	argtypes: tuple[_SupportsFromParam]
	paramFlags: tuple[
		tuple[ParamDirectionFlag, str] | tuple[ParamDirectionFlag, str, int | ctypes._SimpleCData]
	]


def getFuncSPec(
	pyFunc: types.FunctionType,
	restype: Type[ctypes._SimpleCData] | None = None,
) -> FuncSpec:
	sig = inspect.signature(pyFunc)
	# Extract argument types from annotations
	argtypes = []
	paramFlags = []
	for param in sig.parameters.values():
		t = param.annotation
		if t is inspect.Parameter.empty:
			raise TypeError(f"Missing type annotation for parameter: {param.name}")
		elif get_origin(t) is Annotated:
			if len(t.__metadata__) != 1 or not isinstance(t.__metadata__[0], _SupportsFromParam):
				raise TypeError(f"Expected single annotation of a ctypes type for parameter: {param.name}")
			t = t.__metadata__[0]
		if not isinstance(t, _SupportsFromParam):
			raise TypeError(
				f"Expected a ctypes compatible type for parameter: {param.name}, got {t.__name__!r}",
			)
		argtypes.append(t)
		if param.default in (inspect.Parameter.empty, 0):
			paramFlags.append(
				(ParamDirectionFlag.IN_ZERO if param.default == 0 else ParamDirectionFlag.IN, param.name),
			)
		else:
			paramFlags.append((ParamDirectionFlag.IN, param.name, param.default))

	# Extract return type
	expectedRestype = sig.return_annotation
	if expectedRestype is inspect.Signature.empty:
		raise TypeError("Missing return type annotation")
	elif isinstance(expectedRestype, tuple):
		if restype is None:
			raise TypeError("restype should be provided when using a tuple for return type")
		requireOutParamAnnotations = True
		restypes = list(expectedRestype)
	else:
		requireOutParamAnnotations = restype is not None
		restypes = [expectedRestype]
	for i, t in enumerate(restypes):
		isAnnotated = get_origin(t) is Annotated and len(t.__metadata__) == 1
		if requireOutParamAnnotations:
			if not isAnnotated or not isinstance(t.__metadata__[0], OutParam):
				raise TypeError(f"Expected single annotation of type 'OutParam' for parameter: {param.name}")
			outParam = t.__metadata__[0]
			argtypes.insert(outParam.position, outParam.type)
			paramFlags.insert(outParam.position, (ParamDirectionFlag.OUT, outParam.name))
		elif isAnnotated:
			annotation = t.__metadata__[0]
			if not isinstance(annotation, _SupportsFromParam):
				raise TypeError(
					f"Expected single annotation of a ctypes type for result type, got {annotation!r}",
				)
			restype = annotation
		else:
			restype = t

	return FuncSpec(
		restype=restype,
		argtypes=tuple(argtypes),
		paramFlags=tuple(paramFlags),
	)


def dllFunc(
	library: ctypes.CDLL,
	funcName: str,
	restype: Type[ctypes._SimpleCData] = None,
	*,
	cFunctype=ctypes.WINFUNCTYPE,
	annotateOriginalCFunc=True,
	wrapNewCFunc=True,
):
	cFunc = getattr(library, funcName)

	def decorator(pyFunc: types.FunctionType):
		nonlocal restype
		if not isinstance(pyFunc, types.FunctionType):
			raise TypeError(f"Expected a function, got {type(pyFunc).__name__!r}")
		spec = getFuncSPec(pyFunc, restype)
		# Set ctypes metadata for the original function in case it is called from outside
		if annotateOriginalCFunc:
			if cFunc.argtypes is not None:
				log.warning(
					f"Overriding existing argtypes for {pyFunc.__name__!r}: {cFunc.argtypes} -> {spec.argtypes}",
					stack_info=True,
				)
			cFunc.argtypes = spec.argtypes
			if cFunc.restype is not None:
				log.warning(
					f"Overriding existing restype for {pyFunc.__name__!r}: {cFunc.restype} -> {spec.restype}",
					stack_info=True,
				)
			cFunc.restype = spec.restype

		wrapper = wraps(pyFunc)
		if not wrapNewCFunc:
			return wrapper(cFunc)
		newCFuncClass = cFunctype(spec.restype, *spec.argtypes)
		newCFunc = newCFuncClass((funcName, library), spec.paramFlags)
		return wrapper(newCFunc)

	return decorator
