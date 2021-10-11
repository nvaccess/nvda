import api
import tones
import controlTypes
import textInfos
import locationHelper
import speech

class ScreenExplorer(object):

	updateReview=False

	def __init__(self):
		self._obj=None
		self._pos=None

	def moveTo(self,x,y,new=False,unit=textInfos.UNIT_LINE):
		obj=api.getDesktopObject().objectFromPoint(x,y)
		prevObj=None
		while obj  and obj.beTransparentToMouse:
			prevObj=obj
			obj=obj.parent
		if not obj or (obj.presentationType!=obj.presType_content and obj.role!=controlTypes.Role.PARAGRAPH):
			obj=prevObj
		if not obj:
			return
		hasNewObj=False
		if obj!=self._obj:
			self._obj=obj
			hasNewObj=True
			if self.updateReview:
				api.setNavigatorObject(obj)
		else:
			obj=self._obj
		pos=None
		if obj.treeInterceptor:
			try:
				pos=obj.treeInterceptor.makeTextInfo(obj)
			except LookupError:
				pos=None
			if pos:
				obj=obj.treeInterceptor.rootNVDAObject
				if hasNewObj and self._obj and obj.treeInterceptor is self._obj.treeInterceptor:
					hasNewObj=False 
		if not pos:
			try:
				pos=obj.makeTextInfo(locationHelper.Point(x,y))
			except (NotImplementedError,LookupError):
				pass
			if pos: pos.expand(unit)
		if pos and self.updateReview:
			api.setReviewPosition(pos)
		speechCanceled=False
		if hasNewObj:
			speech.cancelSpeech()
			speechCanceled=True
			speech.speakObject(obj)
		if pos  and (new or not self._pos or pos.__class__!=self._pos.__class__ or pos.compareEndPoints(self._pos,"startToStart")!=0 or pos.compareEndPoints(self._pos,"endToEnd")!=0):
				self._pos=pos
				if not speechCanceled:
					speech.cancelSpeech()
				speech.speakTextInfo(pos, reason=controlTypes.OutputReason.CARET)
