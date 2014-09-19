#touchTracker.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012 NV Access Limited

import time
from collections import OrderedDict

#Possible actions (single trackers)
action_tap="tap"
action_hold="hold"
action_tapAndHold="tapandhold"
action_flickUp="flickup"
action_flickDown="flickdown"
action_flickLeft="flickleft"
action_flickRight="flickright"
action_hoverDown="hoverdown"
action_hover="hover"
action_hoverUp="hoverup"
action_unknown="unknown"
hoverActions=(action_hoverDown,action_hover,action_hoverUp)
#timeout for detection of flicks and plural trackers 
multitouchTimeout=0.25
#The distance a finger must travel to be treeted as a flick
minFlickDistance=50
#How far a finger is allowed to drift purpandicular to a flick direction to make the flick impossible
maxAccidentalDrift=10

actionLabels={
	# Translators: a very quick touch and release of a finger on a touch screen 
	action_tap:pgettext("touch action","tap"),
	# Translators: a very quick touch and release, then another touch with no release, on a touch screen
	action_tapAndHold:pgettext("touch action","tap and hold"),
	# Translators: a touch with no release, on a touch screen. 
	action_hold:pgettext("touch action","hold"),
	# Translators: a quick swipe of a finger in an up direction, on a touch screen. 
	action_flickUp:pgettext("touch action","flick up"),
	# Translators: a quick swipe of a finger in an down direction, on a touch screen. 
	action_flickDown:pgettext("touch action","flick down"),
	# Translators: a quick swipe of a finger in a left direction, on a touch screen. 
	action_flickLeft:pgettext("touch action","flick left"),
	# Translators: a quick swipe of a finger in a right direction, on a touch screen. 
	action_flickRight:pgettext("touch action","flick right"),
	# Translators:  a finger has been held on the touch screen long enough to be considered as hovering
	action_hoverDown:pgettext("touch action","hover down"),
	# Translators: A finger is still touching the touch screen and is moving around with out breaking contact. 
	action_hover:pgettext("touch action","hover"),
	# Translators: a finger that was hovering (touching the touch screen for a long time) has been released 
	action_hoverUp:pgettext("touch action","hover up"),
}

