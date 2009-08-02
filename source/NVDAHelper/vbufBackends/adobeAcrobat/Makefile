###
# backends/adobeAcrobat/Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007-2009 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..\..
!include $(TOPDIR)\make.opts

all: $(OUTDIR)\VBufBackend_adobeAcrobat.dll

$(OUTDIR)\VBufBackend_adobeAcrobat.dll: adobeAcrobat.obj $(TOPDIR)\..\include\AcrobatAccess\AcrobatAccess_i.c
	cd $(TOPDIR)\vbufBase && $(MAKE) /NOLOGO DEBUG=$(DEBUG) DEBUGLOG=$(DEBUGLOG)
	$(CPP) $(CPPFLAGS) $** $(OUTDIR)\vbufBase_static.lib user32.lib kernel32.lib oleacc.lib oleaut32.lib /link /dll /out:$@ $(LINKERFLAGS)

clean:
	cd $(TOPDIR)\vbufBase && $(MAKE) /NOLOGO clean
	-del *.obj 2>NUL
	-del *.pdb 2>NUL
