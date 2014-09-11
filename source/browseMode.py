#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2014 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import nvwave
import config
import speech
import treeInterceptorHandler

def reportPassThrough(treeInterceptor,onlyIfChanged=True):
	"""Reports the virtual buffer pass through mode if it has changed.
	@param treeInterceptor: The current Browse Mode treeInterceptor.
	@type treeInterceptor: L{BrowseModeTreeInterceptor}
	@param onlyIfChanged: if true reporting will not happen if the last reportPassThrough reported the same thing.
	@type onlyIfChanged: bool
	"""
	if not onlyIfChanged or treeInterceptor.passThrough != reportPassThrough.last:
		if config.conf["virtualBuffers"]["passThroughAudioIndication"]:
			sound = r"waves\focusMode.wav" if treeInterceptor.passThrough else r"waves\browseMode.wav"
			nvwave.playWaveFile(sound)
		else:
			if treeInterceptor.passThrough:
				speech.speakMessage(_("focus mode"))
			else:
				speech.speakMessage(_("browse mode"))
		reportPassThrough.last = treeInterceptor.passThrough
reportPassThrough.last = False

class BrowseModeTreeInterceptor(treeInterceptorHandler.TreeInterceptor):
	pass
