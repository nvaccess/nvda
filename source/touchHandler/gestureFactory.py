import time
import inputCore
import speech

#Possible actions (single gestures)
action_tap="tap"
action_flickUp="flickup"
action_flickDown="flickdown"
action_flickLeft="flickleft"
action_flickRight="flickright"
action_hover="hover"
action_hoverUp="hoverup"
action_unknown="unknown"
# actions that are treeted as one plural action when the same one is performed multiple times in quick succession (e.g. double tap)
pluralActions=(action_tap,action_flickLeft,action_flickRight,action_flickUp,action_flickDown)
#timeout for detection of flicks and plural actions 
multitouchTimeout=0.3
#The distance a finger must travel to be treeted as a flick
minFlickDistance=50
#How far a finger is allowed to drift purpandicular to a flick direction to make the flick impossible
maxAccidentalDrift=10

class SingleTouchTracker(object):
	"""
	Represents the lifetime of one single finger while its in contact with the touch device, tracking start and current coordinates, start and end times, and whether its complete (broken contact yet).
	It also calculates what kind of single gesture (tap, flick, hover) this finger is performing, once it has enough data.
	"""

	def __init__(self,ID,x,y):
		self.ID=ID
		self.x=self.startX=x
		self.y=self.startY=y
		self.startTime=time.time()
		self.maxAbsDeltaX=0
		self.maxAbsDeltaY=0
		self.action=action_unknown

	def update(self,x,y,complete=False):
		"""Called to alert this single tracker that the finger has moved or broken contact."""
		self.x=x
		self.y=y
		deltaX=x-self.startX
		deltaY=y-self.startY
		absDeltaX=abs(deltaX)
		absDeltaY=abs(deltaY)
		self.maxAbsDeltaX=max(absDeltaX,self.maxAbsDeltaX)
		self.maxAbsDeltaY=max(absDeltaY,self.maxAbsDeltaY)
		deltaTime=time.time()-self.startTime
		if deltaTime<multitouchTimeout: #not timed out yet
			if complete and self.maxAbsDeltaX<maxAccidentalDrift and self.maxAbsDeltaY<maxAccidentalDrift:
				#The completed quick touch never drifted too far from its initial contact point therefore its a tap
				self.action=action_tap
			elif complete and self.maxAbsDeltaX>=minFlickDistance and self.maxAbsDeltaX>self.maxAbsDeltaY:
				#The completed quick touch traveled far enough horizontally to be a flick and was also not off by more than 45 degrees. 
				if deltaX>0: #Traveling to the right
					self.action=action_flickRight
				else: #traveling to the left
					self.action=action_flickLeft
			elif complete and self.maxAbsDeltaY>=minFlickDistance and self.maxAbsDeltaY>self.maxAbsDeltaX:
				#The completed quick touch traveled far enough vertically to be a flick and was also not off by more than 45 degrees. 
				if deltaY>0: #traveling down
					self.action=action_flickDown
				else: #traveling up
					self.action=action_flickUp
		else: #The tuch is long enough to be a hover
			self.action=action_hover


class TouchInputGesture(inputCore.InputGesture):

	counterNames=["single","double","tripple","quodruple"]

	def _get_speechEffectWhenExecuted(self):
		if self.action in (action_hover,action_hoverUp): return None
		return super(TouchInputGesture,self).speechEffectWhenExecuted

	def __init__(self,action,x,y,startTime,endTime,numFingers,actionCount):
		super(TouchInputGesture,self).__init__()
		self.action=action
		self.x=x
		self.y=y
		self.startTime=startTime
		self.endTime=endTime
		self.numFingers=numFingers
		self.actionCount=actionCount

	def _get_identifiers(self):
		ID="ts:"
		if self.numFingers>1:
			ID+="%dfinger_"%self.numFingers
		if self.actionCount>1:
			ID+="%s_"%self.counterNames[min(self.actionCount,4)-1]
		ID+=self.action
		return [ID]

	def _get_displayName(self):
		return self.identifiers[0]