class SingleTouchTracker(object):
	"""
	Represents the lifetime of one single finger while its in contact with the touch device, tracking start and current coordinates, start and end times, and whether its complete (broken contact yet).
	It also calculates what kind of single action (tap, flick, hover) this finger is performing, once it has enough data.
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
		else: #timeout exceeded, must be a kind of hover
			self.action=action_hover

class MultiTouchTracker(object):
	"""Represents an action joinly performed by 1 or more fingers."""

	def __init__(self,action,x,y,startTime,endTime,numFingers,actionCount,numHeldFingers):
		self.action=action
		self.x=x
		self.y=y
		self.startTime=startTime
		self.endTime=endTime
		self.numFingers=numFingers
		self.actionCount=actionCount
		self.numHeldFingers=numHeldFingers

	def __repr__(self):
		return "<MultiTouchTracker {numFingers}finger {action} {actionCount} times at position {x},{y} with {numHeldFingers} extra fingers held>".format(action=self.action,x=self.x,y=self.y,numFingers=self.numFingers,actionCount=self.actionCount,numHeldFingers=self.numHeldFingers)

class TrackerManager(object):
	"""
	Tracks touch input by managing L{SingleTouchTracker} instances and emitting L{MultiTouchTracker} instances representing high-level multiFingered plural trackers.
	"""

	def __init__(self):
		self.singleTouchTrackersByID=OrderedDict()
		self.multiTouchTrackers=[]
		self.numHeldFingers=0

	def update(self,ID,x,y,complete=False):
		"""
		Called to Alert the multiTouch tracker of a new, moved or completed contact (finger touch).
		It creates new single trackers or updates existing ones, and queues/processes multi trackers for later emition.
		""" 
		#See if we know about this finger
		tracker=self.singleTouchTrackersByID.get(ID)
		if not tracker:
			if not complete:
				#This is a new contact (finger) so start tracking it
				self.singleTouchTrackersByID[ID]=SingleTouchTracker(ID,x,y)
			return
		#We already know about this finger
		#Update its position and completion status
		#But also find out its action before and after the update to decide what to do with it
		oldAction=tracker.action
		tracker.update(x,y,complete)
		newAction=tracker.action
		if complete: #This finger has broken contact
			#Forget about this finger
			del self.singleTouchTrackersByID[ID]
			#A completed hover should be a hoverUp
			if newAction==action_hover:
				newAction=action_hoverUp
		#if the action changed and its not unknown, then we will be queuing it
		if newAction!=oldAction and newAction!=action_unknown:
			if newAction==action_hover:
				#New hovers must be queued as hover down
				newAction=action_hoverDown
			#for most  gestures the start coordinates are what we want to emit with trackers 
			#But hovers should always use their current coordinates
			x,y=(tracker.x,tracker.y) if newAction in hoverActions else (tracker.startX,tracker.startY)
			#We keep a count of held fingers as a modification  for gesutres.
			#We must decrement the count before queuing a hover up, but incrementing for hoverDown happens after queuing.
			#Otherwize hoverDowns and hoverUps would accidently get their own heldFinger modifiers.
			if oldAction==action_hover and newAction==action_hoverUp:
				self.numHeldFingers-=1
			#Queue the tracker for processing or emition
			self.addMultiTouchTracker(MultiTouchTracker(newAction,x,y,tracker.startTime,time.time(),1,1,self.numHeldFingers))
			if newAction==action_hoverDown:
				self.numHeldFingers+=1

	def addMultiTouchTracker(self,tracker):
		"""Queues the given tracker, replacing old trackers with a multiFingered plural action where possible"""
		#Reverse iterate through the existing queued trackers comparing the given tracker to each of them
		#as L{emitTrackers} constantly dequeues, the queue only contains trackers newer than multiTouchTimeout, though may contain more if there are still unknown singleTouchTrackers around.
		for index in xrange(len(self.multiTouchTrackers)):
			index=-1-index
			delayedTracker=self.multiTouchTrackers[index]
			#We never want to merge actions if the held fingers modifier has changed at all\
			if tracker.numHeldFingers==delayedTracker.numHeldFingers:
				if tracker.action==delayedTracker.action and delayedTracker.startTime<=tracker.startTime<delayedTracker.endTime and delayedTracker.actionCount==tracker.actionCount==1:
					#The old and new tracker are the same kind of action, they are not themselves plural actions, and their start and end times overlap
					#Therefore they should be treeted as one multiFingered action
					delayedTracker.numFingers+=tracker.numFingers
				elif tracker.action==action_tap==delayedTracker.action and delayedTracker.numFingers==tracker.numFingers:
					#The new and old action are  both tap and have the same number of fingers, but they do not overlap in time
					#Therefore they should be treeted as 1 plural action (e.g. double tap)
					delayedTracker.actionCount+=tracker.actionCount
				elif tracker.action==action_hoverDown and delayedTracker.action==action_tap and tracker.numFingers==delayedTracker.numFingers:
					#A tap and then a hover down is a tapAndHold
					delayedTracker.action=action_tapAndHold
				else: #They don't match, go to the next one
					continue
				#The old tracker's finger count or repete count was affected by the new tracker, therefore
				#Update the old tracker's times to match the new tracker, and remove an requeue the old action for further processing
				#Its necessary to reprocess to catch certain plural trackers (e.g. 1 finger tap turns to 2 finger tap, but later can match a previous 2 finger tap which makes a 2 finger double tap).
				del self.multiTouchTrackers[index]
				delayedTracker.startTime=tracker.startTime
				delayedTracker.endTime=tracker.endTime
				self.addMultiTouchTracker(delayedTracker)
				break
		else: #The new tracker did not affect any old tracker, so really queue it. 
			if tracker.action!=action_hoverDown:
				self.multiTouchTrackers.append(tracker)

	pendingEmitInterval=None #: If set: how long to wait before calling emitTrackers again as trackers are still in the queue 
	def emitTrackers(self):
		"""
		Yields queued trackers that have existed in the queue for long enough to not be connected with other trackers.
		A part from a timeout, trackers are also not emitted if there are other fingers touching that still have an unknown action. 
		If there are no queued trackers to yield but there is a hover tracker, a hover action is yielded instead.
		"""
		self.pendingEmitInterval=None
		t=time.time()
		hasUnknownTrackers=False
		lastHoverTracker=None
		#Check to see if there are any unknown trackers, and also find the most recent hover tracker if any.
		for tracker in self.singleTouchTrackersByID.itervalues():
			if tracker.action==action_hover:
				lastHoverTracker=tracker
			if tracker.action==action_unknown:
				hasUnknownTrackers=True
		foundTrackers=False
		#Only emit trackers if there are not unknown actions
		if not hasUnknownTrackers:
			for tracker in list(self.multiTouchTrackers):
				#All trackers can be emitted with no delay except for tap which must wait for the timeout (to detect plural taps)
				trackerTimeout=(tracker.startTime+multitouchTimeout)-t if tracker.action==action_tap else 0 
				if trackerTimeout<=0: 
					self.multiTouchTrackers.remove(tracker)
					foundTrackers=True
					yield tracker
				else:
					self.pendingEmitInterval=min(self.pendingEmitInterval,trackerTimeout) if self.pendingEmitInterval else trackerTimeout
		#If no tracker could be emitted, at least emit the most recent  hover tracker if there is one
		if not foundTrackers and lastHoverTracker:
			yield MultiTouchTracker(lastHoverTracker.action,lastHoverTracker.x,lastHoverTracker.y,lastHoverTracker.startTime,t,1,1,self.numHeldFingers-1)
