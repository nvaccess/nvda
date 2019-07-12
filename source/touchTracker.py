#touchTracker.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012 NV Access Limited

import threading
import time
from collections import OrderedDict
from logHandler import log

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
	@ivar ID: the ID this finger has been assigned by the Operating System.
	@type ID: int
	@ivar x: The last known x screen coordinate of this finger
	@type x: int
	@ivar y: The last known y screen coordinate of this finger
	@type y: int
	@ivar startX: The x screen coordinate  where the finger first made contact
	@type startX: int
	@ivar startY: The y screen coordinate  where the finger first made contact
	@type startY: int
	@ivar startTime: the time at which the finger first made contact
	@type startTime: float
	@ivar endTime: the time at which the finger broke contact. Before breaking contact the value is -1
	@type endTime: float
	@ivar maxAbsDeltaX: the maximum distance this finger has traveled on the x access while making contact
	@type maxAbsDeltaX: int
	@ivar maxAbsDeltaY: the maximum distance this finger has traveled on the y access while making contact
	@type maxAbsDeltaY: int
	@ivar action: the action this finger has performed (one of the action_* constants,E.g. tap, flickRight, hover etc). If not enough data has been collected yet the action will be unknown. 
	@type action: string
	@ivar complete: If true then this finger has broken contact
	@type complete: bool
	"""
	__slots__=['ID','x','y','startX','startY','startTime','endTime','maxAbsDeltaX','maxAbsDeltaY','action','complete']

	def __init__(self,ID,x,y):
		self.ID=ID
		self.x=self.startX=x
		self.y=self.startY=y
		self.startTime=time.time()
		self.endTime=-1
		self.maxAbsDeltaX=0
		self.maxAbsDeltaY=0
		self.action=action_unknown
		self.complete=False

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
		curTime=time.time()
		deltaTime=curTime-self.startTime
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
		self.complete=complete
		if complete:
			self.endTime=curTime

class MultiTouchTracker(object):
	"""Represents an action jointly performed by 1 or more fingers.
	@ivar action: the action this finger has performed (one of the action_* constants,E.g. tap, flickRight, hover etc).
	@type action: string
	@ivar x: the x screen coordinate where the action was performed. For multi-finger actions it is the average position of each of the fingers. For plural actions it is based on the first occurence
	@type x: int
	@ivar y: the y screen coordinate where the action was performed. For multi-finger actions it is the average position of each of the fingers. For plural actions it is based on the first occurence
	@type y: int
	@ivar startTime: the time the action began
	@type startTime: float
	@ivar endTime: the time the action was complete 
	@type endTime: float
	@ivar numFingers: the number of fingers that performed this action
	@type numFingers: int
	@ivar actionCount: the number of times this action was performed in quick succession (E.g. 2 for a double tap)
	@ivar childTrackers: a list of L{MultiTouchTracker} objects which represent the direct sub-actions of this action. E.g. a 2-finger tripple tap's childTrackers will contain 3 2-finger taps. Each of the 2-finger taps' childTrackers will contain 2 taps.
	@type childTrackers: list of L{MultiTouchTracker} objeccts
	@ivar rawSingleTouchTracker: if this tracker represents a 1-fingered non-plural action then this will be the L{SingleTouchTracker} object for that 1 finger. If not then it is None.
	@type rawSingleTouchTracker: L{SingleTouchTracker}
	@ivar pluralTimeout: the time at which this tracker could no longer possibly be merged with another to be pluralized, thus it is aloud to be emitted
	@type pluralTimeout: float
	"""
	__slots__=['action','x','y','startTime','endTime','numFingers','actionCount','childTrackers','rawSingleTouchTracker','pluralTimeout']

	def __init__(self,action,x,y,startTime,endTime,numFingers=1,actionCount=1,rawSingleTouchTracker=None,pluralTimeout=None):
		self.action=action
		self.x=x
		self.y=y
		self.startTime=startTime
		self.endTime=endTime
		self.numFingers=numFingers
		self.actionCount=actionCount
		self.childTrackers=[]
		self.rawSingleTouchTracker=rawSingleTouchTracker
		# We only allow pluralizing of taps, no other action.
		if pluralTimeout is None and action==action_tap:
			pluralTimeout=startTime+multitouchTimeout
		self.pluralTimeout=pluralTimeout

	def iterAllRawSingleTouchTrackers(self):
		if self.rawSingleTouchTracker: yield self.rawSingleTouchTracker
		for child in self.childTrackers:
			for i in child.iterAllRawSingleTouchTrackers():
				yield i

	def __repr__(self):
		return "<MultiTouchTracker {numFingers}finger {action} {actionCount} times at position {x},{y}>".format(action=self.action,x=self.x,y=self.y,numFingers=self.numFingers,actionCount=self.actionCount)

	def getDevInfoString(self):
		msg="%s\n"%self
		if self.childTrackers:
			msg+="--- made of ---\n"
			for t in self.childTrackers:
				msg+=t.getDevInfoString()
			msg+="--- end ---\n"
		return msg

class TrackerManager(object):
	"""
	Tracks touch input by managing L{SingleTouchTracker} instances and emitting L{MultiTouchTracker} instances representing high-level multiFingered plural trackers.
	"""

	def __init__(self):
		self.singleTouchTrackersByID=OrderedDict()
		self.multiTouchTrackers=[]
		self.curHoverStack=[]
		self.numUnknownTrackers=0
		self._lock=threading.Lock()

	def makePreheldTrackerFromSingleTouchTrackers(self,trackers):
		childTrackers=[MultiTouchTracker(action_hold,tracker.x,tracker.y,tracker.startTime,time.time()) for tracker in trackers if tracker.action==action_hover]
		numFingers=len(childTrackers)
		if numFingers==0: return
		if numFingers==1: return childTrackers[0]
		avgX: int = sum(t.x for t in childTrackers) // numFingers
		avgY: int = sum(t.y for t in childTrackers) // numFingers
		tracker=MultiTouchTracker(action_hold,avgX,avgY,childTrackers[0].startTime,time.time(),numFingers)
		tracker.childTrackers=childTrackers
		return tracker

	def makePreheldTrackerForTracker(self,tracker):
		curHoverSet={x for x in self.singleTouchTrackersByID.values() if x.action==action_hover}
		excludeHoverSet={x for x in tracker.iterAllRawSingleTouchTrackers() if x.action==action_hover}
		return self.makePreheldTrackerFromSingleTouchTrackers(curHoverSet-excludeHoverSet)

	def update(self,ID,x,y,complete=False):
		"""
		Called to Alert the multiTouch tracker of a new, moved or completed contact (finger touch).
		It creates new single trackers or updates existing ones, and queues/processes multi trackers for later emition.
		""" 
		with self._lock:
			#See if we know about this finger
			tracker=self.singleTouchTrackersByID.get(ID)
			if not tracker:
				if not complete:
					#This is a new contact (finger) so start tracking it
					self.singleTouchTrackersByID[ID]=SingleTouchTracker(ID,x,y)
					self.numUnknownTrackers+=1
				return
			#We already know about this finger
			#Update its position and completion status
			#But also find out its action before and after the update to decide what to do with it
			oldAction=tracker.action
			tracker.update(x,y,complete)
			newAction=tracker.action
			if (oldAction==action_unknown and newAction!=action_unknown):
				self.numUnknownTrackers-=1
			if complete: #This finger has broken contact
				#Forget about this finger
				del self.singleTouchTrackersByID[ID]
				if tracker.action==action_unknown:
					self.numUnknownTrackers-=1
			#if the action changed and its not unknown, then we will be queuing it
			if newAction!=oldAction and newAction!=action_unknown:
				if newAction==action_hover:
					#New hovers must be queued as holds 
					newAction=action_hold
				#for most  gestures the start coordinates are what we want to emit with trackers 
				#But hovers should always use their current coordinates
				x,y=(tracker.x,tracker.y) if newAction in hoverActions else (tracker.startX,tracker.startY)
				#Queue the tracker for processing or emition
				self.processAndQueueMultiTouchTracker(MultiTouchTracker(newAction,x,y,tracker.startTime,time.time(),rawSingleTouchTracker=tracker))

	def makeMergedTrackerIfPossible(self,oldTracker,newTracker):
		if newTracker.action==oldTracker.action and  newTracker.startTime<oldTracker.endTime and oldTracker.startTime<newTracker.endTime and oldTracker.actionCount==newTracker.actionCount==1:
			#The old and new tracker are the same kind of action, they are not themselves plural actions, and their start and end times overlap
			#Therefore they should be treeted as one multiFingered action
			childTrackers=[]
			childTrackers.extend(oldTracker.childTrackers) if oldTracker.numFingers>1 else childTrackers.append(oldTracker)
			childTrackers.extend(newTracker.childTrackers) if newTracker.numFingers>1 else childTrackers.append(newTracker)
			numFingers=oldTracker.numFingers+newTracker.numFingers
			avgX: int =sum(t.x for t in childTrackers) // numFingers
			avgY: int = sum(t.y for t in childTrackers) // numFingers
			mergedTracker=MultiTouchTracker(newTracker.action,avgX,avgY,oldTracker.startTime,newTracker.endTime,numFingers,newTracker.actionCount,pluralTimeout=newTracker.pluralTimeout)
			mergedTracker.childTrackers=childTrackers
		elif self.numUnknownTrackers==0 and newTracker.pluralTimeout is not None and newTracker.startTime>=oldTracker.endTime and newTracker.startTime<oldTracker.pluralTimeout and newTracker.action==oldTracker.action and oldTracker.numFingers==newTracker.numFingers:
			#The new and old action are   the same and allow pluralising and have the same number of fingers and there are no other unknown trackers left and they do not overlap in time
			#Therefore they should be treeted as 1 plural action (e.g. double tap)
			mergedTracker=MultiTouchTracker(newTracker.action,oldTracker.x,oldTracker.y,oldTracker.startTime,newTracker.endTime,newTracker.numFingers,oldTracker.actionCount+newTracker.actionCount,pluralTimeout=newTracker.pluralTimeout)
			mergedTracker.childTrackers.extend(oldTracker.childTrackers) if oldTracker.actionCount>1 else mergedTracker.childTrackers.append(oldTracker)
			mergedTracker.childTrackers.extend(newTracker.childTrackers) if newTracker.actionCount>1 else mergedTracker.childTrackers.append(newTracker)
		elif self.numUnknownTrackers==0 and newTracker.action==action_hold and oldTracker.action==action_tap and newTracker.numFingers==oldTracker.numFingers and newTracker.startTime>oldTracker.endTime:
			#A tap and then a hover down  is a tapAndHold
			mergedTracker=MultiTouchTracker(action_tapAndHold,oldTracker.x,oldTracker.y,oldTracker.startTime,newTracker.endTime,newTracker.numFingers,oldTracker.actionCount,pluralTimeout=newTracker.pluralTimeout)
			mergedTracker.childTrackers.append(oldTracker)
			mergedTracker.childTrackers.append(newTracker)
		else: #They don't match, go to the next one
			return
		return mergedTracker

	def processAndQueueMultiTouchTracker(self,tracker):
		"""Queues the given tracker, replacing old trackers with a multiFingered plural action where possible"""
		#Reverse iterate through the existing queued trackers comparing the given tracker to each of them
		#as L{emitTrackers} constantly dequeues, the queue only contains trackers newer than multiTouchTimeout, though may contain more if there are still unknown singleTouchTrackers around.
		for index in range(len(self.multiTouchTrackers)):
			index=len(self.multiTouchTrackers)-1-index
			delayedTracker=self.multiTouchTrackers[index]
			mergedTracker=self.makeMergedTrackerIfPossible(delayedTracker,tracker)
			if mergedTracker:
				# The trackers were successfully merged
				# remove the old one from the queue, and queue the merged one for possible further matching
				del self.multiTouchTrackers[index]
				self.processAndQueueMultiTouchTracker(mergedTracker)
				return
		else:
			self.multiTouchTrackers.append(tracker)

	pendingEmitInterval=None #: If set: how long to wait before calling emitTrackers again as trackers are still in the queue 
	def emitTrackers(self):
		"""
		Yields queued trackers that have existed in the queue for long enough to not be connected with other trackers.
		A part from a timeout, trackers are also not emitted if there are other fingers touching that still have an unknown action. 
		If there are no queued trackers to yield but there is a hover tracker, a hover action is yielded instead.
		"""
		with self._lock:
			self.pendingEmitInterval=None
			t=time.time()
			# yield hover ups for complete hovers from most recent backwards
			for singleTouchTracker in list(self.curHoverStack): 
				if singleTouchTracker.complete:
					self.curHoverStack.remove(singleTouchTracker)
					tracker=MultiTouchTracker(action_hoverUp,singleTouchTracker.x,singleTouchTracker.y,singleTouchTracker.startTime,time.time())
					preheldTracker=self.makePreheldTrackerFromSingleTouchTrackers(self.curHoverStack)
					yield preheldTracker,tracker
			#Only emit trackers if there are not unknown actions
			hasUnknownTrackers=self.numUnknownTrackers
			if not hasUnknownTrackers:
				for tracker in list(self.multiTouchTrackers):
					# isolated holds can be dropped as we only care when they are tapAndHolds (and preheld is handled later)
					#All trackers can be emitted with no delay except for tap which must wait for the timeout (to detect plural taps)
					trackerTimeout=tracker.pluralTimeout-t if tracker.pluralTimeout is not None else 0 
					if trackerTimeout<=0: 
						self.multiTouchTrackers.remove(tracker)
						# isolated holds should not be emitted as they are covered by hover downs later
						if tracker.action==action_hold:
							continue
						preheldTracker=self.makePreheldTrackerFromSingleTouchTrackers(self.curHoverStack)
						# If this tracker was made up of any new hovers (e.g. a tapAndHold) they should be quietly added to the current hover stack so that hover downs are not produced
						for singleTouchTracker in tracker.iterAllRawSingleTouchTrackers():
							if singleTouchTracker.action==action_hover and singleTouchTracker not in self.curHoverStack:
								self.curHoverStack.append(singleTouchTracker)
						yield preheldTracker,tracker
					else:
						self.pendingEmitInterval=min(self.pendingEmitInterval,trackerTimeout) if self.pendingEmitInterval else trackerTimeout
			# yield hover downs for any new hovers
			# But only once  there are no more trackers in the queue waiting to timeout (E.g. a hold for a tapAndHold)
			if len(self.multiTouchTrackers)==0:
				for singleTouchTracker in self.singleTouchTrackersByID.values():
					if singleTouchTracker.action==action_hover and singleTouchTracker not in self.curHoverStack:
						self.curHoverStack.append(singleTouchTracker)
						tracker=MultiTouchTracker(action_hoverDown,singleTouchTracker.x,singleTouchTracker.y,singleTouchTracker.startTime,time.time())
						preheldTracker=self.makePreheldTrackerFromSingleTouchTrackers(self.curHoverStack[:-1])
						yield preheldTracker,tracker
			# yield a hover for the most recent hover
			if len(self.curHoverStack)>0:
				singleTouchTracker=self.curHoverStack[-1]
				tracker=MultiTouchTracker(action_hover,singleTouchTracker.x,singleTouchTracker.y,singleTouchTracker.startTime,time.time())
				preheldTracker=self.makePreheldTrackerFromSingleTouchTrackers(self.curHoverStack[:-1])
				yield preheldTracker,tracker
