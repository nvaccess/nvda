from . import IAccessible

class Document(IAccessible):

	def _get_virtualBufferClass(self):
		from virtualBuffers.msaaTest import MSAATest
		return MSAATest
