#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""Unit tests for the languageDetection module.
"""

import unittest
import languageDetection
from speech import LangChangeCommand
from unicodeScriptData import scriptRanges
import config

class TestLanguageDetection(unittest.TestCase):

	def setUp(self):
		languageDetection.initialize()
		config.conf["languageDetection"]["disableScriptDetection"] = "false" 
		languageDetection.updateLanguagePriorityFromConfig()

	def compareSpeechSequence(self , sequence1 , sequence2 ):
		try:
			self.assertEqual(len( sequence1) , len( sequence2) )
		except AssertionError as e:
			e.args += (u"[" , u", ".join(map(unicode, sequence1 )) , "]\n[" , u", ".join(map(unicode, sequence2 )) , "]")
			raise

		for index in xrange( len(sequence1)): 
			self.assertEqual( type(sequence1[index]) , type(sequence2[index]) ) 
			if isinstance( sequence1[index] , LangChangeCommand):
				self.assertEqual(sequence1[index].lang , sequence2[index].lang  )
			else:
				self.assertEqual(sequence1[index] , sequence2[index] )

	def test_englishAndHindiWithEnglishAsDefault(self):
		englishText = u"hello"
		hindiText = u"नमस्ते"
		combinedText = englishText + hindiText 
		testSequence = []
		testSequence.append (englishText )
		testSequence.append ( LangChangeCommand( "hi") )
		testSequence.append (hindiText )
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText , "en" )
		self.compareSpeechSequence(detectedLanguageSequence  , testSequence) 

	def test_englishAndHindiWithHindiAsDefault(self):
		englishText = u"hello"
		hindiText = u"नमस्ते"
		combinedText = englishText + hindiText 
		testSequence = []
		testSequence.append ( LangChangeCommand( "en") )
		testSequence.append (englishText )
		testSequence.append ( LangChangeCommand( "hi") )
		testSequence.append (hindiText )
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText , "hi" )
		self.compareSpeechSequence(detectedLanguageSequence  , testSequence) 

	def test_englishPlainTextWithEnglishAsDefault(self):
		englishText = u"hello"
		testSequence = []
		testSequence.append (englishText )
		detectedLanguageSequence = languageDetection.detectLanguage( englishText , "en" )
		self.compareSpeechSequence(detectedLanguageSequence  , testSequence) 

	def test_englishPlainTextWithHindiAsDefault(self):
		englishText = u"hello"
		testSequence = []
		testSequence.append ( LangChangeCommand( "en") )
		testSequence.append (englishText )
		detectedLanguageSequence = languageDetection.detectLanguage( englishText , "hi" )
		self.compareSpeechSequence(detectedLanguageSequence  , testSequence) 

	def test_numbersBetweenEnglishAndHindiWithEnglishAsDefaultAndPreferedLanguageAsHindi(self):
		englishText = u"hello"
		numbersText = "247"
		hindiText = u"नमस्ते"
		combinedText = englishText + numbersText + hindiText 
		testSequence = []
		testSequence.append (englishText + numbersText )
		testSequence.append ( LangChangeCommand( "hi") )
		testSequence.append (hindiText )
		config.conf["languageDetection"]["preferredLanguages"] = ("hi",)
		languageDetection.updateLanguagePriorityFromConfig()
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText , "en" )
		config.conf["languageDetection"]["preferredLanguages"] = ()
		languageDetection.updateLanguagePriorityFromConfig()
		self.compareSpeechSequence(detectedLanguageSequence  , testSequence) 

	def test_numbersBetweenEnglishAndHindiWithHindiAsDefaultAndPreferedLanguageAsHindi(self):
		englishText = u"hello"
		numbersText = "247"
		hindiText = u"नमस्ते"
		combinedText = englishText + numbersText + hindiText 
		testSequence = []
		testSequence.append ( LangChangeCommand( "en") )
		testSequence.append (englishText )
		testSequence.append ( LangChangeCommand( "hi") )
		testSequence.append (numbersText + hindiText )
		config.conf["languageDetection"]["preferredLanguages"] = ("hi",)
		languageDetection.updateLanguagePriorityFromConfig()
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText , "hi" )
		config.conf["languageDetection"]["preferredLanguages"] = ()
		languageDetection.updateLanguagePriorityFromConfig()
		self.compareSpeechSequence(detectedLanguageSequence  , testSequence) 

	def test_numbersBetweenEnglishAndHindiWithEnglishAsDefaultAndWithoutAnyPreferedLanguage(self):
		englishText = u"hello"
		numbersText = "247"
		hindiText = u"नमस्ते"
		combinedText = englishText + numbersText + hindiText 
		testSequence = []
		testSequence.append (englishText + numbersText )
		testSequence.append ( LangChangeCommand( "hi") )
		testSequence.append ( hindiText )
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText , "en" )
		self.compareSpeechSequence(detectedLanguageSequence  , testSequence) 

	def test_numbersBetweenEnglishAndHindiWithHindiAsDefaultAndWithoutAnyPreferedLanguage(self):
		englishText = u"hello"
		numbersText = "247"
		hindiText = u"नमस्ते"
		combinedText = englishText + numbersText + hindiText 
		testSequence = []
		testSequence.append ( LangChangeCommand( "en") )
		testSequence.append (englishText )
		testSequence.append ( LangChangeCommand( "hi") )
		testSequence.append ( numbersText + hindiText )
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText , "hi" )
		self.compareSpeechSequence(detectedLanguageSequence  , testSequence) 

	def test_numbersMixedWithCommaBetweenEnglishAndHindiWithHindiAsDefaultAndPreferedLanguageAsHindi(self):
		englishText = u"hello"
		numbersText = "2,4,7"
		hindiText = u"नमस्ते"
		combinedText = englishText + numbersText + hindiText 
		testSequence = []
		testSequence.append ( LangChangeCommand( "en") )
		testSequence.append (englishText )
		testSequence.append ( LangChangeCommand( "hi") )
		testSequence.append (numbersText + hindiText )
		config.conf["languageDetection"]["preferredLanguages"] = ("hi",)
		languageDetection.updateLanguagePriorityFromConfig()
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText , "hi" )
		config.conf["languageDetection"]["preferredLanguages"] = ()
		languageDetection.updateLanguagePriorityFromConfig()
		self.compareSpeechSequence(detectedLanguageSequence  , testSequence) 

	def test_latinScriptForEnglish(self):
		scriptIDForEnglish = languageDetection.getScriptIDFromLangID( "en" )
		self.assertIn(  "Latin" , scriptIDForEnglish )

	def test_englishAsDefaultLanguageForNumbers(self):
		languageCode = languageDetection.getLangID( "Number" )  
		self.assertEqual("en" , languageCode )

	def test_JapaneseAsDefaultAndEnglishAsPreferred_case1(self):
		combinedText = u"ウィンドウズ 10 文字認識"
		config.conf["languageDetection"]["preferredLanguages"] = ("en",)
		languageDetection.updateLanguagePriorityFromConfig()
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText, "ja_JP")
		self.compareSpeechSequence(detectedLanguageSequence, [
			u"ウィンドウズ 10 文字認識",
			])
		config.conf["languageDetection"]["preferredLanguages"] = ()
		languageDetection.updateLanguagePriorityFromConfig()
		
	def test_JapaneseAsDefaultAndEnglishAsPreferred_case2(self):
		combinedText = u"10文字"
		config.conf["languageDetection"]["preferredLanguages"] = ("en",)
		languageDetection.updateLanguagePriorityFromConfig()
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText, "ja_JP")
		self.compareSpeechSequence(detectedLanguageSequence, [
			u"10文字",
		])
		config.conf["languageDetection"]["preferredLanguages"] = ()
		languageDetection.updateLanguagePriorityFromConfig()
		
	def test_JapaneseAsDefaultAndEnglishAsPreferred_case3(self):
		combinedText = u"Windows 10"
		config.conf["languageDetection"]["preferredLanguages"] = ("en",)
		languageDetection.updateLanguagePriorityFromConfig()
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText, "ja_JP")
		self.compareSpeechSequence(detectedLanguageSequence, [
			LangChangeCommand('en'),
			u"Windows ",
			LangChangeCommand('ja_JP'),
			u"10",
		])
		config.conf["languageDetection"]["preferredLanguages"] = ()
		languageDetection.updateLanguagePriorityFromConfig()
		
	def test_JapaneseAsDefaultAndEnglishAsPreferred_case4(self):
		combinedText = u"Windows 10 文字認識"
		config.conf["languageDetection"]["preferredLanguages"] = ("en",)
		languageDetection.updateLanguagePriorityFromConfig()
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText, "ja_JP")
		self.compareSpeechSequence(detectedLanguageSequence, [
			LangChangeCommand('en'),
			u"Windows ",
			LangChangeCommand('ja_JP'),
			u"10 文字認識",
		])
		config.conf["languageDetection"]["preferredLanguages"] = ()
		languageDetection.updateLanguagePriorityFromConfig()

	def test_JapaneseAsDefaultAndEnglishAsPreferred_case5(self):
		combinedText = u"Windows １０文字認識"
		config.conf["languageDetection"]["preferredLanguages"] = ("en",)
		languageDetection.updateLanguagePriorityFromConfig()
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText, "ja_JP")
		self.compareSpeechSequence(detectedLanguageSequence, [
			LangChangeCommand('en'),
			u"Windows ",
			LangChangeCommand('ja_JP'),
			u"１０文字認識",
		])
		config.conf["languageDetection"]["preferredLanguages"] = ()
		languageDetection.updateLanguagePriorityFromConfig()

	def test_Japanese_EnglishAsDefault_case1(self):
		combinedText = u"ウィンドウズ 10 文字認識"
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText, "en_US")
		self.compareSpeechSequence(detectedLanguageSequence, [
			LangChangeCommand('ja'),
			u"ウィンドウズ ",
			LangChangeCommand('en_US'),
			u"10 ",
			LangChangeCommand('ja'),
			u"文字認識",
		])
		
	def test_Japanese_EnglishAsDefault_case2(self):
		combinedText = u"10文字"
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText, "en_US")
		self.compareSpeechSequence(detectedLanguageSequence, [
			u"10",
			LangChangeCommand('ja'),
			u"文字",
		])
		
	def test_Japanese_EnglishAsDefault_case4(self):
		combinedText = u"Windows 10 文字認識"
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText, "en_US")
		self.compareSpeechSequence(detectedLanguageSequence, [
			u"Windows 10 ",
			LangChangeCommand('ja'),
			u"文字認識",
		])

	def test_Japanese_EnglishAsDefault_case5(self):
		combinedText = u"Windows １０文字認識"
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText, "en_US")
		self.compareSpeechSequence(detectedLanguageSequence, [
			u"Windows ",
			LangChangeCommand('ja'),
			u"１０文字認識",
		])

	def test_englishWithGreekTextWithEnglishAsDefaultAndPreferedLanguageAsHindi(self):
		combinedText = u"gamma (γ) is"
		testSequence = []
		testSequence.append ( u"gamma (" )
		testSequence.append ( LangChangeCommand( "el") )
		testSequence.append ( u"γ" )
		testSequence.append ( LangChangeCommand( "en") )
		testSequence.append ( u") is" )
		config.conf["languageDetection"]["preferredLanguages"] = ("en",)
		languageDetection.updateLanguagePriorityFromConfig()
		detectedLanguageSequence = languageDetection.detectLanguage(combinedText , "en" )
		config.conf["languageDetection"]["preferredLanguages"] = ()
		languageDetection.updateLanguagePriorityFromConfig()
		self.compareSpeechSequence(detectedLanguageSequence  , testSequence) 

	def test_unicodeRangesEntryStartLessEqualEnd(self):
		for scriptRangeStart, scriptRangeEnd, scriptName in scriptRanges:
			self.assertTrue(scriptRangeStart <= scriptRangeEnd)

	def test_unicodeRangesEntriesDoNotOverlapAndAreSorted(self):
		for index in xrange( len(scriptRanges) -1): 
			#check is there is no overlap
			currentRange = scriptRanges[index]
			nextRange = scriptRanges[index+1]
			currentRangeEnd = currentRange[1]
			nextRangeStart = nextRange[0]
			self.assertTrue(currentRangeEnd   < nextRangeStart)

	def test_unicodeRangesEntryScriptNamesExist(self):
		for scriptRangeStart, scriptRangeEnd, scriptName in scriptRanges:
			self.assertTrue(scriptName)

	def test_unicodeRangesEntryFirstRangeStartGreaterThanZero(self):
		firstRangeStart = scriptRanges[0][0]
		self.assertTrue(firstRangeStart >= 0)
