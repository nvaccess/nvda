# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter

"""Utilities to annotate ctypes dll exports."""

import ctypes
import functools
import inspect
import dataclasses
import types
import typing
from enum import IntEnum

from logHandler import log


class ParamDirectionFlag(IntEnum):
	IN = 1
	"""Specifies an input parameter to the function."""
	OUT = 2
	"""Output parameter. The foreign function fills in a value."""
	# Note: IN | OUT is not supported, as ctypes will require this as input parameter and will also return it, which is useless.


@typing.runtime_checkable
class _SupportsFromParam(typing.Protocol):
	"""Protocol for types that can be used as input parameters to ctypes functions."""

	@classmethod
	def from_param(cls, value: typing.Any) -> typing.Self: ...


@dataclasses.dataclass(frozen=True)
class OutParam:
	"""Annotation for output parameters in function signatures."""

	type: ctypes._Pointer
	"""The type of the output parameter. This should be a pointer type."""
	name: str
	"""The name of the output parameter."""
	position: int = 0
	"""The position of the output parameter in argtypes."""


@dataclasses.dataclass
class FuncSpec:
	"""Specification of a ctypes function."""

	restype: typing.Type[_SupportsFromParam]
	argtypes: tuple[_SupportsFromParam]
	paramFlags: tuple[
		tuple[ParamDirectionFlag, str] | tuple[ParamDirectionFlag, str, int | ctypes._SimpleCData]
	]


def getFuncSPec(
	pyFunc: types.FunctionType,
	restype: typing.Type[ctypes._SimpleCData] | None = None,
) -> FuncSpec:
	sig = inspect.signature(pyFunc)
	# Extract argument types from annotations
	argtypes = []
	paramFlags = []
	for param in sig.parameters.values():
		if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
			raise TypeError(
				f"Unsupported parameter kind: {param.kind} for parameter: {param.name} "
				"*args and **kwargs are not supported.",
			)
		t = param.annotation
		if t is inspect.Parameter.empty:
			raise TypeError(f"Missing type annotation for parameter: {param.name}")
		elif typing.get_origin(t) in (typing.Union, types.UnionType):
			t = next((c for c in typing.get_args(t) if isinstance(c, _SupportsFromParam)), t)
		elif typing.get_origin(t) is typing.Annotated:
			if len(t.__metadata__) != 1 or not isinstance(t.__metadata__[0], _SupportsFromParam):
				raise TypeError(f"Expected single annotation of a ctypes type for parameter: {param.name}")
			t = t.__metadata__[0]
		if not isinstance(t, _SupportsFromParam):
			raise TypeError(
				f"Expected a ctypes compatible type for parameter: {param.name}, got {t!r}",
			)
		argtypes.append(t)
		if param.default is inspect.Parameter.empty:
			paramFlags.append((ParamDirectionFlag.IN, param.name))
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
		handledPositions = []
		isAnnotated = typing.get_origin(t) is typing.Annotated and len(t.__metadata__) == 1
		if requireOutParamAnnotations:
			if not isAnnotated or not isinstance(t.__metadata__[0], OutParam):
				raise TypeError(f"Expected single annotation of type 'OutParam' for parameter: {param.name}")
			outParam = t.__metadata__[0]
			if len(argtypes) < outParam.position:
				raise IndexError(
					f"Output parameter {outParam.name} at position {outParam.position} "
					f"exceeds the number of processed input parameters ({len(argtypes)})",
				)
			elif outParam.position in handledPositions:
				raise IndexError(
					f"Output parameter at position {outParam.position} has already been processed",
				)
			handledPositions.append(outParam.position)
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
	funcName: str | None = None,
	restype: typing.Type[ctypes._SimpleCData] = None,
	*,
	cFunctype=ctypes.WINFUNCTYPE,
	annotateOriginalCFunc=True,
	wrapNewCFunc=True,
	errcheck=None,
):
	"""
	Decorator to bind a Python function to a C function from a loaded DLL using ctypes.
	This function creates a decorator that can be applied to a Python function, specifying its argument and return types,
	and optionally wrapping it as a new ctypes function. It also allows for annotating the original C function with
	the correct ctypes metadata and setting custom error checking.
	:param library: The loaded DLL containing the target C function.
	:param funcName: The name of the C function to bind.
	When not provided, the name is fetched from the decorated python function.
	:param restype: The ctypes return type of the C function. Defaults to None.
	:param cFunctype: The ctypes function type constructor (e.g., ctypes.WINFUNCTYPE)
	:param annotateOriginalCFunc: Whether to set ctypes metadata (argtypes, restype) on the original C function.
	:param wrapNewCFunc: Whether to wrap the function as a new ctypes function. If False, returns the original C function wrapped.
	:param errcheck: An optional error checking function to assign to the new ctypes function.
	:returns: A decorator that can be applied to a Python function to bind it to the specified C function.
	"""

	def decorator(pyFunc: types.FunctionType):
		if not isinstance(pyFunc, types.FunctionType):
			raise TypeError(f"Expected a function, got {type(pyFunc)!r}")
		if typing.TYPE_CHECKING:
			# Return early when type checking.
			return pyFunc
		nonlocal restype, funcName
		funcName = funcName or pyFunc.__name__
		cFunc = getattr(library, funcName)
		spec = getFuncSPec(pyFunc, restype)
		# Set ctypes metadata for the original function in case it is called from outside
		if annotateOriginalCFunc:
			if cFunc.argtypes is not None:
				log.warning(
					f"Overriding existing argtypes for {pyFunc!r}: {cFunc.argtypes} -> {spec.argtypes}",
					stack_info=True,
				)
			cFunc.argtypes = spec.argtypes
			if cFunc.restype is not None:
				log.warning(
					f"Overriding existing restype for {pyFunc!r}: {cFunc.restype} -> {spec.restype}",
					stack_info=True,
				)
			cFunc.restype = spec.restype

		wrapper = functools.wraps(pyFunc)
		if not wrapNewCFunc:
			return wrapper(cFunc)
		newCFuncClass = cFunctype(spec.restype, *spec.argtypes)
		newCFunc = newCFuncClass((funcName, library), spec.paramFlags)
		if errcheck:
			newCFunc.errcheck = errcheck
		return wrapper(newCFunc)

	return decorator
