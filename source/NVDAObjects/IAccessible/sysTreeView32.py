#NVDAObjects/IAccessible/sysTreeView32.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

from ctypes import *
from ctypes.wintypes import *
import api
import winKernel
import winUser
import controlTypes
import speech
import UIAHandler
from . import IAccessible
if UIAHandler.isUIAAvailable: from ..UIA import UIA
from .. import NVDAObject
from logHandler import log

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

class TreeView(IAccessible):

	def _get_firstChild(self):
		try:
			return super(TreeView, self).firstChild
		except:
			# Broken commctrl 5 tree view.
			return BrokenCommctrl5Item.getFirstItem(self)

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

class BrokenCommctrl5Item(IAccessible):
	"""Handle broken CommCtrl v5 SysTreeView32 items in 64 bit applications.
	In these controls, IAccessible fails to retrieve any info, so we must retrieve it using UIA.
	We do this by obtaining a UIA NVDAObject and redirecting properties to it.
	We can't simply use UIA objects alone for these controls because UIA events are also broken.
	"""

	def findOverlayClasses(self, clsList):
		# This class can be directly instantiated.
		return (BrokenCommctrl5Item,)

	def __init__(self, _uiaObj=None, **kwargs):
		# This class is being directly instantiated.
		if not _uiaObj:
			raise ValueError("Cannot instantiate directly without supplying _uiaObj")
		self._uiaObj = _uiaObj
		super(BrokenCommctrl5Item, self).__init__(**kwargs)

	def initOverlayClass(self):
		self._uiaObj = None
		if UIAHandler.handler and super(BrokenCommctrl5Item, self).parent.hasFocus:
			try:
				kwargs = {}
				UIA.kwargsFromSuper(kwargs, relation="focus")
				self._uiaObj = UIA(**kwargs)
			except:
				log.debugWarning("Retrieving UIA focus failed", exc_info=True)

	def _get_role(self):
		return self._uiaObj.role if self._uiaObj else controlTypes.ROLE_UNKNOWN

	def _get_name(self):
		return self._uiaObj.name if self._uiaObj else None

	def _get_description(self):
		return self._uiaObj.description if self._uiaObj else None

	def _get_value(self):
		return self._uiaObj.value if self._uiaObj else None

	def _get_states(self):
		return self._uiaObj.states if self._uiaObj else set()

	def _get_positionInfo(self):
		return self._uiaObj.positionInfo if self._uiaObj else {}

	def _get_location(self):
		return self._uiaObj.location if self._uiaObj else None

	def _makeRelatedObj(self, uiaObj):
		# We need to wrap related UIA objects so that the ancestry will return to IAccessible for the tree view itself.
		if not uiaObj:
			return None
		return BrokenCommctrl5Item(IAccessibleObject=self.IAccessibleObject, IAccessibleChildID=self.IAccessibleChildID, windowHandle=self.windowHandle, _uiaObj=uiaObj)

	def _get_parent(self):
		if self._uiaObj:
			uiaParent = self._uiaObj.parent
			# If the parent is the tree view itself (root window object), just use super's parent. IAccessible isn't broken on the container itself.
			if not uiaParent.UIAElement.cachedNativeWindowHandle:
				return self._makeRelatedObj(uiaParent)
		return super(BrokenCommctrl5Item, self).parent

	def _get_next(self):
		return self._makeRelatedObj(self._uiaObj.next) if self._uiaObj else None

	def _get_previous(self):
		return self._makeRelatedObj(self._uiaObj.previous) if self._uiaObj else None

	def _get_firstChild(self):
		return self._makeRelatedObj(self._uiaObj.firstChild) if self._uiaObj else None

	def _get_lastChild(self):
		return self._makeRelatedObj(self._uiaObj.lastChild) if self._uiaObj else None

	def _get_children(self):
		# Use the base algorithm, which uses firstChild and next.
		return NVDAObject._get_children(self)

	@classmethod
	def getFirstItem(cls, treeObj):
		"""Get an instance for the first item in a given tree view.
		"""
		if not UIAHandler.handler:
			return None
		# Get a UIA object for the tree view by getting the root object for the window.
		try:
			kwargs = {"windowHandle": treeObj.windowHandle}
			UIA.kwargsFromSuper(kwargs)
			uiaObj = UIA(**kwargs)
		except:
			log.debugWarning("Error retrieving UIA object for tree view", exc_info=True)
			return None
		# Get the first tree item.
		uiaObj = uiaObj.firstChild
		if not uiaObj:
			return None
		# The IAccessibleChildID for this object isn't really used.
		# However, it must not be 0, as 0 is the tree view itself.
		return cls(IAccessibleObject=treeObj.IAccessibleObject, IAccessibleChildID=1, windowHandle=treeObj.windowHandle, _uiaObj=uiaObj)
