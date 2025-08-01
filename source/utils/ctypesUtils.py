# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025 NV Access Limited, Leonard de Ruijter

"""Utilities to annotate ctypes dll exports."""

import abc
import ctypes
import functools
import inspect
import dataclasses
import types
import typing
from enum import IntEnum
from typing import Annotated, Any, Callable, ParamSpec, TypeVar


from logHandler import log


class ParamDirectionFlag(IntEnum):
	"""Flags to indicate the direction of parameters in ctypes function signatures."""

	IN = 1
	"""Specifies an input parameter to the function."""
	OUT = 2
	"""Output parameter. The foreign function fills in a value."""
	IN_OUT = IN
	"""
	Synonym to IN.
	Note that ctypes also supports a value of IN | OUT.
	However, marking a parameter as such makes no sense, as it must be provided as input parameter but is also returned as output parameter.
	In other words, it would behave like this:
		def func(in): return in
	Therefore, such parameters can simply be treated as input parameters.
	ctypes will still be able to fill in values in these parameters.
	This synonym is therefore only meant for convenience, to make it clear that the parameter is both an input and output parameter.
	"""


class CType(abc.ABC):
	"""Abstract class for ctypes types.
	This class is used to validate type annotations for ctypes functions.
	"""

	def __new__(cls, *args, **kwargs):
		raise TypeError(
			f"{cls.__name__} may not be instantiated. "
			"It is only used as an abstract class to annotate ctypes objects or parameters.",
		)


# Hacky, but there's no other way to get to the base class for ctypes types.
CType.register(ctypes.c_int.__mro__[-2])

if typing.TYPE_CHECKING:
	from ctypes import _Pointer as Pointer
else:

	class Pointer(CType):
		"""A pointer type that can be used as a type annotation for ctypes functions."""

		@classmethod
		def __class_getitem__(cls, t: type) -> type:
			return ctypes.POINTER(t)

	# Register known pointer types
	for t in (ctypes._Pointer, ctypes._CFuncPtr, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_wchar_p):
		Pointer.register(t)


@dataclasses.dataclass
class OutParam:
	"""Annotation for output parameters in function signatures.
	This is used to specify that a parameter is an output parameter, which will be filled by the wrapped foreign function."""

	name: str
	"""The name of the output parameter."""
	position: int = 0
	"""The position of the output parameter in argtypes."""
	type: Pointer | inspect.Parameter.empty = inspect.Parameter.empty
	"""The type of the output parameter. This should be a pointer type.
	If ``inspect.Parameter.empty`` (default), the type from the annotation is used and a pointer type is created from it automatically."""
	default: CType | inspect.Parameter.empty = inspect.Parameter.empty
	"""The default value for the output parameter."""


ErrcheckType = Callable[[Any, ctypes._CFuncPtr, tuple[Any, ...]], Any]


def windowsErrCheckdef(result: int, func: ctypes._CFuncPtr, args: tuple[Any, ...]) -> Any:
	"""
	Checks the result of a Windows API call and raises a WinError if the result indicates failure.
	This function can be used as an error checking callback
	for ctypes functions that call Windows API functions that return zero on failure, usually ``ctypes.wintypes.BOOL``.
	:param result: The result returned by the Windows API function.
	:param func: The ctypes function pointer that was called.
	:param args: The arguments passed to the function.
	:raises WinError: If the result is 0, indicating an error.
	:returns: The arguments passed to the function.
	"""

	if result == 0:
		raise ctypes.WinError()
	return args


_pyfuncParams = ParamSpec("_pyfuncParams")
_pyfuncReturn = TypeVar("_pyfuncReturn")


@dataclasses.dataclass
class FuncSpec(typing.Generic[_pyfuncParams, _pyfuncReturn]):
	"""Specification of a ctypes function."""

	restype: type[CType] | None
	argtypes: tuple[CType]
	paramFlags: tuple[
		tuple[ParamDirectionFlag, str] | tuple[ParamDirectionFlag, str, int | ctypes._SimpleCData]
	]


