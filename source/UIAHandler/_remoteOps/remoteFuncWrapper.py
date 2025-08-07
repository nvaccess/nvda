# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-2024 NV Access Limited


from __future__ import annotations
from typing import (
	Generator,
	ContextManager,
	Callable,
	Concatenate,
	ParamSpec,
	TypeVar,
)
import functools
import contextlib
from . import builder


_remoteFunc_self = TypeVar("_remoteFunc_self", bound=builder._RemoteBase)
_remoteFunc_paramSpec = ParamSpec("_remoteFunc_paramSpec")
_remoteFunc_return = TypeVar("_remoteFunc_return")


class _BaseRemoteFuncWrapper:
	def generateArgsKwargsString(self, *args, **kwargs) -> str:
		argsString = ", ".join(map(repr, args))
		kwargsString = ", ".join(f"{key}={repr(val)}" for key, val in kwargs.items())
		return f"({', '.join([argsString, kwargsString])})"

	def _execRawFunc(
		self,
		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return],
		funcSelf: _remoteFunc_self,
		*args: _remoteFunc_paramSpec.args,
		**kwargs: _remoteFunc_paramSpec.kwargs,
	) -> _remoteFunc_return:
		main = funcSelf.rob.getInstructionList("main")
		main.addComment(
			f"Entering {func.__qualname__}{self.generateArgsKwargsString(*args, **kwargs)}",
		)
		res = func(funcSelf, *args, **kwargs)
		main.addComment(f"Exiting {func.__qualname__}")
		return res

	def __call__(
		self,
		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return],
	) -> Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return]:
		@functools.wraps(func)
		def wrapper(
			funcSelf: _remoteFunc_self,
			*args: _remoteFunc_paramSpec.args,
			**kwargs: _remoteFunc_paramSpec.kwargs,
		) -> _remoteFunc_return:
			return self._execRawFunc(func, funcSelf, *args, **kwargs)

		return wrapper


class RemoteMethodWrapper(_BaseRemoteFuncWrapper):
	_mutable: bool

	def __init__(self, mutable: bool = False):
		self._mutable = mutable

	def _execRawFunc(
		self,
		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return],
		funcSelf: _remoteFunc_self,
		*args: _remoteFunc_paramSpec.args,
		**kwargs: _remoteFunc_paramSpec.kwargs,
	) -> _remoteFunc_return:
		if self._mutable and not funcSelf._mutable:
			raise RuntimeError(f"{funcSelf.__class__.__name__} is not mutable")
		return super()._execRawFunc(func, funcSelf, *args, **kwargs)


class RemoteContextManager(_BaseRemoteFuncWrapper):
	def __call__(
		self,
		func: Callable[
			Concatenate[_remoteFunc_self, _remoteFunc_paramSpec],
			Generator[_remoteFunc_return, None, None],
		],
	) -> Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], ContextManager[_remoteFunc_return]]:
		contextFunc = contextlib.contextmanager(func)
		return super().__call__(contextFunc)

	@contextlib.contextmanager
	def _execRawFunc(
		self,
		func: Callable[
			Concatenate[_remoteFunc_self, _remoteFunc_paramSpec],
			ContextManager[_remoteFunc_return],
		],
		funcSelf: _remoteFunc_self,
		*args: _remoteFunc_paramSpec.args,
		**kwargs: _remoteFunc_paramSpec.kwargs,
	) -> Generator[_remoteFunc_return, None, None]:
		main = funcSelf.rob.getInstructionList("main")
		main.addComment(
			f"Entering context manager {func.__qualname__}{self.generateArgsKwargsString(*args, **kwargs)}",
		)
		with func(funcSelf, *args, **kwargs) as val:
			main.addComment("Yielding to outer scope")
			yield val
			main.addComment(f"Reentering context manager {func.__qualname__}")
		funcSelf.rob.getInstructionList("main").addComment(f"Exiting context manager {func.__qualname__}")


remoteFunc = _BaseRemoteFuncWrapper()
remoteMethod = RemoteMethodWrapper()
remoteMethod_mutable = RemoteMethodWrapper(mutable=True)
remoteContextManager = RemoteContextManager()
