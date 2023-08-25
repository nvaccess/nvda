#NVDAObjects/IAccessible/webKit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2011 NV Access Inc
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import IAccessibleHandler
import controlTypes
import braille
from . import IAccessible

"""NVDAObjects for WebKit.
"""

class Node(IAccessible):

	def _get_parent(self):
		acc = IAccessibleHandler.accParent(self.IAccessibleObject, 0)
		if not acc:
			return super(IAccessible,self).parent
		# HACK: WindowFromAccessibleObject fails on some WebKit objects retrieved using accParent.
		# The window handle is the same for all nodes in a document anyway.
		# Note that WindowFromAccessibleObject seems to work for children and siblings,
		# so we don't need to do this for those.
		return IAccessible(IAccessibleObject=acc[0], IAccessibleChildID=0, windowHandle=self.windowHandle)

class Document(IAccessible):

	def _get_treeInterceptorClass(self):
		from virtualBuffers.webKit import WebKit
		return WebKit

class EditableText(Node):

	def event_valueChange(self):
		# We don't want the value to be spoken every time it is changed.
		braille.handler.handleUpdate(self)

def findExtraOverlayClasses(obj, clsList):
	"""Determine the most appropriate class(es) for WebKit objects.
	This works similarly to L{NVDAObjects.NVDAObject.findOverlayClasses} except that it never calls any other findOverlayClasses method.
	"""
	role = obj.role
	if role == controlTypes.Role.WINDOW:
		return
	if role == controlTypes.Role.DOCUMENT:
		clsList.append(Document)
	elif role == controlTypes.Role.EDITABLETEXT:
		clsList.append(EditableText)
	clsList.append(Node)
