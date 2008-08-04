import controlTypes
import api
import speech
from . import IAccessible

class IMECandidate(IAccessible):

	def _handleNewCandidate(self):
		oldNav=api.getNavigatorObject()
		if oldNav.windowClassName!=self.windowClassName:
			speech.speakObjectProperties(self.parent,name=True)
		api.setNavigatorObject(self)
		speech.speakMessage(str(self.event_objectID))
		speech.speakObjectProperties(self,name=True)

	def event_nameChange(self):
		if self.event_objectID>=1 and self.event_objectID<=9:
			self._handleNewCandidate()

	def event_stateChange(self):
		if self.event_objectID>=1 and self.event_objectID<=9:
			self._handleNewCandidate()
