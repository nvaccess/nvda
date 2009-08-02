###
# backends/gecko_ia2/Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..\..
!include $(TOPDIR)\make.opts

all: $(OUTDIR)\VBufBackend_gecko_ia2.dll

$(TOPDIR)\..\include\ia2\ia2_i.c:
	cd $(TOPDIR)\..\include\ia2 && $(MAKE) /NOLOGO DEBUG=$(DEBUG)

$(OUTDIR)\VBufBackend_gecko_ia2.dll: gecko_ia2.cpp $(TOPDIR)\vbufBase\ia2Utils.cpp $(TOPDIR)\..\include\ia2\ia2_i.c
	cd $(TOPDIR)\vbufBase && $(MAKE) /NOLOGO DEBUG=$(DEBUG)
	$(CPP) $(CPPFLAGS) $** /link $(OUTDIR)\vbufBase_static.lib user32.lib kernel32.lib oleacc.lib oleaut32.lib /dll /out:$@ 

clean:
	cd $(TOPDIR)\vbufBase && $(MAKE) /NOLOGO clean
	cd $(TOPDIR)\..\include\ia2 && $(MAKE) /NOLOGO clean
	-del *.obj 2>NUL
	-del *.pdb 2>NUL
