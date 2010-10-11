#keyUtils.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import globalVars
from logHandler import log
import winUser
import queueHandler
import wx
import vkCodes

def key(name):
	"""Converts a string representation of a keyPress in to a set of modifiers and a key (which is NVDA's internal key representation).
@param name: keyPress name to convert
@type name: string
@returns: the internal key representation 
"""
	name=name.lower()
	l = name.split("+")
	for num in range(len(l)):
		t=l[num]
		if len(t)>1:
			t="%s%s"%(t[0],t[1:])
		elif len(t)==1:
			t=t[0]
		l[num]=t
	if len(l) >= 2:
		s=set()
		for m in l[0:-1]:
			s.add(m)
		modifiers = frozenset(s)
	else:
		modifiers = None
	return (modifiers, l[-1])

def keyName(keyPress):
	"""Converts an internal key press to a printable name
@param keyPress: a keyPress
@type keyPress: key
"""
	keyName=""
	for k in list(keyPress[0] if isinstance(keyPress[0],frozenset) else [])+[keyPress[1]]:
		keyName+="+%s"%k
	return keyName[1:]

localizedKeyLabels={
	'browserBack': _("back"),
	'browserForward': _("forward"),
	'browserRefresh': _("refresh"),
	'browserStop': _("browser stop"),
	'browserSearch': _("search page"),
	'browserFavorites': _("favorites"),
	'browserHome': _("home page"),
	'volumeMute': _("mute"),
	'volumeDown': _("volume down"),
	'volumeUp': _("volume up"),
	'mediaNextTrack': _("next track"),
	'mediaPrevTrack': _("previous track"),
	'mediaStop': _("stop"),
	'mediaPlayPause': _("play pause"),
	'launchMail': _("email"),
	'launchMediaPlayer': _("media player"),
	'launchApp1': _("custom application 1"),
	'launchApp2': _("custom application 2"),
	'backspace': _("backspace"),
	'capsLock': _("caps lock"),
	'control': _("ctrl"),
	'alt': _("alt"),
	'shift': _("shift"),
	'windows': _("windows"),
	'enter': _("enter"),
	'numpadEnter': _("numpad enter"),
	'escape': _("escape"),
	'space': _("space"),
	'pageUp': _("page up"),
	'pageDown': _("page down"),
	'end': _("end"),
	'home': _("home"),
	'delete': _("delete"),
	'numpadDelete': _("numpad delete"),
	'leftArrow': _("left arrow"),
	'rightArrow': _("right arrow"),
	'upArrow': _("up arrow"),
	'downArrow': _("down arrow"),
	'applications': _("applications"),
	'numLock': _("num lock"),
	'printScreen': _("print screen"),
	'scrollLock': _("scroll lock"),
	'numpadLeftArrow': _("numpad left"),
	'numpadRightArrow': _("numpad right"),
	'numpadUpArrow': _("numpad up"),
	'numpadDownArrow': _("numpad down"),
	'numpadPageUp': _("numpad page up"),
	'numpadPageDown': _("numpad page down"),
	'numpadEnd': _("numpad end"),
	'numpadHome': _("numpad home"),
	'numpadDivide': _("numpad slash"),
	'numpadMultiply': _("numpad star"),
	'numpadSubtract': _("numpad minus"),
	'numpadAdd': _("numpad plus"),
	'leftControl': _("left control"),
	'rightControl': _("right control"),
	'leftWindows': _("left windows"),
	'leftShift': _("left shift"),
	'rightShift': _("right shift"),
	'leftAlt': _("left alt"),
	'rightAlt': _("right alt"),
	'rightWindows': _("right windows")
}
