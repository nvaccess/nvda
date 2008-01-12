from .IAccessible import IAccessible

class Gecko(IAccessible):
	pass

	def isAlive(self):
		if super(Gecko,self).isAlive() and controlTypes.STATE_READONLY in self.rootNVDAObject.states:
			return True
		else:
			return False
