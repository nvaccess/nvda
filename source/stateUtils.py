#stateUtils.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import math
from constants import *
import globalVars

def createStateList(stateBits):
	stateList=[]
	for bitPos in range(32):
		bitVal=1<<bitPos
		if stateBits&bitVal:
			stateList+=[bitVal]
	return stateList

def filterStates(states):
	if STATE_SYSTEM_SELECTABLE&states:
		states-=STATE_SYSTEM_SELECTABLE
	if STATE_SYSTEM_MULTISELECTABLE&states:
		states-=STATE_SYSTEM_MULTISELECTABLE
	if STATE_SYSTEM_FOCUSABLE&states:
		states-=STATE_SYSTEM_FOCUSABLE
	if STATE_SYSTEM_FOCUSED&states:
		states-=STATE_SYSTEM_FOCUSED
	if STATE_SYSTEM_HOTTRACKED&states:
		states-=STATE_SYSTEM_HOTTRACKED
	if STATE_SYSTEM_UNAVAILABLE&states:
		states-=STATE_SYSTEM_UNAVAILABLE
	if STATE_SYSTEM_DEFAULT&states:
		states-=STATE_SYSTEM_DEFAULT
	if STATE_SYSTEM_INVISIBLE&states:
		states-=STATE_SYSTEM_INVISIBLE
	return states


