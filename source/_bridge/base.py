import rpyc


class Service(rpyc.Service):
	pass


class Proxy:
	_remoteService = None

	@classmethod
	def _createBoundProxyClass(cls, remoteService):
		class BoundProxyClass(cls):
			def __init__(self, *args, **kwargs):
				super().__init__(remoteService, *args, **kwargs)
		BoundProxyClass.__name__ = cls.__name__
		return BoundProxyClass

	def __init__(self, remoteService):
		self._remoteService = remoteService
