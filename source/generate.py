#generate.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Script to generate needed com interfaces and language files"""
import os
import sys
from glob import glob
import comtypesClient

#MS HTML
try:
	print "MS HTML"
	comtypesClient.GetModule('mshtml.tlb')
	print "done"
except:
	print "not found"

#IAccessible2
try:
	print "IAccessible2"
	comtypesClient.GetModule('lib/ia2.tlb')
	print "done"
except:
	print "not found"

#IServiceProvider library
try:
	print "IServiceProvider library"
	comtypesClient.GetModule('lib/servprov.tlb')
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

#Sapi5
try:
	print "Sapi5"
	comtypesClient.CreateObject("Sapi.SPVoice")
	print "done"
except:
	print "not found"

print "Language files"
poFiles=glob('locale/*/LC_MESSAGES/nvda.po')
for f in poFiles:
	print f
	os.spawnv(os.P_WAIT,"%s\\python.exe"%sys.exec_prefix,['python',"%s\\Tools\\i18n\\msgfmt.py"%sys.exec_prefix,f])

