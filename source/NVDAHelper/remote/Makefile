###
# remote/Makefile
# Part of NVDA Helper
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..
!include $(TOPDIR)\make.opts

all: $(OUTDIR)\NVDAHelperRemote.dll

#IAccessible2
$(TOPDIR)\..\include\ia2\ia2_i.c: $(TOPDIR)\..\include\ia2\ia2.idl
	cd $(TOPDIR)\..\include\ia2 && $(MAKE) /NOLOGO DEBUG=$(DEBUG) DEBUGLOG=$(DEBUGLOG)

#VBuf interface
$(TOPDIR)\interfaces\vbuf\vbuf_s.c: $(TOPDIR)\interfaces\vbuf\vbuf.acf $(TOPDIR)\interfaces\vbuf\vbuf.idl
	cd $(TOPDIR)\interfaces\vbuf && $(MAKE) /nologo DEBUG=$(DEBUG) DEBUGLOG=$(DEBUGLOG)

$(OUTDIR)\NVDAHelperRemote.dll: NVDAHelperRemote.cpp inputLangChange.cpp typedCharacter.cpp IA2Support.cpp $(TOPDIR)\..\include\ia2\ia2_i.c rpcSrv.cpp vbufRemote.cpp $(TOPDIR)\interfaces\vbuf\vbuf_s.c 
	$(CPP) $(CPPFLAGS) $** /link $(LINKERFLAGS) user32.lib ole32.lib rpcrt4.lib /dll /out:$@

clean:
	cd $(TOPDIR)\..\include\ia2 && $(MAKE) /NOLOGO clean
	cd $(TOPDIR)\interfaces\vbuf && $(MAKE) /nologo clean
	-del *.obj 2>NUL
