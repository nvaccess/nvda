###
# Makefile
# Part of NVDA Helper
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=.
!include $(TOPDIR)\make.opts

all: 
	if not EXIST $(OUTDIR) mkdir $(OUTDIR)
	cd remote && $(MAKE) /nologo DEBUG=$(DEBUG) DEBUGLOG=$(DEBUGLOG)
	cd local && $(MAKE) /nologo DEBUG=$(DEBUG) DEBUGLOG=$(DEBUGLOG)
	cd vbufBackends && $(MAKE) /nologo DEBUG=$(DEBUG) DEBUGLOG=$(DEBUGLOG)

install: all
	xcopy $(OUTDIR)\*.dll ..\lib

clean:
	cd remote && $(MAKE) /nologo clean
	cd local && $(MAKE) /nologo clean
	cd vbufBackends && $(MAKE) /nologo clean

distclean: clean
 	-rmdir /Q /s build 2>NUL
 	-rmdir /Q /s build_debug 2>NUL