def getFuncSpec(
	pyFunc: Callable[_pyfuncParams, _pyfuncReturn],
	restype: type[CType] | None | inspect.Parameter.empty = inspect.Parameter.empty,
) -> FuncSpec[_pyfuncParams, _pyfuncReturn]:
	"""
	Generates a function specification (`FuncSpec`) to generate a ctypes foreign function wrapper.

	This function inspects the signature and type annotations of the given Python function to determine the argument types,
	parameter flags (input/output), and return type(s) for use with ctypes. It enforces that all parameters and the return
	type are properly annotated with ctypes-compatible types, and supports handling of output parameters via ``Annotated`` types.

	:param pyFunc: The Python function to inspect. Must have type annotations for all parameters and the return type.
	:param restype: Optional explicit ctypes return type. Required if the function has output parameters.

	:raises TypeError: If parameter kinds are unsupported, type annotations are missing or invalid, or output parameter annotations are incorrect.
	:raises IndexError: If output parameter positions are invalid or duplicated.

	:returns: A :class:`FuncSpec` object containing the ctypes-compatible function specification.
	"""
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
			t = next((c for c in typing.get_args(t) if issubclass(c, CType)), t)
		elif typing.get_origin(t) is Annotated:
			if len(t.__metadata__) != 1 or not issubclass(t.__metadata__[0], CType):
				raise TypeError(f"Expected single annotation of a ctypes type for parameter: {param.name}")
			t = t.__metadata__[0]
		if not issubclass(t, CType):
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
		if restype is inspect.Parameter.empty:
			raise TypeError("restype should be provided when using a tuple for return type")
		requireOutParamAnnotations = True
		restypes = list(expectedRestype)
	else:
		requireOutParamAnnotations = restype is not inspect.Parameter.empty
		restypes = [expectedRestype]
	for i, t in enumerate(restypes):
		handledPositions = []
		isAnnotated = typing.get_origin(t) is Annotated and len(t.__metadata__) == 1
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
			if outParam.type is inspect.Parameter.empty:
				outParam.type = (
					t.__origin__ if isinstance(t.__origin__, ctypes.Array) else ctypes.POINTER(t.__origin__)
				)
			handledPositions.append(outParam.position)
			argtypes.insert(outParam.position, outParam.type)
			if outParam.default is inspect.Parameter.empty:
				paramFlags.insert(outParam.position, (ParamDirectionFlag.OUT, outParam.name))
			else:
				paramFlags.insert(
					outParam.position,
					(ParamDirectionFlag.OUT, outParam.name, outParam.default),
				)
		elif isAnnotated:
			annotation = t.__metadata__[0]
			if not issubclass(annotation, CType):
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
	restype: type[CType] | None | inspect.Parameter.empty = inspect.Parameter.empty,
	*,
	cFunctype: Callable = ctypes.WINFUNCTYPE,
	annotateOriginalCFunc: bool = False,
	wrapNewCFunc: bool = True,
	errcheck: ErrcheckType | None = None,
) -> Callable[[Callable[_pyfuncParams, _pyfuncReturn]], Callable[_pyfuncParams, _pyfuncReturn]]:
	"""
	Decorator to bind a Python function to a C function from a DLL using ctypes,
	automatically setting argument and return types based on the Python function's signature.

	This decorator simplifies the process of wrapping C functions from a DLL,
	by inferring argument and return types from the Python function and applying them to the C function pointer.

	:param library: The ctypes.CDLL instance representing the loaded DLL.
	:param funcName: The name of the function in the DLL. If None, uses the Python function's name.
	:param restype: Optional explicit ctypes return type. Required if the function has output parameters.
	:param cFunctype: The ctypes function type to use (e.g., ctypes.WINFUNCTYPE or ctypes.CFUNCTYPE).
	:param annotateOriginalCFunc: Whether to annotate the original C function with argtypes/restype.
	:param wrapNewCFunc: Whether to return a new ctypes function pointer or the original.
	:param errcheck: Optional error checking function to attach to the ctypes function.
		this parameter only applies when `wrapNewCFunc` is True.

	:raises TypeError: If the decorated object is not a function, if parameter kinds are unsupported, type annotations are missing or invalid, or output parameter annotations are incorrect.
	:raises IndexError: If output parameter positions are invalid or duplicated.
	:raises ValueError: If neither `annotateOriginalCFunc` nor `wrapNewCFunc` is True.

	:returns: The decorated function, now bound to the C function from the DLL.

	:example:


		user32 = ctypes.windll.user32

		@dllFunc(user32, restype=ctypes.c_bool, errcheck=windowsErrCheck)
		def GetClientRect(
			hWnd: int | HWND,
		) -> Annotated[RECT, OutParam(Pointer[RECT], "lpRect", 1)]: ...
			'''Wraps the GetClientRect function from user32.dll.
			:param hWnd: Handle to the window.
			:return: A RECT structure that contains the coordinates of the client area.
			:raise WindowsError: If the function fails, an exception is raised with the error'''
			pass

	"""

	def decorator(pyFunc: Callable[_pyfuncParams, _pyfuncReturn]) -> Callable[_pyfuncParams, _pyfuncReturn]:
		if not isinstance(pyFunc, types.FunctionType):
			raise TypeError(f"Expected a function, got {type(pyFunc)!r}")
		if not annotateOriginalCFunc and not wrapNewCFunc:
			raise ValueError(
				"At least one of annotateOriginalCFunc or wrapNewCFunc must be True.",
			)
		if typing.TYPE_CHECKING:
			# Return early when type checking.
			return pyFunc
		nonlocal restype, funcName
		funcName = funcName or pyFunc.__name__
		cFunc = getattr(library, funcName)
		spec = getFuncSpec(pyFunc, restype)
		# Set ctypes metadata for the original function in case it is called from outside
		if annotateOriginalCFunc:
			if cFunc.argtypes != spec.argtypes:
				log.warning(
					f"Overriding existing argtypes for {pyFunc!r}: {cFunc.argtypes} -> {spec.argtypes}",
					stack_info=True,
				)
			cFunc.argtypes = spec.argtypes
			if cFunc.restype != spec.restype:
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
