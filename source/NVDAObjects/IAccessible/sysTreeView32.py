from ctypes import *
from ctypes.wintypes import *
import api
import winKernel
import winUser
import controlTypes
import speech
from . import IAccessible

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

	def _get_role(self):
		return controlTypes.ROLE_TREEVIEWITEM

	def _get_treeview_hItem(self):
		if not hasattr(self,'_treeview_hItem'):
			self._treeview_hItem=winUser.sendMessage(self.windowHandle,TVM_MAPACCIDTOHTREEITEM,self.IAccessibleChildID,0)
			if not self._treeview_hItem:
				# Tree views from comctl < 6.0 use the hItem as the child ID.
				self._treeview_hItem=self.IAccessibleChildID
		return self._treeview_hItem

	def _get_treeview_level(self):
		return int(self.IAccessibleObject.accValue(self.IAccessibleChildID))

	def _get_states(self):
		states=super(TreeViewItem,self)._get_states()
		hItem=self.treeview_hItem
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
			return super(TreeViewItem,self)._get_parent()
		hItem=self.treeview_hItem
		if not hItem:
			return super(TreeViewItem,self)._get_parent()
		parentItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_PARENT,hItem)
		if parentItem<=0:
			return super(TreeViewItem,self)._get_parent()
		newID=winUser.sendMessage(self.windowHandle,TVM_MAPHTREEITEMTOACCID,parentItem,0)
		if not newID:
			# Tree views from comctl < 6.0 use the hItem as the child ID.
			newID=parentItem
		return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=newID)

	def _get_firstChild(self):
		if self.IAccessibleChildID==0:
			return super(TreeViewItem,self)._get_firstChild()
		hItem=self.treeview_hItem
		if not hItem:
			return super(TreeViewItem,self)._get_firstChild()
		childItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_CHILD,hItem)
		if childItem<=0:
			return super(TreeViewItem,self)._get_firstChild()
		newID=winUser.sendMessage(self.windowHandle,TVM_MAPHTREEITEMTOACCID,childItem,0)
		if not newID:
			# Tree views from comctl < 6.0 use the hItem as the child ID.
			newID=childItem
		return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=newID)

	def _get_next(self):
		if self.IAccessibleChildID==0:
			return super(TreeViewItem,self)._get_next()
		hItem=self.treeview_hItem
		if not hItem:
			return None
		nextItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_NEXT,hItem)
		if nextItem<=0:
			return None
		newID=winUser.sendMessage(self.windowHandle,TVM_MAPHTREEITEMTOACCID,nextItem,0)
		if not newID:
			# Tree views from comctl < 6.0 use the hItem as the child ID.
			newID=nextItem
		return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=newID)

	def _get_previous(self):
		if self.IAccessibleChildID==0:
			return super(TreeViewItem,self)._get_previous()
		hItem=self.treeview_hItem
		if not hItem:
			return None
		prevItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_PREVIOUS,hItem)
		if prevItem<=0:
			return None
		newID=winUser.sendMessage(self.windowHandle,TVM_MAPHTREEITEMTOACCID,prevItem,0)
		if not newID:
			# Tree views from comctl < 6.0 use the hItem as the child ID.
			newID=prevItem
		return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=newID)

	def _get_children(self):
		children=[]
		child=self.firstChild
		while child:
			children.append(child)
			child=child.next
		return children

	def _get_childCount(self):
		hItem=self.treeview_hItem
		if not hItem:
			return 0
		childItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_CHILD,hItem)
		if childItem<=0:
			return 0
		numItems=0
		while childItem>0:
			numItems+=1
			childItem=winUser.sendMessage(self.windowHandle,TVM_GETNEXTITEM,TVGN_NEXT,childItem)
		return numItems

	def _get_positionInfo(self):
		if self.IAccessibleChildID==0:
			return super(TreeViewItem,self)._get_positionInfo()
		info={}
		info['level']=self.treeview_level
		hItem=self.treeview_hItem
		if not hItem:
			return info
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
		info['indexInGroup']=index
		info['similarItemsInGroup']=numItems
		return info

	def event_stateChange(self):
		if self is api.getFocusObject() and controlTypes.STATE_EXPANDED in self.states and not controlTypes.STATE_EXPANDED in getattr(self,'_speakObjectPropertiesCache',set()):
			announceContains=True
		else:
			announceContains=False
		super(TreeViewItem,self).event_stateChange()
		if announceContains:
			speech.speakMessage(_("%s items")%self.childCount)

