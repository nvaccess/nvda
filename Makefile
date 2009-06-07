###
# Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=.
!include $(TOPDIR)\make.opts

!if !defined(BACKEND)
BACKEND=""
!endif

all: 
	if not EXIST $(OUTDIR) mkdir $(OUTDIR)
	if not $(BACKEND)=="" cd backends\$(BACKEND) && $(MAKE) /nologo DEBUG=$(DEBUG) 
	-if $(BACKEND)=="" cd backends\gecko_ia2 && $(MAKE) /nologo DEBUG=$(DEBUG) 
	-if $(BACKEND)=="" cd backends\mshtml && $(MAKE) /nologo DEBUG=$(DEBUG) 
	-if $(BACKEND)=="" cd backends\adobeAcrobat && $(MAKE) /nologo DEBUG=$(DEBUG) 
	cd base && $(MAKE) /nologo DEBUG=$(DEBUG)
	cd client && $(MAKE) /nologo DEBUG=$(DEBUG)

test:
	if not EXIST $(OUTDIR) mkdir $(OUTDIR)
	cd tests && $(MAKE) /nologo DEBUG=$(DEBUG)

clean:
	if not $(BACKEND)=="" cd backends\$(BACKEND) && $(MAKE) /nologo clean
	if $(BACKEND)=="" cd backends\gecko_ia2 && $(MAKE) /nologo clean
	if $(BACKEND)=="" cd backends\mshtml && $(MAKE) /nologo clean
	if $(BACKEND)=="" cd backends\adobeAcrobat && $(MAKE) /nologo clean 
	cd base && $(MAKE) /nologo clean
	cd client && $(MAKE) /nologo clean
	cd remoteApi && $(MAKE) /nologo clean
	cd tests && $(MAKE) /nologo clean

distclean: clean
 	-rmdir /Q /s build 2>NUL
 	-rmdir /Q /s build_debug 2>NUL
