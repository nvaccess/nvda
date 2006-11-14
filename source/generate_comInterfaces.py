import os
import comtypesClient

#MS Word
try:
	print "MS Word"
	comtypesClient.CreateObject('Word.Application')
	print "done"
except:
	print "not found"

#MS Excel
try:
	print "MS Excel"
	comtypesClient.CreateObject('Excel.Application')
	print "done"
except:
	print "not found"

#MS HTML
try:
	print "MS HTML"
	comtypesClient.GetModule('mshtml.tlb')
	print "done"
except:
	print "not found"

#MS Active Accessibility
try:
	print "MS Active Accessibility"
	comtypesClient.GetModule('oleacc.dll')
	print "done"
except:
	print "not found"

#Rich edit
try:
	print "Rich edit"
	comtypesClient.GetModule('msftedit.dll')
	print "done"
except:
	print "not found"

#Sapi5
try:
	print "Sapi5"
	comtypesClient.CreateObject("Sapi.SPVoice")
	print "done"
except:
	print "not found"

#Sapi4
try:
	print "Sapi4"
	comtypesClient.CreateObject("speech.voiceText")
	print "done"
except:
	print "not found"


