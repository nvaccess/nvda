#autoPropertyType.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

#Based on example from:
#http://www.python.org/download/releases/2.2.3/descrintro/
#Added a check for the length of the _set_ and _get_ names to make sure they are 5 or more characters long or else we can't use them

class autoPropertyType(type):
	"""Creates properties for any _get_x or _set_x methods."""
	def __init__(cls,name,bases,dict):
		super(autoPropertyType,cls).__init__(cls,name,bases,dict)
		properties={}
		for name in dict.keys():
			if (len(name)>=5) and (name.startswith('_set_') or name.startswith('_get_')):
				properties[name[5:]]=dict[name]
		for name in properties:
			setattr(cls,name,property(fget=dict.get('_get_%s'%name,None),fset=dict.get('_set_%s'%name,None)))
