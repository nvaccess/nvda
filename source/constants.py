#constants.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import pyAA

#Roles, object IDs  and states
for attrib in dir(pyAA.Constants):
	if (attrib[0:4]=="ROLE") or (attrib[0:5]=="STATE") or (attrib[0:5]=="OBJID"):
		globals()[attrib]=getattr(pyAA.Constants,attrib)
	ROLE_SYSTEM_SPLITBUTTON=62
	ROLE_SYSTEM_OUTLINEBUTTON=64
STATE_SYSTEM_HASSUBMENU=1073741824

#types
OBJECT_NAME=1
OBJECT_ROLE=2
OBJECT_STATE=3
OBJECT_VALUE=4
OBJECT_DESCRIPTION=5
OBJECT_HELP=6
OBJECT_POSITION=7
OBJECT_GROUP=8
TEXT_LINE=9
OBJECT_STATE_OFF=10

