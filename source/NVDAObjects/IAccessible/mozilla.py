#NVDAObjects/IAccessible/mozilla.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import IAccessibleHandler
import oleacc
from . import IAccessible
import textHandler

class Mozilla(IAccessible):

	def _get_description(self):
		rawDescription=super(Mozilla,self).description
		if isinstance(rawDescription,basestring) and rawDescription.startswith('Description: '):
			return rawDescription[13:]
		else:
			return ""


	def _get_parent(self):
		#Special code to support Mozilla node_child_of relation (for comboboxes)
		res=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVRELATION_NODE_CHILD_OF)
		if res and res!=(self.IAccessibleObject,self.IAccessibleChildID):
			newObj=IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
			if newObj:
				return newObj
		return super(Mozilla,self).parent

class Application(Mozilla):

	def _get_value(self):
		return None

	def event_nameChange(self):
		if self.windowHandle==api.getForegroundObject().windowHandle:
			speech.speakObjectProperties(self,name=True,reason=speech.REASON_QUERY)

class Document(Mozilla):

	def _get_value(self):
		return 

class ListItem(Mozilla):

	def _get_name(self):
		name=super(ListItem,self)._get_name()
		if self.IAccessibleStates&oleacc.STATE_SYSTEM_READONLY:
			children=super(ListItem,self)._get_children()
			if len(children)>0 and (children[0].IAccessibleRole in ["bullet",oleacc.ROLE_SYSTEM_STATICTEXT]):
				name=children[0].value
		return name

	def _get_children(self):
		children=super(ListItem,self)._get_children()
		if self.IAccessibleStates&oleacc.STATE_SYSTEM_READONLY and len(children)>0 and (children[0].IAccessibleRole in ("bullet",oleacc.ROLE_SYSTEM_STATICTEXT)):
			del children[0]
		return children

class Label(Mozilla):

	def _get_name(self):
		name=super(Label,self)._get_name()
		if not name or name=="":
			name=self.makeTextInfo(textHandler.POSITION_ALL).text
		return name
