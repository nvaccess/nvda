###
# backends/gecko_ia2/Makefile
# Part of the NV  Virtual Buffer Library
# This library is copyright 2007, 2008 NV Virtual Buffer Library Contributors
# This library is licensed under the GNU Lesser General Public Licence. See license.txt which is included with this library, or see
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
###

TOPDIR=..\..
!include $(TOPDIR)\make.opts
CPPFLAGS=$(CPPFLAGS) /DVBUFLIBENTRYTYPE=2

all: $(OUTDIR)\VBufBackend_gecko_ia2.dll

$(TOPDIR)\ia2\ia2_i.c:
	cd $(TOPDIR)\ia2 && $(MAKE) /NOLOGO DEBUG=$(DEBUG)

$(OUTDIR)\VBufBase.lib:
	cd $(TOPDIR)\base && $(MAKE) /NOLOGO DEBUG=$(DEBUG)

$(OUTDIR)\VBufBackend_gecko_ia2.dll: gecko_ia2.cpp $(TOPDIR)\common\utils.cpp $(TOPDIR)\common\ia2utils.cpp $(TOPDIR)\deps\ia2\ia2_i.c $(OUTDIR)\VBufBase.lib
	$(CPP) $(CPPFLAGS) $** user32.lib kernel32.lib oleacc.lib oleaut32.lib /link /dll /out:$@ $(LINKERFLAGS)

clean:
	-del *.obj 2>NUL
	-del *.pdb 2>NUL
