# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt


"""Base classes for NVDA Bridge components."""


class Proxy:
	"""Proxy for wrapping remote rpyc services.
	All NVDA Bridge proxies should inherit from this class.

	This class stores a reference to a remote rpyc service and provides a
	helper method to create a subclass with the remote service bound.

	:ivar _remoteService: The remote rpyc service instance associated with this proxy.
	"""

	_remoteService = None

	@classmethod
	def _createBoundProxyClass(cls, remoteService):
		"""Create a subclass of this proxy class with the remote service bound.
		This causes the existing constructor to be called with the remote service as the first argument.
		This should be used when injecting a proxy into existing NvDA components.
		E.g. `nvwave.WavePlayer = WavePlayerProxy._createBoundProxyClass(remoteService.WavePlayer)`
		So then `nvwave.WavePlayer` is instantiated as normal, but the remote service is passed in automatically.

		:param remoteService: The remote rpyc service instance to bind.
		:return: A subclass of this proxy class with the remote service bound.
		"""
		class BoundProxyClass(cls):
			def __init__(self, *args, **kwargs):
				super().__init__(remoteService, *args, **kwargs)
		BoundProxyClass.__name__ = cls.__name__
		return BoundProxyClass

	def __init__(self, remoteService):
		self._remoteService = remoteService
