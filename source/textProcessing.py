#textProcessing.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
import characterSymbols

re_capAfterNoCapsInWord=re.compile(r"([a-z])([A-Z])")
re_singleCapAfterCapsInWord=re.compile(r"([A-Z])([A-Z][a-z])")
re_numericAfterAlphaInWord=re.compile(r"([a-zA-Z])([0-9])")
re_sentence_dot=re.compile(r"(\w|\)|\"|')\.(\s|$)")
re_sentence_comma=re.compile(r"(\w|\)|\"|'),(\s|$)")
re_sentence_question=re.compile(r"(\w|\))\?(\s|$)")
re_sentence_colon=re.compile(r"(\w|\)|\"|'):(\s|$)")
re_sentence_semiColon=re.compile(r"(\w|\)|\"|');(\s|$)")
re_sentence_exclimation=re.compile(r"(\w|\)|\"|')!(\s|$)")
re_word_apostraphy=re.compile(r"(\w)'(\w)")


def processTextSymbols(text,expandPunctuation=False):
	if (text is None) or (len(text)==0) or (isinstance(text,basestring) and (set(text)<=set(characterSymbols.blankList))):
		return _("blank") 
	#Limit groups of the same character to 5 or less.
	trunkatedText=""
	lastChar=""
	sameCharCount=0
	for char in text:
		if char==lastChar:
			sameCharCount+=1
		else:
			sameCharCount=1
		if sameCharCount<11:
			trunkatedText="".join([trunkatedText,char])
		lastChar=char
	text=trunkatedText
	#breaks up words that use a capital letter to denote another word
	text=re_capAfterNoCapsInWord.sub(r"\1 \2",text)
	#Like the last one, but this breaks away the last capital letter from an entire group of capital letters imbedded in a word (e.g. NVDAObject) 
	text=re_singleCapAfterCapsInWord.sub(r"\1 \2",text)
	#Breaks words that have numbers at the end
	text=re_numericAfterAlphaInWord.sub(r"\1 \2",text)
	#expands ^ and ~ so they can be used as protector symbols
	#Expands special sentence punctuation keeping the origional physical symbol but protected by ^ and ~
	#Expands any other symbols and removes ^ and ~ protectors
	if expandPunctuation is False:
		return text 
	protector=False
	buf=""
	for char in text:
		if (char=="^") or (char=="~"):
			buf+=" %s "%characterSymbols.names[char]
		else:
			buf+=char
	text=buf
	text=re_sentence_dot.sub(r"\1 ^%s.~ \2"%characterSymbols.names["."],text)
	text=re_sentence_comma.sub(r"\1 ^%s,~ \2"%characterSymbols.names[","],text)
	text=re_sentence_question.sub(r"\1 ^%s?~ \2"%characterSymbols.names["?"],text)
	text=re_sentence_colon.sub(r"\1 ^%s:~ \2"%characterSymbols.names[":"],text)
	text=re_sentence_semiColon.sub(r"\1 ^%s;~ \2"%characterSymbols.names[";"],text)
	text=re_sentence_exclimation.sub(r"\1 ^%s!~ \2"%characterSymbols.names["!"],text)
	#text=re_word_apostraphy.sub(r"\1 %s^.~ \2"%characterSymbols.names["'"],text)
	buf=""
	for char in text:
		if char=="^":
			protector=True
			buf+="^"
			continue
		if char=="~":
			protector=False
			buf+="~"
			continue
		if not protector:
			if (char not in characterSymbols.blankList) and characterSymbols.names.has_key(char):
				buf+=" ^%s~ "%characterSymbols.names[char]
			else:
				buf+=char
		else:
			buf+=char
	text=buf
	text=text.replace("^","")
	text=text.replace("~","")
	return text

def processSymbol(symbol):
	newSymbol=characterSymbols.names.get(symbol,symbol)
	return newSymbol


