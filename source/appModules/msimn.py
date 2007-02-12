#appModules/msimn.py - Outlook Express appModule
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import audio
import winUser
import _default

class appModule(_default.appModule):

	def event_IAccessible_gainFocus(self,window,objectID,childID,nextHandler):
		controlID=winUser.getControlID(window)
		parent=winUser.getAncestor(window,winUser.GA_PARENT)
		parentClassName=winUser.getClassName(parent)
		if parentClassName=="OE_Envelope":
			if controlID==1001:
				audio.speakText(_("To:"))
			elif controlID==1003:
				audio.speakText(_("CC:"))
			elif controlID==1026:
				audio.speakText(_("BCC:"))
			elif controlID==1004:
				audio.speakText(_("Subject:"))
			elif controlID==1005:
				audio.speakText(_("From:"))
			elif controlID==1037:
				audio.speakText(_("From:"))
			elif controlID==1016:
				audio.speakText(_("Date:"))
			elif controlID==1000:
				audio.speakText(_("Attachments"))
		nextHandler(window,objectID,childID)
