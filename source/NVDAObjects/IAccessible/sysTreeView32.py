from ctypes import *
from ctypes.wintypes import *
import api
import winKernel
import winUser
import controlTypes
import speech
from . import IAccessible

oldLevel=None

TV_FIRST=0x1100
TVIS_STATEIMAGEMASK=0xf000

#Window messages
TVM_GETITEMSTATE=TV_FIRST+39
TVM_GETITEM=TV_FIRST+62
TVM_MAPACCIDTOHTREEITEM=TV_FIRST+42
TVM_MAPHTREEITEMTOACCID=TV_FIRST+43
TVM_GETNEXTITEM=TV_FIRST+10

#item mask flags
TVIF_CHILDREN=0x40

#Relation codes
TVGN_ROOT=0
TVGN_NEXT=1
TVGN_PREVIOUS=2
TVGN_PARENT=3
TVGN_CHILD=4

class TVItemStruct(Structure):
	_fields_=[
		('mask',c_uint),
		('hItem',c_void_p),
		('state',c_uint),
		('stateMask',c_uint),
		('pszText',LPWSTR),
		('cchTextMax',c_int),
		('iImage',c_int),
		('iSelectedImage',c_int),
		('cChildren',c_int),
		('lParam',LPARAM),
	]

class TreeViewItem(IAccessible):

	def _get_treeLevel(self):
		return int(self.IAccessibleObject.accValue(self.IAccessibleChildID))

	def _get_states(self):
		states=super(TreeViewItem,self)._get_states()
		hItem=winUser.sendMessage(self.windowHandle,TVM_MAPACCIDTOHTREEITEM,self.IAccessibleChildID,0)
		itemStates=winUser.sendMessage(self.windowHandle,TVM_GETITEMSTATE,hItem,TVIS_STATEIMAGEMASK)
		ch=(itemStates>>12)&3
		if ch>0:
			states.add(controlTypes.STATE_CHECKABLE)
		if ch==2:
			states.add(controlTypes.STATE_CHECKED)
		elif ch==3:
			states.add(controlTypes.STATE_HALFCHECKED)
		return states

	def _get_value(self):
		return None

	def _get_parent(self):
		if self.IAccessibleChildID==0:
			return super(self.__class__,self)._get_parent()
		hItem=winUser.sendMessage(self.windowHandle,TVM_MAPACCIDTOHTREEITEM,self.IAccessibleChildID,0)
		if not hItem:
			return super(self.__class__,self)._get_parent()
		parentItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_PARENT,hItem)
		if parentItem<=0:
			return super(self.__class__,self)._get_parent()
		newID=winUser.sendMessage(self.windowHandle,TVM_MAPHTREEITEMTOACCID,parentItem,0)
		if newID<=0:
			return super(self.__class__,self)._get_parent()
		return self.__class__(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=newID)

	def _get_firstChild(self):
		if self.IAccessibleChildID==0:
			return super(self.__class__,self)._get_firstChild()
		hItem=winUser.sendMessage(self.windowHandle,TVM_MAPACCIDTOHTREEITEM,self.IAccessibleChildID,0)
		if not hItem:
			return super(self.__class__,self)._get_firstChild()
		childItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_CHILD,hItem)
		if childItem<=0:
			return super(self.__class__,self)._get_firstChild()
		newID=winUser.sendMessage(self.windowHandle,TVM_MAPHTREEITEMTOACCID,childItem,0)
		if newID<=0:
			return super(self.__class__,self)._get_firstChild()
		return self.__class__(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=newID)

	def _get_next(self):
		if self.IAccessibleChildID==0:
			return super(self.__class__,self)._get_next()
		hItem=winUser.sendMessage(self.windowHandle,TVM_MAPACCIDTOHTREEITEM,self.IAccessibleChildID,0)
		if not hItem:
			return None
		nextItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_NEXT,hItem)
		if nextItem<=0:
			return None
		newID=winUser.sendMessage(self.windowHandle,TVM_MAPHTREEITEMTOACCID,nextItem,0)
		if newID<=0:
			return None
		return self.__class__(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=newID)

	def _get_previous(self):
		if self.IAccessibleChildID==0:
			return super(self.__class__,self)._get_previous()
		hItem=winUser.sendMessage(self.windowHandle,TVM_MAPACCIDTOHTREEITEM,self.IAccessibleChildID,0)
		if not hItem:
			return None
		prevItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_PREVIOUS,hItem)
		if prevItem<=0:
			return None
		newID=winUser.sendMessage(self.windowHandle,TVM_MAPHTREEITEMTOACCID,prevItem,0)
		if newID<=0:
			return None
		return self.__class__(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=newID)

	def _get_children(self):
		children=[]
		child=self.firstChild
		while child:
			children.append(child)
			child=child.next
		return children

	def _get_childCount(self):
		return len(self.children)

	def _get_positionString(self):
		if self.IAccessibleChildID==0:
			return super(self.__class__,self)._get_positionString()
		hItem=winUser.sendMessage(self.windowHandle,TVM_MAPACCIDTOHTREEITEM,self.IAccessibleChildID,0)
		if not hItem:
			return None
		newItem=hItem
		index=0
		while newItem>0:
			index+=1
			newItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_PREVIOUS,newItem)
		newItem=hItem
		numItems=index-1
		while newItem>0:
			numItems+=1
			newItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_NEXT,newItem)
		return _("%d of %d")%(index,numItems)

	def event_stateChange(self):
		if self is api.getFocusObject() and controlTypes.STATE_EXPANDED in self.states and not controlTypes.STATE_EXPANDED in getattr(self,'_speakObjectPropertiesCache',set()):
			announceContains=True
		else:
			announceContains=False
		super(self.__class__,self).event_stateChange()
		if announceContains:
			speech.speakMessage(_("%s items")%self.childCount)

	def event_gainFocus(self):
		global oldLevel
		newLevel=self.treeLevel
 		if newLevel!=oldLevel and self is api.getFocusObject():
			speech.speakMessage(_("level %d")%newLevel)
			oldLevel=newLevel
		super(self.__class__,self).event_gainFocus()
