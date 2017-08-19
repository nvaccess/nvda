#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""Unit tests for the languageDetection module.
"""

import unittest
import languageDetection
from speech import LangChangeCommand
import config

class TestLanguageDetection(unittest.TestCase):

	def setUp(self):
		languageDetection.initialize()

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