class TouchGestureFactory(object):
	"""
	Tracks touch input by managing L{SingleTouchTracker} instances and emitting L{TouchInputGesture} instances representing high-level multiFingered plural actions.
	"""

	def __init__(self):
		self.liveTrackersByID={}
		self.hoverTracker=None
		self.multitouchGestures=[]

	def update(self,ID,x,y,complete=False):
		"""
		Called to Alert the multiTouch tracker of a new, moved or completed contact (finger touch).
		It creates new single trackers or updates existing ones, and queues/processes gestures for later emition.
		""" 
		#See if we know about this finger
		tracker=self.liveTrackersByID.get(ID)
		if not tracker:
			if not complete:
				#This is a new contact (finger) so start tracking it
				self.liveTrackersByID[ID]=SingleTouchTracker(ID,x,y)
			return
		#We already know about this finger
		#Update its position and completion status
		tracker.update(x,y,complete)
		if not complete:
			if tracker.action==action_hover and not self.hoverTracker:
				#This finger seems to be hovering and we're not aware of any others right now,
				#So make this the special hover tracker (handles split taps etc)
				self.hoverTracker=tracker
		else: #This finger has broken contact
			#Forget about this finger
			del self.liveTrackersByID[ID]
			if tracker is self.hoverTracker:
				#Its no longer the hover tracker because it broke contact
				self.hoverTracker=None
				#Though queue a hoverUp gesture
				gesture=TouchInputGesture(action_hoverUp,tracker.x,tracker.y,tracker.startTime,time.time(),1,1)
				self.addGesture(gesture)
			elif tracker.action in pluralActions:
				#This finger performed a well-known completed action so queue an appropriate gesture
				gesture=TouchInputGesture(tracker.action,tracker.x,tracker.y,tracker.startTime,time.time(),1,1)
				self.addGesture(gesture)

	def addGesture(self,gesture):
		"""Queues the given gesture, replacing old gestures with a multiFingered plural gesture where possible"""
		#Reverse iterate through the existing queued gestures comparing the given gesture to each of them
		#as L{emitGestures} constantly dequeues, the queue only contains gestures newer than multiTouchTimeout
		for index in xrange(len(self.multitouchGestures)):
			index=-1-index
			delayedGesture=self.multitouchGestures[index]
			if gesture.action==delayedGesture.action:
				if delayedGesture.startTime<=gesture.startTime<delayedGesture.endTime and delayedGesture.actionCount==gesture.actionCount==1:
					#The old and new gesture are the same kind of action, they are not themselves plural actions, and their start and end times overlap
					#Therefore they should be treeted as one multiFingered gesture
					delayedGesture.numFingers+=gesture.numFingers
				elif delayedGesture.numFingers==gesture.numFingers:
					#The new and old gesture are the same type of action and have the same number of fingers, but they do not overlap in time
					#Therefore they should be treeted as 1 plural gesture (e.g. double tap)
					delayedGesture.actionCount+=gesture.actionCount
				else: #They don't match, go to the next one
					continue
				#The old gesture's finger count or repete count was affected by the new gesture, therefore
				#Update the old gesture's times to match the new gesture, and remove an requeue the old gesture for further processing
				#Its necessary to reprocess to catch certain plural actions (e.g. 1 finger tap turns to 2 finger tap, but later can match a previous 2 finger tap which makes a 2 finger double tap).
				del self.multitouchGestures[index]
				delayedGesture.startTime=gesture.startTime
				delayedGesture.endTime=gesture.endTime
				self.addGesture(delayedGesture)
				break
		else: #The new gesture did not affect any old gesture, so really queue it. 
			self.multitouchGestures.append(gesture)

	def emitGestures(self):
		"""
		Yields queued gestures that have existed in the queue for long enough to not be connected with other gestures.
		If there is a hover being tracked, each yielded gesture's action count (plurality) goes up by one and its coordinates are changed to match the hover coordinates.
		e.g. hover plus a tap becomes a double tap at the hover point.
		If there are no queued gestures to yield but there is a hover tracker, a hover gesture is yielded instead.
		"""
		t=time.time()
		foundGestures=False
		for gesture in list(self.multitouchGestures):
			if (gesture.startTime+multitouchTimeout)<=t:
				self.multitouchGestures.remove(gesture)
				if self.hoverTracker:
					gesture.actionCount+=1
					gesture.x=self.hoverTracker.x
					gesture.y=self.hoverTracker.y
					self.hoverTracker=None
				foundGestures=True
				yield gesture
		if not foundGestures and self.hoverTracker:
			tracker=self.hoverTracker
			yield TouchInputGesture(tracker.action,tracker.x,tracker.y,tracker.startTime,time.time(),1,1)
