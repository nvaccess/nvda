from . import TestCase

class TestCase(TestCase):

	def test_foo(self):
		self.keyCommand("NVDA+c")
		self.expectPresentation([r"Speaking [u'asdf']"])
