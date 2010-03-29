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
	'browser_back': _("back"),
	'browser_forward': _("forward"),
	'browser_refresh': _("refresh"),
	'browser_stop': _("browser stop"),
	'browser_search': _("search page"),
	'browser_favorites': _("favorites"),
	'browser_home': _("home page"),
	'volume_mute': _("mute"),
	'volume_down': _("volume down"),
	'volume_up': _("volume up"),
	'extendedmedia_next_track': _("next track"),
	'extendedmedia_prev_track': _("previous track"),
	'extendedmedia_stop': _("stop"),
	'extendedmedia_play_pause':_("play pause"),
	'launch_mail': _("email"),
	'LAUNCH_MEDIA_SELECT': _("media player"),
	'launch_app1': _("custom applications key one"),
	'launch_app2': _("custom applications key two"),
	'back': _("backspace"),
	'capital': _("caps lock"),
	'control': _("ctrl"),
	'alt': _("alt"),
	'shift': _("shift"),
	'win': _("windows"),
	'return': _("enter"),
	'extendedreturn': _("numpad enter"),
	'escape': _("escape"),
	'space': _("space"),
	'extendedprior': _("page up"),
	'extendednext': _("page down"),
	'extendedend': _("end"),
	'extendedhome': _("home"),
	'extendeddelete': _("delete"),
	'extendedleft': _("left arrow"),
	'extendedright': _("right arrow"),
	'extendedup': _("up arrow"),
	'extendeddown': _("down arrow"),
	'extendedapps': _("applications"),
	'extendednumlock': _("num lock"),
	'extendedsnapshot': _("snapshot"),
	'scroll': _("scroll lock"),
	'left': _("numpad left"),
	'right': _("numpad right"),
	'up': _("numpad up"),
	'down': _("numpad down"),
	'prior': _("numpad page up"),
	'next': _("numpad page down"),
	'end': _("numpad end"),
	'home': _("numpad home"),
	'extendeddivide': _("numpad slash"),
	'multiply': _("numpad star"),
	'subtract': _("numpad minus"),
	'add': _("numpad plus"),
	'lcontrol': _("left control"),
	'extendedrcontrol': _("right control"),
	'extendedlwin': _("left windows"),
	'lshift': _("left shift"),
	'extendedrshift': _("right shift"),
	'lmenu': _("left alt"),
	'extendedrmenu': _("right alt"),
	'extendedrwin': _("right windows")
}
