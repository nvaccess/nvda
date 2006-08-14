#textProcessing.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import re
import debug
import dictionaries

re_word_multiCase=re.compile(r"([a-z])([A-Z])")
re_sentence_dot=re.compile(r"(\w|\)|\"|')\.(\s|$)")
re_sentence_comma=re.compile(r"(\w|\)|\"|'),(\s|$)")
re_sentence_question=re.compile(r"(\w|\))\?(\s|$)")
re_sentence_colon=re.compile(r"(\w|\)|\"|'):(\s|$)")
re_sentence_semiColon=re.compile(r"(\w|\)|\"|');(\s|$)")
re_sentence_exclimation=re.compile(r"(\w|\)|\"|')!(\s|$)")
re_word_apostraphy=re.compile(r"(\w)'(\w)")

#Firstly expands ^ and ~ so they can be used as protector symbols
#Expands special sentence punctuation keeping the origional physical symbol but protected by ^ and ~
#Expands any other symbols and removes ^ and ~ protectors
def processTextSymbols(text,keepInflection=False):
	protector=False
	str=""
	for char in text:
			if (char=="^") or (char=="~"):
				str=" %s "%dictionaries.textSymbols[char]
			else:
				str+=char
	text=str
	if keepInflection:
		text=re_sentence_dot.sub(r"\1 ^%s.~ \2"%dictionaries.textSymbols["."],text)
		text=re_sentence_comma.sub(r"\1 ^%s,~ \2"%dictionaries.textSymbols[","],text)
		text=re_sentence_question.sub(r"\1 ^%s?~ \2"%dictionaries.textSymbols["?"],text)
		text=re_sentence_colon.sub(r"\1 ^%s:~ \2"%dictionaries.textSymbols[":"],text)
		text=re_sentence_semiColon.sub(r"\1 ^%s;~ \2"%dictionaries.textSymbols[";"],text)
		text=re_sentence_exclimation.sub(r"\1 ^%s!~ \2"%dictionaries.textSymbols["!"],text)
		#text=re_word_apostraphy.sub(r"\1 %s^.~ \2"%dictionaries.textSymbols["'"],text)
	str=""
	for char in text:
		if char=="^":
			protector=True
			str+="^"
			continue
		if char=="~":
			protector=False
			str+="~"
			continue
		if not protector:
			if (char!=" ") and dictionaries.textSymbols.has_key(char):
				str+=" ^%s~ "%dictionaries.textSymbols[char]
			else:
				str+=char
		else:
			str+=char
	text=str
	text=text.replace("^","")
	text=text.replace("~","")
	return text

def splitMultiCaseWords(text):
	text=re_word_multiCase.sub(r"\1 \2",text)
	return text

def processSymbol(symbol):
	text=dictionaries.characterSymbols.get(symbol,symbol)
	if (symbol>='A') and (symbol<='Z'):
		text="cap %s"%text
	return text

