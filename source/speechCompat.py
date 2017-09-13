# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2017 NV Access Limited, Peter Vágner, Aleksey Sadovoy
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Speech code to support old synthesizers which don't support index and done speaking notifications, etc.
"""

import itertools
import speech
from synthDriverHandler import getSynth
import tones
import queueHandler
import config
import characterProcessing
from logHandler import log
import textInfos
import api
import controlTypes
import sayAllHandler

def getLastSpeechIndex():
	return getSynth().lastIndex

_speakSpellingGenerator=None

def speakSpelling(text,locale=None,useCharacterDescriptions=False):
	global _speakSpellingGenerator
	import speechViewer
	if speechViewer.isActive:
		speechViewer.appendText(text)
	if speech.speechMode==speech.speechMode_off:
		return
	elif speech.speechMode==speech.speechMode_beeps:
		tones.beep(config.conf["speech"]["beepSpeechModePitch"],speechMode_beeps_ms)
		return
	if speech.isPaused:
		speech.cancelSpeech()
	speech.beenCanceled=False
	defaultLanguage=speech.getCurrentLanguage()
	if not locale or (not config.conf['speech']['autoDialectSwitching'] and locale.split('_')[0]==defaultLanguage.split('_')[0]):
		locale=defaultLanguage

	if not text:
		# Translators: This is spoken when NVDA moves to an empty line.
		return getSynth().speak((_("blank"),))
	if not text.isspace():
		text=text.rstrip()
	if _speakSpellingGenerator and _speakSpellingGenerator.gi_frame:
		_speakSpellingGenerator.send((text,locale,useCharacterDescriptions))
	else:
		_speakSpellingGenerator=_speakSpellingGen(text,locale,useCharacterDescriptions)
		try:
			# Speak the first character before this function returns.
			next(_speakSpellingGenerator)
		except StopIteration:
			return
		queueHandler.registerGeneratorObject(_speakSpellingGenerator)

def _speakSpellingGen(text,locale,useCharacterDescriptions):
	synth=getSynth()
	synthConfig=config.conf["speech"][synth.name]
	buf=[(text,locale,useCharacterDescriptions)]
	for text,locale,useCharacterDescriptions in buf:
		textLength=len(text)
		count = 0
		localeHasConjuncts = True if locale.split('_',1)[0] in speech.LANGS_WITH_CONJUNCT_CHARS else False
		charDescList = speech.getCharDescListFromText(text,locale) if localeHasConjuncts else text
		for item in charDescList:
			if localeHasConjuncts:
				# item is a tuple containing character and its description
				char = item[0]
				charDesc = item[1]
			else:
				# item is just a character.
				char = item
				if useCharacterDescriptions:
					charDesc=characterProcessing.getCharacterDescription(locale,char.lower())
			uppercase=char.isupper()
			if useCharacterDescriptions and charDesc:
				#Consider changing to multiple synth speech calls
				char=charDesc[0] if textLength>1 else u"\u3001".join(charDesc)
			else:
				char=characterProcessing.processSpeechSymbol(locale,char)
			if uppercase and synthConfig["sayCapForCapitals"]:
				# Translators: cap will be spoken before the given letter when it is capitalized.
				char=_("cap %s")%char
			if uppercase and synth.isSupported("pitch") and synthConfig["capPitchChange"]:
				oldPitch=synthConfig["pitch"]
				synth.pitch=max(0,min(oldPitch+synthConfig["capPitchChange"],100))
			count = len(char)
			index=count+1
			log.io("Speaking character %r"%char)
			speechSequence=[speech.LangChangeCommand(locale)] if config.conf['speech']['autoLanguageSwitching'] else []
			if len(char) == 1 and synthConfig["useSpellingFunctionality"]:
				speechSequence.append(speech.CharacterModeCommand(True))
			if index is not None:
				speechSequence.append(speech.IndexCommand(index))
			speechSequence.append(char)
			synth.speak(speechSequence)
			if uppercase and synth.isSupported("pitch") and synthConfig["capPitchChange"]:
				synth.pitch=oldPitch
			while textLength>1 and (speech.isPaused or getLastSpeechIndex()!=index):
				for x in xrange(2):
					args=yield
					if args: buf.append(args)
			if uppercase and  synthConfig["beepForCapitals"]:
				tones.beep(2000,50)
		args=yield
		if args: buf.append(args)

_sayAll_generatorID = None

def _sayAll_startGenerator(generator):
	global _sayAll_generatorID
	sayAll_stop()
	_sayAll_generatorID = queueHandler.registerGeneratorObject(generator)

def sayAll_stop():
	global _sayAll_generatorID
	if _sayAll_generatorID is None:
		return
	queueHandler.cancelGeneratorObject(_sayAll_generatorID)
	_sayAll_generatorID = None

def sayAll_isRunning():
	return _sayAll_generatorID is not None

def sayAll_readObjects(obj):
	_sayAll_startGenerator(sayAll_readObjectsHelper_generator(obj))

def sayAll_generateObjectSubtreeSpeech(obj,indexGen):
	index=indexGen.next()
	indexCommand = speech.IndexCommand(index)
	speech.speakObject(obj,reason=controlTypes.REASON_SAYALL,_prefixSpeechCommand=indexCommand)
	yield obj,index
	child=obj.simpleFirstChild
	while child:
		childSpeech=sayAll_generateObjectSubtreeSpeech(child,indexGen)
		for r in childSpeech:
			yield r
		child=child.simpleNext

def sayAll_readObjectsHelper_generator(obj):
	lastSentIndex=0
	lastReceivedIndex=0
	speechGen=sayAll_generateObjectSubtreeSpeech(obj,itertools.count())
	objIndexMap={}
	keepReading=True
	while True:
		# lastReceivedIndex might be None if other speech was interspersed with this say all.
		# In this case, we want to send more text in case this was the last chunk spoken.
		if lastReceivedIndex is None or (lastSentIndex-lastReceivedIndex)<=1:
			if keepReading:
				try:
					o,lastSentIndex=speechGen.next()
				except StopIteration:
					keepReading=False
					continue
				objIndexMap[lastSentIndex]=o
		receivedIndex=getLastSpeechIndex()
		if receivedIndex!=lastReceivedIndex and (lastReceivedIndex!=0 or receivedIndex!=None): 
			lastReceivedIndex=receivedIndex
			lastReceivedObj=objIndexMap.get(lastReceivedIndex)
			if lastReceivedObj is not None:
				api.setNavigatorObject(lastReceivedObj)
			#Clear old objects from the map
			for i in objIndexMap.keys():
				if i<=lastReceivedIndex:
					del objIndexMap[i]
		while speech.isPaused:
			yield
		yield

def sayAll_readText(cursor, trigger):
	_sayAll_startGenerator(sayAll_readTextHelper_generator(cursor, trigger))

def sayAll_readTextHelper_generator(cursor, trigger):
	if cursor==sayAllHandler.CURSOR_CARET:
		try:
			reader=api.getCaretObject().makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError):
			return
	else:
		reader=api.getReviewPosition()

	lastSentIndex=0
	lastReceivedIndex=0
	cursorIndexMap={}
	keepReading=True
	speakTextInfoState=speech.SpeakTextInfoState(reader.obj)
	try:
		while True:
			if not reader.obj:
				# The object died, so we should too.
				return
			# lastReceivedIndex might be None if other speech was interspersed with this say all.
			# In this case, we want to send more text in case this was the last chunk spoken.
			if lastReceivedIndex is None or (lastSentIndex-lastReceivedIndex)<=10:
				if keepReading:
					bookmark=reader.bookmark
					index=lastSentIndex+1
					delta=reader.move(textInfos.UNIT_READINGCHUNK,1,endPoint="end")
					if delta<=0:
						speech.speakWithoutPauses(None)
						keepReading=False
						continue
					indexCommand = speech.IndexCommand(index)
					speech.speakTextInfo(reader,unit=textInfos.UNIT_READINGCHUNK,reason=controlTypes.REASON_SAYALL,_prefixSpeechCommand=indexCommand,useCache=speakTextInfoState)
					lastSentIndex=index
					cursorIndexMap[index]=(bookmark,speakTextInfoState.copy())
					try:
						reader.collapse(end=True)
					except RuntimeError: #MS Word when range covers end of document
						# Word specific: without this exception to indicate that further collapsing is not posible, say-all could enter an infinite loop.
						speech.speakWithoutPauses(None)
						keepReading=False
			else:
				# We'll wait for speech to catch up a bit before sending more text.
				if speech.speakWithoutPauses._lastSentIndex is None or (lastSentIndex-speech.speakWithoutPauses._lastSentIndex)>=10:
					# There is a large chunk of pending speech
					# Force speakWithoutPauses to send text to the synth so we can move on.
					speech.speakWithoutPauses(None)
			receivedIndex=getLastSpeechIndex()
			if receivedIndex!=lastReceivedIndex and (lastReceivedIndex!=0 or receivedIndex!=None): 
				lastReceivedIndex=receivedIndex
				bookmark,state=cursorIndexMap.get(receivedIndex,(None,None))
				if state:
					state.updateObj()
				if bookmark is not None:
					updater=reader.obj.makeTextInfo(bookmark)
					if cursor==sayAllHandler.CURSOR_CARET:
						updater.updateCaret()
					if cursor!=sayAllHandler.CURSOR_CARET or config.conf["reviewCursor"]["followCaret"]:
						api.setReviewPosition(updater)
			elif not keepReading and lastReceivedIndex==lastSentIndex:
				# All text has been sent to the synth.
				# Turn the page and start again if the object supports it.
				if isinstance(reader.obj,textInfos.DocumentWithPageTurns):
					try:
						reader.obj.turnPage()
					except RuntimeError:
						break
					else:
						reader=reader.obj.makeTextInfo(textInfos.POSITION_FIRST)
						keepReading=True
				else:
					break

			while speech.isPaused:
				yield
			yield

		# Wait until the synth has actually finished speaking.
		# Otherwise, if there is a triggered profile with a different synth,
		# we will switch too early and truncate speech (even up to several lines).
		# Send another index and wait for it.
		index=lastSentIndex+1
		speech.speak([speech.IndexCommand(index)])
		while getLastSpeechIndex()<index:
			yield
			yield
		# Some synths say they've handled the index slightly sooner than they actually have,
		# so wait a bit longer.
		for i in xrange(30):
			yield

	finally:
		trigger.exit()
