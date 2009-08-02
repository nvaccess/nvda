###
# Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..
!include $(TOPDIR)\make.opts

all: 
	cd gecko_ia2 && $(MAKE) /nologo DEBUG=$(DEBUG) DEBUGLOG=$(DEBUGLOG) 
	cd adobeAcrobat && $(MAKE) /nologo DEBUG=$(DEBUG) DEBUGLOG=$(DEBUGLOG) 
	cd mshtml && $(MAKE) /nologo DEBUG=$(DEBUG) DEBUGLOG=$(DEBUGLOG) 

clean:
	cd gecko_ia2 && $(MAKE) /nologo clean
	cd adobeAcrobat && $(MAKE) /nologo clean
	cd mshtml && $(MAKE) /nologo clean
